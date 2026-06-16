import { createFileRoute } from "@tanstack/react-router";
import { Icons } from "@/components/icons.tsx";
import PageContainer from "@/components/layout/page-container.tsx";
import { Badge } from "@/components/ui/badge.tsx";
import {
	Card,
	CardAction,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@/components/ui/card.tsx";
import { AreaGraph } from "@/features/overview/components/area-graph.tsx";
import { BarGraph } from "@/features/overview/components/bar-graph.tsx";
import { PieGraph } from "@/features/overview/components/pie-graph.tsx";
import { RecentSales } from "@/features/overview/components/recent-sales.tsx";

export const Route = createFileRoute("/dashboard/overview")({
	component: OverviewPage,
});

function OverviewPage() {
	return (
		<PageContainer>
			<div className="flex flex-1 flex-col space-y-2">
				<div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-7">
					<div className="col-span-4">
						<AreaGraph />
					</div>
					<div className="col-span-4 md:col-span-3 overflow-auto">
						<RecentSales />
					</div>
					{/*<div className="col-span-4">
						<AreaGraph />
					</div>
					<div className="col-span-4 min-h-0 md:col-span-3">
						<PieGraph />
					</div>*/}
				</div>
			</div>
		</PageContainer>
	);
}
