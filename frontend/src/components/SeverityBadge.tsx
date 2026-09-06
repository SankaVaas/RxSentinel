import clsx from "clsx";
import type { Severity } from "@/api/client";

const LABELS: Record<Severity, string> = {
  low: "Low",
  moderate: "Moderate",
  high: "High",
  contraindicated: "Contraindicated",
};

const STYLES: Record<Severity, string> = {
  low: "bg-blue-100 text-blue-800 border-blue-300",
  moderate: "bg-amber-100 text-amber-800 border-amber-300",
  high: "bg-red-100 text-red-800 border-red-300",
  contraindicated: "bg-red-900 text-white border-red-950",
};

export default function SeverityBadge({ severity }: { severity: Severity }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium",
        STYLES[severity]
      )}
    >
      {LABELS[severity]}
    </span>
  );
}
