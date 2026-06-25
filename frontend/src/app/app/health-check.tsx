"use client";

import { useState } from "react";
import { getHealth } from "@/lib/api";

export const HealthCheck = () => {
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      const data = await getHealth();
      setResult(JSON.stringify(data));
    } catch (e) {
      setResult(`Error: ${e}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="border rounded-lg p-4 flex flex-col gap-3">
      <h2 className="font-semibold text-lg">Health Check</h2>
      <div className="flex items-center gap-3 flex-wrap">
        <button
          type="button"
          onClick={handleClick}
          disabled={loading}
          className="rounded-md border border-black px-4 py-2 text-sm hover:bg-zinc-100 disabled:opacity-50"
        >
          {loading ? "Checking…" : "GET /api/v1/health"}
        </button>
        {result && (
          <span className="font-mono text-xs text-zinc-600">{result}</span>
        )}
      </div>
    </section>
  );
};
