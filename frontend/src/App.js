import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={
          token ? <Dashboard token={token} setToken={setToken} /> 
                : <Login setToken={setToken} />
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;