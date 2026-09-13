import type { EvidenceItem } from "@/api/client";

export default function EvidenceCitationCard({ evidence }: { evidence: EvidenceItem }) {
  return (
    <div className="rounded-md border border-line bg-paper p-3 text-sm">
      <div className="flex items-center justify-between">
        <span className="font-data text-xs text-slate">{evidence.source}</span>
        {evidence.url && (
          <a href={evidence.url} target="_blank" rel="noreferrer" className="text-teal-dark hover:underline text-xs">
            Source
          </a>
        )}
      </div>
      <p className="mt-1 text-ink">{evidence.citation}</p>
      {evidence.excerpt && <p className="mt-1 text-slate italic">"{evidence.excerpt}"</p>}
    </div>
  );
}
