import type { Severity } from "@/api/client";

const LABELS: Record<Severity, string> = {
  low: "Low",
  moderate: "Moderate",
  high: "High",
  contraindicated: "Contraindicated",
};

const STYLE_BY_SEVERITY: Record<Severity, string> = {
  low: "text-severity-low-fg bg-severity-low-bg border-severity-low-border",
  moderate: "text-severity-moderate-fg bg-severity-moderate-bg border-severity-moderate-border",
  high: "text-severity-high-fg bg-severity-high-bg border-severity-high-border",
  contraindicated: "text-severity-contraindicated-fg bg-severity-contraindicated-bg border-severity-contraindicated-border",
};

export default function SeverityBadge({ severity }: { severity: Severity }) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${STYLE_BY_SEVERITY[severity]}`}
    >
      {LABELS[severity]}
    </span>
  );
}
