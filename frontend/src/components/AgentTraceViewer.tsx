import type { AgentRunStep } from "@/api/client";

const NODE_LABELS: Record<string, string> = {
  patient_context: "Patient context loaded",
  retrieval: "Literature retrieval",
  interaction_tool: "Structured interaction verification",
  reasoning: "Clinical reasoning",
  critique: "Adversarial critique",
  escalation: "Escalation routing",
};

export default function AgentTraceViewer({ steps }: { steps: AgentRunStep[] }) {
  return (
    <ol className="space-y-2">
      {steps.map((step) => (
        <li key={step.step_index} className="rounded-lg border border-line bg-white p-3">
          <div className="flex items-center justify-between">
            <span className="font-medium text-sm">
              <span className="font-data text-xs text-slate mr-2">{step.step_index + 1}</span>
              {NODE_LABELS[step.node_name] ?? step.node_name}
            </span>
            {step.duration_ms !== null && (
              <span className="font-data text-xs text-slate">{step.duration_ms}ms</span>
            )}
          </div>
          <details className="mt-2 text-xs">
            <summary className="cursor-pointer text-slate">View input / output</summary>
            <pre className="mt-1 overflow-x-auto rounded-md bg-ink text-paper p-2 font-data">
              {JSON.stringify({ input: step.input, output: step.output }, null, 2)}
            </pre>
          </details>
        </li>
      ))}
    </ol>
  );
}
