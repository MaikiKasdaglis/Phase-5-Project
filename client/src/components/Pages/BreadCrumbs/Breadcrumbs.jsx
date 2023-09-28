import { Link, useLocation } from "react-router-dom";
export default function Breadcrumbs() {
  const location = useLocation();
  console.log("from breadcrumbs", location);

  let currentLink = "";
  const crumbs = location.pathname
    .split("/")
    .filter((crumb) => crumb !== "")
    .map((crumb) => {
      currentLink += `/${crumb}`;

      return (
        <div key={crumb}>
          <Link to={currentLink}>{crumb}</Link>
        </div>
      );
    });
  return <div>{crumbs}</div>;
}
