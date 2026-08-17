# Garden Planning & Seed Shelf — Architecture Decision Document

## 1. Domain Concepts

### Garden
- **Real-world concept**: The user's garden as a whole (e.g., "Backyard Garden", "Community Plot").
- **Persistent**: Yes.
- **Created**: When user creates a garden.
- **Changes**: Renamed, location updated, frost dates updated.
- **Deleted**: User deletes the garden (cascades to growing spaces, desires).
- **References**: GrowingSpaces, Desires, Plants (existing).

### GrowingSpace
- **Real-world concept**: Any named area where plants grow: raised bed, in-ground row, pot, grow bag, container, greenhouse bench.
- **Persistent**: Yes.
- **Created**: User adds a growing space.
- **Changes**: Renamed, notes updated.
- **Deleted**: User removes the space (cascades to Occupancies).
- **References**: Occupancies, PlannedPlantings.

### Plant
- **Real-world concept**: An actual living crop instance that the user is growing. "The tomatoes I planted on May 15."
- **Persistent**: Yes.
- **Created**: When the user plants something (or adds a plant record).
- **Changes**: Name, variety, notes updated. Photos, journals, harvests added over time.
- **Deleted**: User deletes the plant (cascades to photos, journals, harvests).
- **References**: Garden (existing), PlantPhotos, JournalEntries, Harvests, Occupancy (optional).

### Occupancy
- **Real-world concept**: The fact that a specific GrowingSpace was occupied by a specific crop during a specific time period. "Bed 3 held tomatoes from May 15 to Sep 15."
- **Persistent**: Yes.
- **Created**: When a planting occurs (actual) or when a plan is committed to a space (planned).
- **Changes**: End date set when crop finishes. Status updated.
- **Deleted**: Rarely. Historical occupancies should be preserved. Soft-delete via status=cancelled if needed.
- **References**: GrowingSpace, Plant (optional, for actual/historical plantings).

### PlannedPlanting
- **Real-world concept**: A tentative intention to plant. "I'm thinking of planting carrots in Bed 3 around Aug 20."
- **Persistent**: Yes.
- **Created**: User creates a plan, or the planning engine proposes one.
- **Changes**: Date, space, crop, variety adjusted before commitment.
- **Deleted/archived**: Cancelled or superseded. Not deleted — status tracks lifecycle.
- **References**: Garden, GrowingSpace (optional), Seed (optional).

### Desire
- **Real-world concept**: A wish to grow something, without commitment to space or time. "I want carrots."
- **Persistent**: Yes.
- **Created**: User expresses intent via voice, text, or UI.
- **Changes**: Fulfilled, cancelled, expired.
- **Deleted**: Not deleted. Marked fulfilled, cancelled, or expired.
- **References**: Garden.

### Seed
- **Real-world concept**: A seed packet or seed lot the user owns or wants. "Nantes carrots, 2 packets, 2025."
- **Persistent**: Yes.
- **Created**: User adds a seed to the shelf.
- **Changes**: Quantity, notes, state updated.
- **Deleted**: User removes it from the shelf (rare; use state=removed or just delete).
- **References**: Garden, PlannedPlanting (optional).

### Harvest
- **Real-world concept**: A picking of produce from a Plant.
- **Persistent**: Yes (existing model, unchanged).
- **Created**: When user records a harvest.
- **Changes**: Quantity, notes, date corrected.
- **Deleted**: User deletes the record.
- **References**: Plant (existing). Future: may also reference Occupancy.

### How they differ: Plant vs. Actual Planting vs. Occupancy

| Aspect | Plant | Actual Planting | Occupancy |
|--------|-------|-----------------|-----------|
| What it is | A biological instance | An event (planting happened) | A spatial-temporal fact |
| Created when | User plants something | Same moment as Plant creation | Same moment, or when a plan is committed |
| Scope | One crop instance, with its own photos, journals, harvests | The act of putting it in the ground | The period a GrowingSpace is occupied |
| Identity | "This is the San Marzano tomato I grew" | "I planted it on Aug 22" | "Bed 3 was occupied by San Marzano tomatoes from May 15 to Sep 15" |
| Can exist without GrowingSpace | Yes (potted plant, not in a formal bed) | Yes (planted in a pot, not a GrowingSpace) | No (by definition, a GrowingSpace is required) |
| Can exist without Plant | N/A | N/A | Yes (planned occupancy, or historical record where Plant was deleted) |
| One-to-one? | One Plant = one biological instance | One Actual Planting = one Plant | One Occupancy = one GrowingSpace × one time window |

**Conclusion**: Plant remains the biological/historical record. Occupancy is the spatial-temporal record. Actual Planting is not a separate model — it is the moment an Occupancy with status=active is created and linked to a Plant.

---

## 2. Should Occupancy Be Persistent?

**Decision**: Yes. Occupancy must be a persistent model.

**Reason**:
- Space availability is temporal. The system must know not only what is growing now, but when a space will become available, what was there historically, and whether a future plan conflicts with an actual commitment.
- Deriving occupancy from Plants alone loses critical information: empty gaps, early removals, future plans, and interplanting windows.
- Conflating spatial-temporal data with biological data (photos, journals, harvests) inside Plant makes both models harder to maintain and query.

**How it handles edge cases**:

- **Current crop**: Active Occupancy with startDate ≤ today and (endDate == nil or endDate ≥ today).
- **Future planned crop**: Occupancy with status=planned and startDate > today.
- **Empty space**: No active Occupancy for the GrowingSpace.
- **Crop removed early**: Occupancy endDate set to actual removal date. Status=completed. Plant record preserved with original plantingDate.
- **Crop remaining longer than expected**: Occupancy endDate updated (or left nil) when user marks it done. Expected dates are estimates; actual dates are facts.
- **Multiple plantings in same space**: Multiple Occupancies in the same GrowingSpace, sequential or overlapping (if interplanting).
- **Overlapping/interplanted crops**: Multiple active Occupancies in the same GrowingSpace with overlapping date ranges. The planning engine treats this as a user-confirmed interplant.
- **Plan that is cancelled**: Occupancy with status=cancelled (or PlannedPlanting with status=cancelled, never promoted to Occupancy).

---

## 3. Complete Lifecycle

### Example 1: User wants carrots but owns no seeds.
1. **Desire**: crop=Carrots, variety=nil, isFulfilled=false, isExpired=false.
2. **Seed**: none.
3. **PlannedPlanting**: none.
4. **Occupancy**: none.
5. **Plant**: none.
6. Planning engine can still recommend carrots. Seed Shelf shows "You want carrots."

### Example 2: User wants carrots and owns Nantes seeds.
1. **Desire**: crop=Carrots, variety=Nantes, isFulfilled=false.
2. **Seed**: crop=Carrots, variety=Nantes, state=OWN, quantity="1 packet".
3. **PlannedPlanting**: none.
4. **Occupancy**: none.
5. **Plant**: none.
6. Planning recommendations note: "You have Nantes seeds."

### Example 3: User plans carrots for Bed 3 but never plants them.
1. **Desire**: crop=Carrots (fulfilled when plan created, or remains until cancelled).
2. **Seed**: OWN.
3. **PlannedPlanting**: crop=Carrots, variety=Nantes, space=Bed3, plannedDate=Aug20, status=planned.
4. **Occupancy**: none (plan never materialized).
5. **Plant**: none.
6. Later: user cancels plan. PlannedPlanting status=cancelled. Desire status=cancelled. Seed remains OWN. Historical record: plan existed, was cancelled, nothing was planted.

### Example 4: User plants the planned carrots two days later than planned.
1. **Desire**: crop=Carrots (fulfilled).
2. **Seed**: OWN, quantity decremented if tracking.
3. **PlannedPlanting**: crop=Carrots, variety=Nantes, space=Bed3, plannedDate=Aug20, status=planted.
4. **Occupancy**: crop=Carrots, variety=Nantes, space=Bed3, startDate=Aug22, status=active, expectedHarvest=Oct20, expectedRelease=Oct25.
5. **Plant**: crop=Carrots, variety=Nantes, plantingDate=Aug22, location=Bed3.
6. The PlannedPlanting is linked to the Occupancy. The planned date (Aug20) and actual date (Aug22) are both preserved.

### Example 5: User plants carrots without ever creating a plan.
1. **Desire**: none (or created implicitly from voice command, then fulfilled).
2. **Seed**: OWN.
3. **PlannedPlanting**: none.
4. **Occupancy**: crop=Carrots, variety=Nantes, space=Bed3, startDate=Aug22, status=active.
5. **Plant**: crop=Carrots, variety=Nantes, plantingDate=Aug22, location=Bed3.
6. The system creates an Occupancy directly. No plan was ever made, but the actual state is recorded.

### Example 6: User changes their future plan after creating it.
1. **Desire**: crop=Carrots (fulfilled).
2. **Seed**: OWN.
3. **PlannedPlanting**: crop=Carrots, variety=Nantes, space=Bed3, plannedDate=Aug20, status=planned.
4. User changes plan: "Actually, plant them in Bed 2 on Aug 25."
5. **PlannedPlanting**: updated to space=Bed2, plannedDate=Aug25. Status remains planned.
6. **Occupancy**: none yet.
7. Historical truth preserved: the original plan was changed, but no actual planting was altered.

### Example 7: User removes the crop earlier than expected.
1. **Desire**: fulfilled.
2. **Seed**: OWN.
3. **PlannedPlanting**: planted.
4. **Occupancy**: crop=Carrots, space=Bed3, startDate=Aug22, endDate=Sep10 (user pulled them early), status=completed.
5. **Plant**: preserved with original plantingDate=Aug22.
6. **Harvests**: any harvests recorded before Sep10 remain linked to Plant.
7. The space is now available as of Sep10. Planning engine can suggest a successor crop for the remaining season.

---

## 4. How Space Availability Works

### Definitions

**harvest date**: The date a specific picking occurs. Multiple harvests can occur from one Occupancy. A harvest does NOT mean the space is available.

**crop release/removal date**: The date the crop is fully removed from the GrowingSpace. This is when the space becomes actually available. For determinate crops like carrots, this is close to the final harvest. For indeterminate crops like tomatoes, this is when the plant is pulled, which may be weeks after the last harvest.

**next planting date**: The date the next Occupancy begins in that GrowingSpace. This must be ≥ crop release/removal date.

### What makes a GrowingSpace occupied, available, or expected:

- **Occupied now**: Has an active Occupancy with startDate ≤ today and endDate == nil.
- **Planned to be occupied**: Has a PlannedPlanting (or future-dated Occupancy with status=planned) with startDate > today.
- **Available now**: No active Occupancy. No future-dated planned occupancy that has already started.
- **Expected to become available**: An active Occupancy has an expectedReleaseDate in the future. The space is not available now, but the app knows when it will be.
- **Unavailable for a particular crop**: The remaining frost-free days are fewer than the crop's days to maturity, or the crop is incompatible with the previous crop (rotation), or the planting window has closed.
- **Available for interplanting**: The space has an active Occupancy, but the crop's canopy or root zone allows additional crops in the same space (e.g., radishes interplanted with tomatoes). The planning engine must know which crops support interplanting.

### Real-world event that causes space to become available:

The user explicitly indicates the crop is done. The app should NOT assume a space is available based on expected dates alone. The user must confirm:

- "Tomatoes are done" → app asks: "Mark Bed 3 as open? Expected release was Sep 15, actual release is today."
- Or: user taps "Mark as done" on the bed detail screen.

This preserves historical truth. Expected dates are estimates. Actual release dates are facts.

---

## 5. Relationship Between Existing Models and New Architecture

### Garden (existing)
- Remains as the top-level container.
- Add a `beds` relationship (one-to-many to GrowingSpace).
- Existing fields (name, location) remain. Add optional frost dates and climate zone here or in a new GardenSettings model.

### Plant (existing)
- Remains unchanged as the biological/historical record.
- Optionally linked to an Occupancy via a `currentOccupancy` or `lastOccupancy` relationship. This is a convenience link, not required for the model to function.
- Plants can exist without a GrowingSpace (pots, containers not tracked as GrowingSpaces).
- Plants can exist without an Occupancy (added before planning features exist, or informal plantings).

### PlantPhoto (existing)
- Remains linked to Plant. No change needed.
- Plant remains the anchor for photos, journals, and harvests.
- Future: photos could also be attached to Occupancy (e.g., "bed after cleanup"), but not needed initially.

### JournalEntry (existing)
- Remains linked to Plant. No change needed.
- A journal entry is about a specific plant's experience: "First flowers appeared," " aphids found," "pruned suckers."
- Future: JournalEntry could optionally link to a GrowingSpace for space-level notes ("added compost to Bed 3"), but not needed initially.

### Harvest (existing)
- Remains linked to Plant. No change needed.
- Harvests are about produce picked from a specific Plant instance.
- Future: Harvest could optionally reference an Occupancy, so the system knows which bed the harvest came from. This is useful for tracking yield per space, but not required for planning. Can be added later without breaking existing Harvests.

### PhotoStore (existing)
- Remains unchanged. Continues to manage plant photos on the filesystem.
- If bed photos are ever added, PhotoStore can be reused or extended.

### Critical rule: Do not break existing data
- All existing models remain valid as-is.
- New models (GrowingSpace, Occupancy, PlannedPlanting, Desire, Seed) are added alongside existing models.
- Existing Plants do not need a GrowingSpace or Occupancy. They remain valid standalone records.
- Migration: SwiftData can add new model types without migrating existing data.

---

## 6. Growing Space Definition

**Decision**: Use `GrowingSpace` as the domain concept, with `Bed` as the default name/type.

**Reason**:
- "Bed" is too narrow. Gardeners grow in pots, grow bags, rows, greenhouse benches, and other structures.
- `GrowingSpace` is the correct domain abstraction. It covers all physical growing locations.
- The UI can still show "Beds" as the default section title, because that is what most gardeners have. The model supports more.
- Do not introduce a type hierarchy (Bed, Pot, Row, etc.) yet. Just use `GrowingSpace` with an optional `name` and `notes`. The name conveys the type: "Bed 1", "Tomato Pot", "Greenhouse Bench A."

**Simplest model**:

```swift
@Model
final class GrowingSpace {
    var id: UUID
    var name: String
    var notes: String?
    var createdAt: Date
    var updatedAt: Date
    
    @Relationship(deleteRule: .cascade, inverse: \Occupancy.growingSpace)
    var occupancies: [Occupancy] = []
    
    @Relationship(deleteRule: .cascade, inverse: \PlannedPlanting.growingSpace)
    var plannedPlantings: [PlannedPlanting] = []
    
    var garden: Garden?
}
```

No `type` enum, no dimensions, no soil type. Add those later if users ask.

---

## 7. Deterministic PlanningEngine

### What it must receive:

```swift
struct PlanningContext {
    let garden: Garden
    let growingSpaces: [GrowingSpace]
    let currentOccupancies: [Occupancy]       // active and planned
    let seeds: [Seed]
    let desires: [Desire]
    let plannedPlantings: [PlannedPlanting]
    let climateZone: ClimateZone?             // optional, from garden settings
    let frostDates: FrostDates?               // optional, from garden settings
    let today: Date
}

struct FrostDates {
    let averageLastFrost: Date?
    let averageFirstFrost: Date?
}

struct ClimateZone {
    let zone: String                          // e.g., "9b"
    let region: String?                       // e.g., "Pacific Northwest"
}
```

### What it must return:

```swift
struct PlantingSuggestion {
    let crop: String
    let variety: String?
    let growingSpace: GrowingSpace?
    let suggestedDate: Date
    let expectedHarvest: Date?
    let expectedRelease: Date?
    let reason: String
    let ranking: SuggestionRank
    let seedState: SeedState?                 // own, want, none
    let warnings: [String]
}

enum SuggestionRank {
    case bestFit
    case alsoGood
    case notRecommended
}

struct SuccessionPlan {
    let growingSpace: GrowingSpace
    let currentOccupancy: Occupancy?
    let suggestedNext: [PlantingSuggestion]
    let reasoning: String
}
```

### Hard constraints vs. soft ranking vs. warnings

**Hard constraints** (cannot be overridden by ranking):
- Frost-free days remaining < days to maturity → reject.
- Planting window closed for this crop in this zone → reject.
- GrowingSpace has an active Occupancy that does not allow interplanting → reject (unless user confirms interplant).
- Crop rotation violation (same family in same space within rotation period) → reject or require explicit override.

**Soft ranking factors** (influence position in list):
- Seed is OWN → boost ranking.
- Seed is WANT → lower ranking, show "you want this."
- Days to maturity fits comfortably before frost → boost.
- Crop follows a compatible predecessor (good rotation) → boost.
- Crop is in user's desire list → boost.
- Succession timing aligns well with existing plans → boost.

**Informational warnings** (shown but do not block):
- "Unusually cold forecast this week — consider waiting 5 days."
- "This is an early planting — protect from late frost."
- "Fast-maturing variety — could fit in a shorter window."

### Example conflicts and resolutions:

**Conflict 1**: User wants beans (70 days) but only 60 frost-free days remain.
- Hard constraint: 60 < 70 → reject.
- Ranking: notRecommended.
- Warning: "Too little season remaining."

**Conflict 2**: User wants tomatoes in Bed 3, but Bed 3 has an active lettuce occupancy that will not be released for 3 weeks. User also wants lettuce in Bed 2, which is empty now.
- Hard constraint: Bed 3 is occupied → cannot plant tomatoes there now.
- Soft ranking: suggest Bed 2 for lettuce now, Bed 3 for tomatoes in 3 weeks.
- Warning: "Bed 3 available ~Aug 20."

**Conflict 3**: User wants to plant carrots in Bed 1, but Bed 1 had tomatoes last year (same family: solanaceae). Carrots are apiaceae — compatible.
- Hard constraint: none (rotation allows).
- Ranking: boost (good rotation).

**Conflict 4**: User wants to plant beans in Bed 1, but Bed 1 had peas last year (same family: fabaceae). Beans are also fabaceae.
- Hard constraint: rotation violation (same family).
- Resolution: reject or require explicit override: "Beans and peas are in the same family. Consider a different space or crop."

**Conflict 5**: User has two plans that both want Bed 3 in September: fall carrots (Aug 20) and garlic (Oct 15).
- Hard constraint: Aug 20 occupancy ends ~Oct 20. Garlic planting Oct 15 overlaps.
- Resolution: reject garlic plan, or suggest adjusting carrot harvest/removal to free Bed 3 by Oct 10. Engine shows conflict and proposes resolution.

---

## 8. Succession Without Overengineering

**Decision**: Succession is an emergent relationship, not an explicit persistent chain.

**Reason**: 
- A succession chain is simply sequential Occupancies in the same GrowingSpace.
- Maintaining an explicit chain object adds complexity without adding query power — the same information is derivable by querying Occupancies ordered by startDate.
- The user should never manually maintain a succession chain. The planning engine proposes sequential occupancies; the user accepts or adjusts them individually.

**How it works**:
- Each Occupancy has a `growingSpace` and `startDate` and `endDate`.
- Succession is implied by: same growingSpace, startDate of next ≥ endDate of previous (or expectedReleaseDate of previous).
- The UI shows a timeline view by querying Occupancies for a GrowingSpace and rendering them in order.
- The planning engine proposes the "next" occupancy based on the current/expected release date of the active occupancy.

**No explicit SuccessionChain model needed.**

---

## 9. Desire Separately from Plan

**Decision**: Desire is a persistent model.

**Reason**: 
- Desires can exist before any plan is made. "I want carrots" may sit unresolved for months until a space opens.
- Desires can be fulfilled without a formal plan (user plants without creating a plan first).
- Desires can be cancelled or expire without any other entity changing.
- Desires drive recommendations even when no plan exists.

**Model**:

```swift
@Model
final class Desire {
    var id: UUID
    var cropName: String
    var variety: String?
    var notes: String?
    var isFulfilled: Bool
    var isExpired: Bool
    var isCancelled: Bool
    var createdAt: Date
    var updatedAt: Date
    
    var garden: Garden?
}
```

**Lifecycle**:
- **Created**: User says "I want carrots" or taps "I want to grow..." in UI.
- **Fulfilled**: When a PlannedPlanting or Occupancy is created for this crop in this garden. Marked fulfilled, not deleted.
- **Cancelled**: User says "I don't want carrots anymore." Marked cancelled.
- **Expired**: Season ends and the desire was not fulfilled. App marks expired automatically (e.g., "fall carrots" desire expires after first frost).
- **Deleted**: Not deleted. All states are preserved for history.

**What happens in each scenario**:
- **Fulfilled**: Desire marked fulfilled. Linked to the resulting PlannedPlanting or Occupancy (optional link).
- **Cancelled**: Desire marked cancelled. Remains visible in history.
- **Season passes**: Desire marked expired. Remains visible.
- **User no longer has seeds**: Desire remains. Seed state changes. Planning engine notes the mismatch.
- **User explicitly says no**: Desire marked cancelled.

---

## 10. Seed Shelf Semantics

**Decision**: Keep the Seed Shelf minimal. OWN and WANT states only. No quantity tracking, no inventory management.

**Reason**: The Seed Shelf is an input to planning, not an inventory system. Forcing quantity tracking, expiration dates, and packet counts adds friction without improving planning quality. The planning engine only needs to know: does the user have this seed or not?

**Minimal model**:

```swift
@Model
final class Seed {
    var id: UUID
    var cropName: String
    var variety: String?
    var state: SeedState
    var notes: String?
    var createdAt: Date
    var updatedAt: Date
    
    var garden: Garden?
}

enum SeedState {
    case own
    case want
}
```

**How quantity, year, source are represented without making them required**:
- Do not add them to the initial model.
- If users request them, add them as optional fields later.
- For now, `notes` is a freeform field where users can write "2 packets, 2025, from seed library" if they want.
- The app does not parse or validate this. It is human-readable only.

**How the Seed Shelf influences ranking without being a prerequisite**:
- A seed being OWN boosts the suggestion ranking.
- A seed being WANT lowers ranking but does not block the suggestion.
- No seed at all: suggestion is shown with neutral ranking. The app says "You don't have seeds for this. Add to Seed Shelf?"
- Planning works even with an empty Seed Shelf. The app recommends based on climate, season, and space. The Seed Shelf adds personalized ranking but is not required.

**What happens when user owns no seed for a crop**:
- Planning engine recommends the crop.
- Suggestion shows: "No seeds — add to Seed Shelf?"
- User can tap to add the crop to WANT list.

**What happens when user wants a crop but doesn't own seeds**:
- Seed record with state=want.
- Planning engine recommends the crop with lower ranking.
- Suggestion shows: "You want this — consider ordering seeds."

**Can planning recommend crops absent from the Seed Shelf?**:
- Yes. The Seed Shelf is a personalization layer, not a gatekeeper.
- The engine maintains a built-in crop database with planting windows, days to maturity, and frost tolerance. This is the baseline.
- The Seed Shelf adds: "you have seeds for this," "you want this," or "no record."

---

## 11. Plan-to-Actual Reconciliation

### Exact behavior for the example:

User plans: Nantes carrots → Bed 3 → Aug 20.
User says: "I planted the carrots today." Today is Aug 22.

1. **System identifies the plan**: Finds the PlannedPlanting for Nantes carrots in Bed 3 with plannedDate=Aug20.
2. **System asks for confirmation**: "You planned Nantes carrots in Bed 3 for Aug 20. Mark as planted today (Aug 22)?"
3. **User confirms**.
4. **System actions**:
   - PlannedPlanting.status = planted.
   - PlannedPlanting.actualDate = Aug22 (new field, optional).
   - Creates Occupancy: crop=Carrots, variety=Nantes, growingSpace=Bed3, startDate=Aug22, status=active, expectedHarvest=Oct20, expectedRelease=Oct25.
   - Creates Plant: crop=Carrots, variety=Nantes, plantingDate=Aug22, location=Bed3, linked to Occupancy.
   - PlannedPlanting.occupancy = the new Occupancy (link both ways).
5. **Historical truth preserved**:
   - PlannedPlanting retains plannedDate=Aug20.
   - Occupancy records actual startDate=Aug22.
   - Plant records actual plantingDate=Aug22.
   - No data is overwritten.

### Other reconciliation scenarios:

**Planting earlier than planned**:
- Same flow. plannedDate=Aug20, actualDate=Aug15. Both preserved.

**Planting later than planned**:
- Same flow. plannedDate=Aug20, actualDate=Aug28. Both preserved.
- Planning engine may note: "Planted 8 days late. Expected harvest may shift."

**Planting somewhere different**:
- User says: "I planted the carrots in Bed 2 instead."
- System updates PlannedPlanting.growingSpace = Bed2 (or creates new PlannedPlanting).
- Creates Occupancy in Bed2.
- Original plan for Bed3 is marked cancelled or moved.

**Planting a different variety**:
- User says: "I planted Napoli carrots instead of Nantes."
- System updates PlannedPlanting.variety = Napoli (or notes the change in Occupancy).
- Preserves original variety in the plan record.

**Planting without a plan**:
- User says: "I planted carrots in Bed 3 today."
- No PlannedPlanting exists.
- System creates Occupancy directly with startDate=today.
- Optionally creates a Desire record and marks it fulfilled.

**User should NOT have to choose "replace" or "keep both"**:
- The only case where ambiguity exists is if multiple plans match (e.g., two planned carrot plantings in Bed 3).
- In that case, the system asks: "Which plan does this match?" and shows the options.
- Normal case: one plan matches. System reconciles automatically.

---

## 12. Architecture Changes Before Implementation

### MUST DECIDE BEFORE CODING

1. **Add GrowingSpace model** — required for all planning features. Cannot proceed without it.
2. **Add Occupancy model** — required for space availability and historical truth.
3. **Add PlannedPlanting model** — required for intention tracking.
4. **Add Desire model** — required for intent-first and seed-first flows.
5. **Add Seed model** — required for Seed Shelf and planning integration.
6. **Add OccupancyStatus enum** — active, planned, completed, cancelled.
7. **Add SeedState enum** — own, want.
8. **Add PlanStatus enum** — planned, planted, cancelled.
9. **Add GardenSettings or extend Garden** with climate zone and frost dates — required for deterministic planning.
10. **Define Plant-Occupancy relationship** — optional link, but must be decided before implementing bed detail views.

### CAN BE DEFERRED

1. **PlannedPlanting.seed relationship** — can add after Seed Shelf is implemented.
2. **Harvest-Occupancy link** — can be added later when yield-per-space tracking is needed.
3. **JournalEntry-GrowingSpace link** — not needed for initial planning features.
4. **ClimateZone and FrostDates as separate models vs. embedded in Garden** — use embedded structs first; extract to models later if needed.
5. **Photo support for GrowingSpace** — add bed photos later if users request.
6. **Quantity tracking for Seed** — add optional fields later.
7. **Voice/NLU layer** — UI flows can be built with deterministic actions first; voice is a later input method.
8. **Year Plan view** — can be derived from existing Occupancies; no new model needed.

### DO NOT BUILD YET

1. **Crop database with full botanical metadata** — start with a minimal set of crops relevant to the user's climate. Expand later.
2. **Rotation constraint engine with full family mapping** — start with simple same-family detection. Full rotation logic is complex and can be added incrementally.
3. **Weather API integration** — climate baseline is sufficient for MVP planning.
4. **Interplanting logic** — start with sequential planting only. Interplanting suggestions require crop-specific knowledge about canopy/root zones.
5. **Seed quantity tracking, expiration, viability** — not needed for planning decisions.
6. **Garden mapping / visual layout** — not needed for planning. Bed list is sufficient.
7. **Multiple garden support with cross-garden planning** — single garden for now.
8. **Backup/restore, iCloud sync, sharing** — local-first for now.
9. **Push notifications for "plant now" reminders** — nice to have, not required for the planning model.
10. **Complex form-based seed entry with variety database lookup** — freeform text with basic parsing is sufficient.

---

## 13. Proposed Minimal Domain Model for Phase 1–3

```swift
// Existing — unchanged
@Model final class Garden { ... }
@Model final class Plant { ... }
@Model final class PlantPhoto { ... }
@Model final class JournalEntry { ... }
@Model final class Harvest { ... }

// New — Phase 1
@Model final class GrowingSpace {
    var id: UUID
    var name: String
    var notes: String?
    var createdAt: Date
    var updatedAt: Date
    var garden: Garden?
    
    @Relationship(deleteRule: .cascade, inverse: \Occupancy.growingSpace)
    var occupancies: [Occupancy] = []
    
    @Relationship(deleteRule: .cascade, inverse: \PlannedPlanting.growingSpace)
    var plannedPlantings: [PlannedPlanting] = []
}

// New — Phase 2
@Model final class Occupancy {
    var id: UUID
    var cropName: String
    var variety: String?
    var startDate: Date
    var endDate: Date?
    var expectedHarvestDate: Date?
    var expectedReleaseDate: Date?
    var status: OccupancyStatus
    var notes: String?
    var createdAt: Date
    var updatedAt: Date
    
    var growingSpace: GrowingSpace?
    var plant: Plant? // optional, linked when actual planting occurs
    
    @Relationship(deleteRule: .nullify, inverse: \PlannedPlanting.occupancy)
    var plannedPlanting: PlannedPlanting?
}

enum OccupancyStatus {
    case active
    case planned
    case completed
    case cancelled
}

@Model final class PlannedPlanting {
    var id: UUID
    var cropName: String
    var variety: String?
    var plannedDate: Date?
    var actualDate: Date?
    var status: PlanStatus
    var notes: String?
    var createdAt: Date
    var updatedAt: Date
    
    var garden: Garden?
    var growingSpace: GrowingSpace?
    var occupancy: Occupancy? // linked when planted
    var seed: Seed? // optional
}

enum PlanStatus {
    case planned
    case planted
    case cancelled
}

@Model final class Desire {
    var id: UUID
    var cropName: String
    var variety: String?
    var notes: String?
    var isFulfilled: Bool
    var isExpired: Bool
    var isCancelled: Bool
    var createdAt: Date
    var updatedAt: Date
    
    var garden: Garden?
}

// New — Phase 1
@Model final class Seed {
    var id: UUID
    var cropName: String
    var variety: String?
    var state: SeedState
    var notes: String?
    var createdAt: Date
    var updatedAt: Date
    
    var garden: Garden?
}

enum SeedState {
    case own
    case want
}

// Existing — extended with optional climate fields
extension Garden {
    var climateZone: String?      // e.g., "9b"
    var lastFrostDate: Date?      // average
    var firstFrostDate: Date?     // average
}
```

**This model supports**:
- Space-first planning (GrowingSpace + Occupancy)
- Intent-first planning (Desire + planning engine)
- Seed-first planning (Seed + state tracking)
- Discovery (planning engine + desires)
- Succession (sequential Occupancies in GrowingSpace)
- Plan-to-actual reconciliation (PlannedPlanting → Occupancy + Plant)
- Historical preservation (Occupancy status, PlannedPlanting status, Desire state)
- Empty states (no GrowingSpace, no Seed, no Desire — app still works)

**This model does NOT support** (yet):
- Quantity tracking for seeds
- Interplanting (overlapping Occupancies are possible but no special UI)
- Harvest-to-occupancy linking
- Weather integration
- Crop rotation family database
- Visual garden mapping
