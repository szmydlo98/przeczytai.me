"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import type { Reading } from "@/lib/api";
import { deleteReading, downloadFile } from "@/lib/api";

export function ReadingRow({ reading }: { reading: Reading }) {
  const queryClient = useQueryClient();

  const deleteMutation = useMutation({
    mutationFn: () => deleteReading(reading.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["readings"] });
    },
  });

  const handleDownload = async (path: string, filename: string) => {
    try {
      await downloadFile(path, filename);
    } catch (e) {
      alert(`Download failed: ${e}`);
    }
  };

  return (
    <div className="border rounded-md p-3 flex flex-col gap-2 text-sm">
      <div className="flex items-center justify-between gap-2 flex-wrap">
        <span className="font-mono text-xs text-zinc-500 truncate">
          {reading.id}
        </span>
        <span
          className={`text-xs px-2 py-0.5 rounded-full font-medium ${
            reading.status === "completed"
              ? "bg-green-100 text-green-800"
              : reading.status === "failed"
                ? "bg-red-100 text-red-800"
                : "bg-yellow-100 text-yellow-800"
          }`}
        >
          {reading.status}
        </span>
      </div>
      <div className="text-xs text-zinc-600 grid grid-cols-2 gap-1">
        <span>chars: {reading.char_count}</span>
        <span>vendor: {reading.vendor ?? "—"}</span>
        <span>voice: {reading.voice ?? "—"}</span>
        <span>created: {new Date(reading.created_at).toLocaleString()}</span>
      </div>
      <div className="flex items-center gap-2 flex-wrap pt-1">
        <button
          type="button"
          onClick={() =>
            handleDownload(
              `/api/v1/readings/${reading.id}/recording`,
              `${reading.id}-recording`,
            )
          }
          disabled={!reading.recording_key}
          className="rounded border px-3 py-1 text-xs hover:bg-zinc-100 disabled:opacity-40"
        >
          Download Recording
        </button>
        <button
          type="button"
          onClick={() =>
            handleDownload(
              `/api/v1/readings/${reading.id}/corrected-text`,
              `${reading.id}-corrected.md`,
            )
          }
          disabled={!reading.corrected_text_key}
          className="rounded border px-3 py-1 text-xs hover:bg-zinc-100 disabled:opacity-40"
        >
          Download Corrected Text
        </button>
        <button
          type="button"
          onClick={() => deleteMutation.mutate()}
          disabled={deleteMutation.isPending}
          className="rounded border border-red-300 px-3 py-1 text-xs text-red-700 hover:bg-red-50 disabled:opacity-50 ml-auto"
        >
          {deleteMutation.isPending ? "Deleting…" : "DELETE"}
        </button>
      </div>
    </div>
  );
}
