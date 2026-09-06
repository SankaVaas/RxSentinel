import axios from "axios";

export const apiClient = axios.create({
  baseURL: "/api/v1",
  timeout: 30_000,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// --- Types mirroring backend/app/schemas ---

export interface Patient {
  id: string;
  mrn: string;
  date_of_birth: string;
  sex: string;
  egfr: number | null;
  hepatic_impairment: string | null;
  allergies: string | null;
}

export interface Medication {
  id: string;
  rxcui: string;
  name: string;
  dose: string | null;
  frequency: string | null;
  active: boolean;
}

export type Severity = "low" | "moderate" | "high" | "contraindicated";
export type FindingStatus = "auto_cleared" | "pending_review" | "escalated" | "acknowledged";

export interface EvidenceItem {
  source: string;
  citation: string;
  url: string | null;
  excerpt: string | null;
}

export interface InteractionFinding {
  id: string;
  drug_pair: [string, string];
  severity: Severity;
  status: FindingStatus;
  mechanism: string;
  clinical_recommendation: string;
  evidence: EvidenceItem[];
  critique_notes: string | null;
}

export interface InteractionCheckResponse {
  agent_run_id: string;
  findings: InteractionFinding[];
}

export interface AgentRunStep {
  step_index: number;
  node_name: string;
  input: Record<string, unknown>;
  output: Record<string, unknown>;
  duration_ms: number | null;
}

// --- API calls ---

export const getPatient = (patientId: string) =>
  apiClient.get<Patient>(`/patients/${patientId}`).then((r) => r.data);

export const listMedications = (patientId: string) =>
  apiClient.get<Medication[]>(`/patients/${patientId}/medications`).then((r) => r.data);

export const addMedication = (patientId: string, payload: { rxcui: string; dose?: string; frequency?: string }) =>
  apiClient.post<Medication>(`/patients/${patientId}/medications`, payload).then((r) => r.data);

export const runInteractionCheck = (patientId: string) =>
  apiClient
    .post<InteractionCheckResponse>("/interactions/check", { patient_id: patientId })
    .then((r) => r.data);

export const getAgentRunTrace = (agentRunId: string) =>
  apiClient
    .get<{ agent_run_id: string; status: string; steps: AgentRunStep[] }>(
      `/agent-runs/${agentRunId}/trace`
    )
    .then((r) => r.data);
