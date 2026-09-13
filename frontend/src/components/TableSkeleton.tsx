export default function TableSkeleton({ columns, rows }: { columns: number; rows: number }) {
  return (
    <>
      {Array.from({ length: rows }).map((_, r) => (
        <tr key={r} className="border-b border-line last:border-0">
          {Array.from({ length: columns }).map((_, c) => (
            <td key={c} className="px-4 py-3">
              <div className="h-3.5 bg-line/60 rounded animate-pulse" style={{ width: `${60 + ((c * 13) % 30)}%` }} />
            </td>
          ))}
        </tr>
      ))}
    </>
  );
}
