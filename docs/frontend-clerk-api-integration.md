# Frontend Clerk API Integration

The backend API is protected by an AWS API Gateway JWT authorizer. The frontend
must call protected endpoints with a Clerk JWT bearer token.

## Protected endpoints

- `POST /api/v1/readings`
- `GET /api/v1/readings`
- `GET /api/v1/readings/{reading_id}`
- `DELETE /api/v1/readings/{reading_id}`
- `GET /api/v1/readings/{reading_id}/recording`
- `GET /api/v1/readings/{reading_id}/corrected-text.md`

Public endpoints:

- `GET /api/v1/health`
- `GET /docs`
- `GET /redoc`
- `GET /openapi.json`

## Clerk setup

Create a Clerk JWT template for backend API calls, for example:

```txt
Template name: przeczytai-api
```

The token must include an audience claim that matches Terraform:

```json
{
  "aud": "przeczytai-api-dev"
}
```

The backend Terraform values must match the Clerk token:

```hcl
clerk_jwt_issuer   = "<the token iss claim>"
clerk_jwt_audience = "przeczytai-api-dev"
```

The easiest way to confirm `clerk_jwt_issuer` is to generate one token from the
template, decode it, and copy the `iss` claim.

## Frontend request

For protected API calls, get a Clerk token from the template and send it as a
bearer token:

```ts
const token = await getToken({ template: "przeczytai-api" });

await fetch(`${apiBaseUrl}/api/v1/readings`, {
  method: "GET",
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
```

For requests with JSON bodies:

```ts
await fetch(`${apiBaseUrl}/api/v1/readings`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ original_text: "Ala ma kota." }),
});
```

Do not send `userId`. Do not send `x-api-key`. The backend uses the verified
JWT `sub` claim as the reading owner.
