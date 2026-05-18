import Link from 'next/link';
import { navItems } from '@/lib/nav';

export function Sidebar() {
  return (
    <aside className="glass p-4 h-full">
      <h2 className="font-semibold mb-4">EduCRM</h2>
      <nav className="space-y-2">
        {navItems.map((item) => (
          <Link key={item.href} href={item.href} className="block rounded-lg px-3 py-2 hover:bg-white/20">
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
