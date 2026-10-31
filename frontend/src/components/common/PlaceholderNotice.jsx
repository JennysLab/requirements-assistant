import { Info } from "lucide-react";
export default function PlaceholderNotice({ children }) {
  return (
    <div className="flex items-start gap-2 rounded-md border border-status-review/30 bg-status-reviewsoft px-3 py-2 text-sm text-ink">
      <Info size={16} className="mt-0.5 shrink-0 text-status-review" />
      <span>{children}</span>
    </div>
  );
}
