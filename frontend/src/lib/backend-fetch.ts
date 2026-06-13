const BACKEND_API_URL =
  process.env.BACKEND_API_URL ??
  "https://ub4r9j3fl2.execute-api.eu-west-1.amazonaws.com";
const BACKEND_API_KEY = process.env.BACKEND_API_KEY ?? "tatuazyk";

type BackendFetchInit = {
  method?: string;
  body?: string;
  redirect?: RequestRedirect;
  searchParams?: URLSearchParams;
};

/**
 * Server-side fetch helper for the backend API.
 * Automatically injects the backend API key.
 * Must only be called from Route Handlers or Server Components.
 */
export async function backendFetch(
  path: string,
  init: BackendFetchInit = {},
): Promise<Response> {
  const headers: Record<string, string> = {
    "X-Api-Key": BACKEND_API_KEY,
  };
  if (init.body !== undefined) headers["Content-Type"] = "application/json";

  const url =
    init.searchParams && init.searchParams.size > 0
      ? `${BACKEND_API_URL}${path}?${init.searchParams.toString()}`
      : `${BACKEND_API_URL}${path}`;

  return fetch(url, {
    method: init.method ?? "GET",
    body: init.body,
    headers,
    redirect: init.redirect ?? "follow",
  });
}
