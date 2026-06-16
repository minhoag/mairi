import { create } from "zustand";
// import { persist } from 'zustand/middleware';
import type {
	NotificationAction,
	NotificationStatus,
} from "@/components/ui/notification-card.tsx";

export type Notification = {
	id: string;
	title: string;
	body: string;
	status: NotificationStatus;
	createdAt: string;
	actions?: NotificationAction[];
};

type NotificationState = {
	notifications: Notification[];
	markAsRead: (id: string) => void;
	markAllAsRead: () => void;
	removeNotification: (id: string) => void;
	addNotification: (notification: Omit<Notification, "status">) => void;
	unreadCount: () => number;
};

const mockNotifications: Notification[] = [
	// MOCKS — device upload failures from log
	{
		id: "dev-fail-1",
		title: "Upload failed — RPi-C3D4",
		body: "Device RPi-C3D4 failed to push road data at 2026-06-17 13:45. Retried successfully at 13:47.",
		status: "unread",
		createdAt: new Date("2026-06-17T13:45:00").toISOString(),
	},
	{
		id: "dev-fail-2",
		title: "Upload failed — RPi-E5F6",
		body: "Device RPi-E5F6 failed to push road data at 2026-06-17 13:27. Retried successfully at 13:29.",
		status: "unread",
		createdAt: new Date("2026-06-17T13:27:00").toISOString(),
	},
	{
		id: "dev-fail-3",
		title: "Upload failed — RPi-G7H8",
		body: "Device RPi-G7H8 failed to push road data at 2026-06-17 13:07. Retried successfully at 13:09.",
		status: "unread",
		createdAt: new Date("2026-06-17T13:07:00").toISOString(),
	},
	{
		id: "dev-fail-4",
		title: "Upload failed — RPi-A1B2",
		body: "Device RPi-A1B2 failed to push road data at 2026-06-17 12:49. Retried successfully at 12:51.",
		status: "unread",
		createdAt: new Date("2026-06-17T12:49:00").toISOString(),
	},
];
// END MOCKS

export const useNotificationStore = create<NotificationState>()(
	// To enable persistence across refreshes, uncomment the persist wrapper below:
	// persist(
	(set, get) => ({
		notifications: mockNotifications,

		markAsRead: (id) =>
			set((state) => ({
				notifications: state.notifications.map((n) =>
					n.id === id ? { ...n, status: "read" as const } : n,
				),
			})),

		markAllAsRead: () =>
			set((state) => ({
				notifications: state.notifications.map((n) => ({
					...n,
					status: "read" as const,
				})),
			})),

		removeNotification: (id) =>
			set((state) => ({
				notifications: state.notifications.filter((n) => n.id !== id),
			})),

		addNotification: (notification) =>
			set((state) => ({
				notifications: [
					{ ...notification, status: "unread" as const },
					...state.notifications,
				],
			})),

		unreadCount: () =>
			get().notifications.filter((n) => n.status === "unread").length,
	}),
	//   ,
	//   { name: 'notifications' }
	// )
);
