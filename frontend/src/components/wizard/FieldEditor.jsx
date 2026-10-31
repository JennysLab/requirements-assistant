// Rendert ein Feld aus der Template-Definition (text / textarea / select).
export default function FieldEditor({ field, value, onChange }) {
  const base = "w-full rounded-sm border border-border bg-surface px-2 py-1.5 text-sm";
  return (
    <label className="block">
      <span className="mb-1 block text-xs font-medium text-muted">{field.label}</span>
      {field.type === "textarea" ? (
        <textarea rows={3} value={value || ""} placeholder={field.hint} onChange={(e) => onChange(e.target.value)} className={base} />
      ) : field.type === "select" ? (
        <select value={value || ""} onChange={(e) => onChange(e.target.value)} className={base}>
          {field.options.map((o) => <option key={o}>{o}</option>)}
        </select>
      ) : (
        <input value={value || ""} onChange={(e) => onChange(e.target.value)} className={base} />
      )}
    </label>
  );
}
