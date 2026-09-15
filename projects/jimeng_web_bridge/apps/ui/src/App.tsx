import { NavLink, Route, Routes } from "react-router-dom";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { PAGES } from "./pages";

export default function App() {
  return (
    <div className="app">
      <nav className="app-nav" aria-label="主导航">
        <div className="app-brand">即梦桥接</div>
        <ul>
          {PAGES.map((page) => (
            <li key={page.path}>
              <NavLink to={page.path} end={page.path === "/"}>
                {page.title}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
      <div className="app-main">
        <div id="queue-banner-slot" />
        <main>
          <Routes>
            {PAGES.map((page) => (
              <Route
                key={page.path}
                path={page.path}
                element={
                  <ErrorBoundary pageTitle={page.title}>
                    <page.Component />
                  </ErrorBoundary>
                }
              />
            ))}
          </Routes>
        </main>
      </div>
    </div>
  );
}
