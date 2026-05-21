# przeczytai.me

**Live:** [przeczytai-me.vercel.app](https://przeczytai-me.vercel.app)

Text-to-speech web app for the Polish language. Paste or type any Polish text and have it read aloud.

## Tech stack

- **Next.js 16** — App Router, TypeScript
- **Tailwind CSS** + **shadcn/ui** — styling and components
- **Clerk** — authentication
- **TanStack Query** — data fetching
- **Biome** — linting and formatting
- **Vercel** — deployment

## Project structure

```
/
├── frontend/       # Next.js app
│   ├── src/
│   │   ├── app/        # Routes and layouts
│   │   ├── components/ # Shared components
│   │   └── lib/        # Utilities and config
│   └── public/
└── docs/           # Architecture and decision notes
```

## Running locally

**Prerequisites:** Node.js 18+, pnpm

```bash
# 1. Clone the repo
git clone https://github.com/szmydlo98/przeczytai.me.git
cd przeczytai.me/frontend

# 2. Install dependencies
pnpm install

# 3. Set up environment variables
cp .env.local.example .env.local
# Fill in your Clerk keys in .env.local

# 4. Start the dev server
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000).

### Environment variables

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Clerk publishable key (`pk_test_...`) |
| `CLERK_SECRET_KEY` | Clerk secret key (`sk_test_...`) |
| `NEXT_PUBLIC_CLERK_SIGN_IN_URL` | Sign-in route (default: `/sign-in`) |
| `NEXT_PUBLIC_CLERK_SIGN_UP_URL` | Sign-up route (default: `/sign-up`) |

Get your Clerk keys at [dashboard.clerk.com](https://dashboard.clerk.com).

## Useful commands

```bash
pnpm dev        # Start dev server
pnpm build      # Production build
pnpm lint       # Run Biome linter
pnpm lint:fix   # Fix lint issues automatically
pnpm format     # Format all files
```

## Deployment

The app is deployed on [Vercel](https://vercel.com). Every push to `main` triggers a production deployment. PRs get a preview deployment automatically.

Vercel is configured to use `frontend/` as the root directory (set in project Settings → General → Root Directory).
