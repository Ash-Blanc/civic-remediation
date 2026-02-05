# Civic Remediation System 🏙️✨

**Turning systemic failures into solved problems using Autonomous AI Agents.**

---

## 💡 The Idea: Why We Built This

It started with a simple thought: **What if we could fix our broken civic systems with AI?**

We all see the loopholes—the potholes that never get filled, the waste management systems that fail, the infrastructure that crumbles while paperwork piles up. I saw a YouTube short about these systemic failures and wondered:

> *"What if we can create an agent system that, when asked on a topic, scans the internet, finds such insightful facts/posts, and calls other agents to figure out solutions and take action to get them solved?"*

That's exactly what this project does. It's not just a chatbot; it's a **digital task force** dedicated to solving real-world civic problems.

![Origin Story](assets/origin_story.png)
*[Read the full original conversation here](https://gemini.google.com/share/edcaf8469ef8)*

![Civic Remediation Pipeline](assets/pipeline_diagram.png)

---

## 🚀 The Singleton Pipeline Architecture

We use a **Converging Singleton Pipeline** that focuses on "One Thing At A Time". Instead of generating divergent lists of problems and solutions, the system narrows down to a single, actionable project launch blueprint.

**The Pipeline Flow:**
1. **ONE Problem** (Selected for max impact/feasibility)
2. **ONE Root Cause** (The critical lever to pull)
3. **ONE Department** (The responsible active body)
4. **ONE Solution** (The most effective technical intervention)
5. **ONE Funding Source** (The best-fit grant/programme)
6. **🚀 Project Launch** (A complete execution blueprint)

---

## 🤖 Meet Your Digital Task Force

Each stage is handled by a specialized agent with a specific "Select One" mandate:

### 1. Sentinel (The Scout) 🔭
**Goal:** Select the SINGLE most critical civic problem.
Analyses severity, population impact, and feasibility to pick the problem where intervention matters most.

### 2. Investigator (The Detective) 🔎
**Goal:** Identify the SINGLE critical root cause.
Digs past symptoms to find the systemic failure point—whether it's industrial discharge, broken incentives, or a specific bottleneck.

### 3. Bureaucrat (The Mapper) 🏛️
**Goal:** Select the SINGLE responsible department.
Navigates the maze of government bodies to find the "Active Body" that actually has the jurisdiction and mandate to act.

### 4. Engineer (The Solver) 🛠️
**Goal:** Design the SINGLE best technical solution.
Matches the root cause to a scalable, modular intervention (e.g., decentralized STPs, sensor networks) that can be piloted quickly.

### 5. Liaison (The Fundraiser) 🤝
**Goal:** Match the SINGLE best funding source.
Scans government schemes, CSR funds, and global grants to find the money that perfectly fits the solution scope.

---

## 🚀 How to Run It

### Prerequisites
- **Python** (installed via `uv`)
- **Docker** (for shared memory)
- API Keys for **Perplexity/OpenAI** (configured in `.env`)

### 1. Setup
```bash
# Install package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Start the brain (Database)
docker compose up -d
```

### 2. Run the Pipeline (Singleton Mode)
This runs the converging pipeline to generate a focused project blueprint:
```bash
uv run python -m app.main "Pollution of the Ganga River"
```

### 3. Run in Team Mode (Legacy)
For broader exploration without strict convergence:
```bash
uv run python -m app.main "Pollution of the Ganga River" team
```

### 4. Go Pro (AgentOS)
Want a nice UI? Run the server and connect it to Agno's interface:
```bash
uv run -m app.agent_os
```
Then visit **[os.agno.com](https://os.agno.com)**.

---

## 🧠 Under the Hood (For Developers)

This system is built on the cutting edge of Agentic AI:
- **Framework**: [Agno](https://agno.com)
- **Architecture**: Sequential Workflow with Pydantic-enforced Singleton Outputs
- **Model**: Perplexity Reasoning / Mistral Large
- **Search**: Parallel Web Search (for high-fidelity browsing)
- **Memory**: PostgreSQL with `pgvector`
- **Monitoring**: LangWatch (for tracing)

---

## 🤝 Join the Mission

We are building this open-source to empower citizens everywhere. If you're a developer, designer, or civic enthusiast, come build with us!

[**Join our Discord Community**](https://discord.gg/g95mrWGm4G) to contribute, discuss ideas, and be part of this ambitious project.

---
*Built with ❤️ for a better civic future.*
