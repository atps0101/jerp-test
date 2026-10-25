# Production tools

- `render.mjs stills`: nine native-resolution Remotion frames for visual inspection.
- `render.mjs draft`: complete 49-second edit at 960×540, 15 fps for motion QA.
- `render.mjs full` (default): complete 1920×1080, 30 fps picture-only master.
- `make_audio.py`: neural English voice cues plus deterministic original music/SFX. Requires the isolated Kokoro Python dependencies and models documented in the production README.
- `mix_audio.py`: speech EQ/compression, music ducking and two-pass EBU loudness normalization.
- `mux.mjs`: combine final picture and audio into a web-playable H.264/AAC MP4; `--draft` combines the draft instead.
- `contact_sheet.py`: grid of the nine current native rendered stills.

The renderer uses the existing `/usr/bin/chromium`, two concurrent workers,
and the system's four effective CPU cores. It reuses the pinned local packages
and bundler cache. No hosted render or paid TTS is invoked.
