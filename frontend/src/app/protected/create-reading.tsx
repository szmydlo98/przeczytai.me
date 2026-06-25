"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { createReading } from "@/lib/api";

export function CreateReading() {
  const queryClient = useQueryClient();

  const [text, setText] = useState("");
  const [vendor, setVendor] = useState("");
  const [voice, setVoice] = useState("");

  const mutation = useMutation({
    mutationFn: () =>
      createReading({
        original_text: text,
        vendor: vendor || null,
        voice: voice || null,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["readings"] });
      setText("");
      setVendor("");
      setVoice("");
    },
  });

  return (
    <section className="border rounded-lg p-4 flex flex-col gap-3">
      <h2 className="font-semibold text-lg">Create Reading</h2>
      <textarea
        className="border rounded-md p-2 text-sm font-mono resize-y min-h-[100px]"
        placeholder="original_text (required)"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <div className="flex gap-2">
        <input
          className="border rounded-md px-3 py-1.5 text-sm flex-1"
          placeholder="vendor (optional)"
          value={vendor}
          onChange={(e) => setVendor(e.target.value)}
        />
        <input
          className="border rounded-md px-3 py-1.5 text-sm flex-1"
          placeholder="voice (optional)"
          value={voice}
          onChange={(e) => setVoice(e.target.value)}
        />
      </div>
      <div className="flex items-center gap-3 flex-wrap">
        <button
          type="button"
          onClick={() => mutation.mutate()}
          disabled={mutation.isPending || !text.trim()}
          className="rounded-md bg-black text-white px-4 py-2 text-sm hover:bg-zinc-800 disabled:opacity-50"
        >
          {mutation.isPending ? "Creating…" : "POST /api/v1/readings"}
        </button>
        {mutation.isSuccess && (
          <span className="text-xs text-green-700">
            Created: {mutation.data?.id}
          </span>
        )}
        {mutation.isError && (
          <span className="text-xs text-red-600">{String(mutation.error)}</span>
        )}
      </div>
    </section>
  );
}
