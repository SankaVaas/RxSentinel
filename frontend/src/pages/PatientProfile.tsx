import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getPatient, listMedications } from "@/api/client";
import MedicationEntryForm from "@/components/MedicationEntryForm";

export default function PatientProfile() {
  const { patientId } = useParams<{ patientId: string }>();

  const { data: patient } = useQuery({
    queryKey: ["patient", patientId],
    queryFn: () => getPatient(patientId!),
    enabled: !!patientId,
  });

  const { data: medications } = useQuery({
    queryKey: ["medications", patientId],
    queryFn: () => listMedications(patientId!),
    enabled: !!patientId,
  });

  if (!patient) return <p className="text-slate-500 text-sm">Loading patient…</p>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold">MRN {patient.mrn}</h1>
        <p className="text-sm text-slate-600">
          {patient.sex} · eGFR {patient.egfr ?? "—"} ·{" "}
          {patient.hepatic_impairment ?? "No hepatic impairment noted"}
        </p>
      </div>

      <section>
        <h2 className="font-medium mb-2">Active medications</h2>
        <ul className="space-y-1 mb-4">
          {medications?.map((m) => (
            <li key={m.id} className="text-sm border rounded px-3 py-2 flex justify-between">
              <span>{m.name}</span>
              <span className="text-slate-500">
                {m.dose} {m.frequency}
              </span>
            </li>
          ))}
        </ul>
        <MedicationEntryForm patientId={patientId!} />
      </section>

      <Link
        to={`/patients/${patientId}/report`}
        className="inline-block bg-slate-900 text-white text-sm rounded px-4 py-2"
      >
        Run interaction safety check
      </Link>
    </div>
  );
}
