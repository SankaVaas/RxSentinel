import { useParams, Link } from "react-router-dom";
import { useEffect } from "react";
import { useInteractionCheck } from "@/hooks/useInteractionCheck";
import SeverityBadge from "@/components/SeverityBadge";
import EvidenceCitationCard from "@/components/EvidenceCitationCard";
import EscalationBanner from "@/components/EscalationBanner";

export default function InteractionReport() {
  const { patientId } = useParams<{ patientId: string }>();
  const { mutate, data, isPending, isError } = useInteractionCheck(patientId!);

  useEffect(() => {
    mutate();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [patientId]);

  if (isPending) return <p className="text-slate-500 text-sm">Running interaction check…</p>;
  if (isError) return <p className="text-red-600 text-sm">Interaction check failed. Please retry.</p>;
  if (!data) return null;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Interaction findings</h1>
        <Link
          to={`/agent-runs/${data.agent_run_id}/trace`}
          className="text-sm text-blue-600 hover:underline"
        >
          View full agent trace →
        </Link>
      </div>

      <EscalationBanner findings={data.findings} />

      {data.findings.length === 0 && (
        <p className="text-sm text-slate-600">No interaction concerns identified for this medication list.</p>
      )}

      <div className="space-y-3">
        {data.findings.map((finding) => (
          <div key={finding.id} className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="font-medium">{finding.drug_pair.join(" + ")}</span>
              <SeverityBadge severity={finding.severity} />
              <span className="text-xs text-slate-500 uppercase">{finding.status.replace("_", " ")}</span>
            </div>
            <p className="text-sm text-slate-700 mb-1">
              <strong>Mechanism:</strong> {finding.mechanism}
            </p>
            <p className="text-sm text-slate-700 mb-2">
              <strong>Recommendation:</strong> {finding.clinical_recommendation}
            </p>
            {finding.critique_notes && (
              <p className="text-xs text-slate-500 italic mb-2">Critique: {finding.critique_notes}</p>
            )}
            <div className="grid gap-2 sm:grid-cols-2">
              {finding.evidence.map((e, i) => (
                <EvidenceCitationCard key={i} evidence={e} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
