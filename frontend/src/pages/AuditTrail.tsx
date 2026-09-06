import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getAgentRunTrace } from "@/api/client";
import AgentTraceViewer from "@/components/AgentTraceViewer";

export default function AuditTrail() {
  const { agentRunId } = useParams<{ agentRunId: string }>();

  const { data } = useQuery({
    queryKey: ["agent-run-trace", agentRunId],
    queryFn: () => getAgentRunTrace(agentRunId!),
    enabled: !!agentRunId,
  });

  if (!data) return <p className="text-slate-500 text-sm">Loading trace…</p>;

  return (
    <div>
      <h1 className="text-xl font-semibold mb-1">Agent run trace</h1>
      <p className="text-sm text-slate-500 mb-4">
        Run {data.agent_run_id} · status: {data.status}
      </p>
      <AgentTraceViewer steps={data.steps} />
    </div>
  );
}
