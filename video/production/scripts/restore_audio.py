"""Restore authored, lossless FLAC stems for mixing without downloading a TTS model."""
from pathlib import Path
import soundfile as sf
root=Path(__file__).resolve().parents[1]/'public/audio'
for stem in ['voiceover','music','sfx']:
 samples,rate=sf.read(root/f'{stem}.flac')
 sf.write(root/f'{stem}.wav',samples,rate,subtype='PCM_24')
 print('Restored',stem)
