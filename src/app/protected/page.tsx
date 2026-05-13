import { auth, currentUser } from "@clerk/nextjs/server";
import { UserButton } from "@clerk/nextjs";
import Link from "next/link";

export default async function ProtectedPage() {
	const { userId } = await auth();
	const user = await currentUser();

	return (
		<main className="flex flex-1 flex-col items-center justify-center gap-6">
			<div className="flex flex-col items-center gap-2 text-center">
				<p className="text-sm text-zinc-500">Logged in as</p>
				<p className="font-semibold">{user?.emailAddresses[0].emailAddress}</p>
				<p className="font-mono text-xs text-zinc-400">userId: {userId}</p>
			</div>

			<div className="rounded-md border border-green-200 bg-green-50 px-6 py-4 text-sm text-green-800">
				Auth is working — you can see this page because you are signed in.
			</div>

			<div className="flex items-center gap-4">
				<UserButton />
				<Link href="/" className="text-sm text-zinc-500 underline hover:text-black">
					Back to home
				</Link>
			</div>
		</main>
	);
}
