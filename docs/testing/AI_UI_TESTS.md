# AI UI — Device-Dependent Test Documentation

## Compile-Only Tests (No Device Required)

The following AI UI tests compile successfully but **cannot execute** on the JVM
because Compose UI testing requires an instrumented Android environment.

### Test Files

- `app/src/androidTest/java/com/soilandsupper/ai/AiInputBarTest.kt`
- `app/src/androidTest/java/com/soilandsupper/ai/AiResponseSheetTest.kt`
- `app/src/androidTest/java/com/soilandsupper/ui/GardenTimelineUiTest.kt`

### Tests That Compile But Need an Emulator/Device

| Test | What it verifies | Status |
|------|------------------|--------|
| `inputBar_rendersPlaceholderAndActions` | AI input bar renders text field, voice, and send buttons | **Compiles only** |
| `inputBar_sendButtonCallsOnSend` | Send button triggers the submit callback | **Compiles only** |
| `inputBar_voiceButtonCallsOnVoice` | Voice button triggers the voice callback | **Compiles only** |
| `inputBar_clearsAfterSend` | Input clears after successful send | **Compiles only** |
| `inputBar_loading_disablesInputAndShowsNoSendAction` | Loading state disables text input and all buttons | **Compiles only** |
| `messageBubble_displaysText` | AI message bubble renders text | **Compiles only** |
| `readOnlyResponse_displaysMessage` | Read-only AI response renders in sheet | **Compiles only** |
| `executedCommands_displaysSuccessAndUndo` | Executed commands show with Undo button | **Compiles only** |
| `errorResponse_displaysError` | Error response renders error text | **Compiles only** |
| `loadingState_showsWorkingMessage` | Loading state shows "Working on that..." spinner | **Compiles only** |
| `emptyGarden_rendersEmptyState` | Garden screen shows empty state when no spaces exist | **Compiles only** |
| `occupiedSpace_currentCropAppears` | Occupied space shows current crop | **Compiles only** |
| `occupiedSpace_currentCropIsVisuallyPrimary` | Current crop is visually primary | **Compiles only** |
| `futureOpening_showsFutureOpportunity` | Future openings show opportunity UI | **Compiles only** |
| `openSpace_showsAvailableSpace` | Open spaces show "Available" state | **Compiles only** |
| `openSpace_showsCurrentSuggestions` | Open spaces show planting suggestions | **Compiles only** |
| `dateScrubber_changesProjection` | Date scrubber changes timeline projection | **Compiles only** |
| `lifecycleStates_haveTextLabels` | Crop lifecycle states have text labels | **Compiles only** |
| `futureSuggestions_haveAccessibleLabels` | Future suggestions have accessible labels | **Compiles only** |
| `dateScrubber_isAccessible` | Date scrubber is accessible and enabled | **Compiles only** |
| `buttons_haveMeaningfulLabels` | UI elements have meaningful labels | **Compiles only** |

### How to Run on a Device

```bash
# Start an emulator or connect a device, then:
./gradlew :app:connectedDebugAndroidTest --tests "com.soilandsupper.ai.*"
./gradlew :app:connectedDebugAndroidTest --tests "com.soilandsupper.ui.GardenTimelineUiTest"
```

## Tests That Do Execute (No Device Required)

| Suite | Tests | Status |
|-------|-------|--------|
| `:shared:testDebugUnitTest` | 20 AI orchestration tests + 12 validation tests = 32 AI tests | **PASS** |
| `:shared:testReleaseUnitTest` | 14+ shared tests | **PASS** |
| `:shared:test` | All shared tests (debug + release): 137 total | **PASS** |
| `:app:testDebugUnitTest` | App unit tests (excluding AI UI tests) | **PASS** |
| `:app:testReleaseUnitTest` | App release unit tests | **PASS** |
| `:app:test` | All app tests: 85 tasks | **PASS** |
| `:app:assembleDebug` | Android debug APK build | **PASS** |
| `:app:compileDebugAndroidTestKotlin` | Instrumented test compilation | **PASS** |

## Known Limitations

1. **No emulator available** in this environment, so Compose UI tests cannot be executed.
2. **ModalBottomSheet behavior** (swipe-to-dismiss, animation, state persistence) requires device validation.
3. **Voice input** requires platform STT integration not yet implemented.
4. **Loading state UX** (spinner visibility, input disable, sheet behavior) requires device validation.
5. **AI response flow** (submit → loading → response sheet → confirm/undo/clarify) requires device validation to verify the full interaction cycle.
