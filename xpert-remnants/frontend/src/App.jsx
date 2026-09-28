import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import { KnowledgeLibrary } from './pages/KnowledgeLibrary';
import { CaptureMemory } from './pages/CaptureMemory';
import { ReviewQueue } from './pages/ReviewQueue';
import { ExpertHandoff } from './pages/ExpertHandoff';
import { ProjectsList } from './pages/ProjectsList';
import { ProjectDetail } from './pages/ProjectDetail';
import { KnowledgeRisks } from './pages/KnowledgeRisks';
import { DecisionReplay } from './pages/DecisionReplay';
import { AdminDashboard } from './pages/AdminDashboard';
import './styles/globals.css';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/knowledge" element={<KnowledgeLibrary />} />
        <Route path="/knowledge/capture" element={<CaptureMemory />} />
        <Route path="/knowledge/review" element={<ReviewQueue />} />
        <Route path="/knowledge/handoff" element={<ExpertHandoff />} />
        <Route path="/projects" element={<ProjectsList />} />
        <Route path="/projects/:id" element={<ProjectDetail />} />
        <Route path="/risks" element={<KnowledgeRisks />} />
        <Route path="/decisions/:id" element={<DecisionReplay />} />
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
