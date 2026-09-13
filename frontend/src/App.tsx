import { Routes, Route, NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";
import PatientsList from "./pages/PatientsList";
import PatientProfile from "./pages/PatientProfile";
import InteractionReport from "./pages/InteractionReport";
import AuditTrail from "./pages/AuditTrail";
import NewPatientDialog from "./components/NewPatientDialog";

const NAV_ITEMS = [{ label: "Patients", to: "/" }];

export default function App() {
  const [showNewPatient, setShowNewPatient] = useState(false);
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex bg-paper text-ink">
      <aside className="w-56 shrink-0 border-r border-line bg-white flex flex-col">
        <div className="px-5 py-5 border-b border-line">
          <span className="text-base font-semibold tracking-tight">RxSentinel</span>
          <p className="text-xs text-slate mt-0.5">Polypharmacy safety</p>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end
              className={({ isActive }) =>
                "block rounded-md px-3 py-2 text-sm font-medium " +
                (isActive ? "bg-teal-light text-teal-dark" : "text-slate hover:bg-paper hover:text-ink")
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="px-4 py-4 border-t border-line">
          <p className="text-xs text-slate leading-relaxed">
            Decision support only. Not a certified medical device.
          </p>
        </div>
      </aside>

      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-14 border-b border-line bg-white flex items-center justify-between px-6">
          <div />
          <button
            onClick={() => setShowNewPatient(true)}
            className="bg-ink text-white text-sm font-medium px-3.5 py-1.5 rounded-md hover:bg-teal-dark transition-colors"
          >
            New patient
          </button>
        </header>

        <main className="flex-1 px-6 py-6 max-w-5xl w-full mx-auto">
          <Routes>
            <Route path="/" element={<PatientsList />} />
            <Route path="/patients/:patientId" element={<PatientProfile />} />
            <Route path="/patients/:patientId/report" element={<InteractionReport />} />
            <Route path="/agent-runs/:agentRunId/trace" element={<AuditTrail />} />
          </Routes>
        </main>
      </div>

      {showNewPatient && (
        <NewPatientDialog
          onClose={() => setShowNewPatient(false)}
          onCreated={(patientId) => {
            setShowNewPatient(false);
            navigate(`/patients/${patientId}`);
          }}
        />
      )}
    </div>
  );
}
