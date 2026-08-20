# Garden Timeline — Exploratory Test Plan

## Purpose

This document provides manual test scenarios for verifying the Garden Timeline UX. These scenarios are designed for execution by a human tester or an automated coding agent with access to the running app on an Android device or emulator.

## Prerequisites

- App built and installed: `./gradlew :app:installDebug`
- App launched to Garden screen
- Test garden loaded with realistic data (see `RealisticGardenFixture`)

---

## Scenario 1: Can I understand what is growing without opening anything?

**Steps:**
1. Open the app to the Garden screen
2. Observe the list of growing spaces

**Expected:**
- Each occupied space shows the crop name and variety as the primary text
- Lifecycle phase label appears below the crop name (e.g., "Growing", "Producing")
- Lifecycle indicator bar is visible and filled proportionally to the phase

**Pass Criteria:**
- [ ] Current crop is visible at a glance
- [ ] Lifecycle stage is understandable without tapping

---

## Scenario 2: Can I tell which space is available today?

**Steps:**
1. Open the app to the Garden screen
2. Look for spaces without an active crop

**Expected:**
- Available spaces show an "Available" badge
- Available spaces show "What you can plant now" with current suggestions
- Available spaces do NOT show an occupancy or lifecycle indicator

**Pass Criteria:**
- [ ] Available spaces are visually distinct from occupied spaces
- [ ] Current planting opportunities are visible without interaction

---

## Scenario 3: Can I tell that a suggested crop is for later rather than now?

**Steps:**
1. Find an occupied space with a future release date
2. Observe the "AFTER THIS" section

**Expected:**
- "AFTER THIS" header appears in a distinct, muted style
- "Space opens ~[date]" text indicates the future timing
- Suggested crops show "Plant ~[date]" with a future date
- No "Plant now" label appears on future suggestions

**Pass Criteria:**
- [ ] Future suggestions are clearly distinguished from current suggestions
- [ ] Future date is visible without tapping

---

## Scenario 4: Can I determine what happens to this bed next?

**Steps:**
1. Find an occupied space with an expected release date
2. Observe the succession suggestions

**Expected:**
- "AFTER THIS" section lists suggested follow-on crops
- Opening date is shown
- Suggested planting dates are shown
- Seeds/desires influence ranking (owned seeds show "You have seeds")

**Pass Criteria:**
- [ ] Succession plan is visible without navigation
- [ ] Timing of next planting is clear

---

## Scenario 5: Can I scrub forward three weeks without accidentally changing my plan?

**Steps:**
1. Note the current date and active crops
2. Drag the date scrubber forward 3 weeks
3. Observe the timeline changes
4. Navigate away from Garden screen and back

**Expected:**
- Timeline updates to show the future projection
- Active crops remain in their spaces
- Lifecycle phases may advance (e.g., Growing → Producing)
- After navigating away and back, the date scrubber returns to today (or the last selected date within the session)
- No data is lost or modified

**Pass Criteria:**
- [ ] Scrubbing is read-only
- [ ] No accidental data mutation occurs
- [ ] App state is preserved across navigation

---

## Scenario 6: Can I understand a crop whose maturity date is unknown?

**Steps:**
1. Load a garden with a crop that has no expected harvest or release date
2. Observe the occupancy details

**Expected:**
- Crop name and variety are shown
- Lifecycle phase is shown
- No fabricated harvest date appears
- "Harvest expected in X days" does NOT appear
- DaysUntilHarvest is null/empty

**Pass Criteria:**
- [ ] Unknown maturity is handled gracefully
- [ ] No speculative dates are shown

---

## Scenario 7: Does the empty garden state guide the user?

**Steps:**
1. Open a garden with no growing spaces
2. Observe the empty state

**Expected:**
- "No growing spaces yet" message appears
- "Add a bed, pot, or row to start tracking your garden." subtext appears
- No fabricated suggestions or future openings appear

**Pass Criteria:**
- [ ] Empty state is clear and actionable
- [ ] No hallucinated content

---

## Scenario 8: Do seeds and desires influence suggestions?

**Steps:**
1. Add seeds to the seed shelf
2. Add desires to the desire list
3. Observe suggestions for an available space

**Expected:**
- Owned seeds show "You have seeds" and rank as "Best fit"
- Desired crops show improved ranking
- Untracked crops remain eligible but rank lower

**Pass Criteria:**
- [ ] Seed/desire influence is visible
- [ ] Untracked crops are not excluded

---

## Scenario 9: Is the date scrubber accessible?

**Steps:**
1. Enable TalkBack or VoiceOver
2. Navigate to the date scrubber
3. Listen to the announced content

**Expected:**
- Date is announced with context (e.g., "Today, August 17, 2026")
- Slider is announced as adjustable
- "Today" button is announced with its label

**Pass Criteria:**
- [ ] All interactive elements have accessibility labels
- [ ] Date context is announced

---

## Scenario 10: Does text remain usable at larger font sizes?

**Steps:**
1. Enable large font size in system settings (e.g., 200%)
2. Open the Garden screen

**Expected:**
- Text scales appropriately
- No text is clipped or truncated
- Layout remains usable

**Pass Criteria:**
- [ ] All text is readable at large font sizes
- [ ] No layout breakage

---

## Scenario 11: Does explicit release free the space?

**Steps:**
1. Find an occupancy with an explicit end date
2. Verify the space shows as occupied before the end date
3. Scrub to a date after the end date

**Expected:**
- Before end date: space shows as occupied with the crop
- After end date: space shows as available with current suggestions

**Pass Criteria:**
- [ ] Explicit end date correctly releases the space
- [ ] No residual occupancy data appears after release

---

## Scenario 12: Does projected release NOT free the space?

**Steps:**
1. Find an occupancy with only an expected release date (no explicit end date)
2. Scrub to a date after the expected release date

**Expected:**
- Space remains occupied
- Phase shows "Space opening soon"
- No current suggestions appear
- Future suggestions may appear if seeds/desires exist

**Pass Criteria:**
- [ ] Projected release does not mutate occupancy
- [ ] Space is not prematurely freed

---

## Notes for Automated Agents

- These scenarios require a running app instance on an Android device or emulator
- Scenarios 1-6 and 11-12 can be verified via UI automation (Espresso/Compose testing)
- Scenarios 9-10 require accessibility and font-size testing APIs
- Screenshots should be captured at each step for visual verification
