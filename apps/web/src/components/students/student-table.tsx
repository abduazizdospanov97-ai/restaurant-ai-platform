export type StudentRow = {
  id: string;
  fullName: string;
  phone?: string;
  status: 'ACTIVE' | 'INACTIVE';
};

export function StudentTable({ rows }: { rows: StudentRow[] }) {
  return (
    <div className="glass rounded-xl p-4 overflow-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left border-b border-white/20">
            <th className="py-2">Student</th>
            <th className="py-2">Telefon</th>
            <th className="py-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className="border-b border-white/10">
              <td className="py-2">{row.fullName}</td>
              <td className="py-2">{row.phone ?? '-'}</td>
              <td className="py-2">{row.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
