import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { addMedication, type DrugSearchResult } from "@/api/client";
import { useToast } from "@/context/ToastContext";
import MedicationSearchInput from "./MedicationSearchInput";

export default function MedicationEntryForm({ patientId }: { patientId: string }) {
  const [selected, setSelected] = useState<DrugSearchResult | null>(null);
  const [dose, setDose] = useState("");
  const [frequency, setFrequency] = useState("");
  const queryClient = useQueryClient();
  const { notify } = useToast();

  const mutation = useMutation({
    mutationFn: () => addMedication(patientId, { rxcui: selected!.rxcui, dose, frequency }),
    onSuccess: (med) => {
      queryClient.invalidateQueries({ queryKey: ["medications", patientId] });
      queryClient.invalidateQueries({ queryKey: ["patient", patientId] });
      notify(`Added ${med.name} to medication list`);
      setSelected(null);
      setDose("");
      setFrequency("");
    },
    onError: () => notify("Couldn't add medication. Try again.", "error"),
  });

  return (
    <form
      className="flex flex-wrap items-end gap-2 border border-line rounded-lg bg-white p-3"
      onSubmit={(e) => {
        e.preventDefault();
        if (selected) mutation.mutate();
      }}
    >
      <div>
        <label className="block text-xs text-slate mb-1">Medication</label>
        {selected ? (
          <div className="input flex items-center justify-between w-72">
            <span>{selected.name}</span>
            <button
              type="button"
              onClick={() => setSelected(null)}
              className="text-slate hover:text-ink text-xs"
              aria-label="Clear selected medication"
            >
              Change
            </button>
          </div>
        ) : (
          <MedicationSearchInput onSelect={setSelected} />
        )}
      </div>
      <div>
        <label className="block text-xs text-slate mb-1">Dose</label>
        <input className="input w-28" value={dose} onChange={(e) => setDose(e.target.value)} placeholder="10mg" />
      </div>
      <div>
        <label className="block text-xs text-slate mb-1">Frequency</label>
        <input
          className="input w-28"
          value={frequency}
          onChange={(e) => setFrequency(e.target.value)}
          placeholder="Once daily"
        />
      </div>
      <button
        type="submit"
        disabled={!selected || mutation.isPending}
        className="bg-ink text-white text-sm font-medium rounded-md px-3.5 py-1.5 disabled:opacity-40 hover:bg-teal-dark"
      >
        {mutation.isPending ? "Adding…" : "Add medication"}
      </button>
    </form>
  );
}
