import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getAgentRunTrace } from "@/api/client";
import AgentTraceViewer from "@/components/AgentTraceViewer";

export default function AuditTrail() {
  const { agentRunId } = useParams<{ agentRunId: string }>();

  const { data, isLoading } = useQuery({
    queryKey: ["agent-run-trace", agentRunId],
    queryFn: () => getAgentRunTrace(agentRunId!),
    enabled: !!agentRunId,
  });

  if (isLoading || !data) return <p className="text-sm text-slate">Loading trace…</p>;

  return (
    <div>
      <Link to=".." relative="path" className="text-xs text-slate hover:text-ink">
        ← Back
      </Link>
      <h1 className="text-lg font-semibold mt-1">Agent run trace</h1>
      <p className="text-sm text-slate mb-4 font-data">
        {data.agent_run_id} · {data.status}
      </p>
      <AgentTraceViewer steps={data.steps} />
    </div>
  );
}
