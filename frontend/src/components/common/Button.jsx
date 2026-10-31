const styles = {
  primary: "bg-accent text-white hover:bg-accent-hover",
  secondary: "bg-surface text-ink border border-border hover:bg-paper",
  ghost: "text-muted hover:text-ink hover:bg-paper",
};
export default function Button({ variant = "primary", className = "", ...p }) {
  return <button {...p} className={`inline-flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition disabled:opacity-50 disabled:cursor-not-allowed ${styles[variant]} ${className}`} />;
}
