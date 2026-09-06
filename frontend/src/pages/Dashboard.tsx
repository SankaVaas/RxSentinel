import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div>
      <h1 className="text-xl font-semibold mb-4">Patients</h1>
      <p className="text-slate-600 text-sm mb-4">
        Search or select a patient to review their medication list and run an
        interaction safety check.
      </p>
      {/* TODO: patient search/list, backed by GET /api/v1/patients (add a
          list endpoint once patient volume justifies pagination). */}
      <Link
        to="/patients/00000000-0000-0000-0000-000000000001"
        className="text-blue-600 hover:underline text-sm"
      >
        Open example patient →
      </Link>
    </div>
  );
}
