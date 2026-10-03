import { Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/common/Header.jsx';
import Landing from './pages/Landing.jsx';
import FamilyContextSetup from './pages/FamilyContextSetup.jsx';
import CounsellingChat from './pages/CounsellingChat.jsx';
import CounsellorDashboard from './pages/CounsellorDashboard.jsx';
import AdminDashboard from './pages/AdminDashboard.jsx';

export default function App() {
  return (
    <>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/setup" element={<FamilyContextSetup />} />
          <Route path="/chat/:sessionId" element={<CounsellingChat />} />
          <Route path="/counsellor" element={<CounsellorDashboard />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </>
  );
}
