import React, { useState, useEffect } from 'react';
import {
  Settings,
  Database,
  Cpu,
  Brain,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Sparkles,
  Layers,
  Activity
} from 'lucide-react';
import { AppShell } from '../components/layout/AppShell';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { api } from '../services/api';
import './AdminDashboard.css';

export function AdminDashboard() {
  const [statusData, setStatusData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [seedingProfile, setSeedingProfile] = useState('DEV');
  const [isSeeding, setIsSeeding] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [notice, setNotice] = useState('');

  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    setLoading(true);
    try {
      const data = await api.getAdminStatus();
      setStatusData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSeed = async () => {
    setIsSeeding(true);
    setNotice('');
    try {
      const res = await api.triggerSeed(seedingProfile);
      setNotice(`Database successfully re-seeded with ${seedingProfile} profile! Total memories: ${res.seeded_counts.memories}`);
      await fetchStatus();
    } catch (err) {
      setNotice(`Seeding failed: ${err.message}`);
    } finally {
      setIsSeeding(false);
    }
  };

  const handleSyncHindsight = async () => {
    setIsSyncing(true);
    setNotice('');
    try {
      const res = await api.syncHindsight();
      setNotice(`Synchronized ${res.retained_count} active memories into Hindsight memory bank '${res.bank_id}'!`);
    } catch (err) {
      setNotice(`Hindsight sync failed: ${err.message}`);
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <AppShell>
      <div className="admin-page-container">
        <div className="page-header">
          <div>
            <h1 className="page-title">
              <Settings className="page-icon" size={24} />
              Administration & System Health Diagnostics
            </h1>
            <p className="page-subtitle">
              Inspect database persistence, official Hindsight SDK connections, LLM provider routing, and synthetic scale generation (Section 38 & 59).
            </p>
          </div>
          <div className="header-actions">
            <Button variant="ghost" size="sm" onClick={fetchStatus} icon={RefreshCw}>
              Refresh Diagnostics
            </Button>
          </div>
        </div>

        {notice && (
          <div className="admin-notice">
            <CheckCircle2 size={16} /> {notice}
          </div>
        )}

        {loading || !statusData ? (
          <div className="loading-state">Checking system components...</div>
        ) : (
          <>
            {/* Core Infrastructure Diagnostics */}
            <div className="diagnostics-grid">
              {/* Structured Database */}
              <div className="diagnostic-card">
                <div className="diagnostic-header">
                  <div className="diag-icon-wrapper">
                    <Database size={20} className="diag-icon" />
                  </div>
                  <div>
                    <h3 className="diag-name">Structured Database</h3>
                    <span className="diag-sub">PostgreSQL / SQLAlchemy</span>
                  </div>
                  <Badge variant={statusData.database.connected ? 'success' : 'warning'}>
                    {statusData.database.connected ? 'Connected' : 'Offline'}
                  </Badge>
                </div>
                <div className="diag-body">
                  <div className="diag-row">
                    <span>Engine Type:</span>
                    <strong>{statusData.database.type}</strong>
                  </div>
                  <div className="diag-row">
                    <span>Connection:</span>
                    <span className="masked-url">{statusData.database.url_masked}</span>
                  </div>
                </div>
              </div>

              {/* Hindsight Memory Engine */}
              <div className="diagnostic-card">
                <div className="diagnostic-header">
                  <div className="diag-icon-wrapper hindsight-wrapper">
                    <Brain size={20} className="diag-icon" />
                  </div>
                  <div>
                    <h3 className="diag-name">Hindsight Memory Engine</h3>
                    <span className="diag-sub">Official Hindsight Python SDK</span>
                  </div>
                  <Badge variant={statusData.hindsight.connected ? 'success' : 'warning'}>
                    {statusData.hindsight.mode}
                  </Badge>
                </div>
                <div className="diag-body">
                  <div className="diag-row">
                    <span>Memory Bank:</span>
                    <strong>{statusData.hindsight.bank_id}</strong>
                  </div>
                  <div className="diag-row">
                    <span>Base URL:</span>
                    <span className="masked-url">{statusData.hindsight.base_url}</span>
                  </div>
                  <div className="diag-row">
                    <span>Credentials:</span>
                    <span>{statusData.hindsight.is_configured ? 'Live API Key Set' : 'Zero-Key Local Engine'}</span>
                  </div>
                </div>
              </div>

              {/* LLM Provider Routing */}
              <div className="diagnostic-card">
                <div className="diagnostic-header">
                  <div className="diag-icon-wrapper llm-wrapper">
                    <Cpu size={20} className="diag-icon" />
                  </div>
                  <div>
                    <h3 className="diag-name">LLM Reasoning Engine</h3>
                    <span className="diag-sub">Provider Abstraction</span>
                  </div>
                  <Badge variant={statusData.llm.is_configured ? 'success' : 'neutral'}>
                    {statusData.llm.mode}
                  </Badge>
                </div>
                <div className="diag-body">
                  <div className="diag-row">
                    <span>Provider:</span>
                    <strong>{statusData.llm.provider}</strong>
                  </div>
                  <div className="diag-row">
                    <span>Configured Model:</span>
                    <strong>{statusData.llm.model}</strong>
                  </div>
                </div>
              </div>
            </div>

            {/* Counts & Enterprise Metrics */}
            <div className="metrics-summary-card">
              <h3>Preserved Enterprise Records</h3>
              <div className="counts-grid">
                <div className="count-item">
                  <span className="count-num">{statusData.counts.memories}</span>
                  <span className="count-label">Total Memories</span>
                </div>
                <div className="count-item">
                  <span className="count-num count-verified">{statusData.counts.verified_memories}</span>
                  <span className="count-label">Verified Active</span>
                </div>
                <div className="count-item">
                  <span className="count-num count-review">{statusData.counts.needs_review}</span>
                  <span className="count-label">Needs Review</span>
                </div>
                <div className="count-item">
                  <span className="count-num">{statusData.counts.decisions}</span>
                  <span className="count-label">Decisions Preserved</span>
                </div>
                <div className="count-item">
                  <span className="count-num">{statusData.counts.incidents}</span>
                  <span className="count-label">Incidents Recorded</span>
                </div>
                <div className="count-item">
                  <span className="count-num">{statusData.counts.knowledge_risks}</span>
                  <span className="count-label">Knowledge Risks</span>
                </div>
                <div className="count-item">
                  <span className="count-num count-feedback">{statusData.counts.feedbacks}</span>
                  <span className="count-label">Outcome Feedback Loops</span>
                </div>
              </div>
            </div>

            {/* Controls: Seeding & Synchronization */}
            <div className="controls-grid">
              <div className="control-card">
                <h3>Synthetic Enterprise Generator (Section 21)</h3>
                <p>
                  Regenerate interconnected enterprise scenarios with predefined profiles without requiring giant full-scale builds during every local dev cycle.
                </p>
                <div className="seeding-form">
                  <select
                    className="profile-select"
                    value={seedingProfile}
                    onChange={(e) => setSeedingProfile(e.target.value)}
                    disabled={isSeeding}
                  >
                    <option value="DEV">DEV Profile (500 memories)</option>
                    <option value="DEMO">DEMO Profile (5,000 memories)</option>
                    <option value="FULL">FULL Profile (100,000 memories)</option>
                    <option value="STRESS">STRESS Profile (500,000+ memories)</option>
                  </select>

                  <Button
                    variant="primary"
                    size="md"
                    onClick={handleSeed}
                    disabled={isSeeding}
                  >
                    {isSeeding ? 'Generating Synthetic Scale...' : `Seed with ${seedingProfile}`}
                  </Button>
                </div>
              </div>

              <div className="control-card">
                <h3>Hindsight Bank Batch Sync (Section 25)</h3>
                <p>
                  Batches all verified PostgreSQL decisions and retains them into Hindsight using <code>MemoryBatchProcessor</code> with progress logging.
                </p>
                <div className="sync-action">
                  <Button
                    variant="ghost"
                    size="md"
                    onClick={handleSyncHindsight}
                    disabled={isSyncing}
                    icon={Brain}
                  >
                    {isSyncing ? 'Batch Retaining into Bank...' : 'Sync Active Memories to Hindsight'}
                  </Button>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </AppShell>
  );
}
