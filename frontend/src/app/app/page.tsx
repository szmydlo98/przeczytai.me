import { UserButton } from "@clerk/nextjs";
import { auth, currentUser } from "@clerk/nextjs/server";
import Link from "next/link";
import { SignOutButton } from "@/components/sign-out-button";
import { ReadingsDashboard } from "./readings-dashboard";

const AppPage = async () => {
  const { userId } = await auth();
  const user = await currentUser();

  return (
    <main className="flex flex-1 flex-col items-center gap-6 px-4">
      <div className="flex flex-col items-center gap-2 pt-8 text-center">
        <p className="text-muted-foreground text-sm">Logged in as</p>
        <p className="font-semibold">{user?.emailAddresses[0].emailAddress}</p>
        <p className="font-mono text-muted-foreground text-xs">
          userId: {userId}
        </p>
      </div>

      <div className="flex items-center gap-4">
        <UserButton />
        <SignOutButton className="rounded-md border border-border px-5 py-2.5 text-sm hover:bg-muted" />
        <Link
          href="/"
          className="text-muted-foreground text-sm underline hover:text-foreground"
        >
          Back to home
        </Link>
      </div>

      <ReadingsDashboard />
    </main>
  );
};

export default AppPage;
