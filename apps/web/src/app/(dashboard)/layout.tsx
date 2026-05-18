import type { ReactNode } from 'react';
import { Sidebar } from '@/components/layout/sidebar';
import { TopNav } from '@/components/layout/top-nav';

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-4 p-4">
      <Sidebar />
      <main>
        <TopNav />
        {children}
      </main>
    </div>
  );
}
