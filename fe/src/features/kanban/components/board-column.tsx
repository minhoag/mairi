import { Icons } from "@/components/icons.tsx";
import { Badge } from "@/components/ui/badge.tsx";
import { Button } from "@/components/ui/button.tsx";
import { KanbanColumn, KanbanColumnHandle } from "@/components/ui/kanban.tsx";
import type { Task } from "../utils/store.ts";
import { TaskCard } from "./task-card.tsx";

const COLUMN_TITLES: Record<string, string> = {
	backlog: "Backlog",
	inProgress: "In Progress",
	review: "Review",
	done: "Done",
};

interface TaskColumnProps
	extends Omit<React.ComponentProps<typeof KanbanColumn>, "children"> {
	tasks: Task[];
}

export function TaskColumn({ value, tasks, ...props }: TaskColumnProps) {
	return (
		<KanbanColumn value={value} className="w-[320px] shrink-0" {...props}>
			<div className="flex items-center justify-between">
				<div className="flex items-center gap-2">
					<span className="text-sm font-semibold">
						{COLUMN_TITLES[value] ?? value}
					</span>
					<Badge variant="secondary" className="pointer-events-none rounded-sm">
						{tasks.length}
					</Badge>
				</div>
				<KanbanColumnHandle asChild>
					<Button variant="ghost" size="icon">
						<Icons.gripVertical className="h-4 w-4" />
					</Button>
				</KanbanColumnHandle>
			</div>
			<div className="flex flex-col gap-2 p-0.5">
				{tasks.map((task) => (
					<TaskCard key={task.id} task={task} asHandle />
				))}
			</div>
		</KanbanColumn>
	);
}
