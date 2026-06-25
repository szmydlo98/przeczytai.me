"use client";

import { CreateReading } from "./create-reading";
import { HealthCheck } from "./health-check";
import { ReadingsList } from "./readings-list";

export const ReadingsDashboard = () => {
  return (
    <div className="w-full max-w-3xl mx-auto flex flex-col gap-8 pb-12">
      <HealthCheck />
      <CreateReading />
      <ReadingsList />
    </div>
  );
};
