import { useLocation } from "react-router-dom";
export default function PairingDashboard() {
  const location = useLocation();
  const passPairing = location.state.passPairing;

  console.log("Received pairing object:", passPairing);
  return <div>PairingDashboard</div>;
}
