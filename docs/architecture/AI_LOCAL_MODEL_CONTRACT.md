# Local AI Model Integration Contract

## Overview

This document defines the contract for integrating a real local/on-device AI model into the Soil & Supper orchestration layer. The existing domain authority, command pipeline, and validator/executor boundaries remain unchanged.

## Current Architecture

```
Natural language
  → LocalAIProvider.interpret()
  → AIInterpretation
  → AIOrchestrator.process()
  → CommandValidator
  → CommandExecutor
  → CommandHistory
  → Repository
```

The `LocalAIProvider` interface is the single pluggable seam. A real local model implements this interface. The orchestrator handles all validation, execution, and history.

## LocalAIProvider Contract

**File:** `shared/src/commonMain/kotlin/com/soilandsupper/ai/orchestration/LocalAIProvider.kt`

```kotlin
interface LocalAIProvider {
    suspend fun interpret(request: AIRequest): AIInterpretation
}
```

### Rules

1. **No platform imports.** The implementation must not import `android.*`, network clients, or cloud SDKs in `commonMain`.
2. **No persistence access.** The provider must not call `GardenRepository` or any DAO. It receives state via `AIRequest.gardenContext` and returns structured intent via `AIInterpretation`.
3. **Single suspend function.** No callbacks, no threading concerns, no platform-specific runtime dependencies in `commonMain`.
4. **Structured output only.** The provider must return one of the `AIInterpretation` subtypes. Free-text responses are not permitted.

### AIInterpretation Output Contract

| Subtype | When to use | Required fields |
|---------|-------------|-----------------|
| `InformationalAnswer` | Read-only query answered | `message` (non-blank) |
| `CommandProposals` | One or more mutation intents | `proposals` (non-empty list) |
| `ClarificationRequest` | Ambiguous intent | `question` (non-blank) |
| `Uncertainty` | Cannot understand | `reason` (non-blank) |
| `RecognitionResult` | Plant/image recognition | `recognized` (non-blank), `confidence` (0.0–1.0) |

### AICommandProposal Contract

| Field | Type | Constraints |
|-------|------|-------------|
| `command` | `GardenCommand` | Must be a valid sealed subtype |
| `explanation` | `String` | Non-blank |
| `confidence` | `Float?` | If present, must be 0.0–1.0 |
| `ambiguities` | `List<String>` | Non-null; empty if none |

### Supported GardenCommand Vocabulary

A real model must be capable of producing any of the 16 `GardenCommand` subtypes:

**Spaces:** `AddGrowingSpace`, `UpdateGrowingSpace`, `RemoveGrowingSpace`
**Crops:** `PlantCrop`, `HarvestCrop`, `EndCrop`
**Journal:** `RecordObservation`
**Seeds/Desires:** `AddSeed`, `AddDesire`, `FulfillDesire`, `CancelDesire`
**Plants:** `RecordPlant`, `UpdatePlant`, `RemovePlant`

Undo is handled by the orchestrator when input starts with "undo" — the provider does not need to emit an undo command.

## Structured Output Parsing Boundary

A real local model outputs raw text (typically JSON). The conversion from raw output to `AIInterpretation` is the provider's responsibility.

### Expected Raw Model Output Format

Providers should map model output to a JSON structure compatible with the following schema:

```json
{
  "type": "command_proposals",
  "proposals": [
    {
      "command_type": "plant_crop",
      "parameters": {
        "cropName": "Tomato",
        "growingSpaceId": 1,
        "startDate": 1696312800000
      },
      "explanation": "Plant tomatoes in Bed 1",
      "confidence": 0.9,
      "ambiguities": []
    }
  ]
}
```

Supported `type` values: `informational_answer`, `command_proposals`, `clarification_request`, `uncertainty`, `recognition_result`.

Supported `command_type` values: `add_growing_space`, `update_growing_space`, `remove_growing_space`, `plant_crop`, `harvest_crop`, `end_crop`, `record_observation`, `add_seed`, `add_desire`, `fulfill_desire`, `cancel_desire`, `record_plant`, `update_plant`, `remove_plant`.

### Parsing Rules

1. **Strict parsing.** Malformed JSON, unknown `type`, missing required fields, or invalid field values must produce a `ValidationResult.Invalid` or throw a `MalformedAIOutputException`.
2. **Safe failure.** Parsing failures must never mutate garden state. The orchestrator catches malformed interpretations and returns an error `AIResponse`.
3. **No silent defaults.** Missing required fields must fail, not be guessed.
4. **Confidence clamping.** Confidence values outside [0.0, 1.0] must be rejected.

### Validation Boundary

`AIOrchestrator` now validates every `AIInterpretation` before processing:

- `CommandProposals` with empty list → rejected
- `AICommandProposal` with blank `explanation` → rejected
- `AICommandProposal` with out-of-range `confidence` → rejected
- `ClarificationRequest` with blank `question` → rejected
- `Uncertainty` with blank `reason` → rejected
- `InformationalAnswer` with blank `message` → rejected
- `RecognitionResult` with blank `recognized` or out-of-range `confidence` → rejected

Validation is performed by `AIInterpretationValidator` in `commonMain`.

## Platform-Neutral Provider Implementation

The `LocalAIProvider` interface lives in `commonMain`. Platform-specific model runtimes must be isolated behind platform boundaries:

```
shared/src/commonMain/   ← LocalAIProvider interface, AIInterpretation, AIOrchestrator
shared/src/androidMain/  ← AndroidLocalAIProvider (wraps TFLite / LiteRT-LM / llama.cpp)
shared/src/iosMain/      ← IosLocalAIProvider (wraps Core ML / llama.cpp)
app/src/main/             ← Android-specific wiring (MainActivity)
```

### Android Runtime Options

| Runtime | Description | Platform dependency location |
|---------|-------------|------------------------------|
| TensorFlow Lite | Already in app dependencies. Supports quantized models via `.tflite`. | `androidMain` / `app` |
| LiteRT-LM | Google's successor to MediaPipe LLM Inference. Supports `.litertlm` format. | `androidMain` / `app` |
| llama.cpp (GGUF) | CPU-first inference via GGUF models. Requires NDK/JNI binding. | `androidMain` / `app` |
| ExecuTorch | PyTorch's on-device runtime. Early development for LLMs. | `androidMain` / `app` |

### iOS Runtime Options

| Runtime | Description | Platform dependency location |
|---------|-------------|------------------------------|
| Core ML | Apple's native ML framework. Supports converted LLMs. | `iosMain` |
| llama.cpp (GGUF) | Cross-platform GGUF inference. | `iosMain` |
| MLX Swift | Apple's MLX framework for LLM inference. | `iosMain` |

## Realistic Local-Model Options

### Option A: Quantized Small Language Models (Recommended for Phase 40+)

Run a 1B–3B parameter quantized model via llama.cpp or LiteRT-LM.

| Model | Parameters | License | Android feasibility | iOS feasibility | Notes |
|-------|-----------|---------|---------------------|-----------------|-------|
| Qwen3-1.7B | ~1.7B | Apache 2.0 | Good (INT4 ~1.3 GB) | Good | Strong general quality, permissive license |
| Qwen3-3B | ~3B | Apache 2.0 | Good (INT4 ~2.2 GB) | Good | Best risk-adjusted pick |
| Phi-4-mini | ~3.8B | MIT | Good (INT4 ~2.5 GB) | Good | Strongest reasoning in sub-4B class |
| Llama 3.2 1B | ~1B | Llama Community | Good (INT4 ~0.8 GB) | Good | Requires "Built with Llama" attribution |
| SmolLM3-3B | ~3B | Apache 2.0 | Good (INT4 ~2.2 GB) | Good | Fully open weights, training data, and code |

**Memory requirements:** 1B–3B INT4 models require 1–3 GB RAM at runtime. Suitable for mid-range devices (6 GB+ RAM).

**Structured output strategy:** Use GBNF grammars (llama.cpp) or constrained decoding to force JSON output matching the `AIInterpretation` schema.

### Option B: Google AI Edge / LiteRT-LM

Use Google's LiteRT-LM runtime with Gemma models.

| Model | Parameters | License | Notes |
|-------|-----------|---------|-------|
| Gemma-3 1B | ~1B | Gemma Terms | Google-supported, optimized for LiteRT |
| Gemma-3n E2B/E4B | ~2–4B | Gemma Terms | Multimodal (text + image) |

**Feasibility:** High on Android (LiteRT-LM is Google's supported path). MediaPipe LLM Inference is deprecated for Android/iOS; LiteRT-LM is the named successor.

**Limitation:** Gemma Terms require propagating terms to downstream users. Not as permissive as Apache 2.0 or MIT.

### Option C: TensorFlow Lite (Existing Dependency)

The project already includes TFLite in `app` dependencies.

**Feasibility:** TFLite supports quantized LLMs but has less mature LLM tooling than llama.cpp or LiteRT-LM. Better suited for the existing plant-recognition pipeline than for conversational LLMs.

**Recommendation:** Use TFLite for `PlantIdentifier` (vision). Use Option A or B for `LocalAIProvider` (text orchestration).

## Licensing Considerations

For commercial redistribution, prefer models with:

- **Apache 2.0** — No attribution required for products, no MAU caps. (Qwen3, SmolLM3, Granite)
- **MIT** — Permissive, no copyleft. (Phi-4-mini, MiniCPM)

Avoid models with:

- **Llama Community License** — Requires "Built with Llama" attribution; 700M MAU cap requires commercial license from Meta.
- **Gemma Terms** — Requires propagating terms to downstream users.
- **Custom non-commercial / research-only** — Hard no for production.

**Inference engine licensing:**
- **llama.cpp** — MIT license. Free for commercial use, modification, and distribution.
- **LiteRT-LM** — Apache 2.0.
- **ExecuTorch** — BSD-style license.

## Decision Matrix

| Criterion | Option A (llama.cpp + GGUF) | Option B (LiteRT-LM + Gemma) | Option C (TFLite) |
|-----------|------------------------------|------------------------------|-------------------|
| Offline operation | Yes | Yes | Yes |
| Android feasibility | Good | Good | Moderate |
| iOS feasibility | Good | Limited | Moderate |
| Structured output control | Excellent (GBNF) | Good | Moderate |
| Model size flexibility | Excellent | Moderate | Moderate |
| Commercial license clarity | Excellent (Apache 2.0 models) | Moderate (Gemma Terms) | Depends on model |
| Memory efficiency | Excellent (INT4 GGUF) | Good | Good |
| CPU-only fallback | Yes | No (GPU-preferred) | Yes |
| Platform-neutral shared code | Yes | Partial (Android-first) | Yes |

## Recommendation

For Soil & Supper's offline-first, cross-platform architecture:

1. **Immediate preparation (Phase 40):** Add `AIInterpretationValidator` to `commonMain` and document the `LocalAIProvider` contract. ✅ Completed.
2. **Model selection:** Target **Qwen3-1.7B** or **Qwen3-3B** (Apache 2.0) for structured-output-capable on-device inference.
3. **Android runtime:** Implement `AndroidLocalAIProvider` in `androidMain` using llama.cpp via GGUF with GBNF grammar constraints for JSON output.
4. **iOS runtime:** Implement `IosLocalAIProvider` in `iosMain` using llama.cpp or MLX Swift.
5. **Keep `commonMain` neutral:** All model runtime code stays in platform source sets. `LocalAIProvider` interface and `AIOrchestrator` remain unchanged.

## Separation from Vision ML

The conversational AI orchestration layer (`LocalAIProvider`) is separate from the plant-recognition ML pipeline (`PlantIdentifier` / TensorFlow Lite). The vision pipeline produces recognition results that can be fed into `AIRequest` as `AIInput.ImageReference`, but the two workstreams do not share runtime dependencies or model formats.
