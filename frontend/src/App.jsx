import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { SettingsProvider } from "./context/SettingsContext.jsx";
import { WizardProvider } from "./context/WizardContext.jsx";
import { ChatProvider } from "./context/ChatContext.jsx";
import { KnowledgeBaseProvider } from "./context/KnowledgeBaseContext.jsx";
import AppLayout from "./layout/AppLayout.jsx";
import LandingPage from "./pages/LandingPage.jsx";
import WizardPage from "./pages/WizardPage.jsx";
import BuddyPage from "./pages/BuddyPage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";

export default function App() {
  return (
    <SettingsProvider>
      <WizardProvider>
        <ChatProvider>
          <KnowledgeBaseProvider>
            <BrowserRouter>
              <Routes>
                <Route element={<AppLayout />}>
                  <Route path="/" element={<LandingPage />} />
                  <Route path="/anforderungen" element={<WizardPage />} />
                  <Route path="/buddy" element={<BuddyPage />} />
                  <Route path="/einstellungen" element={<SettingsPage />} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Route>
              </Routes>
            </BrowserRouter>
          </KnowledgeBaseProvider>
        </ChatProvider>
      </WizardProvider>
    </SettingsProvider>
  );
}
