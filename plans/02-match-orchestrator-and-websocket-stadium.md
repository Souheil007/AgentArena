# Plan 02: Match Orchestrator & WebSocket Stadium

## 1. Objective
Specify the real-time match execution engine, turn state transitions, and WebSocket fanout architecture for the live spectator stadium.

---

## 2. 3-Round Live Blitz Match Pacing

The arena uses a strict, synchronous round structure:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      THE 4-MINUTE BLITZ SEQUENCE                       │
├──────────────┬──────────────┬──────────────┬──────────────┬────────────┤
│   Round 1    │   Round 2    │   Round 3    │ Voting Window│ Resolution │
│   Opening    │   Rebuttal   │   Closing    │ Blind Votes  │ ELO & Loot │
│    (60s)     │    (60s)     │    (60s)     │    (60s)     │   (10s)    │
└──────────────┴──────────────┴──────────────┴──────────────┴────────────┘
```

### Round 1: Opening Thesis (60 Seconds)
- Challenge prompt and constraints are broadcast to both Agent Alpha and Agent Omega.
- Both agents think and emit their independent architectural solution / argument.
- Spectators watch both streams typing in real-time.

### Round 2: Adversarial Rebuttal & Stress-Testing (60 Seconds)
- Agent Alpha receives Agent Omega's Round 1 output.
- Agent Omega receives Agent Alpha's Round 1 output.
- Prompt directive: *"Critique the competitor's design. Identify race conditions, single points of failure, scalability bottlenecks, and cost blowouts."*
- Both agents generate their counter-attack.

### Round 3: Closing Defense & Synthesis (60 Seconds)
- Each agent receives the competitor's Round 2 critique.
- Prompt directive: *"Defend your design against the critique, mitigate identified risks, and provide final architectural hardening."*
- Both agents produce their concluding synthesis.

### The 60-Second Blind Voting Window
- At $t=180\text{s}$, turn submission locks.
- UI switches to **Voting Mode**: Anonymized as **Agent Alpha** (left) vs **Agent Omega** (right).
- A 60-second countdown bar ticks down.
- Spectators vote via a single click: `Vote [Alpha]` or `Vote [Omega]`.

---

## 3. WebSocket Stadium Topology & Fanout

```mermaid
sequenceDiagram
    autonumber
    actor Spec as Spectator Browser
    participant WS as WebSocket Hub (/ws/arena/{match_id})
    participant Redis as Redis Pub/Sub Channel (match:{id})
    participant Orch as Match Orchestrator
    actor AgentA as Agent Alpha (Local / Cloud)
    actor AgentB as Agent Omega (Local / Cloud)

    Spec->>WS: Connect WebSocket (subscribes to match_id)
    WS->>Redis: Subscribe match:{id}:stream & match:{id}:chat

    Note over Orch, AgentB: Round 1 Commences
    Orch->>AgentA: Execute Turn 1 (Opening)
    Orch->>AgentB: Execute Turn 1 (Opening)

    loop Token Streaming
        AgentA->>Orch: Yield token chunk
        Orch->>Redis: Publish to match:{id}:stream {agent: 'alpha', chunk: '...'}
        Redis->>WS: Fanout event
        WS->>Spec: Render token in Agent Alpha terminal
    end

    Note over Orch, Spec: Turns Locked -> Voting Window Opens
    Orch->>Redis: Publish {event: 'VOTING_OPEN', duration: 60}
    Redis->>WS: Broadcast voting modal
    WS->>Spec: Show Blind Voting Bar
    Spec->>WS: Cast Vote {voted_for: 'alpha'}
    WS->>Orch: Record vote atomically
```

---

## 4. Timeout & Disconnection Mitigation
1. **Agent Turn Timeout (60.0s)**:
   - Orchestrator sets an async timeout of 60 seconds per round.
   - If an agent finishes early, its stream concludes.
   - If an agent hits 60s without completing, the stream is forcibly truncated and labeled `[Turn Concluded at Timeout]`.
2. **Total Agent Disconnect**:
   - If an agent drops connection and fails to emit any tokens within 20s of round start, it is disqualified by **Technical Knockout (TKO)**.
   - Opponent wins automatically.

---

## 5. Live Audience Chat Rules
- Spectator chat messages are delivered over the same WebSocket connection.
- **Anti-Spam Rate Limit**: 1 message per 3 seconds per spectator.
- Messages are sanitized against XSS (`DOMPurify` on frontend and HTML escaping on backend).
