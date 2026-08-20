# Garden AI — Orchestration Architecture

## Overview

This document describes the offline-first AI orchestration boundary added in Phase 37. The orchestrator translates natural-language input into validated garden commands, executes them through the existing domain pipeline, and supports confirmation, ambiguity handling, undo, and read-only queries.

The AI layer never touches persistence directly. All mutations flow through `CommandValidator` → `CommandExecutor` → `CommandHistory`. Read-only queries use `GardenQuery`.

```
User input (text / voice / image / document)
        ↓
    LocalAIProvider.interpret()
        ↓
    AIInterpretation
        ↓
    AIOrchestrator.process()
        ↓
    AIResponse
```

---

## 1. LocalAIProvider Boundary

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/orchestration/LocalAIProvider.kt`

`LocalAIProvider` is a platform-agnostic interface. It receives an `AIRequest` (input + optional garden/conversation context) and returns an `AIInterpretation`.

```kotlin
interface LocalAIProvider {
    suspend fun interpret(request: AIRequest): AIInterpretation
}
```

### Rules

- The provider must not import `android.*`, network clients, or cloud SDKs.
- The provider must not mutate persistence.
- The provider produces structured interpretations, not raw SQL or repository calls.
- `FakeAIProvider` is the deterministic test double. No real LLM is introduced.

---

## 2. AIInput

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/orchestration/AIInput.kt`

`AIInput` is a sealed interface representing all supported input modalities.

| Type | Fields | Status |
|------|--------|--------|
| `Text` | `rawContent` | Supported |
| `VoiceTranscript` | `rawContent`, `confidence` | Supported (representation only) |
| `ImageReference` | `rawContent`, `imageId`, `description` | Supported (representation only) |
| `DocumentText` | `rawContent`, `documentType` | Supported (representation only) |

None of these interfaces implement platform hardware. Voice, image, and document inputs are represented as data so future local models or platform pipelines can populate them without changing the orchestration boundary.

---

## 3. AIRequest and Context

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/orchestration/AIRequest.kt`

`AIRequest` bundles user input with optional context:

- `GardenContext` — current spaces, occupancies, seeds, desires, plants.
- `ConversationContext` — session ID, turn count, last interpretation.

If `gardenContext` is omitted, the orchestrator builds it via `GardenQuery` before calling the provider. This ensures the provider always sees authoritative domain state without reaching into persistence itself.

---

## 4. AIInterpretation

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/orchestration/AIInterpretation.kt`

`AIInterpretation` is a sealed interface representing the provider's understanding of the request.

| Type | Meaning |
|------|---------|
| `InformationalAnswer` | Read-only answer (no mutation) |
| `CommandProposals` | One or more proposed `GardenCommand` objects |
| `ClarificationRequest` | Ambiguous intent; needs user clarification |
| `Uncertainty` | Model could not understand the request |
| `RecognitionResult` | Image / plant recognition outcome |

---

## 5. AICommandProposal

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/orchestration/AICommandProposal.kt`

`AICommandProposal` wraps a single `GardenCommand` with explanation, confidence, and ambiguities.

```kotlin
data class AICommandProposal(
    val command: GardenCommand,
    val explanation: String,
    val confidence: Float? = null,
    val ambiguities: List<String> = emptyList()
)
```

---

## 6. AIOrchestrator

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/orchestration/AIOrchestrator.kt`

`AIOrchestrator` is the central coordinator. It receives an `AIRequest`, delegates interpretation to `LocalAIProvider`, and translates the result into an `AIResponse`.

### Flow

1. Detect undo intent.
2. Build or reuse `GardenContext`.
3. Call `provider.interpret()`.
4. Branch on interpretation type:
   - `InformationalAnswer` → return message.
   - `RecognitionResult` → return recognition message.
   - `Uncertainty` → return error message.
   - `ClarificationRequest` → return question + pending proposals.
   - `CommandProposals` → validate and execute.

### Command Proposal Handling

For each proposal:

1. Validate via `CommandValidator`.
2. If validation fails, add to `failures` and skip execution.
3. If validation succeeds, execute via `CommandExecutor`.
4. Add execution result to `executedCommands`.
5. If execution fails, add to `failures`.

### Confirmation States

| State | Condition | User Action |
|-------|-----------|-------------|
| `PROPOSED` | Low confidence (`< 0.5`) or ambiguity | Confirm or correct |
| `CONFIRMED` | User confirmed | Execute |
| `EXECUTED` | Commands ran | None |
| `REJECTED` | User rejected | None |
| `NEEDS_CLARIFICATION` | Ambiguous request | Provide missing detail |

---

## 7. AIResponse

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/orchestration/AIResponse.kt`

`AIResponse` is the user-facing result.

| Property | Type | Meaning |
|----------|------|---------|
| `message` | `String` | Human-readable summary |
| `executedCommands` | `List<CommandResult>` | All attempted commands (validation + execution) |
| `pendingConfirmation` | `List<AICommandProposal>` | Proposals awaiting user confirmation |
| `errors` | `List<String>` | Failure messages |
| `clarificationQuestion` | `String?` | Question when intent is ambiguous |

Derived properties:

- `isSuccess` — `executedCommands.isNotEmpty() && errors.isEmpty()`
- `needsConfirmation` — `pendingConfirmation.isNotEmpty() && executedCommands.isEmpty()`
- `needsClarification` — `clarificationQuestion != null`
- `hasError` — `errors.isNotEmpty()`

---

## 8. GardenQuery

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/query/GardenQuery.kt`

`GardenQuery` provides safe, structured read operations for the AI layer.

### Available Queries

| Query | Description |
|-------|-------------|
| `getAllSpaces()` | All growing spaces |
| `getSpaceById(id)` | Single space by ID |
| `getActiveOccupancies()` | Currently active plantings |
| `getOccupanciesForSpace(spaceId)` | History for a space |
| `getUpcomingOpenings(beforeDate)` | Spaces opening before a date |
| `getAllSeeds()` | Seed shelf |
| `getAllDesires()` | Crop desires |
| `getAllPlants()` | Recorded plants |
| `getAllHarvests()` | All harvest records |
| `getHarvestsForPlant(plantId)` | Harvests for one plant |

### Design Rules

- Read queries do not mutate state.
- Queries return structured domain models, not raw database rows.
- Queries do not expose internal implementation details.
- Projections are returned as data; they are not silently converted into mutations.

---

## 9. Interpretation → Proposal → Validation → Execution

```
AIInput
  ↓
LocalAIProvider.interpret()
  ↓
AIInterpretation
  ↓
AIOrchestrator.process()
  ↓
AICommandProposal(s)
  ↓
CommandValidator.validate()
  ↓
CommandResult.Success | ValidationError | NotFound | Conflict
  ↓
CommandExecutor.execute()
  ↓
CommandResult + CommandHistory entry
  ↓
AIResponse
```

### Key Invariants

1. AI cannot directly mutate persistence.
2. Mutations go through `CommandValidator`.
3. Valid mutations go through `CommandExecutor`.
4. `CommandHistory` records mutations.
5. Undo uses domain-owned history.
6. Read-only questions use `GardenQuery`.
7. Ambiguous requests do not silently execute.
8. Low-confidence / uncertain mutations do not silently execute.
9. Multi-command requests are supported.
10. Voice / image / document inputs are represented without implementing platform hardware.

---

## 10. Ambiguity Handling

When a proposal carries `ambiguities`, the orchestrator returns a `ClarificationRequest` response. No commands are executed. The pending proposals are attached to the response so the caller can resume execution once the user provides missing detail.

---

## 11. Undo

`AIOrchestrator.handleUndo()` delegates to `CommandHistory.undoLast(repository)`. The history implementation reverses the most recent successful mutation using the current repository state. If no commands are recorded, the orchestrator returns an error.

Undo is deterministic and domain-owned. The AI simply invokes it.

---

## 12. FakeAIProvider

Location: `shared/src/commonTest/kotlin/com/soilandsupper/ai/orchestration/FakeAIProvider.kt`

`FakeAIProvider` is a deterministic test double. It returns pre-registered `AIInterpretation` values for exact input matches, falling back to a default interpretation. No randomness, no network, no platform APIs.

---

## 13. Future Local Model Integration

`LocalAIProvider` is designed to be implemented by a future offline model (e.g., a quantized LLM running on-device). The interface is intentionally minimal:

- One suspend function.
- No platform dependencies.
- No threading or callback concerns.

A future implementation can load a local model, run inference, and map the output to `AIInterpretation` subtypes without changing the orchestrator or domain layers.

---

## 14. Offline-First Constraint

The entire orchestration layer lives in `commonMain`. No network clients, no cloud SDKs, no API keys, and no platform-specific LLM runtimes are introduced. The app can function fully offline using `FakeAIProvider` or a future local-model implementation.

---

## 15. Limitations

1. **No persistent command history** — `InMemoryCommandHistory` is lost when the app closes.
2. **No atomic transactions** — Batch operations are sequential; partial failure leaves partial state.
3. **No real AI** — This phase establishes the boundary and tests only.
4. **Undo is best-effort** — Some reversals depend on repository state at undo time.
