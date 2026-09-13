import type { InteractionFinding } from "@/api/client";

export default function EscalationBanner({ findings }: { findings: InteractionFinding[] }) {
  const escalated = findings.filter((f) => f.status === "escalated");
  if (escalated.length === 0) return null;

  return (
    <div className="rounded-lg border border-severity-contraindicated-border bg-severity-contraindicated-bg text-white p-4 mb-4">
      <p className="font-semibold">
        {escalated.length} urgent interaction{escalated.length > 1 ? "s" : ""} require immediate review
      </p>
      <ul className="mt-1 text-sm list-disc list-inside space-y-0.5">
        {escalated.map((f) => (
          <li key={f.id}>
            {f.drug_pair.join(" + ")} — {f.mechanism}
          </li>
        ))}
      </ul>
    </div>
  );
}
