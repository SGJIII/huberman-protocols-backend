import { useUser } from '@auth0/nextjs-auth0';
import Link from 'next/link';

export default function Login() {
  const { user, error, isLoading } = useUser();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;

  if (user) {
    return (
      <div>
        <h1>Welcome {user.name}</h1>
        <Link href="/api/auth/logout">Logout</Link>
      </div>
    );
  }

  return (
    <div>
      <h1>Please log in</h1>
      <Link href="/api/auth/login">Login</Link>
    </div>
  );
}
