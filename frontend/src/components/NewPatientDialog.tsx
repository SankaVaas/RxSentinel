import { useEffect, useRef, useState, type FormEvent } from "react";
import { useMutation } from "@tanstack/react-query";
import { createPatient, type PatientCreatePayload } from "@/api/client";
import { useToast } from "@/context/ToastContext";

interface Props {
  onClose: () => void;
  onCreated: (patientId: string) => void;
}

const SEX_OPTIONS = ["Female", "Male", "Other"];

export default function NewPatientDialog({ onClose, onCreated }: Props) {
  const { notify } = useToast();
  const dialogRef = useRef<HTMLDivElement>(null);
  const [form, setForm] = useState<PatientCreatePayload>({
    mrn: "",
    first_name: "",
    last_name: "",
    date_of_birth: "",
    sex: "Female",
    egfr: undefined,
    hepatic_impairment: "",
    allergies: "",
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKeyDown);
    dialogRef.current?.querySelector("input")?.focus();
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  const mutation = useMutation({
    mutationFn: () =>
      createPatient({
        ...form,
        egfr: form.egfr ? Number(form.egfr) : null,
        hepatic_impairment: form.hepatic_impairment || null,
        allergies: form.allergies || null,
      }),
    onSuccess: (patient) => {
      notify(`Patient ${patient.first_name} ${patient.last_name} created`);
      onCreated(patient.id);
    },
    onError: (err: unknown) => {
      const message =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        "Could not create patient. Check the form and try again.";
      setError(message);
    },
  });

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    mutation.mutate();
  };

  return (
    <div
      className="fixed inset-0 z-40 bg-ink/40 flex items-start justify-center pt-16"
      onMouseDown={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="new-patient-title"
        className="bg-white rounded-lg shadow-panel border border-line w-full max-w-md"
      >
        <div className="px-5 py-4 border-b border-line flex items-center justify-between">
          <h2 id="new-patient-title" className="font-semibold text-sm">
            New patient
          </h2>
          <button onClick={onClose} aria-label="Close" className="text-slate hover:text-ink text-sm">
            Close
          </button>
        </div>

        <form onSubmit={handleSubmit} className="px-5 py-4 space-y-3">
          {error && (
            <p className="text-sm text-severity-high-fg bg-severity-high-bg border border-severity-high-border rounded-md px-3 py-2">
              {error}
            </p>
          )}

          <div className="grid grid-cols-2 gap-3">
            <Field label="First name" required>
              <input
                required
                className="input"
                value={form.first_name}
                onChange={(e) => setForm({ ...form, first_name: e.target.value })}
              />
            </Field>
            <Field label="Last name" required>
              <input
                required
                className="input"
                value={form.last_name}
                onChange={(e) => setForm({ ...form, last_name: e.target.value })}
              />
            </Field>
          </div>

          <Field label="MRN" required>
            <input
              required
              className="input font-data"
              value={form.mrn}
              onChange={(e) => setForm({ ...form, mrn: e.target.value })}
              placeholder="e.g. 100234"
            />
          </Field>

          <div className="grid grid-cols-2 gap-3">
            <Field label="Date of birth" required>
              <input
                required
                type="date"
                className="input"
                value={form.date_of_birth}
                onChange={(e) => setForm({ ...form, date_of_birth: e.target.value })}
              />
            </Field>
            <Field label="Sex" required>
              <select
                className="input"
                value={form.sex}
                onChange={(e) => setForm({ ...form, sex: e.target.value })}
              >
                {SEX_OPTIONS.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </Field>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <Field label="eGFR (mL/min/1.73m²)">
              <input
                type="number"
                step="0.1"
                className="input"
                value={form.egfr ?? ""}
                onChange={(e) => setForm({ ...form, egfr: e.target.value ? Number(e.target.value) : undefined })}
              />
            </Field>
            <Field label="Hepatic impairment">
              <input
                className="input"
                value={form.hepatic_impairment ?? ""}
                onChange={(e) => setForm({ ...form, hepatic_impairment: e.target.value })}
                placeholder="None"
              />
            </Field>
          </div>

          <Field label="Allergies">
            <input
              className="input"
              value={form.allergies ?? ""}
              onChange={(e) => setForm({ ...form, allergies: e.target.value })}
              placeholder="None known"
            />
          </Field>

          <div className="pt-2 flex justify-end gap-2">
            <button type="button" onClick={onClose} className="text-sm text-slate px-3 py-1.5">
              Cancel
            </button>
            <button
              type="submit"
              disabled={mutation.isPending}
              className="bg-ink text-white text-sm font-medium px-4 py-1.5 rounded-md hover:bg-teal-dark disabled:opacity-50"
            >
              {mutation.isPending ? "Creating…" : "Create patient"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function Field({
  label,
  required,
  children,
}: {
  label: string;
  required?: boolean;
  children: React.ReactNode;
}) {
  return (
    <label className="block">
      <span className="block text-xs text-slate mb-1">
        {label}
        {required && <span className="text-severity-high-fg"> *</span>}
      </span>
      {children}
    </label>
  );
}
