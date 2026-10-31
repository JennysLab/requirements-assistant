const map = {
  entwurf: ["Entwurf", "bg-status-reviewsoft text-status-review"],
  bestaetigt: ["Bestätigt", "bg-status-acceptedsoft text-status-accepted"],
  verworfen: ["Verworfen", "bg-status-reworksoft text-status-rework"],
};
export const statusRailColor = { entwurf: "border-l-status-review", bestaetigt: "border-l-status-accepted", verworfen: "border-l-status-rework" };
export default function StatusBadge({ status }) {
  const [label, cls] = map[status] || map.entwurf;
  return <span className={`rounded-sm px-2 py-0.5 text-xs font-medium ${cls}`}>{label}</span>;
}
