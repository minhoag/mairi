import { useEffect, useState } from "react";
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui/card.tsx";
import {
	type ChartConfig,
	ChartContainer,
	ChartTooltip,
	ChartTooltipContent,
} from "@/components/ui/chart.tsx";

const chartConfig = {
	estimated_iri: { label: "Estimated IRI", color: "#f97316" },
	speed_kmh: { label: "Speed (km/h)", color: "#6b7280" },
} satisfies ChartConfig;

interface DashboardPoint {
	segment_index: number;
	road_name: string;
	start_distance_m: number;
	end_distance_m: number;
	distance_m: number;
	estimated_iri: number;
	speed_kmh: number;
	condition: "Good" | "Fair" | "Poor";
}

// MOCK
// MOCK: Seeded PRNG so the demo is deterministic across reloads
function mulberry32(seed: number) {
	let s = seed >>> 0;
	return () => {
		s = (s + 0x6d2b79f5) >>> 0;
		let t = s;
		t = Math.imul(t ^ (t >>> 15), t | 1);
		t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
}

const MOCK_SEGMENT_COUNT = 200;

interface MockSpeedSegment {
	road_name: string;
	segment_length_m: number;
	speed_kmh: number;
}

function columnIndex(headers: string[], name: string) {
	const index = headers.indexOf(name);
	if (index === -1) throw new Error(`Missing CSV column: ${name}`);
	return index;
}

function getCondition(estimatedIri: number): DashboardPoint["condition"] {
	if (estimatedIri < 2.7) return "Good";
	if (estimatedIri <= 4) return "Fair";
	return "Poor";
}

function isInRoughZone(segmentIndex: number) {
	const roughZones = [
		{ start: 42, end: 55 },
		{ start: 108, end: 123 },
		{ start: 162, end: 176 },
	];

	for (const zone of roughZones) {
		if (segmentIndex >= zone.start && segmentIndex <= zone.end) return true;
	}

	return false;
}

function isPotholeSpike(segmentIndex: number) {
	return [31, 88, 145, 188].includes(segmentIndex);
}

function getMockIri(segmentIndex: number, rand: () => number) {
	let estimatedIri = 1.5 + rand() * 2;

	if (isInRoughZone(segmentIndex)) {
		estimatedIri = 4 + rand() * 2.5;
	}

	if (isPotholeSpike(segmentIndex)) {
		estimatedIri = 7 + rand() * 1.5;
	}

	return Number(estimatedIri.toFixed(2));
}

function buildMockDashboardData(
	validSegments: MockSpeedSegment[],
): DashboardPoint[] {
	const rand = mulberry32(42);
	if (validSegments.length === 0) {
		throw new Error("No valid mock speed rows found");
	}

	const dashboardRows: DashboardPoint[] = [];
	let startDistanceM = 0;

	for (let i = 0; i < validSegments.length; i++) {
		const segment = validSegments[i];
		const endDistanceM = startDistanceM + segment.segment_length_m;
		const estimatedIri = getMockIri(i, rand);

		dashboardRows.push({
			segment_index: i + 1,
			road_name: segment.road_name,
			start_distance_m: startDistanceM,
			end_distance_m: endDistanceM,
			distance_m: endDistanceM,
			speed_kmh: segment.speed_kmh,
			estimated_iri: estimatedIri,
			condition: getCondition(estimatedIri),
		});

		startDistanceM = endDistanceM;
	}

	return dashboardRows;
}

function parseMockSpeedRow(
	line: string,
	roadNameIndex: number,
	lengthIndex: number,
	shapeLengthIndex: number,
	speedIndex: number,
) {
	const values = line.split(",");
	const speedKmh = Number(values[speedIndex]);
	const lengthKm = Number(values[lengthIndex]);
	let segmentLengthM = Number(values[shapeLengthIndex]);

	if (!Number.isFinite(segmentLengthM) || segmentLengthM <= 0) {
		segmentLengthM = lengthKm * 1000;
	}

	if (!Number.isFinite(speedKmh)) return null;
	if (speedKmh === 0) return null;
	if (speedKmh < 5 || speedKmh > 130) return null;
	if (!Number.isFinite(segmentLengthM)) return null;
	if (segmentLengthM <= 0) return null;

	return {
		road_name: values[roadNameIndex].trim(),
		segment_length_m: segmentLengthM,
		speed_kmh: speedKmh,
	} satisfies MockSpeedSegment;
}

async function fetchMockDashboardData() {
	const response = await fetch("/speed_mock.csv");
	if (!response.body) {
		throw new Error("Missing response body for mock speed CSV");
	}

	const reader = response.body.getReader();
	const decoder = new TextDecoder();
	const validSegments: MockSpeedSegment[] = [];
	let buffer = "";
	let headersParsed = false;
	let roadNameIndex = -1;
	let lengthIndex = -1;
	let shapeLengthIndex = -1;
	let speedIndex = -1;

	try {
		while (validSegments.length < MOCK_SEGMENT_COUNT) {
			const { done, value } = await reader.read();
			buffer += decoder.decode(value ?? new Uint8Array(), { stream: !done });

			const lines = buffer.split(/\r?\n/);
			buffer = lines.pop() ?? "";

			for (const rawLine of lines) {
				const line = rawLine.trim();
				if (!line) continue;

				if (!headersParsed) {
					const headers = line.split(",").map((header) => header.trim());
					roadNameIndex = columnIndex(headers, "RDNAME");
					lengthIndex = columnIndex(headers, "LENGTH");
					shapeLengthIndex = columnIndex(headers, "Shape__Length");
					speedIndex = columnIndex(headers, "ATS_PM");
					headersParsed = true;
					continue;
				}

				const segment = parseMockSpeedRow(
					line,
					roadNameIndex,
					lengthIndex,
					shapeLengthIndex,
					speedIndex,
				);

				if (!segment) continue;
				validSegments.push(segment);

				if (validSegments.length === MOCK_SEGMENT_COUNT) {
					await reader.cancel();
					break;
				}
			}

			if (done) {
				if (
					buffer.trim() &&
					headersParsed &&
					validSegments.length < MOCK_SEGMENT_COUNT
				) {
					const segment = parseMockSpeedRow(
						buffer.trim(),
						roadNameIndex,
						lengthIndex,
						shapeLengthIndex,
						speedIndex,
					);

					if (segment) validSegments.push(segment);
				}
				break;
			}
		}
	} finally {
		reader.releaseLock();
	}

	return buildMockDashboardData(validSegments);
}
// END MOCK

export function AreaGraph() {
	const [data, setData] = useState<DashboardPoint[]>([]);

	useEffect(() => {
		// MOCK
		fetchMockDashboardData().then((rows) => setData(rows));
		// END MOCK
	}, []);

	return (
		<Card>
			<CardHeader>
				<CardTitle>Road Roughness</CardTitle>
				<CardDescription>
					Estimated IRI and segment speed along travel distance
				</CardDescription>
			</CardHeader>
			<CardContent>
				<ChartContainer config={chartConfig}>
					<LineChart data={data}>
						<CartesianGrid vertical={false} strokeDasharray="3 3" />
						<XAxis
							dataKey="distance_m"
							type="number"
							tickLine={false}
							axisLine={false}
							tickMargin={8}
							tickFormatter={(value: number) =>
								value >= 1000 ? `${(value / 1000).toFixed(1)} km` : `${value} m`
							}
						/>
						<YAxis
							yAxisId="iri"
							orientation="left"
							tickLine={false}
							axisLine={false}
						/>
						<YAxis
							yAxisId="speed"
							orientation="right"
							domain={[0, 130]}
							tickLine={false}
							axisLine={false}
						/>
						<ChartTooltip cursor={false} content={<ChartTooltipContent />} />
						<Line
							yAxisId="iri"
							type="monotone"
							dataKey="estimated_iri"
							stroke="#f97316"
							dot={false}
							strokeWidth={2}
						/>
						<Line
							yAxisId="speed"
							type="monotone"
							dataKey="speed_kmh"
							stroke="#6b7280"
							dot={false}
							strokeWidth={2}
						/>
					</LineChart>
				</ChartContainer>
			</CardContent>
		</Card>
	);
}
