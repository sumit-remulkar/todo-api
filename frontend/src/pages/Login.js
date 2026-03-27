import React, { useState } from "react";
const API = "http://127.0.0.1:8000"

function Login({ setToken }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
  try {
    const res = await fetch(`${API}/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ username, password }),
    });

    if (!res.ok) {
      alert("Invalid username or password ❌");
      return;
    }

    const data = await res.json();

    if (!data.access_token) {
      alert("Login failed ❌");
      return;
    }

    localStorage.setItem("token", data.access_token);
    setToken(data.access_token);

  } catch (err) {
    alert("Server unreachable. Try again! ❌");
    console.error(err);
  }
};

  return (
    <div className="flex h-screen items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded shadow w-80">
        <h2 className="text-xl mb-4 font-bold">Login</h2>

        <input
          placeholder="Username"
          className="border p-2 w-full mb-3"
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          placeholder="Password"
          type="password"
          className="border p-2 w-full mb-3"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleLogin}
          className="bg-blue-600 hover:bg-blue-700 text-white w-full py-2 rounded transition"
        >
          Login 🚀
        </button>
      </div>
    </div>
  );
}

export default Login;