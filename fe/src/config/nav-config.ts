import type { NavGroup } from "@/types/index.ts";

/**
 * Navigation configuration
 *
 * This configuration is used for both the sidebar navigation and Cmd+K bar.
 * Items are organized into groups, each rendered with a SidebarGroupLabel.
 */
export const navGroups: NavGroup[] = [
	{
		label: "Overview",
		items: [
			{
				title: "Dashboard",
				url: "/dashboard/overview",
				icon: "dashboard",
				isActive: false,
				shortcut: ["d", "d"],
				items: [],
			},
			{
				title: "Kanban",
				url: "/dashboard/kanban",
				icon: "kanban",
				shortcut: ["k", "k"],
				isActive: false,
				items: [],
			},
			{
				title: "Chat",
				url: "/dashboard/chat",
				icon: "chat",
				shortcut: ["c", "c"],
				isActive: false,
				items: [],
			},
		],
	},
	{
		label: "",
		items: [
			{
				title: "Account",
				url: "#",
				icon: "account",
				isActive: true,
				items: [
					{
						title: "Notifications",
						url: "/dashboard/notifications",
						icon: "notification",
						shortcut: ["n", "n"],
					},
				],
			},
		],
	},
];
