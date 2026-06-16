import PageContainer from "@/components/layout/page-container.tsx";
import { KanbanBoard } from "./kanban-board.tsx";
import NewTaskDialog from "./new-task-dialog.tsx";

export default function KanbanViewPage() {
	return (
		<PageContainer
			pageTitle="Kanban"
			pageDescription="Manage tasks with drag and drop"
			pageHeaderAction={<NewTaskDialog />}
		>
			<KanbanBoard />
		</PageContainer>
	);
}
