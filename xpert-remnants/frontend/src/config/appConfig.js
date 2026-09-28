export const appConfig = {
  appName: import.meta.env.VITE_APP_NAME || 'XPERT REMNANTS',
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  tagline: 'Preserve what experience knows.',
  subtitle: 'Ask about decisions, failures, reasoning, and lessons from the organization\'s expert memory.',
  organization: 'Northstar Technologies India',
  leadExpert: 'Arjun Mehta (Principal Software Architect)',
  navItems: [
    { id: 'chat', label: 'Decision Chat', path: '/', icon: 'MessageSquare' },
    { id: 'knowledge', label: 'Knowledge Library', path: '/knowledge', icon: 'BookOpen' },
    { id: 'capture', label: 'Capture Memory', path: '/knowledge/capture', icon: 'PlusCircle' },
    { id: 'review', label: 'Review Queue', path: '/knowledge/review', icon: 'CheckSquare' },
    { id: 'handoff', label: 'Expert Handoff', path: '/knowledge/handoff', icon: 'UserCheck' },
    { id: 'projects', label: 'Projects', path: '/projects', icon: 'FolderGit2' },
    { id: 'risks', label: 'Knowledge Risks', path: '/risks', icon: 'AlertTriangle' },
    { id: 'replay', label: 'Decision Replay', path: '/decisions/1', icon: 'Clock' },
    { id: 'admin', label: 'Administration', path: '/admin', icon: 'Settings' }
  ],
  capabilities: [
    {
      id: "decisions",
      title: "Past Decisions",
      description: "Explore why critical architectural & business paths were chosen.",
      iconName: "GitBranch"
    },
    {
      id: "tradeoffs",
      title: "Reasoning & Trade-offs",
      description: "Understand discarded alternatives and technical compromises.",
      iconName: "Scale"
    },
    {
      id: "failures",
      title: "Failures & Warnings",
      description: "Review past incidents, pitfalls, and operational gotchas.",
      iconName: "AlertTriangle"
    },
    {
      id: "lessons",
      title: "Lessons Learned",
      description: "Tap into accumulated historical wisdom and domain context.",
      iconName: "Lightbulb"
    }
  ],
  placeholderChats: [
    { id: '1', title: 'Payment API latency surge under load', date: 'Yesterday', category: 'Incident' },
    { id: '2', title: 'DEC-219 DB connection pool expansion', date: '3 days ago', category: 'Architecture' },
    { id: '3', title: 'DEC-288 PgBouncer vs Pool conflict', date: 'Last week', category: 'Database' },
    { id: '4', title: 'Redis volatile-lru cache invalidation', date: '2 weeks ago', category: 'Performance' },
  ],
  samplePrompts: [
    "Payment API latency increased after a traffic spike. What should I investigate?",
    "Why was local connection pool expansion rejected in favor of PgBouncer in Billing?",
    "What warnings did the departed lead architect leave regarding zero-downtime DB migrations?",
    "What recurring gotchas happen during flash sales in the payment gateway?"
  ]
};
