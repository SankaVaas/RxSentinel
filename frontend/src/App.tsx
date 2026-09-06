import { Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import PatientProfile from "./pages/PatientProfile";
import InteractionReport from "./pages/InteractionReport";
import AuditTrail from "./pages/AuditTrail";

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white px-6 py-4 flex items-center gap-6">
        <Link to="/" className="font-semibold text-lg">
          RxSentinel
        </Link>
        <span className="text-xs text-slate-500">
          Decision support only — not a certified medical device
        </span>
      </header>

      <main className="p-6 max-w-5xl mx-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/patients/:patientId" element={<PatientProfile />} />
          <Route path="/patients/:patientId/report" element={<InteractionReport />} />
          <Route path="/agent-runs/:agentRunId/trace" element={<AuditTrail />} />
        </Routes>
      </main>
    </div>
  );
}
