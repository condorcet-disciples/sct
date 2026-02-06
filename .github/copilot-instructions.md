# SCT Voting Simulation - Developer Instructions

## 🎯 Project Overview

This is a **voting simulation frontend** for the Social Choice Theory (SCT) research project. It allows users to:

1. **Manually cast votes** using sliders (Strongly Disagree → Strongly Agree)
2. **Generate synthetic voters** with random preferences using different strategies
3. **View aggregated results** in real-time

The project demonstrates preference-based voting systems in a city planning context with four transportation policy options.

---

## 🏗️ Architecture

```
sct/
├── frontend/                   # Node.js frontend application
│   ├── server.js               # Express server + API routes
│   ├── package.json            # Node dependencies
│   ├── public/                 # Static frontend assets
│   │   ├── index.html          # Main HTML page
│   │   ├── app.js              # Frontend JavaScript
│   │   └── styles.css          # Kahoot-inspired styles
│   ├── scripts/
│   │   └── generate_votes.py   # Bridge to Python randomization
│   └── data/
│       └── votes.db            # SQLite database (auto-created)
│
└── sct/
    ├── elections.py            # Core voting systems (existing)
    └── randomization/          # NEW: Preference generation module
        ├── __init__.py
        └── preference_generator.py
```

---

## 🎨 Design Philosophy

### Visual Style
- **Kahoot-inspired** color palette (vibrant purples, reds, blues, greens, yellows)
- **Minimalistic** UI with focus on the voting experience
- **Card-based** layout with subtle gradients and shadows
- **Responsive** design for mobile and desktop

### Color Variables
```css
--kahoot-red: #E21B3C;
--kahoot-blue: #1368CE;
--kahoot-yellow: #D89E00;
--kahoot-green: #26890C;
--kahoot-purple: #864CBF;
--bg-primary: #46178F;
--bg-secondary: #2D1459;
```

### UX Principles
1. **Immediate feedback** - Toast notifications for all actions
2. **Keyboard accessible** - Press Enter to cast vote
3. **Reset on vote** - Sliders return to neutral after voting
4. **Session-based** - Each voting session is isolated and reproducible

---

## 🔧 Setup Instructions

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- npm or yarn

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the server
npm start
```

The server runs at `http://localhost:3000`

### Python Module Setup

The randomization module is automatically imported from the parent `sct` package. Ensure the Python environment can import from the project root:

```bash
# From project root
pip install -e .
```

---

## 📡 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/candidates` | Get candidate list and rating labels |
| POST | `/api/sessions` | Create new voting session |
| GET | `/api/sessions` | List all sessions |
| GET | `/api/sessions/:id` | Get session details with votes |
| POST | `/api/sessions/:id/votes` | Cast a vote |
| POST | `/api/sessions/:id/generate` | Generate random votes |
| GET | `/api/sessions/:id/results` | Get aggregated results |
| DELETE | `/api/sessions/:id/votes` | Clear all votes in session |
| DELETE | `/api/sessions/:id` | Delete session |

### Vote Payload
```json
{
  "preferences": [0, 1, 2, 3],  // 0-4 for each candidate
  "isSynthetic": false,
  "agentId": "optional-id"
}
```

### Generate Payload
```json
{
  "numAgents": 10,
  "strategy": "biased",  // "random" | "clustered" | "biased"
  "seed": 42             // optional, for reproducibility
}
```

---

## 🎲 Randomization Strategies

Located in `sct/randomization/preference_generator.py`:

### 1. **Random Strategy**
Completely random ratings (0-4) for each candidate. Useful for baseline comparisons.

### 2. **Clustered Strategy**
Creates voter archetypes/clusters, then assigns agents to clusters with noise. Simulates polarized populations.

### 3. **Biased Strategy** (Default)
Uses predefined archetypes based on city planning attitudes:
- `conservative`: Prefers business-as-usual
- `moderate`: Prefers slow cars
- `progressive`: Prefers few cars
- `radical`: Prefers no cars
- `neutral`: No strong preference

---

## 🗃️ Database Schema

SQLite database at `frontend/data/votes.db`:

```sql
-- Voting sessions
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    seed INTEGER,
    description TEXT
);

-- Individual votes
CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    is_synthetic INTEGER DEFAULT 0,
    candidate_1 INTEGER NOT NULL CHECK(candidate_1 BETWEEN 0 AND 4),
    candidate_2 INTEGER NOT NULL CHECK(candidate_2 BETWEEN 0 AND 4),
    candidate_3 INTEGER NOT NULL CHECK(candidate_3 BETWEEN 0 AND 4),
    candidate_4 INTEGER NOT NULL CHECK(candidate_4 BETWEEN 0 AND 4),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔮 Future Development Ideas

### Short-term
- [ ] Add voting system selection (Plurality, Borda, Instant Runoff)
- [ ] Show detailed distribution charts per candidate
- [ ] Export results to CSV/JSON
- [ ] Session sharing via URL

### Medium-term
- [ ] Real-time multi-user voting (WebSockets)
- [ ] Visualize preference matrices
- [ ] Compare different voting systems on same data
- [ ] Add manipulation detection

### Long-term
- [ ] Integration with `elections.py` voting systems
- [ ] Paradox detection and visualization
- [ ] Educational mode with step-by-step explanations
- [ ] A/B testing different UX for voting

---

## 🧪 Testing

### Manual Testing Checklist
1. [ ] Create new session
2. [ ] Cast vote with various slider positions
3. [ ] Verify sliders reset after vote
4. [ ] Generate random votes (try all strategies)
5. [ ] Generate with specific seed twice → same results
6. [ ] Clear votes and verify counts reset
7. [ ] Check mobile responsiveness

### Reproducibility Test
```bash
# Generate 100 votes with seed 42
# Do this twice → should get identical results
curl -X POST http://localhost:3000/api/sessions/:id/generate \
  -H "Content-Type: application/json" \
  -d '{"numAgents": 100, "strategy": "biased", "seed": 42}'
```

---

## 📝 Code Style Guidelines

### JavaScript
- ES6+ syntax
- Use `async/await` for async operations
- Descriptive function names
- JSDoc comments for complex functions

### CSS
- BEM-like naming with prefixes (`.btn-`, `.candidate-`, etc.)
- CSS custom properties for theming
- Mobile-first responsive design

### Python
- Type hints for function signatures
- Docstrings for public functions
- Follow PEP 8

---

## 🤝 Contributing

1. Create feature branch from `main`
2. Follow existing code style
3. Update this README if adding new features
4. Test manually before submitting PR

---

## 📚 Related Documentation

- [csc-lectures.md](docs/notes/csc-lectures.md) - Social Choice Theory lecture notes
- [elections.py](sct/elections.py) - Core voting system implementations
- [simulator.md](docs/notes/simulator.md) - Simulator design notes

---

## 🎯 Candidates Reference

| ID | Name | Emoji | Color | Description |
|----|------|-------|-------|-------------|
| 1 | Business-as-usual | 🏢 | Red | Keep current transportation policy |
| 2 | Slow cars | 🐌 | Blue | Reduce speed limits, traffic calming |
| 3 | Few cars | 🚗 | Yellow | Reduce car ownership/usage |
| 4 | No cars | 🚶 | Green | Car-free zone, pedestrian priority |

---

*Last updated: February 2026*
