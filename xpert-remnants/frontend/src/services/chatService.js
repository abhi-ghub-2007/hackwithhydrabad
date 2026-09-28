import { api } from './api';

const CHATS_STORAGE_KEY = 'xpert_chat_history_v1';
const ACTIVE_CHAT_KEY = 'xpert_active_chat_id_v1';

export const SEED_CHATS = [
  {
    id: 'chat-kafka',
    title: 'Why did Raj choose Kafka?',
    date: 'Yesterday',
    expertId: 1,
    messages: [
      {
        id: 'msg-u1',
        sender: 'user',
        text: 'Why did Raj choose Kafka?',
        timestamp: '10:14 AM'
      },
      {
        id: 'msg-a1',
        sender: 'assistant',
        text: `Raj selected Kafka after evaluating multiple approaches for the payment processing bottleneck.

The historical records show that:

• Increasing the API timeout did not solve the queueing problem.
• Redis Streams caused reliability issues during peak traffic due to in-memory persistence constraints.
• Kafka was selected because the system required durable, high-throughput event processing and replayability for financial audit requirements.

The final decision was documented in Raj's payment-platform architecture records (DEC-219 / INC-1842).`,
        timestamp: '10:14 AM',
        evidenceCount: 3,
        sources: [
          { id: 'DEC-49281', title: 'Payment Platform Event Streaming Architecture', type: 'Decision' },
          { id: 'INC-72819', title: 'Payment Queue Bottleneck & Redis Saturation', type: 'Incident' },
          { id: 'MEM-92183', title: 'Queueing Bottleneck & Event Replay Lesson', type: 'Lesson' }
        ],
        decisionMemoryId: 1
      }
    ]
  },
  {
    id: 'chat-latency',
    title: 'Payment latency issue',
    date: '2 days ago',
    expertId: 1,
    messages: [
      {
        id: 'msg-u2',
        sender: 'user',
        text: 'Payment API latency increased after a traffic spike. What should I investigate?',
        timestamp: '3:20 PM'
      },
      {
        id: 'msg-a2',
        sender: 'assistant',
        text: `Historical organizational records show a closely matching situation previously addressed by the backend platform team.

During high-throughput events, Payment API p99 latency spiked due to database connection pool saturation.

Key historical findings:
• Inspect database connection pool acquisition metrics and master CPU.
• If CPU is low (<30%) but application threads are waiting for connections, expanding the pool allocation from 50 to 100 resolved the latency spike by 68%.
• However, if the database max_connections limit is near capacity, connection thrashing will occur and PgBouncer connection pooling must be used instead.`,
        timestamp: '3:20 PM',
        evidenceCount: 2,
        sources: [
          { id: 'INC-1842', title: 'Payment Gateway Connection Saturation', type: 'Incident' },
          { id: 'DEC-MEM-1', title: 'Database Pool Expansion & Timeout Tuning', type: 'Decision' }
        ],
        decisionMemoryId: 1
      }
    ]
  },
  {
    id: 'chat-redis',
    title: 'Redis Streams decision',
    date: 'Last week',
    expertId: 1,
    messages: [
      {
        id: 'msg-u3',
        sender: 'user',
        text: 'Why was Redis Streams rejected for transaction queues?',
        timestamp: '11:05 AM'
      },
      {
        id: 'msg-a3',
        sender: 'assistant',
        text: `Redis Streams was evaluated as a lightweight alternative for payment queueing, but was rejected by Raj Mehta and the infrastructure committee.

Reasons for rejection:
• Cluster node failover during high memory pressure resulted in unacknowledged message loss.
• Financial transactions required strict at-least-once persistence with partition replication, which Redis could not guarantee under memory capping.
• Kafka was chosen instead for strict auditability and disaster recovery replays.`,
        timestamp: '11:05 AM',
        evidenceCount: 2,
        sources: [
          { id: 'DEC-312', title: 'Message Broker Evaluation & Redis Rejection', type: 'Decision' },
          { id: 'MEM-404', title: 'Financial Audit Compliance Architecture', type: 'Lesson' }
        ],
        decisionMemoryId: 1
      }
    ]
  },
  {
    id: 'chat-db-migration',
    title: 'Database migration',
    date: '2 weeks ago',
    expertId: 2,
    messages: [
      {
        id: 'msg-u4',
        sender: 'user',
        text: 'What was the zero-downtime database migration strategy?',
        timestamp: '4:15 PM'
      },
      {
        id: 'msg-a4',
        sender: 'assistant',
        text: `Priya Sharma established the dual-write schema migration policy for critical customer databases.

The protocol requires:
1. Deploy schema with backward-compatible additive columns.
2. Enable dual-writing in application code with shadow verification.
3. Backfill historical records asynchronously with rate-limiting.
4. Cut over read queries after data parity is 100% verified.
5. Decommission deprecated columns in a subsequent release cycle.`,
        timestamp: '4:15 PM',
        evidenceCount: 2,
        sources: [
          { id: 'DEC-809', title: 'Dual-Write Database Migration Standard', type: 'Decision' },
          { id: 'DOC-112', title: 'Zero Downtime Schema Evolution Guide', type: 'Document' }
        ]
      }
    ]
  }
];

export const chatService = {
  getStoredChats() {
    try {
      const raw = localStorage.getItem(CHATS_STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed;
        }
      }
    } catch (e) {
      console.warn('Failed to parse stored chats, loading seeds:', e);
    }
    // Initialize with seeds
    localStorage.setItem(CHATS_STORAGE_KEY, JSON.stringify(SEED_CHATS));
    return SEED_CHATS;
  },

  saveChats(chats) {
    try {
      localStorage.setItem(CHATS_STORAGE_KEY, JSON.stringify(chats));
    } catch (e) {
      console.warn('Failed to save chats to localStorage:', e);
    }
  },

  getActiveChatId() {
    return localStorage.getItem(ACTIVE_CHAT_KEY) || null;
  },

  setActiveChatId(chatId) {
    if (chatId) {
      localStorage.setItem(ACTIVE_CHAT_KEY, chatId);
    } else {
      localStorage.removeItem(ACTIVE_CHAT_KEY);
    }
  },

  async askQuestion(query, { expertId = null, projectId = null, contextHint = null } = {}) {
    try {
      const response = await api.ask(query, { expertId, projectId, contextHint });

      // Transform backend response into clean chat structure
      const sources = (response.sources || []).map((src, index) => {
        let title = 'Historical Record';
        let type = 'Record';
        if (src === 'PUBLIC-KNOWLEDGE') {
          type = 'Public Knowledge';
          title = 'General Technical Industry Knowledge';
        } else if (src === 'SYS-CONFIG') {
          type = 'System';
          title = 'System Configuration & Capabilities';
        } else if (src.includes('ACT')) {
          type = 'Active Decision';
          title = 'Current Active Project Decision';
        } else if (src.startsWith('DEC')) {
          type = 'Decision';
          title = response.previous_decision ? response.previous_decision.substring(0, 50) + '...' : 'Architectural Decision';
        } else if (src.startsWith('INC')) {
          type = 'Incident';
          title = response.what_happened ? response.what_happened.substring(0, 50) + '...' : 'Historical Incident Report';
        } else if (src.startsWith('MEM')) {
          type = 'Lesson';
          title = 'Preserved Expert Experience';
        }
        return {
          id: src,
          title,
          type
        };
      });

      return {
        success: true,
        answer: response.answer,
        matchScore: response.historical_match_score || 'Medium',
        sources,
        evidenceCount: sources.length || 1,
        decisionMemoryId: response.decision_memory_id,
        raw: response
      };
    } catch (err) {
      console.error('chatService.askQuestion error:', err);
      return {
        success: false,
        error: 'Something went wrong. Please try again.',
        details: err.message
      };
    }
  },

  async submitFeedback(query, feedbackType, actualResult = null, decisionMemoryId = null) {
    try {
      return await api.submitFeedback(query, feedbackType, actualResult, decisionMemoryId);
    } catch (err) {
      console.error('chatService.submitFeedback error:', err);
      throw err;
    }
  }
};
