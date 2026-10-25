# JERP — The Unsupported Leap

**49 seconds · 1920×1080 · 30 fps · English neural VO · original score/SFX**

[Download / open the final MP4](output/jerp-the-unsupported-leap.mp4) · [Actual film frames](output/contact-sheet.jpg) · [Subtitles](output/jerp-film.srt)

![Animated excerpts — not the complete film](output/preview.gif)

This production follows the [source-led scenario](../preproduction/SCENARIO-RU.md):
a fictional time-tracker page offers a free trial, while an AI draft invents
“free forever” and “best choice.” JERP's guard, verdict and speaker are explained
through one continuing example, ending in a compact answer with its source.

The fictional demonstration is marked in the picture. It is not a recording of
authenticated MCP results. No confidence percentage, benchmark saving or
complete-protection promise is fabricated.

## Production stack

| Tool | Actual role |
|---|---|
| ASTRA | Motion direction and authored Remotion scenes; one implementation agent, followed by targeted visual feedback |
| Remotion 4.0.538 / React 19.3.1 | Frame-accurate 1470-frame timeline, frame-driven motion, text, composition and rendering |
| CSS 3D | Perspective, explicit front/back/side faces, thickness, source bridge, articulated folding panels and card-to-answer morph |
| Original JERP fonts and graphics | Locally loaded Bitcount and Barlow, CSS wordmark rules, favicon/orb, graphite/glass palette and primary-blue accent |
| HyperFrames 0.8.198 | Local audio loudness, silence, moment and clipping analysis; retained JSON reports |
| Kokoro ONNX | Local neural English voice, `af_heart`; no hosted voice service or real-person voice clone |
| Python / NumPy | Original deterministic ambient score and tactile transitions |
| FFmpeg | Stem restoration, music ducking, two-pass loudness mix, H.264/AAC mux and full decode verification |

Three.js, `@remotion/three`, React Three Fiber and GSAP are installed and pinned
for further production work. The final film uses the CSS 3D route; it does not
claim an unused WebGL or Blender path was used. This avoids software-WebGL
bottlenecks on the four effective CPU cores while preserving actual perspective
and articulated 3D planes. HyperFrames is not a second redundant timeline.

## Watch / edit / rebuild

Required: Node.js 22+, npm, Python 3, FFmpeg/ffprobe and Chromium.
The verified browser is `/usr/bin/chromium`; edit `scripts/render.mjs` and
`remotion.config.ts` if the executable is elsewhere.

From this directory:

```sh
npm ci --cache /workspace/.cache/npm
npm run studio
```

To rebuild the **complete** final film, including audio, from the retained
lossless authored stems (no TTS model download needed):

```sh
npm run typecheck
npm run build
```

`npm run build` decodes FLAC stems, rebuilds the mix, renders the picture and
muxes `output/jerp-the-unsupported-leap.mp4`. The Python mixing script uses only
the standard library. Full rendering uses two concurrent browser workers.

A quicker complete motion draft:

```sh
node scripts/build.mjs --draft
```

This writes a 960×540 / 15 fps review movie. Native stills:

```sh
npm run stills
```

The final 90 frames are deterministic and visually identical: the CTA has
three seconds of uninterrupted reading time.

## Change narration or generate new music

The retained FLAC stems are sufficient to rebuild the current film. To change
speech, install the isolated Python audio dependencies:

```sh
python3 -m venv /workspace/.cache/jerp-tts-venv
/workspace/.cache/jerp-tts-venv/bin/pip install -r requirements-audio.txt
```

Download the upstream Kokoro model and voices with normal TLS verification:

```sh
mkdir -p /workspace/.cache/jerp-tts-models
curl -L --fail https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx -o /workspace/.cache/jerp-tts-models/kokoro-v1.0.onnx
curl -L --fail https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin -o /workspace/.cache/jerp-tts-models/voices-v1.0.bin
```

The retrieved file SHA-256s and upstream URLs are retained in
`public/audio/provenance.json`. The model weights are not in Git. Upstream
lists the runtime as MIT and the model as Apache-2.0.

The authored VO lines/timing are in `public/story.json`. After editing,
remove only the affected generated `public/audio/voiceover-cues/NN-raw.wav`
cache, then run:

```sh
/workspace/.cache/jerp-tts-venv/bin/python scripts/make_audio.py
python3 scripts/mix_audio.py
```

When replacing WAV stems, refresh the corresponding lossless FLAC files before
committing: `npm run build` restores from retained FLAC. Subtitles are cue-aligned
to the synthesized clips, not falsely advertised as word-level ASR alignment.

## Files

- `entry.ts`, `src/`, `remotion.config.ts`: actual animation source.
- `scripts/`: picture rendering, synthesis, mix, mux, contact sheet and reproducible build.
- `public/brand/`: original local site font assets and favicon.
- `public/audio/*.flac`: lossless VO, score and SFX stems.
- `public/audio/provenance.json`: cue durations and synthesis provenance.
- `output/jerp-the-unsupported-leap.mp4`: final web-playable film.
- `output/jerp-film.srt`: English captions timed to the actual voice cues.
- `output/QA.json`: measured final checks and explicit scope.
- `output/*analysis.json`: actual HyperFrames local audio reports.
- `output/render-source-hashes.json`: frozen source/package-lock hashes used for render.

Original production stills and the complete draft are local QA intermediates;
Git retains the final movie, poster, contact sheet, captions and reports.
