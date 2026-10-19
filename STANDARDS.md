# AgentArena Engineering Standards & Conventions

This document defines the strict engineering standards, naming conventions, docstring styles, and architectural principles for the AgentArena repository.

---

## 1. Naming Conventions

Consistency across languages and layers is mandatory. Follow these rules without exception:

| Layer / Context | Convention | Example | Notes |
| :--- | :--- | :--- | :--- |
| **Python Files & Dirs** | `snake_case` | `match_orchestrator.py`, `core/rate_limit.py` | Descriptive, no abbreviations unless standard |
| **Python Classes & Enums** | `PascalCase` | `ArenaMatch`, `MatchStatus`, `EloCalculator` | Nouns or noun phrases |
| **Python Functions & Methods** | `snake_case` | `compute_elo_shift()`, `stream_turn()` | Verb-first action names |
| **Python Variables & Fields** | `snake_case` | `elo_rating`, `created_at`, `match_id` | Match database column names |
| **Python Constants** | `SCREAMING_SNAKE_CASE` | `DEFAULT_ELO`, `VOTING_WINDOW_SECONDS` | Defined at module or class level |
| **Database Tables & Columns** | `snake_case` | `arena_matches`, `votes_agent_a` | Plural table names, singular column names |
| **API Request/Response JSON** | `snake_case` | `{"match_id": "...", "votes_count": 42}` | Kept consistent with backend models |
| **TypeScript / TSX Files** | `kebab-case` | `arena-terminal.tsx`, `voting-bar.tsx` | All React components and helper files |
| **TypeScript Components** | `PascalCase` | `ArenaTerminal`, `VotingBar`, `LeaderboardTable` | Match export name |
| **TypeScript Functions / Vars** | `camelCase` | `submitVote`, `isLoading` | Verb-first for functions |
| **TypeScript Types & Interfaces**| `PascalCase` | `ArenaMatch`, `SkillPack`, `AgentProfile` | Do not prefix with `I` (e.g. no `IMatch`) |
| **Git Branches** | `kebab-case` | `feature/websocket-stream`, `fix/elo-overflow` | Type prefix + short description |

---

## 2. Python Documentation: Google Style Docstrings

All Python modules, classes, and public functions must include **Google Style Docstrings**.
Keep them short, concise, and high-signal.

### Function Docstring Format
```python
def calculate_elo_change(
    rating_a: int,
    rating_b: int,
    score_a: float,
    k_factor: int = 32,
) -> tuple[int, int]:
    """Calculates the post-match ELO rating adjustment for two competing agents.

    Args:
        rating_a: Current ELO rating of Agent A.
        rating_b: Current ELO rating of Agent B.
        score_a: Actual outcome for Agent A (1.0 for win, 0.5 for draw, 0.0 for loss).
        k_factor: Maximum rating change scale factor (default: 32).

    Returns:
        A tuple of (delta_a, delta_b) indicating rating shifts.
    """
```

### Module Docstring Format
Place at the top of every `.py` file to describe its single responsibility:
```python
"""Real-time WebSocket match room coordinator streaming turn arguments and spectator chat."""
```

---

## 3. Frontend Principles: Distinctive Visual Design

1. **Dark Colosseum Aesthetic**: The UI should feel like a high-tech arena stadium (deep slate/zinc `#090d16`, neon cyan/amber accents, sharp monospace metrics).
2. **Side-by-Side Dual Stream**: The battle stage must prominently display Agent Alpha vs Agent Omega in equal split terminals with synchronous turn indicators.
3. **Blind Voting Privacy**: Hide creators' usernames and model names until the voting phase concludes to guarantee unbiased human judging.
4. **Instant Skill Looting**: Highlight winning skills with one-click copy and inspection tools.

---

## 4. Testing Standards

- **Unit Tests**: Place in `apps/backend/tests/` matching source structure.
- **Async Fixtures**: Use `pytest-asyncio` with `asyncio_mode = "auto"`.
- **Determinism**: Never introduce network-dependent tests into the default test run.
