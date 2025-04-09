import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <>
      <h2>Dashboard</h2>
      <p>Welcome, {user.username}</p>
      <button onClick={logout}>Logout</button>
    </>
  );
}
