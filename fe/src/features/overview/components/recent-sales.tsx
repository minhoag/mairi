import { Badge } from "@/components/ui/badge.tsx";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui/card.tsx";
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table.tsx";

// MOCKS
type Status = "success" | "failed" | "retry";

type LogEntry = {
	device: string;
	event: string;
	status: Status;
	time: string;
};

const logData: LogEntry[] = [
	{
		device: "RPi-A1B2",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 14:00",
	},
	{
		device: "RPi-C3D4",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:57",
	},
	{
		device: "RPi-G7H8",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:55",
	},
	{
		device: "RPi-E5F6",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:52",
	},
	{
		device: "RPi-A1B2",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:49",
	},
	{
		device: "RPi-C3D4",
		event: "Data uploaded",
		status: "retry",
		time: "2026-06-17 13:47",
	},
	{
		device: "RPi-C3D4",
		event: "Upload failed",
		status: "failed",
		time: "2026-06-17 13:45",
	},
	{
		device: "RPi-G7H8",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:42",
	},
	{
		device: "RPi-E5F6",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:40",
	},
	{
		device: "RPi-A1B2",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:37",
	},
	{
		device: "RPi-C3D4",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:34",
	},
	{
		device: "RPi-G7H8",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:32",
	},
	{
		device: "RPi-E5F6",
		event: "Data uploaded",
		status: "retry",
		time: "2026-06-17 13:29",
	},
	{
		device: "RPi-E5F6",
		event: "Upload failed",
		status: "failed",
		time: "2026-06-17 13:27",
	},
	{
		device: "RPi-A1B2",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:24",
	},
	{
		device: "RPi-C3D4",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:22",
	},
	{
		device: "RPi-G7H8",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:19",
	},
	{
		device: "RPi-E5F6",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:16",
	},
	{
		device: "RPi-A1B2",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:14",
	},
	{
		device: "RPi-C3D4",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:11",
	},
	{
		device: "RPi-G7H8",
		event: "Data uploaded",
		status: "retry",
		time: "2026-06-17 13:09",
	},
	{
		device: "RPi-G7H8",
		event: "Upload failed",
		status: "failed",
		time: "2026-06-17 13:07",
	},
	{
		device: "RPi-E5F6",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:04",
	},
	{
		device: "RPi-A1B2",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 13:02",
	},
	{
		device: "RPi-C3D4",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 12:59",
	},
	{
		device: "RPi-G7H8",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 12:57",
	},
	{
		device: "RPi-E5F6",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 12:54",
	},
	{
		device: "RPi-A1B2",
		event: "Data uploaded",
		status: "retry",
		time: "2026-06-17 12:51",
	},
	{
		device: "RPi-A1B2",
		event: "Upload failed",
		status: "failed",
		time: "2026-06-17 12:49",
	},
	{
		device: "RPi-C3D4",
		event: "Data uploaded",
		status: "success",
		time: "2026-06-17 12:46",
	},
];
// END MOCKS

const statusBadge: Record<Status, { label: string; className: string }> = {
	success: {
		label: "SUCCESS",
		className:
			"border-green-200 bg-green-50 text-green-600 dark:border-green-800 dark:bg-green-950 dark:text-green-400",
	},
	failed: {
		label: "FAILED",
		className:
			"border-red-200 bg-red-50 text-red-600 dark:border-red-800 dark:bg-red-950 dark:text-red-400",
	},
	retry: {
		label: "RETRY",
		className:
			"border-orange-200 bg-orange-50 text-orange-600 dark:border-orange-800 dark:bg-orange-950 dark:text-orange-400",
	},
};

export function RecentSales() {
	return (
		<Card className="h-full">
			<CardHeader>
				<CardTitle>Device Update Log</CardTitle>
				<CardDescription>
					Latest uploads from road monitoring devices.
				</CardDescription>
			</CardHeader>
			<CardContent>
				<div className="overflow-auto max-h-[480px]">
					<Table>
						<TableHeader>
							<TableRow>
								<TableHead>Device</TableHead>
								<TableHead>Event</TableHead>
								<TableHead>Status</TableHead>
								<TableHead>Time</TableHead>
							</TableRow>
						</TableHeader>
						<TableBody>
							{logData.map((entry, index) => {
								const badge = statusBadge[entry.status];
								return (
									<TableRow key={index}>
										<TableCell className="font-mono">{entry.device}</TableCell>
										<TableCell
											className={
												entry.status === "retry" ? "text-orange-500" : ""
											}
										>
											{entry.event}
										</TableCell>
										<TableCell>
											<Badge variant="outline" className={badge.className}>
												{badge.label}
											</Badge>
										</TableCell>
										<TableCell className="text-muted-foreground">
											{entry.time}
										</TableCell>
									</TableRow>
								);
							})}
						</TableBody>
					</Table>
				</div>
			</CardContent>
		</Card>
	);
}
