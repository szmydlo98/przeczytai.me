import { SignIn } from "@clerk/nextjs";

const SignInPage = () => {
  return (
    <main className="flex flex-1 items-center justify-center">
      <SignIn />
    </main>
  );
};

export default SignInPage;
