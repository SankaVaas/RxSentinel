import type { InteractionFinding } from "@/api/client";

export default function EscalationBanner({ findings }: { findings: InteractionFinding[] }) {
  const escalated = findings.filter((f) => f.status === "escalated");
  if (escalated.length === 0) return null;

  return (
    <div className="rounded-md border border-red-300 bg-red-50 p-4 mb-4">
      <p className="font-semibold text-red-900">
        {escalated.length} urgent interaction{escalated.length > 1 ? "s" : ""} require immediate review
      </p>
      <ul className="mt-1 text-sm text-red-800 list-disc list-inside">
        {escalated.map((f) => (
          <li key={f.id}>
            {f.drug_pair.join(" + ")} — {f.mechanism}
          </li>
        ))}
      </ul>
    </div>
  );
}
