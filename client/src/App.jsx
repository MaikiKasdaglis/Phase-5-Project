import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  createBrowserRouter,
  Route,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";
// import { useEffect } from "react";

//=========Layouts====================================
import RootLayout from "./components/Layouts/RootLayout";
//=========Pages======================================
import Login from "./components/Pages/Login";
import Dashboard from "./components/Pages/Dashboard";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />}>
      <Route path="login" element={<Login />} />
      <Route path="dashboard" element={<Dashboard />} />
      <Route />
    </Route>
  )
);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
