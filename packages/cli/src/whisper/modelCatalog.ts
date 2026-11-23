/**
 * The whisper.cpp models `transcribe` can download, including the latest
 * large-v3-turbo family.
 *
 * ADDITIVE ONLY: nothing here changes how a model is chosen, named or fetched.
 * `manager.ts` keeps `DEFAULT_MODEL = "small.en"` and builds every URL as
 * `ggml-<id>.bin`, so any id below already worked with `ensureModel(id)` — this
 * module just makes the set discoverable instead of tribal knowledge.
 *
 * Sizes and availability are deliberately NOT baked in: they are whatever
 * Hugging Face serves at download time. The ids follow the upstream
 * ggerganov/whisper.cpp naming, where `-q5_0` / `-q8_0` are quantised builds and
 * a `.en` suffix marks an English-only model.
 */
export interface WhisperModelInfo {
  /** The id passed to `ensureModel` / `--model`; the file is `ggml-<id>.bin`. */
  id: string;
  label: string;
  /** English-only (`.en`) models are smaller and faster but cannot transcribe other languages. */
  englishOnly: boolean;
  /** Quantised builds trade a little accuracy for a much smaller download. */
  quantised: boolean;
  family: "tiny" | "base" | "small" | "medium" | "large";
}

const entry = (id: string, label: string, family: WhisperModelInfo["family"]): WhisperModelInfo => ({
  id,
  label,
  englishOnly: id.endsWith(".en"),
  quantised: /-q\d/.test(id),
  family,
});

export const WHISPER_MODELS: readonly WhisperModelInfo[] = [
  entry("tiny", "Tiny — fastest, lowest accuracy", "tiny"),
  entry("tiny.en", "Tiny (English only)", "tiny"),
  entry("base", "Base", "base"),
  entry("base.en", "Base (English only)", "base"),
  entry("small", "Small — the default balance", "small"),
  entry("small.en", "Small (English only) — current default", "small"),
  entry("medium", "Medium", "medium"),
  entry("medium.en", "Medium (English only)", "medium"),
  entry("large-v1", "Large v1", "large"),
  entry("large-v2", "Large v2", "large"),
  entry("large-v3", "Large v3 — highest accuracy, slowest", "large"),
  entry("large-v3-q5_0", "Large v3 (quantised q5_0)", "large"),
  entry("large-v3-turbo", "Large v3 Turbo — near-v3 accuracy, much faster", "large"),
  entry("large-v3-turbo-q5_0", "Large v3 Turbo (quantised q5_0)", "large"),
  entry("large-v3-turbo-q8_0", "Large v3 Turbo (quantised q8_0)", "large"),
];

export function isKnownWhisperModel(id: string): boolean {
  return WHISPER_MODELS.some((m) => m.id === id);
}

/** The newest general-purpose recommendation. Not a default — `manager.ts` still
 *  defaults to `small.en`; this is only what a caller may offer as "latest". */
export const LATEST_WHISPER_MODEL = "large-v3-turbo";

export function modelsForFamily(family: WhisperModelInfo["family"]): WhisperModelInfo[] {
  return WHISPER_MODELS.filter((m) => m.family === family);
}
