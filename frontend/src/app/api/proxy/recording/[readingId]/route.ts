import { type NextRequest, NextResponse } from "next/server";

const BACKEND = "https://ub4r9j3fl2.execute-api.eu-west-1.amazonaws.com";
const API_KEY = "tatuazyk";

// The backend redirects (307) straight to a presigned S3 URL.
// If the browser follows that redirect it gets a CORS error.
// This route handler resolves it server-side and returns the URL as JSON.
export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ readingId: string }> },
) {
  const { readingId } = await params;

  const res = await fetch(`${BACKEND}/api/v1/readings/${readingId}/recording`, {
    headers: { "X-Api-Key": API_KEY },
    redirect: "manual",
  });

  // 3xx → extract Location header (only readable server-side)
  if (res.status >= 300 && res.status < 400) {
    const location = res.headers.get("location");
    if (location) {
      return NextResponse.json({ url: location });
    }
  }

  if (!res.ok) {
    const text = await res.text();
    return NextResponse.json({ error: text }, { status: res.status });
  }

  const data = await res.json();
  return NextResponse.json(data);
}
