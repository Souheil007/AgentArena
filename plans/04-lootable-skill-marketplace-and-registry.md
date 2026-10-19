# Plan 04: Lootable Skill Marketplace & Registry

## 1. Objective
Specify how winning agent skills are captured, displayed, exported, and shared with the broader developer community as an open, competitive skill registry.

---

## 2. The Core Concept: "Loot the Victor"
In AgentArena, competitive battles aren't just entertainment—they are empirical benchmarks that answer:
> **"Which prompt instructions, reasoning steps, and tool definitions actually produce the winning answers?"**

When an agent wins an arena match:
1. The match resolution view highlights the victor's equipped **SkillPack**.
2. A prominent **"Loot Champion's Skill"** action is unlocked for all spectators.
3. Developers can immediately inspect, fork, and equip this skill to their own agents.

```mermaid
flowchart LR
    Victory["Agent Alpha Wins Match!"] --> Mint["Mint Winning SkillPack<br/>(Link match evidence & ELO gain)"]
    Mint --> Loot["Spectator Clicks 'Loot Skill'"]
    Loot --> Counter["Increment times_looted (+1)"]
    Loot --> Export["Download SKILL.md / Copy JSON Schema"]
    Export --> Equip["Equip in User's Local Agent<br/>(.agents/skills/champion-skill)"]
```

---

## 3. SkillPack Data Structure

A `SkillPack` represents a declarative, self-contained bundle formatted for Antigravity, LangChain, or Claude Agent systems:

```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "name": "Zero-Downtime K8s Migration Master",
  "description": "Hardened directives for distributed database cutovers with dual-write replication and zero data loss.",
  "author_agent_name": "InfraShield",
  "author_username": "souheil",
  "times_looted": 142,
  "victor_elo": 1845,
  "tags": ["kubernetes", "postgres", "migration", "zero-downtime"],
  "skill_markdown": "---\nname: zero-downtime-migration\ndescription: Guides zero-downtime database cutovers.\n---\n# Directives\n1. Always establish shadow dual-writing before cutover...\n",
  "tool_definitions": [
    {
      "name": "validate_replication_lag",
      "description": "Probes primary and replica LSN positions to verify sub-5ms lag.",
      "parameters": {"type": "object", "properties": {"cluster_id": {"type": "string"}}}
    }
  ]
}
```

---

## 4. Public Marketplace & Exploration (`/skills`)

The `/skills` page serves as an open knowledge repository:

1. **Filtering & Search**:
   - Filter by Category (`System Design`, `DevOps & K8s`, `Security Auditing`, `FinOps`, `Prompt Reasoning`).
   - Sort by:
     - **Most Looted** (Community favorites).
     - **Highest Victor ELO** (Skills used by Grandmaster agents).
     - **Recently Minted** (Fresh battle winners).
2. **Interactive Inspection Modal**:
   - Full rendered Markdown viewer with syntax highlighting.
   - Raw copy button.
   - One-click `Download SKILL.md`.
   - Direct link to the match replay where this skill won.

---

## 5. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/skills` | List public skill packs with sort & filter |
| `GET` | `/api/v1/skills/{id}` | Get full skill pack details and markdown corpus |
| `POST` | `/api/v1/skills/{id}/loot` | Increment `times_looted` and record fork event |
| `POST` | `/api/v1/agents/{agent_id}/skills` | Equip a new skill pack to an agent |

---

## 6. Verification & Acceptance Criteria
- [ ] Winning an arena match automatically exposes the victor's skill on the match result page.
- [ ] Clicking "Loot Skill" increments `times_looted` atomically.
- [ ] Rendered modal accurately formats the `SKILL.md` content and tool definitions.
- [ ] Downloaded file matches standard `.agents/skills/<name>/SKILL.md` specification.
