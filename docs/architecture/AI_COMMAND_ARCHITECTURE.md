# Garden AI — Command Architecture

## Overview

This document describes the shared command architecture that enables natural-language interaction with the Soil & Supper garden domain.

The AI layer interprets user input and produces structured `GardenCommand` objects. These commands are validated, executed, and recorded through a deterministic domain pipeline.

```
User input (text / voice / image / document)
        ↓
    AI interpretation
        ↓
    GardenCommand(s)
        ↓
    CommandValidator
        ↓
    CommandExecutor
        ↓
    GardenService / domain mutation
        ↓
    GardenRepository / PlantRepository
        ↓
    Database (authoritative)
        ↓
    Explicit confirmation
```

---

## 1. Input Interfaces

Future input modalities:

| Interface | Status | Notes |
|-----------|--------|-------|
| Text | Planned | Natural language commands |
| Voice | Planned | Speech-to-text → text pipeline |
| Image / plant recognition | Planned | Camera → classification → command |
| Document / garden-plan import | Planned | PDF/image → structured data |

**None of these interfaces are implemented in this phase.**

All input interfaces must converge on the same `GardenCommand` model. They do not bypass validation or execute directly against persistence.

---

## 2. AI Interpretation

The AI interpretation layer is responsible for converting raw user input into structured `GardenCommand` objects.

Rules:

- AI must never write directly to Room, SwiftData, Core Data, SQLDelight, or any platform persistence layer.
- AI must never execute arbitrary SQL.
- AI must not invent dates, crops, or garden spaces.
- AI must not infer that a timeline projection is an actual event.

The AI produces commands. The domain owns truth.

---

## 3. GardenCommand

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/command/GardenCommand.kt`

`GardenCommand` is a sealed interface representing all valid garden mutations.

### Supported Commands

| Command | Description |
|---------|-------------|
| `AddGrowingSpace` | Create a new bed, pot, or row |
| `UpdateGrowingSpace` | Rename or resize a space |
| `RemoveGrowingSpace` | Delete an empty space |
| `PlantCrop` | Start a new occupancy |
| `HarvestCrop` | Record a harvest from an active occupancy |
| `EndCrop` | Explicitly end an active occupancy |
| `RecordObservation` | Add a journal note |
| `AddSeed` | Add a seed to the shelf |
| `AddDesire` | Add a crop desire |
| `FulfillDesire` | Mark a desire as fulfilled |
| `CancelDesire` | Cancel a desire |
| `RecordPlant` | Record a generic plant |
| `UpdatePlant` | Update a recorded plant |
| `RemovePlant` | Delete a recorded plant |

### Design Rules

- Commands contain structured, typed data.
- Commands do not contain raw natural-language strings for mutation.
- Commands do not contain platform-specific types.
- Commands are immutable data classes.

---

## 4. CommandValidator

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/command/CommandValidator.kt`

`CommandValidator` is a deterministic, AI-free validation layer.

### Validation Rules

- Referenced growing space exists
- Referenced crop/seed/desire/plant exists where required
- Required fields are present (non-blank names, positive quantities, etc.)
- Dates are valid (harvest/release after planting, end after start)
- Operation is legal for current state (no double-planting, no harvesting inactive spaces, etc.)
- Command does not violate existing domain rules

### Result

Returns `CommandResult.Success` or a structured failure:

| Result | Meaning |
|--------|---------|
| `Success` | Command passed validation |
| `ValidationError` | Required field missing or malformed |
| `NotFound` | Referenced entity does not exist |
| `Conflict` | Operation illegal in current state |
| `NeedsClarification` | Ambiguous command (reserved for future AI use) |
| `NotSupported` | Command type not recognized |

---

## 5. CommandExecutor

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/command/DefaultCommandExecutor.kt`

`CommandExecutor` orchestrates validation → execution → history recording.

### Flow

1. Load current state from repository flows
2. Validate command via `CommandValidator`
3. If invalid, return validation result immediately
4. If valid, execute mutation via `GardenService` + `GardenRepository`
5. If successful, record in `CommandHistory`

### Key Constraints

- `CommandExecutor` never manipulates Room, SwiftData, Core Data, SQLDelight, or platform persistence directly.
- All mutations flow through `GardenService` and `GardenRepository`.
- `CommandExecutor` is platform-independent and lives in `commonMain`.

---

## 6. CommandHistory / Undo

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/command/CommandHistory.kt`

`CommandHistory` records successful mutations and supports `undoLast`.

### Design

- `InMemoryCommandHistory` is the default implementation.
- Each entry records the command and timestamp.
- `undoLast` reverses the most recent successful mutation.
- Undo is deterministic and domain-owned; the AI simply invokes it.
- If a command cannot be safely reversed, `undoLast` returns `NotSupported`.

### Limitations

- In-memory history is lost when the app closes.
- Future phases may add persistent history with cross-platform storage.
- Undo accuracy depends on repository state at undo time.

---

## 7. Batch Operations

Multiple commands can be executed sequentially:

```kotlin
val commands = listOf(
    GardenCommand.EndCrop(occupancyId = 1, endDate = ...),
    GardenCommand.RemoveGrowingSpace(spaceId = 2),
    GardenCommand.PlantCrop(cropName = "Carrot", growingSpaceId = 2, startDate = ...)
)

val results = commands.map { cmd -> executor.execute(cmd, repository) }
```

### Result Semantics

| Outcome | Meaning |
|---------|---------|
| All succeeded | Every command in the batch succeeded |
| Partially failed | Some commands succeeded, some failed |
| Rejected | No commands executed (e.g., first command failed validation) |
| Needs clarification | Batch could not proceed without user input |

**Note:** True atomic transactions across platforms are not implemented in this phase. If a batch partially fails, the garden may be in a partially mutated state. Future work should add transactional boundaries at the repository layer.

---

## 8. CommandResult

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/command/CommandResult.kt`

`CommandResult` is a sealed interface communicating structured outcomes.

### Result Types

| Type | Fields | Meaning |
|------|--------|---------|
| `Success` | `command`, `message` | Mutation applied |
| `ValidationError` | `command`, `reason`, `message` | Input rejected |
| `NotFound` | `command`, `entityType`, `entityId`, `message` | Referenced entity missing |
| `Conflict` | `command`, `reason`, `message` | State conflict |
| `NeedsClarification` | `command`, `question`, `message` | Ambiguous intent |
| `NotSupported` | `command`, `message` | Unknown command |

### Usage

Results contain enough structured information for a future conversation layer to explain exactly what happened. The domain layer does not generate conversational prose.

---

## 9. Read Queries

Location: `shared/src/commonMain/kotlin/com/soilandsupper/ai/query/GardenQuery.kt`

`GardenQuery` provides safe, structured read operations for the AI interface.

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
- Queries do not expose internal implementation details (no Room entities, no SQL).
- Projections are returned as data; they are not silently converted into mutations.

---

## 10. Authority Boundaries

```
+-------------------+     interprets      +----------------+
|   AI Interface    | ------------------> | GardenCommand  |
+-------------------+                     +----------------+
                                                |
                                                | validates
                                                v
                                         +----------------+
                                         | CommandValidator|
                                         +----------------+
                                                |
                                                | executes
                                                v
                                         +----------------+
                                         | CommandExecutor |
                                         +----------------+
                                                |
                                                | mutates via
                                                v
                                         +----------------+
                                         | GardenService   |
                                         +----------------+
                                                |
                                                | persists via
                                                v
                                         +----------------+
                                         | GardenRepository|
                                         +----------------+
                                                |
                                                | writes to
                                                v
                                         +----------------+
                                         |    Database     |
                                         +----------------+
```

### AI Must Not

- Write directly to Room / SwiftData / Core Data / SQLDelight
- Execute arbitrary SQL
- Modify domain state without validation
- Infer projections are actual events
- Silently invent dates, crops, or spaces

### Database Is Authoritative

The database is the source of truth. All reads and writes flow through the repository boundary. The AI never bypasses this boundary.

---

## 11. CMP Boundary

| Layer | Location | Platform Code Allowed |
|-------|----------|----------------------|
| Domain models | `shared/src/commonMain` | No |
| GardenService | `shared/src/commonMain` | No |
| GardenRepository interface | `shared/src/commonMain` | No |
| Command model | `shared/src/commonMain` | No |
| Validator | `shared/src/commonMain` | No |
| Executor | `shared/src/commonMain` | No |
| Query | `shared/src/commonMain` | No |
| Tests | `shared/src/commonTest` | No |

Platform-specific implementations (Room, SwiftData, etc.) live in platform source sets and implement the shared interfaces.

---

## 12. Future Integration Points

| Feature | Integration Point |
|---------|------------------|
| Text chat UI | `GardenCommand` + `CommandResult` |
| Voice commands | STT → text → `GardenCommand` |
| Plant recognition | Image classification → `GardenCommand.PlantCrop` or `RecordObservation` |
| Document import | PDF parser → structured `GardenCommand` batch |
| Undo button | `CommandHistory.undoLast()` |
| Conversation history | Extend `HistoryEntry` with AI context |
| Confidence scoring | Future field on `CommandResult` |

---

## 13. Testing

All command architecture code is tested in `shared/src/commonTest`:

- Valid command executes successfully
- Invalid command is rejected
- Nonexistent entities are rejected
- Successful mutations are recorded in history
- Failed commands do not create history entries
- Undo restores previous state (best-effort)
- Batch operations produce structured results
- Read queries return current authoritative state
- Projections are not converted into mutations
- Commands remain deterministic

See `GardenCommandArchitectureTest.kt` for the full test suite.

---

## 14. Limitations

1. **No persistent command history** — `InMemoryCommandHistory` is lost on app close.
2. **No atomic transactions** — Batch operations are sequential; partial failure leaves partial state.
3. **No AI integration** — This phase establishes the domain foundation only.
4. **Undo is best-effort** — Some reversals depend on repository state at undo time.
5. **No `NeedsClarification` flow** — The result type exists but no AI layer populates it yet.
