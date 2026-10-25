> **Готовая новая версия:** [The Unsupported Leap — 49 s, 1080p, озвучка и исходники](production/README.md).

> **Новая сценарная разработка:** [The Unsupported Leap — 49 s, сценарий и визуальная режиссура](preproduction/README.md). MP4 ниже — ранний эскиз; готовый ролик находится в `production/`.

# JERP motion marketing film

`output/jerp-marketing.mp4`: 30 seconds, 1280×720, 24 fps, H.264/AAC,
English titles and original synthesized electronic audio. Six scenes cover
question, guard, verdict, speaker, workflow and call to action.

## Render

Requires Python 3, Pillow, NumPy, FFmpeg, and DejaVu Sans at the path declared
in `film.py`. From `/workspace/jerp-test`:

```sh
python video/film.py
```

The render is deterministic and uses no external assets. `film.py` builds
perspective-projected rotating 3D geometry, vector-style cards and typography,
scene wipes, and the original score. Edit `scenes`, timings, colors and `orb`
to change the film. The public film is a conceptual product explanation,
not a recording of authenticated MCP responses.

## Research

Reviewed 2026-10-25:
- https://getjerp.com/ — homepage copy and public tool descriptions.
- https://getjerp.com/llms-full.txt — public guard/verdict/speaker contract.
- https://getjerp.com/jerp-court-desktop.mp4 — existing 37.3-second homepage
  reference, sampled at 5 and 18 seconds. Reference footage is not reused.

Do not imply guaranteed prompt-injection protection, universal accuracy,
or invented savings percentages. The film contains no such guarantees.

## Outputs and checks

- `output/storyboard.jpg`: six sampled scenes.
- `output/score.wav`: original synthesized stereo bed.
- `output/picture.mp4`: silent intermediate.
- `output/jerp-marketing.mp4`: final mux, verified as 30 seconds with H.264
  1280×720 at 24 fps and AAC audio; full decode completed without errors.

`render.py` is the earlier standalone Blender 3D study. Blender 4.3.2 renders
its editable `output/jerp-motion.blend` and PNG frames. It is independent of
the full marketing film, which uses its own procedural 3D projection code.
