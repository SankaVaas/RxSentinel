import { useParams, Link } from "react-router-dom";
import { useEffect, useRef } from "react";
import { useInteractionCheck } from "@/hooks/useInteractionCheck";
import SeverityBadge from "@/components/SeverityBadge";
import EvidenceCitationCard from "@/components/EvidenceCitationCard";
import EscalationBanner from "@/components/EscalationBanner";

export default function InteractionReport() {
  const { patientId } = useParams<{ patientId: string }>();
  const { mutate, data, isPending, isError } = useInteractionCheck(patientId!);
  const hasRun = useRef(false);

  useEffect(() => {
    if (hasRun.current) return;
    hasRun.current = true;
    mutate();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [patientId]);

  if (isPending) {
    return (
      <div className="flex items-center gap-2 text-sm text-slate">
        <span className="h-2 w-2 rounded-full bg-teal animate-pulse" />
        Running interaction safety check…
      </div>
    );
  }

  if (isError) {
    return (
      <div className="border border-severity-high-border bg-severity-high-bg text-severity-high-fg rounded-lg px-4 py-3 text-sm">
        Interaction check failed. <button onClick={() => mutate()} className="underline">Retry</button>
      </div>
    );
  }
  if (!data) return null;

  return (
    <div className="space-y-4">
      <div>
        <Link to={`/patients/${patientId}`} className="text-xs text-slate hover:text-ink">
          ← Patient
        </Link>
        <div className="flex items-center justify-between mt-1">
          <h1 className="text-lg font-semibold">Interaction findings</h1>
          <Link to={`/agent-runs/${data.agent_run_id}/trace`} className="text-sm text-teal-dark hover:underline">
            View agent trace
          </Link>
        </div>
      </div>

      <EscalationBanner findings={data.findings} />

      {data.findings.length === 0 && (
        <div className="border border-line rounded-lg bg-white px-4 py-8 text-center text-sm text-slate">
          No interaction concerns identified for this medication list.
        </div>
      )}

      <div className="space-y-3">
        {data.findings.map((finding) => (
          <div key={finding.id} className="border border-line rounded-lg bg-white p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="font-medium">{finding.drug_pair.join(" + ")}</span>
              <SeverityBadge severity={finding.severity} />
              <span className="text-xs text-slate">{finding.status.replace("_", " ")}</span>
            </div>
            <p className="text-sm text-ink mb-1">
              <span className="text-slate">Mechanism: </span>
              {finding.mechanism}
            </p>
            <p className="text-sm text-ink mb-2">
              <span className="text-slate">Recommendation: </span>
              {finding.clinical_recommendation}
            </p>
            {finding.critique_notes && (
              <p className="text-xs text-slate italic mb-2">Critique: {finding.critique_notes}</p>
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