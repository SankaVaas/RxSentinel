import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { listPatients } from "@/api/client";
import TableSkeleton from "@/components/TableSkeleton";

function useDebouncedValue<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);
  return debounced;
}

function calculateAge(dob: string): number {
  const birth = new Date(dob);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) age--;
  return age;
}

export default function PatientsList() {
  const [search, setSearch] = useState("");
  const debouncedSearch = useDebouncedValue(search, 300);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["patients", debouncedSearch],
    queryFn: () => listPatients({ q: debouncedSearch || undefined, limit: 25 }),
  });

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-lg font-semibold">Patients</h1>
      </div>

      <div className="mb-4">
        <input
          type="search"
          placeholder="Search by name or MRN"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="input max-w-sm"
          aria-label="Search patients"
        />
      </div>

      <div className="border border-line rounded-lg bg-white overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-line text-left text-slate">
              <th className="px-4 py-2.5 font-medium">MRN</th>
              <th className="px-4 py-2.5 font-medium">Name</th>
              <th className="px-4 py-2.5 font-medium">Age / sex</th>
              <th className="px-4 py-2.5 font-medium">Active meds</th>
              <th className="px-4 py-2.5"></th>
            </tr>
          </thead>
          <tbody>
            {isLoading && <TableSkeleton columns={5} rows={4} />}

            {isError && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-sm text-severity-high-fg">
                  Couldn't load patients. Check the backend connection and retry.
                </td>
              </tr>
            )}

            {data && data.results.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-sm text-slate">
                  {search
                    ? `No patients match "${search}".`
                    : "No patients yet. Add one with the New patient button."}
                </td>
              </tr>
            )}

            {data?.results.map((patient) => (
              <tr key={patient.id} className="border-b border-line last:border-0 hover:bg-paper">
                <td className="px-4 py-2.5 font-data text-slate">{patient.mrn}</td>
                <td className="px-4 py-2.5 font-medium">
                  {patient.last_name}, {patient.first_name}
                </td>
                <td className="px-4 py-2.5 text-slate">
                  {calculateAge(patient.date_of_birth)} · {patient.sex}
                </td>
                <td className="px-4 py-2.5 text-slate">{patient.active_medication_count}</td>
                <td className="px-4 py-2.5 text-right">
                  <Link to={`/patients/${patient.id}`} className="text-teal-dark hover:underline font-medium">
                    Open
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {data && data.total > (data.results?.length ?? 0) && (
        <p className="text-xs text-slate mt-2">
          Showing {data.results.length} of {data.total} patients. Refine your search to narrow results.
        </p>
      )}
    </div>
  );
}
