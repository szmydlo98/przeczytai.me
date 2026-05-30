import { type NextRequest, NextResponse } from "next/server";
import { backendFetch } from "@/lib/backend-fetch";

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ readingId: string }> },
) {
  const { readingId } = await params;
  const res = await backendFetch(`/api/v1/readings/${readingId}/recording`, {
    redirect: "manual",
  });

  // Backend redirects (307) to a presigned S3 URL.
  // Resolve it here so the browser never makes a cross-origin request.
  if (res.status >= 300 && res.status < 400) {
    const location = res.headers.get("location");
    if (location) return NextResponse.json({ url: location });
  }

  if (!res.ok) {
    const text = await res.text();
    return NextResponse.json({ error: text }, { status: res.status });
  }

  const data = await res.json();
  return NextResponse.json(data);
}
