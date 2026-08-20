# Garden AI — UX Design

## Overview

This document describes the user experience design for the Phase 38 AI interaction layer. The goal is to make AI feel like a natural, optional interface to the garden rather than a separate "AI feature."

## Design Principles

1. **LOW FRICTION** — Minimize steps between intent and action.
2. **NO MODE OVERLOAD** — No "AI mode" toggle. AI is always available.
3. **GARDEN CONTEXT FIRST** — Responses use actual garden data, not generic chatbot prose.
4. **AI IS OPTIONAL** — All existing flows work without AI.
5. **OFFLINE-FIRST** — No network required.
6. **CLEAR USER CONTROL** — User confirms before destructive actions.
7. **EASY UNDO** — Undo is immediately available after any AI mutation.
8. **NO SILENT MUTATIONS** — Every change is visible and confirmable.
9. **NO UNNECESSARY CONFIRMATIONS** — High-confidence, unambiguous actions execute immediately.
10. **ACCESSIBLE** — Semantic labels, keyboard navigation, screen-reader support.
11. **FAST FEELING** — Instant feedback, no artificial loading delays.
12. **CALM / SERENE VISUAL DESIGN** — Matches existing garden aesthetic.

## Entry Point

### Location

The AI input bar lives at the bottom of the **Garden** screen, below the timeline content. It is visible whenever the user is on the Garden tab.

### Components

| Component | Purpose |
|-----------|---------|
| Text field | Type natural-language requests |
| Send button | Submit text |
| Voice button | Placeholder for future voice input |
| Camera button | Placeholder for future plant recognition |
| Document button | Placeholder for future garden-plan import |

### Interaction

- User types a request and taps Send (or presses ImeAction.Send).
- Voice, camera, and document buttons show placeholder feedback via `FakeAIProvider`.
- Input clears after sending.
- Response appears in a bottom sheet.

## Response Display

### Modal Bottom Sheet

AI responses appear in a `ModalBottomSheet` anchored to the bottom of the screen. This feels native on Android and keeps the garden timeline visible behind the response.

### Response States

| State | UI |
|-------|----|
| Read-only answer | Message bubble only |
| Executed mutation | Success messages + Undo FAB |
| Failed mutation | Error messages + partial results |
| Pending confirmation | Proposal cards + Confirm/Cancel buttons |
| Clarification needed | Question + ambiguity buttons |
| Error/uncertainty | Error bubble + Dismiss button |

## Proposal / Confirmation UX

### High-Confidence, Unambiguous

For high-confidence proposals with no ambiguities, the action executes immediately. The user sees the result and an Undo option.

**Example:**
- User: "Add a bed"
- AI: Executes `AddGrowingSpace("Bed 2")`
- Sheet shows: "Growing space added: Bed 2" + [Undo]

### Low-Confidence

When confidence is below 0.5, the system requests confirmation before executing.

**Example:**
- User: "Maybe plant beans"
- AI: "I'm not confident enough to do that. Can you confirm?"
- Shows proposal cards with confidence percentage
- Buttons: [Confirm] [Cancel]

### Ambiguous

When the request is ambiguous, the system asks for clarification.

**Example:**
- User: "Plant beans"
- AI: "I found two possible beds. Which one?"
- Buttons: [Zone B] [Zone C]

### Destructive / Large Operations

For operations affecting many items, the system surfaces the scope and requires confirmation.

**Example:**
- User: "Remove all harvested plants"
- AI: "I found 14 plants that would be removed."
- Buttons: [Remove them] [Cancel]

## Undo UX

### Immediate Undo

After any successful AI mutation, an Undo FAB appears in the response sheet.

**Example:**
- Sheet shows: "Added 12 Brussels sprouts to Zone B."
- Floating Undo button: [Undo]

### Conversational Undo

User can type "undo" or "undo that" at any time.

**Example:**
- User: "Undo that"
- AI: "Undone: growing space removed"

## Read-Only Questions

Read-only responses are displayed as message bubbles. No action buttons are shown.

**Examples:**
- "What is in Zone B?" → "Tomato is growing in Bed 1"
- "What am I harvesting this month?" → "You have 2 harvests scheduled..."
- "What's still growing?" → Lists active occupancies

## Image / Plant Recognition UX

### Entry

User taps the Camera button in the AI input bar.

### Flow

1. Placeholder triggers `AIInput.ImageReference`
2. AI returns a `RecognitionResult` interpretation
3. Sheet shows candidate results with confidence:
   - "Looks like: Zucchini — 82%, Cucumber — 11%, Pumpkin — 4%"
4. User confirms with [That's zucchini] or [Try again]

### Future Integration

The UI consumes generic `RecognitionResult` data. When the local ML model is ready, it plugs into `LocalAIProvider` without UI changes.

## Document Import UX

### Entry

User taps the Document button in the AI input bar.

### Flow

1. Placeholder triggers `AIInput.DocumentText`
2. AI returns `CommandProposals` representing extracted garden items
3. Sheet shows grouped proposed changes:
   - Garden spaces: 3 new beds
   - Crops: 12 items
   - Planting dates: 8 dates
4. Buttons: [Review import] [Cancel]

### Future Integration

The UI accepts any list of `AICommandProposal` objects. When document extraction is implemented, it maps to the same proposal format.

## Accessibility

- All buttons have `contentDescription`.
- Input field has a placeholder.
- Response text uses `bodyLarge` for readability.
- Colors use Material 3 contrast ratios.
- Keyboard navigation works (ImeAction.Send on input field).
- Screen readers announce response content.

## What Is NOT Implemented

- Real speech-to-text (voice button is a placeholder)
- Real camera capture (camera button is a placeholder)
- Real document OCR (document button is a placeholder)
- Real LLM (uses `FakeAIProvider`)
- Persistent command history (uses `InMemoryCommandHistory`)
