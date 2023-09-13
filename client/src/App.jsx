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
import Dashboard from "./components/Pages/Dashboard";
import Login from "./components/Pages/Login";
import Logout from "./components/Pages/Logout";
import Signup from "./components/Pages/Signup";
import PairingDashboard from "./components/Pages/PairingDashboard";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />}>
      <Route path="login" element={<Login />} />
      <Route path="logout" element={<Logout />} />
      <Route path="login/signup" element={<Signup />} />
      <Route path="dashboard" element={<Dashboard />} />
      <Route
        path="dashboard/pairing_dashboard"
        element={<PairingDashboard />}
      />
    </Route>
  )
);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
