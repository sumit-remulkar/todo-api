import React, { useState, useEffect } from "react";
import toast from "react-hot-toast";

const API ="http://127.0.0.1:8000";
function Dashboard({ token, setToken }) {

  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  // 🔥 FETCH TODOS
  const fetchTodos = async () => {
    try {
      setLoading(true);

      const res = await fetch(`${API}/items/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();
      setTasks(data);

    } catch (error) {
      toast.error("Failed to fetch tasks ❌");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/login";
      return;
    }

    fetchTodos();
  }, []);

  // 🔥 CREATE TASK
const addTask = async () => {
  if (!title) {
    toast.error("Title required ❌");
    return;
  }

  try {
    setLoading(true);

    const res = await fetch(`${API}/items/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        title,
        description: "frontend",
        priority: "high",
      }),
    });

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Error");
    }

    toast.success("Task added ✅");

    setTitle("");
    fetchTodos();

  } catch (err) {
    toast.error(err.message || "Error adding task ❌");
  } finally {
    setLoading(false);
  }
};

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <div className="flex h-screen bg-gray-100">

      {/* SIDEBAR */}
      <div className="w-64 bg-gray-900 text-white p-5">
        <h1 className="text-2xl font-bold mb-6">🚀 Dashboard</h1>
      </div>

      {/* MAIN */}
      <div className="flex-1 p-6">

        {/* NAVBAR */}
        <div className="flex justify-between mb-4">
          <h2 className="text-xl font-semibold">Tasks</h2>
          <button onClick={logout} className="bg-red-500 text-white px-3 py-1 rounded">
            Logout
          </button>
        </div>

        {/* INPUT */}
        <div className="flex gap-2 mb-4">
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="border p-2 w-full"
            placeholder="New Task"
          />
          <button onClick={addTask} className="bg-blue-500 text-white px-4 rounded">
            Add
          </button>
        </div>

        {/* 🔥 LOADING */}
        {loading && (
          <div className="flex justify-center mt-4">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          </div>
        )}

        {/* LIST */}
        <div className="bg-white p-4 rounded shadow">
          {tasks.map((t) => (
            <div key={t.id} className="flex justify-between border-b py-2">
              <span>{t.title}</span>
              <span className="text-gray-500">{t.priority}</span>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}

export default Dashboard;