import type { AgentRunStep } from "@/api/client";

const NODE_LABELS: Record<string, string> = {
  patient_context: "1. Patient context loaded",
  retrieval: "2. Literature retrieval",
  interaction_tool: "3. Structured interaction verification",
  reasoning: "4. Clinical reasoning",
  critique: "5. Adversarial critique",
  escalation: "6. Escalation routing",
};

export default function AgentTraceViewer({ steps }: { steps: AgentRunStep[] }) {
  return (
    <ol className="space-y-3">
      {steps.map((step) => (
        <li key={step.step_index} className="rounded-md border border-slate-200 p-3">
          <div className="flex items-center justify-between">
            <span className="font-medium text-sm">
              {NODE_LABELS[step.node_name] ?? step.node_name}
            </span>
            {step.duration_ms !== null && (
              <span className="text-xs text-slate-500">{step.duration_ms}ms</span>
            )}
          </div>
          <details className="mt-2 text-xs">
            <summary className="cursor-pointer text-slate-500">View input / output</summary>
            <pre className="mt-1 overflow-x-auto rounded bg-slate-900 text-slate-100 p-2">
              {JSON.stringify({ input: step.input, output: step.output }, null, 2)}
            </pre>
          </details>
        </li>
      ))}
    </ol>
  );
}
