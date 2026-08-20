# AI UI — Device-Dependent Test Documentation

## Compile-Only Tests (No Device Required)

The following AI UI tests compile successfully but **cannot execute** on the JVM
because Compose UI testing requires an instrumented Android environment.

### Test Files

- `app/src/androidTest/java/com/soilandsupper/ai/AiInputBarTest.kt`
- `app/src/androidTest/java/com/soilandsupper/ai/AiResponseSheetTest.kt`

### Tests That Compile But Need an Emulator/Device

| Test | What it verifies | Status |
|------|------------------|--------|
| `inputBar_rendersPlaceholderAndActions` | AI input bar renders text field, voice, camera, and document buttons | **Compiles only** |
| `inputBar_sendButtonCallsOnSend` | Send button triggers the submit callback | **Compiles only** |
| `inputBar_voiceButtonCallsOnVoice` | Voice button triggers the voice callback | **Compiles only** |
| `inputBar_cameraButtonCallsOnCamera` | Camera button triggers the camera callback | **Compiles only** |
| `inputBar_documentButtonCallsOnDocument` | Document button triggers the document callback | **Compiles only** |
| `inputBar_clearsAfterSend` | Input clears after successful send | **Compiles only** |
| `messageBubble_displaysText` | AI message bubble renders text | **Compiles only** |
| `readOnlyResponse_displaysMessage` | Read-only AI response renders in sheet | **Compiles only** |
| `executedCommands_displaysSuccessAndUndo` | Executed commands show with Undo button | **Compiles only** |
| `errorResponse_displaysError` | Error response renders error text | **Compiles only** |

### How to Run on a Device

```bash
# Start an emulator or connect a device, then:
./gradlew :app:connectedDebugAndroidTest --tests "com.soilandsupper.ai.*"
```

## Tests That Do Execute (No Device Required)

| Suite | Tests | Status |
|-------|-------|--------|
| `:shared:testDebugUnitTest` | 20 AI orchestration tests | **PASS** |
| `:shared:testReleaseUnitTest` | 14+ shared tests | **PASS** |
| `:shared:test` | All shared tests (debug + release) | **PASS** |
| `:app:testDebugUnitTest` | App unit tests (excluding AI UI tests) | **PASS** |
| `:app:testReleaseUnitTest` | App release unit tests | **PASS** |
| `:app:test` | All app tests | **PASS** |
| `:app:assembleDebug` | Android debug APK build | **PASS** |

## Known Limitations

1. **No emulator available** in this environment, so Compose UI tests cannot be executed.
2. **ModalBottomSheet behavior** (swipe-to-dismiss, animation, state persistence) requires device validation.
3. **Photo picker integration** (camera button) requires Android `ActivityResultContracts.PickVisualMedia` on a device.
4. **Voice input** requires platform STT integration not yet implemented.
5. **Document import** requires platform document picker not yet implemented.
