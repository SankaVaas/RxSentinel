import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { addMedication } from "@/api/client";

export default function MedicationEntryForm({ patientId }: { patientId: string }) {
  const [rxcui, setRxcui] = useState("");
  const [dose, setDose] = useState("");
  const [frequency, setFrequency] = useState("");
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: () => addMedication(patientId, { rxcui, dose, frequency }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["medications", patientId] });
      setRxcui("");
      setDose("");
      setFrequency("");
    },
  });

  return (
    <form
      className="flex flex-wrap gap-2 items-end"
      onSubmit={(e) => {
        e.preventDefault();
        mutation.mutate();
      }}
    >
      <div>
        <label className="block text-xs text-slate-500">RxCUI</label>
        <input
          className="border rounded px-2 py-1 text-sm"
          value={rxcui}
          onChange={(e) => setRxcui(e.target.value)}
          required
        />
      </div>
      <div>
        <label className="block text-xs text-slate-500">Dose</label>
        <input className="border rounded px-2 py-1 text-sm" value={dose} onChange={(e) => setDose(e.target.value)} />
      </div>
      <div>
        <label className="block text-xs text-slate-500">Frequency</label>
        <input
          className="border rounded px-2 py-1 text-sm"
          value={frequency}
          onChange={(e) => setFrequency(e.target.value)}
        />
      </div>
      <button
        type="submit"
        disabled={mutation.isPending}
        className="bg-slate-900 text-white text-sm rounded px-3 py-1.5 disabled:opacity-50"
      >
        {mutation.isPending ? "Adding…" : "Add medication"}
      </button>
    </form>
  );
}
