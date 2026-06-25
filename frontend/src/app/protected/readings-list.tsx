"use client";

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { listReadings } from "@/lib/api";
import { ReadingRow } from "./reading-row";

export function ReadingsList() {
  const [cursor, setCursor] = useState<string | null>(null);
  const [cursorHistory, setCursorHistory] = useState<(string | null)[]>([null]);
  const [pageIndex, setPageIndex] = useState(0);

  const { data, isLoading, isFetching, error, refetch } = useQuery({
    queryKey: ["readings", cursor],
    queryFn: () => listReadings(20, cursor),
  });

  const handleNext = () => {
    if (data?.next_cursor) {
      setCursorHistory((h) => [...h, data.next_cursor]);
      setPageIndex((i) => i + 1);
      setCursor(data.next_cursor);
    }
  };

  const handlePrev = () => {
    if (pageIndex > 0) {
      const newIndex = pageIndex - 1;
      setPageIndex(newIndex);
      setCursor(cursorHistory[newIndex]);
    }
  };

  return (
    <section className="border rounded-lg p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between gap-2">
        <h2 className="font-semibold text-lg">
          Readings{" "}
          <span className="text-sm font-normal text-zinc-400">
            GET /api/v1/readings
          </span>
        </h2>
        <button
          type="button"
          onClick={() => refetch()}
          disabled={isFetching}
          className="rounded-md border px-3 py-1.5 text-sm hover:bg-zinc-100 disabled:opacity-50"
        >
          {isFetching ? "Refreshing…" : "Refresh"}
        </button>
      </div>
      {isLoading && <p className="text-sm text-zinc-500">Loading…</p>}
      {error && <p className="text-sm text-red-600">{String(error)}</p>}
      {!isLoading && data?.items.length === 0 && (
        <p className="text-sm text-zinc-500">No readings yet.</p>
      )}
      <div className="flex flex-col gap-3">
        {data?.items.map((reading) => (
          <ReadingRow key={reading.id} reading={reading} />
        ))}
      </div>
      <div className="flex items-center gap-2 pt-1">
        <button
          type="button"
          onClick={handlePrev}
          disabled={pageIndex === 0}
          className="rounded-md border px-3 py-1.5 text-sm hover:bg-zinc-100 disabled:opacity-40"
        >
          Previous
        </button>
        <span className="text-sm text-zinc-500">Page {pageIndex + 1}</span>
        <button
          type="button"
          onClick={handleNext}
          disabled={!data?.next_cursor}
          className="rounded-md border px-3 py-1.5 text-sm hover:bg-zinc-100 disabled:opacity-40"
        >
          Next
        </button>
      </div>
    </section>
  );
}
