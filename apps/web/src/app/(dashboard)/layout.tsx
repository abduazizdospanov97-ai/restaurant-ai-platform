import type { ReactNode } from 'react';

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen grid grid-cols-1 lg:grid-cols-[260px_1fr]">
      <aside className="glass p-4">Sidebar</aside>
      <main className="p-4 lg:p-6">{children}</main>
    </div>
  );
}
