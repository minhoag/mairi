import { NotificationCenter } from "@/features/notifications/components/notification-center.tsx";
import { Breadcrumbs } from "../breadcrumbs.tsx";
import SearchInput from "../search-input.tsx";
import { ThemeModeToggle } from "../themes/theme-mode-toggle.tsx";
import { Separator } from "../ui/separator.tsx";
import { SidebarTrigger } from "../ui/sidebar.tsx";
import CtaGithub from "./cta-github.tsx";

export default function Header() {
	return (
		<header className="bg-background/60 sticky top-0 z-20 flex h-14 shrink-0 items-center justify-between gap-2 rounded-t-xl border-b backdrop-blur-md px-4">
			<div className="flex items-center gap-2">
				<SidebarTrigger className="-ml-1" />
				<Separator orientation="vertical" className="mr-2 h-4" />
				<Breadcrumbs />
			</div>

			<div className="flex items-center gap-2">
				<CtaGithub />
				<div className="hidden md:flex">
					<SearchInput />
				</div>
				<ThemeModeToggle />
				<NotificationCenter />
			</div>
		</header>
	);
}
