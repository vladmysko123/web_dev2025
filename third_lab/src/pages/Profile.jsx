import { useAuth } from "../context/AuthContext";

export default function Profile() {
  const { user } = useAuth();
  return (
    <>
      <h2>Profile</h2>
      <p>User: {user.username}</p>
    </>
  );
}
