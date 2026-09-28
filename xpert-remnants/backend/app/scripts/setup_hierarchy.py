"""
Database Setup & Hierarchy Configuration (Antigravity / Gemini 3.8 Flash)
1. Ensures Organization 1 is 'Microsoft'.
2. Links all 50 synthetic experts directly to their respective 5 canonical projects (10 per project).
3. Creates and populates project_modules for the 5 projects based on genuine public project architecture.
4. Creates knowledge_updates and learning_events tables if needed.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "xpert_remnants.db")

def run():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Update Organization
    cursor.execute("""
        UPDATE organizations
        SET name = 'Microsoft', slug = 'microsoft', domain = 'microsoft.com'
        WHERE id = 1
    """)
    print("Organization 1 set to Microsoft.")

    # 2. Add project_id to experts table if missing
    cursor.execute("PRAGMA table_info(experts)")
    cols = [r[1] for r in cursor.fetchall()]
    if "project_id" not in cols:
        cursor.execute("ALTER TABLE experts ADD COLUMN project_id INTEGER REFERENCES projects(id)")
        print("Added project_id column to experts.")

    # Link experts to their canonical projects
    canonical_projects = [
        (10, 'Visual Studio Code'),
        (11, 'PowerToys'),
        (12, 'Windows Terminal'),
        (13, 'TypeScript'),
        (14, 'Semantic Kernel')
    ]

    for p_id, p_name in canonical_projects:
        # Find experts with memories in this project
        cursor.execute("""
            SELECT DISTINCT expert_id FROM decision_memories
            WHERE project_id = ? AND expert_id IS NOT NULL
        """, (p_id,))
        exp_ids = [r[0] for r in cursor.fetchall()]
        for eid in exp_ids:
            cursor.execute("UPDATE experts SET project_id = ? WHERE id = ?", (p_id, eid))
        print(f"Linked {len(exp_ids)} experts to project '{p_name}' (ID {p_id}).")

    # 3. Create project_modules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL REFERENCES projects(id),
            name TEXT NOT NULL,
            description TEXT,
            technology TEXT,
            dependencies TEXT,
            risks TEXT,
            current_state TEXT DEFAULT 'ACTIVE',
            provenance TEXT DEFAULT 'PUBLIC_PROJECT_DOC',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("Created project_modules table.")

    # Seed modules for 5 projects if empty
    cursor.execute("SELECT COUNT(*) FROM project_modules")
    if cursor.fetchone()[0] == 0:
        modules_data = [
            # Visual Studio Code (ID 10)
            (10, "Integrated Terminal", "Terminal subsystem integrating ConPTY and xterm.js for high-throughput shell sessions.", "ConPTY, xterm.js, C++", "Node.js IPC", "Latency during rapid log streaming; ConPTY Windows 10 compatibility"),
            (10, "Extension Host", "Out-of-process execution container guaranteeing UI thread responsiveness.", "Node.js, RPC, V8 Isolation", "Core Workbench", "Memory leaks in third-party extensions; IPC saturation"),
            (10, "Workbench & Editor Core", "High-performance code editing buffer and syntax tree coordination.", "Monaco Editor, WebGL, Electron", "Chromium, V8", "Large file (>100MB) memory exhaustion; GPU rendering fallbacks"),
            (10, "Remote Development", "SSH, WSL, and Container tunnel architecture for headless remote workspaces.", "Node.js, SSH, WSL2 gRPC", "Local Extension Host", "Network disconnect state recovery; port forwarding security"),
            (10, "Language Server Protocol (LSP)", "Standardized protocol decoupling editors from language compilers.", "JSON-RPC, TypeScript, Async IO", "Compiler CLI", "High latency during whole-project semantic index passes"),

            # PowerToys (ID 11)
            (11, "PowerToys Run", "Modular quick-launcher with fuzzy search and plugin extensibility.", "C#, WPF, Win32 API", "Windows Indexer", "Cold-start latency; plugin IPC crashes"),
            (11, "FancyZones", "Window management utility for organizing windows into defined grid layouts.", "C++, Win32 APIs, DirectX", "DWM, Shell32", "Multi-monitor DPI scaling artifacts; virtual desktop transitions"),
            (11, "Keyboard Manager", "Low-level keyboard remapping and shortcut interceptor.", "C++, Low-level Win32 Hooks", "User32", "Hook latency impacting gaming frame pacing; UAC elevated window bypass"),
            (11, "ColorPicker", "System-wide color selection utility with color space conversions.", "C#, WinUI 3, Direct2D", "DWM API", "DirectX capture overhead on high-refresh displays"),
            (11, "Text Extractor", "Optical character recognition tool for extracting text from screen clips.", "C#, Windows.Media.Ocr", "Snipping Infrastructure", "Low OCR accuracy on non-standard fonts"),

            # Windows Terminal (ID 12)
            (12, "Terminal Core Engine", "High-performance VT parsing and text buffer manipulation subsystem.", "C++/WinRT, UTF-16 Buffer", "Windows Console", "Buffer synchronization deadlocks under saturated output"),
            (12, "DirectX Rendering Engine", "GPU-accelerated text and glyph renderer built on DirectWrite.", "DirectX 11, DirectWrite, DXGI", "D3D11 Driver", "Fallback tearing on older Intel integrated GPUs"),
            (12, "ConPTY Translation Layer", "Bridge translating legacy console API calls to standard VT escape sequences.", "C++, Named Pipes, Win32", "Kernel32 Console API", "Double-echoing and line-wrapping artifacts on legacy CMD tools"),
            (12, "Profile & Tab Manager", "Multi-tab UI hosting dynamic shell profiles (PowerShell, WSL, Cloud Shell).", "XAML Islands, WinUI", "Windows Shell", "Settings migration schema conflicts across versions"),
            (12, "Cascadia Code Glyph Pipeline", "Font ligature parsing and glyph caching pipeline.", "OpenType, DWrite Font Cache", "DirectWrite", "Memory overhead with large emoji sequences"),

            # TypeScript (ID 13)
            (13, "Type Checker & Semantic Analyzer", "Core engine calculating type relationships, inference, and union reduction.", "TypeScript, Node.js", "AST Parser", "Exponential type instantiation in recursive conditional types"),
            (13, "Scanner & AST Parser", "Incremental recursive-descent scanner and syntax tree generator.", "TypeScript, Node.js", "File System", "Incremental syntax tree corruption on incomplete tokens"),
            (13, "Emitter & Code Generation", "Transpiler transforming TypeScript and modern ECMAScript to JS and source maps.", "SourceMap Generator", "AST", "Source map mapping offset drifts in complex JSX transforms"),
            (13, "Language Service (TSServer)", "Long-running daemon serving auto-complete, rename, and refactoring to IDEs.", "JSON-RPC, Node.js IPC", "Type Checker", "TSServer memory bloat on monorepos with 10k+ files"),
            (13, "Incremental Project Builder (--build)", "Multi-project dependency graph scheduler and tsbuildinfo cache engine.", "DAG Scheduler, File Hashes", "TSServer", "Out-of-order build cache invalidation in circular project references"),

            # Semantic Kernel (ID 14)
            (14, "AI Kernel & Context Orchestrator", "Core orchestration runtime sequencing LLM prompts, native functions, and memories.", "C#, Python, Async Tasks", "HTTP Client", "Context window overflow during multi-step chains"),
            (14, "Native & Semantic Function Registry", "Plugin registry indexing tool functions and semantic prompt templates.", "Reflection, JSON Schema", "Kernel Core", "Schema validation failures on dynamic parameters"),
            (14, "Memory & Vector Connectors", "Abstraction layer for text embeddings and vector search backends.", "Azure AI Search, Qdrant, Chroma", "Embedding APIs", "Rate limiting on batch embedding calls"),
            (14, "Planners & Reasoning Engine", "Stepwise and action planners decomposing user intents into function call sequences.", "Prompt Engineering, Few-shot", "Kernel Functions", "Infinite loops in autonomous goal decomposition"),
            (14, "Connector Infrastructure", "Standardized client connectors for OpenAI, Azure OpenAI, and local models.", "REST, gRPC, SSE Streaming", "HTTP Stack", "Streaming token buffering latency and timeout recovery")
        ]

        cursor.executemany("""
            INSERT INTO project_modules (project_id, name, description, technology, dependencies, risks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, modules_data)
        print(f"Inserted {len(modules_data)} project modules across 5 canonical projects.")

    # 4. Create knowledge_updates table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER REFERENCES projects(id),
            type TEXT DEFAULT 'DECISION_CHANGE',
            old_state TEXT,
            new_state TEXT NOT NULL,
            reason TEXT,
            actor TEXT DEFAULT 'Current authorized user',
            effective_at TEXT,
            source TEXT DEFAULT 'USER_UPDATE',
            confidence REAL DEFAULT 1.0,
            related_decision_id INTEGER REFERENCES decision_memories(id),
            related_memory_id TEXT,
            provenance TEXT DEFAULT 'USER_PROVIDED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("Created knowledge_updates table.")

    # 5. Create learning_events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            project_id INTEGER REFERENCES projects(id),
            event_type TEXT DEFAULT 'USER_CORRECTION',
            source TEXT DEFAULT 'USER_UPDATE',
            content TEXT NOT NULL,
            confidence REAL DEFAULT 1.0,
            promotion_status TEXT DEFAULT 'CONFIRMED',
            promoted_memory_id INTEGER REFERENCES decision_memories(id),
            promoted_decision_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("Created learning_events table.")

    conn.commit()
    conn.close()
    print("Hierarchy and database setup complete!")

if __name__ == "__main__":
    run()
