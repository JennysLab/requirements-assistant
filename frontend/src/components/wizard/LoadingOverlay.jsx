import { Loader2 } from "lucide-react";
export default function LoadingOverlay() {
  return (
    <div role="status" className="fixed inset-0 z-50 flex items-center justify-center bg-ink/30">
      <div className="flex items-center gap-3 rounded-md bg-surface px-5 py-4 text-sm shadow">
        <Loader2 className="animate-spin" size={18} /> Wir generieren den nächsten Schritt…
      </div>
    </div>
  );
}
