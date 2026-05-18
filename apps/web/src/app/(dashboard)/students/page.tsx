import { StudentTable } from '@/components/students/student-table';

const rows = [
  { id: '1', fullName: 'Aydos Jumaniyazov', phone: '+998901112233', status: 'ACTIVE' as const },
  { id: '2', fullName: 'Madina Qudaybergenova', phone: '+998907778899', status: 'INACTIVE' as const }
];

export default function StudentsPage() {
  return (
    <section className="space-y-4">
      <div className="glass rounded-xl p-4 flex flex-col md:flex-row gap-3 md:items-center md:justify-between">
        <h1 className="text-xl font-semibold">Studentler bólimi</h1>
        <input className="rounded-lg px-3 py-2 bg-white/30 dark:bg-slate-800/50" placeholder="Search student..." />
      </div>
      <StudentTable rows={rows} />
    </section>
  );
}
