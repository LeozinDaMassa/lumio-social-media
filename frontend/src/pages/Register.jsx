import { useState } from "react";
import { register } from "../lib/auth";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await register(email, password, username);
      alert("Account created! Check your email to confirm.");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-night flex items-center justify-center px-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm flex flex-col gap-4"
      >
        <h1 className="text-3xl text-text-primary tracking-widest text-center mb-6">
          LUMIO
        </h1>

        {error && <p className="text-red-400 text-sm text-center">{error}</p>}

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="bg-surface text-text-primary border border-border rounded-lg px-4 py-3 outline-none focus:border-lavender transition-colors"
          required
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="bg-surface text-text-primary border border-border rounded-lg px-4 py-3 outline-none focus:border-lavender transition-colors"
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="bg-surface text-text-primary border border-border rounded-lg px-4 py-3 outline-none focus:border-lavender transition-colors"
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="bg-lavender text-night font-medium rounded-lg px-4 py-3 mt-2 hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          {loading ? "Creating account..." : "Create account"}
        </button>
      </form>
    </div>
  );
}

export default Register;
