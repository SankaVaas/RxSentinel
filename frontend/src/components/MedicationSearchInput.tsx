import { useEffect, useRef, useState } from "react";
import { searchDrugs, type DrugSearchResult } from "@/api/client";

interface Props {
  onSelect: (drug: DrugSearchResult) => void;
}

/** Typeahead for drug names, backed by RxNorm's approximate-match API
 * (see backend GET /medications/search). Clinicians search by name --
 * they should never need to know or type a raw RxCUI. */
export default function MedicationSearchInput({ onSelect }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<DrugSearchResult[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (query.trim().length < 2) {
      setResults([]);
      return;
    }
    setIsLoading(true);
    const timer = setTimeout(async () => {
      try {
        const data = await searchDrugs(query.trim());
        setResults(data);
        setIsOpen(true);
      } finally {
        setIsLoading(false);
      }
    }, 250);
    return () => clearTimeout(timer);
  }, [query]);

  useEffect(() => {
    const onClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, []);

  return (
    <div ref={containerRef} className="relative w-72">
      <input
        className="input"
        placeholder="Search medication by name…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => results.length > 0 && setIsOpen(true)}
        aria-label="Search medication by name"
      />

      {isOpen && (
        <div className="absolute z-10 mt-1 w-full bg-white border border-line rounded-md shadow-panel max-h-56 overflow-y-auto">
          {isLoading && <div className="px-3 py-2 text-sm text-slate">Searching…</div>}

          {!isLoading && results.length === 0 && query.trim().length >= 2 && (
            <div className="px-3 py-2 text-sm text-slate">No matches. Try a different spelling.</div>
          )}

          {!isLoading &&
            results.map((drug) => (
              <button
                key={drug.rxcui}
                type="button"
                className="w-full text-left px-3 py-2 text-sm hover:bg-paper flex items-center justify-between"
                onClick={() => {
                  onSelect(drug);
                  setQuery("");
                  setResults([]);
                  setIsOpen(false);
                }}
              >
                <span>{drug.name}</span>
                <span className="font-data text-xs text-slate">{drug.rxcui}</span>
              </button>
            ))}
        </div>
      )}
    </div>
  );
}
