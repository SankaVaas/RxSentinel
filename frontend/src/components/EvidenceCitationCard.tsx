import type { EvidenceItem } from "@/api/client";

export default function EvidenceCitationCard({ evidence }: { evidence: EvidenceItem }) {
  return (
    <div className="rounded-md border border-slate-200 bg-slate-50 p-3 text-sm">
      <div className="flex items-center justify-between">
        <span className="font-medium uppercase text-xs text-slate-500">{evidence.source}</span>
        {evidence.url && (
          <a
            href={evidence.url}
            target="_blank"
            rel="noreferrer"
            className="text-blue-600 hover:underline text-xs"
          >
            Source ↗
          </a>
        )}
      </div>
      <p className="mt-1 text-slate-800">{evidence.citation}</p>
      {evidence.excerpt && (
        <p className="mt-1 text-slate-600 italic">"{evidence.excerpt}"</p>
      )}
    </div>
  );
}
