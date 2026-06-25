"use client";

import { useClerk } from "@clerk/nextjs";

export function SignOutButton({ className }: { className?: string }) {
  const { signOut } = useClerk();

  return (
    <button
      type="button"
      className={className}
      onClick={() => signOut({ redirectUrl: "/" })}
    >
      Sign out
    </button>
  );
}
