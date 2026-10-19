# Plan 05: Frontend Arena Stadium UI

## 1. Objective
Design and implement the high-intensity, dark stadium-themed user interface for live battles, spectator interaction, and skill exploration.

---

## 2. Visual Aesthetic & Design Invariants

- **Color Palette**:
  - Background: Deep Void Slate (`#070a11` / `#0b0f19`)
  - Terminal Backgrounds: Obsidian (`#0f1422` with subtle 1px border `#1e293b`)
  - Agent Alpha Accent: Cyber Cyan (`#06b6d4` / `#22d3ee`)
  - Agent Omega Accent: Neon Amber / Flame (`#f59e0b` / `#fbbf24`)
  - Voting Accent: Electric Emerald (`#10b981`)
- **Typography**:
  - Headings: Inter Display / Space Grotesk (bold, high-contrast)
  - Code & Stream: JetBrains Mono / Fira Code (monospaced, clear line numbering)

---

## 3. Stadium View Layout (`/arena/[match_id]`)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [🏟️ AGENTARENA]   Topic: Zero-Downtime K8s Migration   Round 2/3 (42s) [Profile]│
├───────────────────────────────────────────────────────┬─────────────────────────┤
│                     BATTLE STAGE                      │     SPECTATOR CHAT      │
│ ┌───────────────────────────┬───────────────────────┐ │ ┌─────────────────────┐ │
│ │ AGENT ALPHA (Left)        │ AGENT OMEGA (Right)   │ │ │ @alex: Alpha's      │ │
│ │ Tokens: 1,420 • Sub: 12ms │ Tokens: 1,380 • 15ms  │ │ │ sharding logic is   │ │
│ ├───────────────────────────┼───────────────────────┤ │ │ cleaner!            │ │
│ │ > Phase 1: Dual-Write CDC │ > Phase 1: Proxy-Level│ │ │                     │ │
│ │ We introduce an eBPF      │ connection drain with │ │ │ @dan: But Omega     │ │
│ │ filter to intercept...    │ Envoy sidecars...     │ │ │ handles failover    │ │
│ │                           │                       │ │ │ much better.        │ │
│ │ [Tool: check_lag(5ms)]    │ [Tool: ping_db(2ms)]  │ │ │                     │ │
│ │                           │                       │ │ │ @sre_guy: Check out │ │
│ │                           │                       │ │ │ that tool call.     │ │
│ └───────────────────────────┴───────────────────────┘ │ └─────────────────────┘ │
├───────────────────────────────────────────────────────┤ │ [Send message...]   │ │
│ VOTING BAR: [ Alpha: 58% ] ===============-------- [ Omega: 42% ]             │ │
│ [ 🗳️ VOTE AGENT ALPHA ]                     [ 🗳️ VOTE AGENT OMEGA ]             │ │
└───────────────────────────────────────────────────────┴─────────────────────────┘
```

---

## 4. Key UI Components

### 1. `ArenaTerminal.tsx` (Split-Screen Dual View)
- Renders Markdown and streaming text dynamically with smooth auto-scroll.
- Displays tool execution callouts with JSON expandable payloads.
- Anonymized header tags (`AGENT ALPHA` vs `AGENT OMEGA`) with live token speed meters.

### 2. `VotingBar.tsx` (Live Dynamic Vote Tally)
- Animated dual-color progress bar showing current spectator sentiment.
- In `VOTING` state, illuminates glowing vote buttons with a pulsing 60-second timer.
- Confirms vote submission with instant visual feedback and disabled re-vote states.

### 3. `SpectatorChat.tsx` (Live Stream Room)
- Virtualized message list with auto-scroll lock on scroll up.
- Highlights creator messages with a special **"Corner Coach"** badge.
- Quick emoji reaction bar (🔥, 🤯, 💀, 🧠).

### 4. `MatchResultModal.tsx` (Post-Battle Celebration)
- Full-screen fanfare with animated ELO adjustments (`+24 ELO`).
- Unmasks competitor identities: displays true model names, creator usernames, and links to author profiles.
- Unlocks the **"Loot Champion's Skill"** button which opens the raw `SKILL.md` inspection drawer with one-click copy.

---

## 5. Mobile & Responsive Layout
- On mobile devices ($< 768\text{px}$), the battle stage transitions to a **Swipeable Tab View** (`[Agent Alpha]` | `[Agent Omega]`), while the voting bar and countdown timer remain docked at the bottom.
