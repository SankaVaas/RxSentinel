import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getPatient, listMedications } from "@/api/client";
import MedicationEntryForm from "@/components/MedicationEntryForm";

function calculateAge(dob: string): number {
  const birth = new Date(dob);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) age--;
  return age;
}

export default function PatientProfile() {
  const { patientId } = useParams<{ patientId: string }>();

  const { data: patient, isLoading: patientLoading, isError: patientError } = useQuery({
    queryKey: ["patient", patientId],
    queryFn: () => getPatient(patientId!),
    enabled: !!patientId,
  });

  const { data: medications, isLoading: medsLoading } = useQuery({
    queryKey: ["medications", patientId],
    queryFn: () => listMedications(patientId!),
    enabled: !!patientId,
  });

  if (patientError) {
    return (
      <div className="border border-severity-high-border bg-severity-high-bg text-severity-high-fg rounded-lg px-4 py-3 text-sm">
        Couldn't find this patient. <Link to="/" className="underline">Back to patients</Link>
      </div>
    );
  }

  if (patientLoading || !patient) {
    return <p className="text-sm text-slate">Loading patient…</p>;
  }

  return (
    <div className="space-y-6">
      <div>
        <Link to="/" className="text-xs text-slate hover:text-ink">
          ← Patients
        </Link>
        <div className="flex items-baseline gap-3 mt-1">
          <h1 className="text-lg font-semibold">
            {patient.last_name}, {patient.first_name}
          </h1>
          <span className="font-data text-sm text-slate">MRN {patient.mrn}</span>
        </div>
      </div>

      <dl className="grid grid-cols-2 sm:grid-cols-4 gap-4 border border-line rounded-lg bg-white p-4">
        <div>
          <dt className="text-xs text-slate">Age / sex</dt>
          <dd className="text-sm font-medium mt-0.5">
            {calculateAge(patient.date_of_birth)} · {patient.sex}
          </dd>
        </div>
        <div>
          <dt className="text-xs text-slate">eGFR</dt>
          <dd className="text-sm font-medium mt-0.5">
            {patient.egfr ?? "Not recorded"}
          </dd>
        </div>
        <div>
          <dt className="text-xs text-slate">Hepatic impairment</dt>
          <dd className="text-sm font-medium mt-0.5">{patient.hepatic_impairment ?? "None noted"}</dd>
        </div>
        <div>
          <dt className="text-xs text-slate">Allergies</dt>
          <dd className="text-sm font-medium mt-0.5">{patient.allergies ?? "None known"}</dd>
        </div>
      </dl>

      <section>
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-sm font-semibold">Active medications</h2>
          <span className="text-xs text-slate">{medications?.length ?? 0} total</span>
        </div>

        <div className="border border-line rounded-lg bg-white overflow-hidden mb-3">
          {medsLoading && <div className="px-4 py-3 text-sm text-slate">Loading medications…</div>}

          {medications && medications.length === 0 && (
            <div className="px-4 py-6 text-sm text-slate text-center">
              No active medications. Add one below to get started.
            </div>
          )}

          {medications?.map((m, i) => (
            <div
              key={m.id}
              className={
                "flex items-center justify-between px-4 py-2.5 text-sm" +
                (i < medications.length - 1 ? " border-b border-line" : "")
              }
            >
              <span className="font-medium">{m.name}</span>
              <span className="text-slate">
                {m.dose} {m.frequency}
              </span>
            </div>
          ))}
        </div>

        <MedicationEntryForm patientId={patientId!} />
      </section>

      <Link
        to={`/patients/${patientId}/report`}
        className={
          "inline-block text-sm font-medium rounded-md px-4 py-2 " +
          (medications && medications.length >= 2
            ? "bg-teal text-white hover:bg-teal-dark"
            : "bg-line text-slate pointer-events-none")
        }
        aria-disabled={!medications || medications.length < 2}
      >
        Run interaction safety check
      </Link>
      {medications && medications.length < 2 && (
        <p className="text-xs text-slate mt-1">Add at least 2 medications to run a check.</p>
      )}
    </div>
  );
}
