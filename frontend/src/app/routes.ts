import { createBrowserRouter } from "react-router";
import { DashboardLayout } from "./components/DashboardLayout";
import { DashboardPage } from "./pages/DashboardPage";
import { ValidateIdeaPage } from "./pages/ValidateIdeaPage";
import { ResultsPage } from "./pages/ResultsPage";
import { ReportsPage } from "./pages/ReportsPage";
import { DatasetPage } from "./pages/DatasetPage";
import { SettingsPage } from "./pages/SettingsPage";
import { AboutPage } from "./pages/AboutPage";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: DashboardLayout,
    children: [
      { index: true, Component: DashboardPage },
      { path: "validate", Component: ValidateIdeaPage },
      { path: "results", Component: ResultsPage },
      { path: "reports", Component: ReportsPage },
      { path: "dataset", Component: DatasetPage },
      { path: "settings", Component: SettingsPage },
      { path: "about", Component: AboutPage },
    ],
  },
]);