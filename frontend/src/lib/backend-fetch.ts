import { auth } from "@clerk/nextjs/server";

const BACKEND = "https://ub4r9j3fl2.execute-api.eu-west-1.amazonaws.com";

type BackendFetchInit = {
  method?: string;
  body?: string;
  redirect?: RequestRedirect;
  searchParams?: URLSearchParams;
};

/**
 * Server-side fetch helper for the backend API.
 * Automatically injects the Clerk JWT as a Bearer token.
 * Must only be called from Route Handlers or Server Components.
 */
export async function backendFetch(
  path: string,
  init: BackendFetchInit = {},
): Promise<Response> {
  const { getToken } = await auth();
  const token = await getToken();

  const headers: Record<string, string> = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  if (init.body !== undefined) headers["Content-Type"] = "application/json";

  const url =
    init.searchParams && init.searchParams.size > 0
      ? `${BACKEND}${path}?${init.searchParams.toString()}`
      : `${BACKEND}${path}`;

  return fetch(url, {
    method: init.method ?? "GET",
    body: init.body,
    headers,
    redirect: init.redirect ?? "follow",
  });
}
