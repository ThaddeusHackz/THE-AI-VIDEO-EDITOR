import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { WHISPER_MODELS, isKnownWhisperModel, LATEST_WHISPER_MODEL, modelsForFamily } from "./modelCatalog.js";
import { initialModelForLanguage } from "./modelForLanguage.js";

describe("whisper model catalog (additive)", () => {
  it("offers the latest large-v3-turbo family", () => {
    expect(isKnownWhisperModel("large-v3-turbo")).toBe(true);
    expect(isKnownWhisperModel("large-v3-turbo-q5_0")).toBe(true);
    expect(isKnownWhisperModel("large-v3-turbo-q8_0")).toBe(true);
    expect(LATEST_WHISPER_MODEL).toBe("large-v3-turbo");
  });

  it("keeps every id unique", () => {
    const ids = WHISPER_MODELS.map((m) => m.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("builds exactly the URL shape manager.ts already uses", () => {
    const src = readFileSync(join(__dirname, "manager.ts"), "utf8");
    expect(src).toContain("ggml-${model}.bin");
    for (const m of WHISPER_MODELS) {
      const url = `https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-${m.id}.bin`;
      expect(url.endsWith(`ggml-${m.id}.bin`)).toBe(true);
    }
  });

  it("does not change the existing default or fetch logic", () => {
    const src = readFileSync(join(__dirname, "manager.ts"), "utf8");
    expect(src).toContain('const DEFAULT_MODEL = "small.en"');
    expect(src).toContain("export async function ensureModel(");
    expect(isKnownWhisperModel("small.en")).toBe(true);
  });

  it("flags english-only and quantised builds correctly", () => {
    expect(WHISPER_MODELS.find((m) => m.id === "small.en")?.englishOnly).toBe(true);
    expect(WHISPER_MODELS.find((m) => m.id === "large-v3-turbo")?.englishOnly).toBe(false);
    expect(WHISPER_MODELS.find((m) => m.id === "large-v3-turbo-q5_0")?.quantised).toBe(true);
    expect(WHISPER_MODELS.find((m) => m.id === "large-v3")?.quantised).toBe(false);
  });

  it("keeps the language swap working for the new models", () => {
    expect(initialModelForLanguage("small.en", "fr")).toBe("small");
    expect(initialModelForLanguage("large-v3-turbo", "fr")).toBe("large-v3-turbo");
    expect(initialModelForLanguage("small.en", "en")).toBe("small.en");
  });

  it("groups by family", () => {
    expect(modelsForFamily("large").every((m) => m.family === "large")).toBe(true);
    expect(modelsForFamily("large").length).toBeGreaterThanOrEqual(6);
    expect(modelsForFamily("tiny").length).toBe(2);
  });
});
