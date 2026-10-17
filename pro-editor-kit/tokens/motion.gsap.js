/* pro-editor-kit motion helpers for HyperFrames / GSAP. Values mirror tokens/motion-tokens.json.
 * Load after gsap:  <script src="motion.gsap.js"></script>  then use window.ProMotion.
 * HyperFrames contract: ONE gsap.timeline({ paused: true }) per composition, registered at
 * window.__timelines["<data-composition-id>"] only after the build is complete.
 */
(function (root) {
  "use strict";
  var EASE = { out: "expo.out", in: "power3.in", inOut: "power3.inOut", soft: "power2.out", snap: "power4.out" };
  var DUR = { micro: 0.2, textIn: 0.4, textOut: 0.28, panel: 0.55, sceneTransition: 0.6, cameraMove: 2.5 };
  var STAGGER = { tight: 0.04, normal: 0.06, loose: 0.09, lines: 0.12 };

  function snap(t, fps) {
    return Math.round(t * (fps || 30)) / (fps || 30);
  }

  /** Paused, seekable timeline. Call register(id, tl) when finished building. */
  function timeline() {
    return root.gsap.timeline({ paused: true });
  }

  function register(id, tl) {
    root.__timelines[id] = tl;
    return tl;
  }

  /** Fade + rise entrance at time `at` (seconds), frame-snapped. */
  function enter(tl, targets, at, opts) {
    var o = opts || {};
    return tl.fromTo(
      targets,
      { autoAlpha: 0, y: o.y === undefined ? 24 : o.y, scale: o.from || 1 },
      {
        autoAlpha: 1,
        y: 0,
        scale: 1,
        duration: o.duration || DUR.textIn,
        ease: o.ease || EASE.out,
        stagger: o.stagger === undefined ? STAGGER.normal : o.stagger,
      },
      snap(at, o.fps),
    );
  }

  /** Exit at time `at`; ~70% of entrance duration, eases in. */
  function exit(tl, targets, at, opts) {
    var o = opts || {};
    return tl.to(
      targets,
      { autoAlpha: 0, y: o.y === undefined ? -12 : o.y, duration: o.duration || DUR.textIn * 0.7, ease: EASE.in },
      snap(at, o.fps),
    );
  }

  /** Word-by-word caption pop driven by captions.pages.json from tools/captions.py. */
  function captionPages(tl, container, pages, opts) {
    var o = opts || {};
    var doc = root.document;
    pages.forEach(function (page) {
      var line = doc.createElement("div");
      line.className = o.lineClass || "cap-line";
      line.style.opacity = "0";
      page.words.forEach(function (w) {
        var span = doc.createElement("span");
        span.textContent = w.text + " ";
        span.className = w.emphasis ? o.emphasisClass || "cap-em" : o.wordClass || "cap-w";
        line.appendChild(span);
        tl.fromTo(span, { autoAlpha: 0, y: 10, scale: 0.94 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.16, ease: EASE.soft }, snap(w.start, o.fps));
      });
      container.appendChild(line);
      tl.set(line, { opacity: 1 }, snap(page.start, o.fps));
      tl.set(line, { opacity: 0 }, snap(page.end, o.fps));
    });
    return tl;
  }

  root.ProMotion = { EASE: EASE, DUR: DUR, STAGGER: STAGGER, snap: snap, timeline: timeline, register: register, enter: enter, exit: exit, captionPages: captionPages };
})(typeof window !== "undefined" ? window : globalThis);
