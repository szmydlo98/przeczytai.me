import Link from "next/link";
import { auth } from "@clerk/nextjs/server";
import { SignOutButton } from "@/components/sign-out-button";

export default async function Home() {
	const { userId } = await auth();

	return (
		<main className="flex flex-1 flex-col items-center justify-center gap-6">
			<h1 className="text-3xl font-semibold">PrzeczytAI</h1>

			{userId ? (
				<div className="flex gap-4">
					<Link
						href="/protected"
						className="rounded-md bg-black px-5 py-2.5 text-sm text-white hover:bg-zinc-700"
					>
						Go to protected page
					</Link>
					<SignOutButton className="rounded-md border border-black px-5 py-2.5 text-sm hover:bg-zinc-100" />
				</div>
			) : (
				<div className="flex gap-4">
					<Link
						href="/sign-in"
						className="rounded-md bg-black px-5 py-2.5 text-sm text-white hover:bg-zinc-700"
					>
						Sign in
					</Link>
					<Link
						href="/sign-up"
						className="rounded-md border border-black px-5 py-2.5 text-sm hover:bg-zinc-100"
					>
						Sign up
					</Link>
				</div>
			)}
		</main>
	);
}
