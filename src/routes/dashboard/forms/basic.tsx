import { createFileRoute } from "@tanstack/react-router";
import DemoForm from "@/components/forms/demo-form";
import PageContainer from "@/components/layout/page-container";

export const Route = createFileRoute("/dashboard/forms/basic")({
	head: () => ({ meta: [{ title: "Dashboard: Basic Form" }] }),
	component: () => (
		<PageContainer
			pageTitle="Basic Form"
			pageDescription="A comprehensive form demo with all field types."
		>
			<DemoForm />
		</PageContainer>
	),
});
