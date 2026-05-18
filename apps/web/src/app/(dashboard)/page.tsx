export default function DashboardPage() {
  return (
    <section>
      <h1 className="text-2xl font-semibold">Basqarıw paneli</h1>
      <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {['Studentler', 'Gruppalar', 'Davomat', 'Aylıq kirim'].map((item) => (
          <article key={item} className="glass rounded-xl p-4">{item}</article>
        ))}
      </div>
    </section>
  );
}
