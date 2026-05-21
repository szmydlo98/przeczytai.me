import { UserButton } from "@clerk/nextjs";
import { auth, currentUser } from "@clerk/nextjs/server";
import Link from "next/link";
import { SignOutButton } from "@/components/sign-out-button";
import { ReadingsDashboard } from "./readings-dashboard";

export default async function ProtectedPage() {
  const { userId } = await auth();
  const user = await currentUser();

  return (
    <main className="flex flex-1 flex-col items-center gap-6 px-4">
      <div className="flex flex-col items-center gap-2 text-center pt-8">
        <p className="text-sm text-zinc-500">Logged in as</p>
        <p className="font-semibold">{user?.emailAddresses[0].emailAddress}</p>
        <p className="font-mono text-xs text-zinc-400">userId: {userId}</p>
      </div>

      <div className="flex items-center gap-4">
        <UserButton />
        <SignOutButton className="rounded-md border border-black px-5 py-2.5 text-sm hover:bg-zinc-100" />
        <Link
          href="/"
          className="text-sm text-zinc-500 underline hover:text-black"
        >
          Back to home
        </Link>
      </div>

      <ReadingsDashboard />
    </main>
  );
}
