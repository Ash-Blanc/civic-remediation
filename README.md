# Civic Remediation System 🏙️✨

**Turning systemic failures into solved problems using Autonomous AI Agents.**

---

## 💡 The Idea: Why We Built This

It started with a simple thought: **What if we could fix our broken civic systems with AI?**

We all see the loopholes—the potholes that never get filled, the waste management systems that fail, the infrastructure that crumbles while paperwork piles up. I saw a YouTube short about these systemic failures and wondered:

> *"What if we can create an agent system that, when asked on a topic, scans the internet, finds such insightful facts/posts, and calls other agents to figure out solutions and take action to get them solved?"*

That's exactly what this project does. It's not just a chatbot; it's a **digital task force** dedicating to solving real-world civic problems.

![Origin Story](assets/origin_story.png)
*[Read the full original conversation here](https://gemini.google.com/share/edcaf8469ef8)*

---

## 🤖 Meet Your Digital Task Force

This isn't one AI trying to do everything. It's a **Team of Specialists**, each with a specific job, working together to get results.

### 1. The Scout (Sentinel) 🔭
**"I see the problem."**
Scans the internet to find proof of systemic failures (news reports, data, citizen complaints). It separates noise from hard facts.

### 2. The Scientist (Analyst) 🔬
**"I understand why it's happening."**
Digs deep into the root causes. Is it a budget issue? A technical flaw? A policy gap? It uses scientific data to diagnose the disease, not just the symptoms.

### 3. The Solver (Engineer) 🛠️
**"I know who can fix it."**
Searches the private sector for startups and vendors who have the exact technology to solve this specific problem.

### 4. The Planner (Strategist) ♟️
**"Here is the best path forward."**
Ranks the solutions based on cost, speed, and impact. It creates a battle plan for remediation.

### 5. The Doer (Liaison) 🤝
**"Let's make it happen."**
Drafts the actual partnership proposals and emails to connect the city with the solvers. (Don't worry, it asks for your permission before hitting send!)

---

## 🚀 How to Run It

Ready to unleash the agents? Here is the simple guide.

### Prerequisites
- **Python** (installed via `uv`)
- **Docker** (for their shared brain/memory)
- API Keys for **Mistral AI** and **Parallel** (for browsing)

### 1. Setup
```bash
# Install the package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Start the brain (Database)
docker compose up -d
```

### 2. Wake Up the Team
Run the full team to solve a problem:
```bash
uv run python app/main.py "Pollution of the Ganga River" team
```

### 3. Go Pro (AgentOS)
Want a nice UI? Run the server and connect it to Agno's interface:
```bash
uv run python app/agent_os.py
```
Then visit **[os.agno.com](https://os.agno.com)**.

---

## 🧠 Under the Hood (For Developers)

This system is built on the cutting edge of Agentic AI:
- **Framework**: [Agno](https://agno.com)
- **Model**: Mistral Large (via `Agno` models)
- **Search**: Parallel Web Search (for high-fidelity browsing)
- **Memory**: PostgreSQL with `pgvector` (they remember everything)
- **Monitoring**: LangWatch (for tracing their thoughts)

---
*Built with ❤️ for a better civic future.*
