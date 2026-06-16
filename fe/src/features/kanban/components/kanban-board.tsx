import { useCallback, useRef } from "react";
import {
	Kanban,
	KanbanBoard as KanbanBoardPrimitive,
	KanbanOverlay,
} from "@/components/ui/kanban.tsx";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area.tsx";
import { createRestrictToContainer } from "../utils/restrict-to-container.ts";
import { useTaskStore } from "../utils/store.ts";
import { TaskColumn } from "./board-column.tsx";
import { TaskCard } from "./task-card.tsx";

export function KanbanBoard() {
	const { columns, setColumns } = useTaskStore();
	const containerRef = useRef<HTMLDivElement>(null);

	// eslint-disable-next-line react-hooks/exhaustive-deps -- factory function, stable after mount
	const restrictToBoard = useCallback(
		createRestrictToContainer(() => containerRef.current),
		[],
	);

	return (
		<div ref={containerRef}>
			<Kanban
				value={columns}
				onValueChange={setColumns}
				getItemValue={(item) => item.id}
				modifiers={[restrictToBoard]}
				autoScroll={false}
			>
				<ScrollArea className="w-full rounded-md pb-4">
					<KanbanBoardPrimitive className="flex items-start">
						{Object.entries(columns).map(([columnValue, tasks]) => (
							<TaskColumn key={columnValue} value={columnValue} tasks={tasks} />
						))}
					</KanbanBoardPrimitive>
					<ScrollBar orientation="horizontal" />
				</ScrollArea>
				<KanbanOverlay>
					{({ value, variant }) => {
						if (variant === "column") {
							const tasks = columns[value] ?? [];
							return <TaskColumn value={value} tasks={tasks} />;
						}

						const task = Object.values(columns)
							.flat()
							.find((task) => task.id === value);

						if (!task) return null;
						return <TaskCard task={task} />;
					}}
				</KanbanOverlay>
			</Kanban>
		</div>
	);
}
