/**
 * pro-editor-kit motion helpers for Remotion.
 * Copy into remotion/src (or import by relative path). Values mirror tokens/motion-tokens.json.
 * Everything is a pure function of the frame: safe for seeking, Lambda and parallel renders.
 */
import { Easing, interpolate, spring } from "remotion";

export const EASE = {
  out: Easing.bezier(0.16, 1, 0.3, 1),
  in: Easing.bezier(0.7, 0, 0.84, 0),
  inOut: Easing.bezier(0.65, 0, 0.35, 1),
  soft: Easing.bezier(0.33, 1, 0.68, 1),
  snap: Easing.bezier(0.2, 0.9, 0.1, 1),
} as const;

export const SPRING = {
  gentle: { damping: 20, mass: 1, stiffness: 120 },
  snappy: { damping: 14, mass: 0.6, stiffness: 180 },
  pop: { damping: 12, mass: 0.7, stiffness: 200 },
  heavy: { damping: 22, mass: 1.2, stiffness: 90 },
} as const;

export const DUR = {
  micro: 0.2,
  textIn: 0.4,
  textOut: 0.28,
  panel: 0.55,
  sceneTransition: 0.6,
  cameraMove: 2.5,
} as const;

/** Seconds -> whole frames (motion must start and end on a frame). */
export const sec = (fps: number, seconds: number): number => Math.round(seconds * fps);

/** 0..1 entrance progress starting at `startFrame`, clamped, eased out. */
export const enter = (
  frame: number,
  fps: number,
  startFrame: number,
  seconds: number = DUR.textIn,
  easing: (t: number) => number = EASE.out,
): number =>
  interpolate(frame, [startFrame, startFrame + Math.max(1, sec(fps, seconds))], [0, 1], {
    easing,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

/** 1..0 exit progress ending at `endFrame`; exits run ~70% of the entrance and ease in. */
export const exit = (
  frame: number,
  fps: number,
  endFrame: number,
  seconds: number = DUR.textIn * 0.7,
): number =>
  interpolate(frame, [endFrame - Math.max(1, sec(fps, seconds)), endFrame], [1, 0], {
    easing: EASE.in,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

/** Spring with a named preset; never use the bouncy default config. */
export const springIn = (
  frame: number,
  fps: number,
  startFrame: number,
  preset: keyof typeof SPRING = "snappy",
): number => spring({ frame: frame - startFrame, fps, config: SPRING[preset] });

/** Start frame for sibling `index` in a staggered group (default 60 ms apart). */
export const stagger = (fps: number, startFrame: number, index: number, seconds = 0.06): number =>
  startFrame + Math.round(index * seconds * fps);

/** Minimum frames a text must stay fully visible to be read: 0.3 s + 0.06 s per word. */
export const holdFrames = (fps: number, words: number): number => Math.ceil((0.3 + 0.06 * words) * fps);

/** Pop scale with capped overshoot (<= 1.08) from a 0..1 progress. */
export const popScale = (progress: number, from = 0.92, overshoot = 1.06): number =>
  progress < 0.7
    ? interpolate(progress, [0, 0.7], [from, overshoot], { extrapolateLeft: "clamp" })
    : interpolate(progress, [0.7, 1], [overshoot, 1], { extrapolateRight: "clamp" });

/** Alternating punch-in scale per cut segment to hide jump cuts (never two equal scales in a row). */
export const punchIn = (segmentIndex: number, scales: readonly number[] = [1, 1.12]): number =>
  scales[segmentIndex % scales.length];

/** Title/caption-safe rectangle in pixels for the current canvas. */
export const safeArea = (width: number, height: number) => {
  const vertical = height > width;
  const x = Math.round(width * (vertical ? 0.08 : 0.1));
  const top = Math.round(height * (vertical ? 0.12 : 0.1));
  const bottom = Math.round(height * (vertical ? 0.18 : 0.1));
  return { x, y: top, width: width - 2 * x, height: height - top - bottom, vertical };
};
