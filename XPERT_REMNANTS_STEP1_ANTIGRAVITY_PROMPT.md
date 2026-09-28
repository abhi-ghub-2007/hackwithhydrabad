# ANTIGRAVITY MASTER PROMPT — XPERT REMNANTS
## STEP 1: Full-Stack Foundation + Production-Grade Landing / Chat Shell

> **Role to adopt:** Act simultaneously as a Senior Prompt Designer, AI Systems Architect, Loop Engineer, Harness Engineer, Senior Full-Stack Engineer, UI/UX Engineer, and Technical Product Architect.
>
> **Working methodology/extensions to follow:** UI/UX, Ralph Loop, Roo Code, and Get Shit Done.
>
> **Primary objective:** Build the clean, extensible foundation and first visual experience of a real application called **XPERT REMNANTS**.
>
> **Important:** This is a real full-stack product foundation. It is NOT a throwaway landing page, static HTML mockup, or disposable prototype.

---

# 1. PRODUCT CONTEXT

Create the initial foundation of a real full-stack application called:

# XPERT REMNANTS

### Product concept

**XPERT REMNANTS** is an AI knowledge-preservation application.

It preserves the knowledge of an expert who has left an organization, allowing authorized employees to interact with that expert's **digital memory** through a ChatGPT-like interface.

The eventual application will allow users to ask questions about:

- The expert's past decisions
- Reasoning behind decisions
- Rejected approaches
- Mistakes and failures
- Warnings
- Lessons learned
- Previous experiences
- Technical knowledge
- Business knowledge
- Context behind important decisions
- Historical outcomes
- Situations the expert previously encountered

### Core product philosophy

The application should NOT eventually pretend to literally be the departed employee.

The product should preserve and expose **historical expert knowledge, experience, reasoning, decisions, outcomes, and lessons**.

The long-term conceptual model is:

```text
Expert Experience
      ↓
Knowledge Capture
      ↓
Persistent Memory
      ↓
Recall
      ↓
Contextual Reasoning
      ↓
Employee Question
      ↓
Evidence-Based Response
      ↓
Feedback / New Outcome
      ↓
Updated Organizational Memory
```

The future memory architecture will eventually use Hindsight.

However:

# DO NOT IMPLEMENT HINDSIGHT IN THIS STEP.

---

# 2. CRITICAL SCOPE BOUNDARY

This is **STEP 1 ONLY**.

For this step, build ONLY:

1. Project foundation
2. Frontend foundation
3. Backend foundation
4. Modern landing/welcome experience
5. ChatGPT-like application shell
6. Responsive/mobile-first architecture
7. Clean REST communication foundation
8. Health endpoint
9. Documentation
10. Verification and error fixing

DO NOT implement:

- AI
- LLM
- Hindsight
- RAG
- Vector database
- Embeddings
- Fine-tuning
- Agent system
- Memory engine
- Database
- Authentication
- Authorization
- User management
- Real chat persistence
- Advanced analytics
- Knowledge graph
- File processing
- Document ingestion
- Production integrations
- Slack
- Teams
- Jira
- GitHub
- Voice
- Payments
- Admin dashboard
- Complex state management
- Any other future feature

Do NOT create fake implementations of these systems.

You may create clean **extension points/interfaces/placeholders** where architecturally useful, but they must not pretend to be implemented.

---

# 3. PRODUCT NAME

Use exactly:

**XPERT REMNANTS**

Do not rename the application.

Use consistent branding across:

- Browser title
- Logo/wordmark
- Sidebar
- Welcome screen
- README
- API metadata where appropriate
- Package/application naming where practical

---

# 4. FUTURE-PROOF ARCHITECTURE REQUIREMENT

The most important architectural requirement is:

> Build the foundation so that the application can evolve rapidly without requiring a rewrite.

The project will go through frequent changes during development.

Therefore:

- Avoid tightly coupled components.
- Avoid giant files.
- Avoid putting everything in `App.jsx`.
- Avoid mixing API logic with UI components.
- Avoid mixing styling with business logic unnecessarily.
- Avoid hardcoded future infrastructure.
- Keep components reusable.
- Keep backend routes modular.
- Keep configuration centralized.
- Keep environment-specific values in environment variables.
- Create clean service boundaries.
- Prefer composition over duplication.
- Keep future Hindsight/AI integration easy.
- Keep the frontend independent from the future AI implementation.
- Keep the backend capable of adding future services without restructuring the entire project.

Do not over-engineer the foundation.

The goal is:

> **Simple now, extensible later.**

---

# 5. MOBILE / APK REQUIREMENT

This is initially a web application.

However, the architecture and UI must be designed so the application can later be packaged into an Android APK.

Therefore:

## Frontend must be:

- Responsive
- Mobile-first
- Touch-friendly
- Component-based
- Browser-compatible
- Free from desktop-only assumptions
- Free from hover-only essential interactions
- Free from fixed layouts that break on small screens
- Free from browser-specific hacks

Design the frontend so that later it can reasonably be wrapped using a technology such as:

- Capacitor
- Trusted Web Activity
- Another WebView-based packaging solution

Do NOT install or configure Capacitor yet unless absolutely necessary.

Do NOT build a native Android application in this step.

Instead, make the React application **APK-conversion friendly**.

### Mobile requirements

The interface must work comfortably at:

- 320px+
- 375px
- 390px
- 414px
- Tablet widths
- Desktop widths

The sidebar should become a mobile drawer/sheet when appropriate.

The message composer must remain usable on mobile.

Buttons must have comfortable touch targets.

Avoid horizontal overflow.

---

# 6. REQUIRED TECH STACK

## Frontend

- React
- Vite
- JavaScript

Use modern React patterns.

## Backend

- Python
- FastAPI

## Communication

- REST API
- JSON

## Project structure

```text
xpert-remnants/
│
├── frontend/
│
├── backend/
│
├── README.md
└── .gitignore
```

Do not merge frontend and backend into one application.

---

# 7. FRONTEND REQUIREMENTS

Create a professional React application.

The frontend should feel like the foundation of a serious AI SaaS product.

It should NOT look like:

- A college project
- A generic Bootstrap dashboard
- A basic CRUD application
- A template with random gradients
- A static marketing page
- An unfinished wireframe

---

# 8. UI/UX DIRECTION

Use the UI/UX methodology to establish a coherent design system before building individual screens.

The visual direction should be:

- Modern
- Elite
- Premium
- Intelligent
- Minimal
- Professional
- Enterprise-ready
- Attractive without being flashy
- Comfortable for long chat sessions

Avoid:

- Excessive gradients
- Excessive glassmorphism
- Neon overload
- Giant decorative text
- Random animations
- Excessive shadows
- Generic AI robot imagery
- Overly futuristic "cyberpunk" aesthetics
- Cringe startup-style copy

The product should communicate:

> **Institutional intelligence + premium AI product + trust**

---

# 9. BRANDING DIRECTION

Application:

**XPERT REMNANTS**

Suggested visual language:

- Strong typography
- Refined neutral base
- One controlled accent color
- Clear hierarchy
- High readability
- Subtle depth
- Premium spacing
- Clean iconography

Do not lock the entire application to a particular color palette if doing so makes future theming difficult.

Create design tokens / CSS variables for:

- Background
- Surface
- Elevated surface
- Text primary
- Text secondary
- Border
- Accent
- Success
- Warning
- Error
- Radius
- Spacing
- Shadows

This allows the visual identity to change later without rewriting components.

---

# 10. LANDING / WELCOME EXPERIENCE

The initial application should open into a polished welcome state.

This is NOT a separate marketing website.

It should feel like the actual product.

Example structure:

```text
┌────────────────────────────────────────────────────────────┐
│ XPERT REMNANTS                                             │
├───────────────┬────────────────────────────────────────────┤
│               │                                            │
│ + New Chat    │              XPERT REMNANTS                │
│               │                                            │
│ Recent        │       Preserve what experience knows.      │
│ Chats         │                                            │
│               │                                            │
│               │       Ask about decisions, failures,       │
│               │       reasoning and lessons from the       │
│               │       organization's expert memory.        │
│               │                                            │
│               │       [ Start a conversation ]              │
│               │                                            │
├───────────────┴────────────────────────────────────────────┤
│ Message XPERT REMNANTS...                         [Send]   │
└────────────────────────────────────────────────────────────┘
```

This is only the visual/product shell.

Do NOT make the message interaction actually call an AI model.

---

# 11. REQUIRED FRONTEND COMPONENTS

Build reusable components.

At minimum:

```text
App
├── AppShell
│
├── Sidebar
│   ├── Logo / Brand
│   ├── NewChatButton
│   ├── ChatHistory
│   └── SidebarFooter
│
├── MainContent
│   ├── WelcomeState
│   ├── ConversationView
│   └── MessageComposer
│
└── MobileNavigation
```

You may adjust this architecture if you have a better clean structure.

Do not put every component in one file.

---

# 12. SIDEBAR

Include:

### Brand

**XPERT REMNANTS**

### New Chat

Button:

> + New Chat

### Chat history placeholder

Example sections:

```text
RECENT

Understanding deployment decisions
Payment incident analysis
Database migration discussion
```

These should be clearly treated as placeholder/demo UI.

Do not implement real persistence yet.

### Future-ready structure

The sidebar should later be able to receive:

```text
GET /api/chats
```

without requiring a major UI rewrite.

---

# 13. MAIN CONVERSATION AREA

Create a professional chat area.

Include:

- Header
- Welcome state
- Conversation container
- Message components
- Empty state
- Input area

The empty state should communicate the product concept.

Suggested copy:

### Heading

> Preserve the experience behind every decision.

### Supporting text

> Ask questions about an expert's decisions, reasoning, failures, warnings, and lessons learned.

Do not claim that AI memory is already active.

---

# 14. MESSAGE COMPONENTS

Create reusable message components.

For example:

```text
Message
├── UserMessage
└── AssistantMessage
```

The UI should already support:

- User messages
- Assistant messages
- Timestamp placeholder
- Avatar/icon placeholder
- Loading state
- Error state

But there should be NO actual AI generation yet.

Use controlled mock/static state only if necessary to demonstrate the UI.

Clearly separate mock UI state from future API logic.

---

# 15. MESSAGE COMPOSER

Create a polished message input.

Requirements:

- Responsive
- Multiline textarea
- Send button
- Disabled state
- Keyboard-friendly
- Mobile-friendly
- Proper focus state
- No horizontal overflow

Placeholder:

> Ask about an expert's experience...

The Send button should NOT call an AI model.

If you demonstrate the button interaction, it may add a clearly marked local placeholder message such as:

> AI memory is not connected yet.

However, do not create fake AI responses that could be mistaken for actual functionality.

---

# 16. RESPONSIVE BEHAVIOR

### Desktop

Persistent sidebar.

### Tablet

Compact sidebar.

### Mobile

Sidebar becomes a drawer/sheet.

Main content takes full width.

Composer stays accessible.

Header remains compact.

No layout should require horizontal scrolling.

---

# 17. FRONTEND FOLDER STRUCTURE

Use a clean structure similar to:

```text
frontend/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AppShell.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── MobileNavigation.jsx
│   │   │
│   │   ├── chat/
│   │   │   ├── ConversationView.jsx
│   │   │   ├── Message.jsx
│   │   │   ├── MessageComposer.jsx
│   │   │   └── WelcomeState.jsx
│   │   │
│   │   └── ui/
│   │       └── reusable UI components
│   │
│   ├── pages/
│   │   └── Home.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── hooks/
│   │
│   ├── utils/
│   │
│   ├── config/
│   │
│   ├── styles/
│   │   ├── globals.css
│   │   └── tokens.css
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── public/
├── .env.example
├── package.json
└── vite.config.js
```

You may modify this if necessary, but preserve the principles:

- UI components separate
- Pages separate
- API services separate
- Configuration separate
- Styles/design tokens separate

---

# 18. FRONTEND API FOUNDATION

Create a small API abstraction.

For example:

```text
src/services/api.js
```

The API base URL must come from an environment variable.

Example:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Do NOT hardcode production URLs.

Do NOT add API keys.

Do NOT create fake future endpoints.

The API layer should simply be ready for future integration.

---

# 19. BACKEND REQUIREMENTS

Create a proper FastAPI application.

The backend must be structured so that future services can be added cleanly.

For now, only implement:

```http
GET /api/health
```

Response:

```json
{
  "status": "ok",
  "application": "XPERT REMNANTS"
}
```

---

# 20. BACKEND STRUCTURE

Use a clean structure similar to:

```text
backend/
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── health.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── constants.py
│   │
│   ├── services/
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   └── __init__.py
│   │
│   └── models/
│       └── __init__.py
│
├── tests/
│   └── test_health.py
│
├── requirements.txt
├── .env.example
└── run.py
```

The exact structure may be improved if necessary.

Do not create empty files just for decoration.

Only create files that establish useful architectural boundaries.

---

# 21. FASTAPI REQUIREMENTS

Configure:

- FastAPI
- CORS
- Environment-based configuration
- API router structure
- Health endpoint
- Basic error handling
- Clean application startup

The backend should be runnable independently.

---

# 22. CORS

Configure CORS so the React frontend can communicate with FastAPI locally.

Do not use unsafe unrestricted configuration if avoidable.

Use environment-based allowed origins where practical.

Example:

```env
FRONTEND_URL=http://localhost:5173
```

---

# 23. ENVIRONMENT VARIABLES

Create:

```text
frontend/.env.example
backend/.env.example
```

Do not commit real secrets.

Do not hardcode:

- API keys
- LLM keys
- Hindsight credentials
- Database credentials
- Tokens

There are no actual external credentials in this step.

---

# 24. README REQUIREMENTS

Create a useful `README.md`.

Include:

## 1. What XPERT REMNANTS is

## 2. Current project status

Explicitly state:

> STEP 1 — Foundation only

## 3. Technology stack

## 4. Project structure

## 5. Prerequisites

## 6. Frontend installation

## 7. Backend installation

## 8. How to run frontend

## 9. How to run backend

## 10. API health endpoint

## 11. Environment variables

## 12. Verification steps

## 13. Future architecture placeholders

For example:

```text
Future Architecture
-------------------

AI / LLM Layer
[Not implemented]

Hindsight Memory
[Not implemented]

Retrieval / RAG
[Not implemented]

Database
[Not implemented]

Authentication
[Not implemented]

Knowledge Capture
[Not implemented]
```

Do not falsely claim these are implemented.

---

# 25. GET SHIT DONE PRINCIPLE

Prioritize working software over unnecessary abstraction.

Rules:

1. Build the smallest correct foundation.
2. Do not over-engineer.
3. Do not install libraries without a reason.
4. Do not create speculative infrastructure.
5. Verify every important step.
6. Fix actual errors before moving on.
7. Keep the application runnable throughout the process.

---

# 26. RALPH LOOP

Use an iterative verification loop.

For every implementation unit:

```text
PLAN
  ↓
IMPLEMENT
  ↓
RUN
  ↓
VERIFY
  ↓
IDENTIFY FAILURE
  ↓
FIX
  ↓
RE-RUN
  ↓
CONFIRM
```

Do not assume that code is correct merely because it was written successfully.

The loop ends only when the current requirement is verified.

---

# 27. ROO CODE STYLE

Work as if another engineer will continue the project tomorrow.

Therefore:

- Keep changes scoped.
- Avoid unrelated refactors.
- Explain important architectural decisions.
- Preserve working code.
- Prefer readable names.
- Keep files focused.
- Avoid hidden magic.
- Avoid unnecessary dependencies.
- Make future modifications easy.

---

# 28. HARNESS ENGINEERING REQUIREMENT

Create a development environment where future agents/developers can safely modify the application.

The project should have:

- Predictable commands
- Clear entry points
- Clear environment variables
- Clear folder boundaries
- Simple local setup
- Basic automated test
- Basic health verification

The project must be understandable without needing the original developer's memory.

---

# 29. TESTING

At minimum, implement:

### Backend

Test:

```text
GET /api/health
```

Expected:

```json
{
  "status": "ok",
  "application": "XPERT REMNANTS"
}
```

### Frontend

Verify:

- App starts
- Home screen loads
- Sidebar renders
- Welcome state renders
- Composer renders
- Responsive layout works
- No console-breaking errors
- API base URL configuration works

Do not add a large testing framework unless required.

---

# 30. QUALITY GATES

Before declaring STEP 1 complete, verify all of the following.

## Architecture

- [ ] Frontend and backend are separate.
- [ ] Folder structure is clean.
- [ ] Components are reusable.
- [ ] API logic is separated.
- [ ] Environment variables are used appropriately.
- [ ] No future credentials are hardcoded.

## Frontend

- [ ] React application starts.
- [ ] UI looks polished.
- [ ] Desktop layout works.
- [ ] Tablet layout works.
- [ ] Mobile layout works.
- [ ] Sidebar works visually.
- [ ] Welcome screen works.
- [ ] Message composer works visually.
- [ ] No horizontal overflow.
- [ ] No major console errors.

## Backend

- [ ] FastAPI starts.
- [ ] `/api/health` works.
- [ ] Correct JSON is returned.
- [ ] CORS is configured.
- [ ] Backend structure is modular.

## Documentation

- [ ] README exists.
- [ ] Setup instructions are correct.
- [ ] Environment variables documented.
- [ ] Current status documented.
- [ ] Future architecture clearly marked as not implemented.

---

# 31. VISUAL QUALITY GATE

Do not stop after making the UI technically functional.

Inspect the application visually.

Check:

- Spacing
- Typography
- Alignment
- Button sizing
- Sidebar proportions
- Input proportions
- Empty-state composition
- Responsive behavior
- Visual hierarchy
- Contrast
- Focus states
- Hover states
- Mobile navigation
- Overall premium feel

The UI should look like an actual product foundation that could eventually become a serious enterprise AI application.

---

# 32. DO NOT BUILD THE FOLLOWING YET

This section is NON-NEGOTIABLE.

Do NOT implement:

```text
❌ Hindsight
❌ Hindsight API
❌ Memory banks
❌ RETAIN
❌ RECALL
❌ REFLECT
❌ RAG
❌ Vector database
❌ Embeddings
❌ LLM
❌ AI agent
❌ Fine-tuned model
❌ Database
❌ Authentication
❌ Authorization
❌ User accounts
❌ Real chat persistence
❌ Document ingestion
❌ Knowledge graph
❌ Voice
❌ External integrations
```

Only create clean architectural extension points if genuinely useful.

---

# 33. IMPORTANT ANTI-OVERENGINEERING RULE

If you are unsure whether something belongs in STEP 1:

**Do not implement it.**

Ask:

> “Is this necessary for a clean, runnable foundation and the initial product shell?”

If the answer is no, leave it for a future step.

---

# 34. DO NOT AUTO-PROCEED

After STEP 1 is implemented and verified:

# STOP.

Do NOT automatically begin:

- Hindsight integration
- AI implementation
- RAG
- database
- authentication
- memory architecture
- advanced chat

Wait for the next explicit instruction.

---

# 35. SIDE TASKS I MUST PERFORM

After implementation, provide me with a separate section titled:

# MY SIDE — REQUIRED ACTIONS

Give me an exact, beginner-friendly checklist of everything I personally need to do.

For example:

```text
1. Open terminal
2. Navigate to project
3. Install Node.js if required
4. Install Python if required
5. Run frontend installation command
6. Run backend installation command
7. Create .env files from .env.example
8. Start backend
9. Start frontend
10. Open browser
11. Test health endpoint
12. Test frontend
```

Do not assume I know what to do.

For every command, tell me:

- Which terminal
- Which directory
- Exact command
- Expected result
- What to do if it fails

---

# 36. SIDE TASK FORMAT

Use this exact style:

```text
STEP 1 — Open Terminal

Directory:
xpert-remnants/

Command:
...

Expected result:
...

If this fails:
...
```

Separate:

### Required

from:

### Optional

Do not give me unnecessary tasks.

---

# 37. FINAL REPORT AFTER IMPLEMENTATION

After you finish implementation and verification, give me:

## 1. What was created

Short summary.

## 2. Final project structure

Show the actual structure.

## 3. Technologies installed

List only what was actually installed.

## 4. Commands used

Show the commands used to install/run/test.

## 5. Verification results

Example:

```text
Frontend: PASS
Backend: PASS
Health API: PASS
CORS: PASS
Responsive UI: PASS
Build: PASS
```

Do not claim PASS unless actually verified.

## 6. Files changed

List important files.

## 7. MY SIDE — REQUIRED ACTIONS

Give exact steps I need to perform.

## 8. Known limitations

Clearly state what is intentionally not implemented.

## 9. NEXT STEP

Write only:

> Ready for the next explicit development instruction.

Do not implement the next step.

---

# 38. DEVELOPMENT BEHAVIOR

While working:

- Inspect the existing environment before making assumptions.
- If this project already contains files, preserve useful existing work unless it conflicts with this specification.
- Do not delete or rewrite working functionality unnecessarily.
- If this is a fresh directory, create the structure described above.
- Prefer stable, simple dependencies.
- Use JavaScript, not TypeScript, for this step because the specified frontend stack is React + Vite + JavaScript.
- Keep the frontend/backend independently runnable.
- Keep the UI production-quality even though the functionality is intentionally limited.
- Do not fabricate successful tests.
- Do not hide errors.
- If something fails, debug it and rerun the relevant verification.

---

# 39. DEFINITION OF DONE

STEP 1 is complete only when:

```text
✓ XPERT REMNANTS project exists
✓ frontend exists
✓ backend exists
✓ frontend runs
✓ backend runs
✓ /api/health works
✓ CORS works
✓ React UI is polished
✓ ChatGPT-like shell exists
✓ Landing/welcome state exists
✓ Sidebar exists
✓ New Chat exists
✓ Chat history placeholder exists
✓ Message UI exists
✓ Composer exists
✓ Responsive behavior exists
✓ APK-friendly frontend structure exists
✓ README exists
✓ .env.example files exist
✓ Basic backend test exists
✓ No major runtime errors
✓ Future AI systems are NOT implemented
✓ Project remains easy to modify
✓ Manual setup instructions are provided
✓ Work stops after STEP 1
```

---

# 40. FINAL INSTRUCTION

Build **STEP 1 of XPERT REMNANTS** exactly according to this specification.

Think like:

- A senior product architect
- A senior UI/UX engineer
- A full-stack engineer
- An AI systems architect
- A harness engineer
- A loop engineer
- A developer who will maintain this code for months

The goal is not to produce the maximum amount of code.

The goal is to produce the **cleanest, most extensible, visually polished, mobile-ready foundation** for XPERT REMNANTS.

Build it.

Run it.

Test it.

Fix it.

Verify it.

Document it.

Then STOP.
