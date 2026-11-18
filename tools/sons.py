# NOCTURNE - writes the factory sounds shipped with the installer (menu SOUNDS) into Presets/Sounds.
# Each sound only lists what differs from the default settings: Nocturne fills in the rest when it loads it.
# Every sound is programmed from scratch on Nocturne by sound type: no factory data or patch of any other
# instrument is copied. A sound can carry a sequence (SEQ ...): press PLAY in SEQUENCER to hear it.
# Usage:  python3 tools/sons.py      then  bash tools/paquet.sh
import os, glob
from xml.sax.saxutils import quoteattr

# Shapes: 0 triangle, .33 saw, .66 square, 1 narrow pulse. Ranges: 0 = 64' ... 3 = 8' ... 5 = 2'.
# oscLayer: 0 = VCO 1 only, 1 = VCO 2 only. POLY-MOD: polyEnv / polyOsc (-1..1) into polyFreq / polyWidth / polyFilter.
# Sequence text: steps separated by ';', notes by ',', 'r' = rest (MIDI note numbers, 60 = C4).
# Nocturne: the multimode filter (filterAType 2) at 12 dB by default; filterMode 0 = low-pass, .5 = notch, 1 = high-pass;
# filterBP = band-pass. chordOn + chord ("0,4,7": intervals above the key) = CHORD memory. voiceSpread 0 alternate, 1 pitch, 2 random.
# NOCTURNE: every factory sound uses the two layers (DUAL). Layer I = VCO 1 > filter I (multimode) > its envelopes;
# layer II = VCO 2 > filter II > its own envelopes; oscLayer mixes them (0 = I only, 1 = II only).
# Filter envelopes are levelled: from I.L (also where they settle) to A.L over the attack, back to I.L over the decay.
# Expression is stored in each sound: pressure (atFilter / atVolume / atPitch / atLfo), velocity, the ribbon's range.
BASE = {"mode": 1, "jupiterMix": 1, "osc1Shape": 6, "osc2Shape": 6, "envLink": 0, "chorusMode": 0, "dualLayer": 1,
        "filterAType": 2, "slope": 0, "filterBType": 1, "slopeB": 0, "hpfFreq": .27, "hpfII": .2, "age": .45, "voiceWidth": .8}

def one(wave=.33, octave=3, cut=800, res=.2, env=.4, il=.15, al=.8, fa=.05, fd=1.0, fr=.8, a=.01, d=1.0, s=.85, r=.7, **more):
    """Layer I: VCO 1, filter I and its two envelopes."""
    return dict(vco1Wave=wave, osc1Octave=octave, cutoff=cut, resonance=res, env=env, fsustain=il, al1=al, fattack=fa, fdecay=fd,
                frelease=fr, attack=a, decay=d, sustain=s, release=r, **more)

def two(wave=.33, octave=3, tune=0, fine=7, cut=900, res=.2, env=.35, il=.15, al=.8, fa=.05, fd=1.0, fr=.8, a=.01, d=1.0, s=.85, r=.7, **more):
    """Layer II: VCO 2 (semitones and cents), filter II and its two envelopes."""
    return dict(vco2Wave=wave, osc2Octave=octave, osc2Tune=tune, detune=fine, cutoffB=cut, resonanceB=res, envB=env, fs2=il, al2=al,
                fa2=fa, fd2=fd, fr2=fr, attack2=a, decay2=d, sustain2=s, release2=r, **more)

def sound(layer1, layer2, mix=.5, **rest):
    return dict(BASE, **layer1, **layer2, oscLayer=mix, **rest)

HALL = dict(reverbType=2, reverbSize=.85, reverbMix=.26)
ROOM = dict(reverbType=1, reverbSize=.55, reverbMix=.16)
VIBRATO = dict(lfoShape=1, rate=5.4, lfoDelay=.8, lfoPitch=.14, wheelDepth=.4)

SOUNDS = {
    # ==== A: brass that swells under the fingers (pressure opens, lifts and drives)
    "BRASS - Night Brass": sound(one(cut=380, env=.5, il=.1, al=.75, fa=.22, fd=1.4, a=.05, d=1.5, s=.9, r=.6),
        two(fine=8, cut=520, env=.4, il=.12, al=.7, fa=.35, fd=1.8, a=.08, d=1.5, s=.9, r=.7),
        atFilter=.5, atVolume=.25, velFilter=.3, **VIBRATO, **ROOM, gain=.6),
    "BRASS - Pressure Swell": sound(one(cut=260, res=.15, env=.35, il=.05, al=.5, fa=.6, fd=2.0, a=.35, d=2.0, s=1, r=.8),
        two(fine=-6, cut=330, env=.3, il=.05, al=.45, fa=.8, fd=2.2, a=.45, d=2.0, s=1, r=.9),
        atFilter=.8, atVolume=.6, atDrive=.3, wheelDepth=.3, **HALL, gain=.7),
    "BRASS - Rising Octave": sound(one(cut=420, env=.45, il=.1, al=.75, fa=.15, fd=1.2, a=.03, d=1.2, s=.85, r=.5),
        two(octave=4, fine=4, cut=700, env=.35, il=.1, al=.6, fa=.9, fd=1.5, a=.9, d=2.0, s=.9, r=.8),
        mix=.42, atFilter=.45, atVolume=.3, **ROOM, gain=.6),
    "BRASS - Wah Horns": sound(one(cut=500, res=.35, env=.5, il=.55, al=.05, fa=.18, fd=.6, a=.02, d=1.0, s=.85, r=.4),
        two(fine=9, cut=650, res=.3, env=.45, il=.5, al=.05, fa=.22, fd=.7, a=.02, d=1.0, s=.85, r=.45),
        atFilter=.4, **ROOM, gain=.6),
    "BRASS - Low Section": sound(one(octave=2, cut=300, env=.5, il=.1, al=.8, fa=.12, fd=1.0, a=.03, d=1.2, s=.85, r=.45),
        two(octave=3, fine=6, cut=420, env=.4, il=.1, al=.7, fa=.2, fd=1.2, a=.05, d=1.2, s=.85, r=.5),
        mix=.45, atFilter=.5, atDrive=.4, voiceDrive=.3, **ROOM, gain=.6),
    "BRASS - Bright Stabs": sound(one(cut=650, env=.6, il=.05, al=.9, fa=.003, fd=.35, a=.003, d=.45, s=.4, r=.25),
        two(tune=7, fine=5, cut=800, env=.5, il=.05, al=.85, fa=.004, fd=.4, a=.003, d=.5, s=.35, r=.25),
        mix=.4, velFilter=.45, voiceDrive=.35, **ROOM, delaySync=6, delayFeedback=.25, delayMix=.1, gain=.6),
    "BRASS - Ribbon Fanfare": sound(one(cut=450, env=.5, il=.1, al=.8, fa=.1, fd=1.0, a=.02, d=1.0, s=.9, r=.5),
        two(fine=10, cut=600, env=.45, il=.1, al=.75, fa=.12, fd=1.1, a=.02, d=1.0, s=.9, r=.5),
        voiceMode=1, legato=1, portamento=.06, ribbonRange=2, atFilter=.5, atPitch=.3, **VIBRATO, **ROOM, gain=.8),
    "BRASS - Felt Horns": sound(one(wave=.15, cut=330, res=.1, env=.4, il=.1, al=.6, fa=.3, fd=1.5, a=.12, d=1.5, s=.9, r=.9),
        two(wave=.5, fine=5, cut=420, res=.1, env=.35, il=.1, al=.55, fa=.4, fd=1.6, a=.15, d=1.5, s=.9, r=.9),
        atFilter=.45, atVolume=.35, chorusMode=1, chorus=.3, **HALL, gain=.75),
    # ==== B: pads that cry (pressure bends the pitch up), dark pads
    "PAD - Crying Strings": sound(one(cut=1200, res=.15, env=.2, il=.1, al=.5, fa=1.0, fd=2.5, a=.9, d=2.0, s=.95, r=2.5),
        two(fine=11, cut=1500, env=.2, il=.1, al=.45, fa=1.2, fd=2.5, a=1.1, d=2.0, s=.95, r=2.8),
        atPitch=.6, atFilter=.35, atVolume=.25, ribbonRange=1, **VIBRATO, chorusMode=2, chorus=.35, **HALL, gain=.65),
    "PAD - Weeping Choir": sound(one(wave=.6, cut=800, res=.55, env=.2, il=.15, al=.5, fa=1.2, fd=2.5, a=1.0, d=2.0, s=.9, r=2.6, filterBP=1),
        two(wave=.4, tune=12, fine=6, cut=1400, res=.4, env=.15, il=.1, al=.4, fa=1.6, fd=3.0, a=1.4, d=2.0, s=.9, r=3.0),
        mix=.4, atPitch=.5, atMode=.4, vcoPwm=.3, **VIBRATO, chorusMode=2, chorus=.4, **HALL, gain=.75),
    "PAD - Dark Hall": sound(one(octave=2, cut=320, res=.25, env=.25, il=.2, al=.6, fa=2.0, fd=4.0, a=1.5, d=3.0, s=.95, r=4.0),
        two(octave=3, fine=-9, cut=420, res=.2, env=.2, il=.15, al=.5, fa=2.5, fd=4.0, a=2.0, d=3.0, s=.95, r=4.5),
        mix=.45, atFilter=.5, age=.7, reverbType=2, reverbSize=.95, reverbMix=.34, gain=.8),
    "PAD - Slow Tide": sound(one(cut=700, env=.3, il=.2, al=.7, fa=.6, fd=2.5, a=.4, d=2.0, s=.9, r=2.5),
        two(octave=4, fine=5, cut=1600, res=.3, env=.25, il=.1, al=.6, fa=4.0, fd=5.0, a=4.0, d=3.0, s=.9, r=4.0),
        mix=.45, atFilter=.35, rate=.08, lfoFilter=.6, lfoShape=1, chorusMode=1, chorus=.3, **HALL, gain=.6),
    "PAD - Midnight Glass": sound(one(cut=900, res=.2, env=.2, il=.2, al=.5, fa=.8, fd=2.0, a=.6, d=2.0, s=.9, r=3.0),
        two(wave=.66, octave=4, fine=3, cut=2600, res=.35, env=.15, il=.15, al=.4, fa=1.5, fd=3.0, a=1.2, d=2.0, s=.9, r=3.5, hpfII=.75),
        mix=.4, ringDepth=.18, ringSpeed=3, atFilter=.3, **HALL, delaySync=5, delayFeedback=.35, delayMix=.12, gain=.6),
    "PAD - Moon Drift": sound(one(cut=1000, res=.3, env=.2, il=.2, al=.55, fa=1.0, fd=2.5, a=.8, d=2.0, s=.9, r=3.0),
        two(fine=14, cut=1100, res=.3, env=.2, il=.2, al=.55, fa=1.4, fd=2.5, a=1.0, d=2.0, s=.9, r=3.0),
        age=.9, voiceSpread=2, voiceWidth=1, rate=.12, lfoFilter=.7, lfoShape=1, atLfo=.5, chorusMode=2, chorus=.4, **HALL, gain=.65),
    "PAD - Sorrow Strings": sound(one(cut=1500, res=.12, env=.15, il=.1, al=.4, fa=1.5, fd=3.0, a=1.6, d=2.0, s=.95, r=3.0, hpfFreq=.4),
        two(tune=-12, fine=7, cut=700, env=.2, il=.1, al=.4, fa=2.0, fd=3.0, a=2.2, d=2.0, s=.95, r=3.5),
        mix=.35, atPitch=.4, atVolume=.35, ribbonRange=1, **VIBRATO, chorusMode=3, chorus=.4, **HALL, gain=.65),
    "PAD - Deep Velvet": sound(one(wave=.05, octave=2, cut=500, res=.1, env=.25, il=.2, al=.5, fa=1.0, fd=2.0, a=.7, d=2.0, s=.95, r=2.5),
        two(fine=6, cut=600, res=.15, env=.25, il=.15, al=.5, fa=1.3, fd=2.5, a=.9, d=2.0, s=.95, r=2.8),
        mix=.5, atFilter=.5, atVolume=.25, vcoSub=.3, chorusMode=1, chorus=.3, **HALL, gain=.7),
    # ==== C: bells and keys (the ring modulator; KEY makes it play in tune with the keyboard)
    "BELL - Ring Bells": sound(one(wave=0, cut=3000, env=.2, il=0, al=.6, fa=.002, fd=1.5, a=.002, d=2.5, s=0, r=2.0),
        two(wave=.0, octave=4, tune=7, fine=0, cut=4000, env=.2, il=0, al=.5, fa=.002, fd=1.0, a=.002, d=1.5, s=0, r=1.5),
        mix=.35, ringDepth=1, ringSpeed=610, ringKey=1, ringDecay=1.4, velFilter=.3, **HALL, delaySync=5, delayFeedback=.3, delayMix=.12, gain=.85),
    "BELL - Glass Chimes": sound(one(wave=0, octave=4, cut=5000, env=.1, il=0, al=.4, fa=.002, fd=1.0, a=.002, d=1.8, s=0, r=1.8),
        two(wave=0, octave=5, fine=0, cut=6000, env=.1, il=0, al=.4, fa=.002, fd=.8, a=.002, d=1.2, s=0, r=1.2),
        mix=.3, ringDepth=.85, ringSpeed=1400, ringKey=1, ringDecay=2.5, reverbType=2, reverbSize=.9, reverbMix=.32, gain=.9),
    "BELL - Temple Gong": sound(one(wave=.1, octave=2, cut=1800, res=.2, env=.2, il=0, al=.6, fa=.003, fd=3.0, a=.003, d=6.0, s=0, r=5.0),
        two(wave=0, octave=3, tune=6, fine=0, cut=2400, env=.15, il=0, al=.5, fa=.004, fd=2.0, a=.004, d=5.0, s=0, r=4.5),
        mix=.4, ringDepth=.9, ringSpeed=87, ringDecay=6.0, reverbType=2, reverbSize=.95, reverbMix=.36, gain=.9),
    "BELL - Ice Mallets": sound(one(wave=.05, cut=2800, res=.25, env=.35, il=0, al=.7, fa=.001, fd=.4, a=.001, d=.9, s=0, r=.8),
        two(wave=.66, octave=4, fine=0, cut=3500, env=.3, il=0, al=.6, fa=.001, fd=.3, a=.001, d=.6, s=0, r=.6),
        mix=.35, ringDepth=.6, ringSpeed=785, ringKey=1, ringDecay=.5, velFilter=.4, **ROOM, delaySync=6, delayFeedback=.3, delayMix=.12, gain=.9),
    "KEYS - Felt Keys": sound(one(wave=.2, cut=900, res=.1, env=.4, il=.05, al=.8, fa=.002, fd=1.2, a=.002, d=2.5, s=.15, r=.8),
        two(octave=4, fine=3, cut=1600, env=.35, il=0, al=.7, fa=.002, fd=.5, a=.002, d=.9, s=0, r=.5),
        mix=.3, velFilter=.6, velocity=.6, chorusMode=1, chorus=.25, **ROOM, gain=.8),
    "KEYS - Ring Tremolo": sound(one(cut=1300, env=.4, il=.05, al=.7, fa=.002, fd=1.0, a=.002, d=2.0, s=.3, r=.7),
        two(wave=.66, fine=4, cut=1500, env=.3, il=.05, al=.6, fa=.002, fd=.8, a=.002, d=1.6, s=.25, r=.7),
        ringDepth=.55, ringSpeed=4.5, velFilter=.4, chorusMode=1, chorus=.25, **ROOM, gain=.8),
    "KEYS - Dual Clav": sound(one(wave=.85, cut=1300, res=.5, env=.5, il=0, al=.8, fa=.001, fd=.25, a=.001, d=.5, s=.1, r=.2, filterBP=1),
        two(wave=.95, octave=4, fine=2, cut=2400, res=.3, env=.4, il=0, al=.7, fa=.001, fd=.2, a=.001, d=.4, s=.05, r=.15),
        mix=.4, velFilter=.5, phaserOn=1, phaserRate=.4, phaserDepth=.5, phaserMix=.3, gain=.95),
    "KEYS - Silver Harpsi": sound(one(wave=.9, cut=2200, res=.15, env=.4, il=0, al=.6, fa=.001, fd=.8, a=.001, d=1.6, s=0, r=.6),
        two(wave=.75, octave=4, fine=4, cut=3000, env=.3, il=0, al=.5, fa=.001, fd=.6, a=.001, d=1.2, s=0, r=.5, hpfII=.6),
        mix=.45, velFilter=.3, **ROOM, gain=.85),
    # ==== D: leads and basses (the ribbon: slide the pitch, pressure for the cry)
    "LEAD - Ribbon Solo": sound(one(cut=900, res=.3, env=.4, il=.15, al=.8, fa=.03, fd=.9, a=.01, d=1.0, s=.9, r=.4),
        two(fine=9, cut=1200, res=.25, env=.35, il=.15, al=.75, fa=.04, fd=1.0, a=.01, d=1.0, s=.9, r=.4),
        voiceMode=1, legato=1, portamento=.05, ribbonRange=2, atFilter=.5, atVolume=.2, **VIBRATO,
        delaySync=5, delayFeedback=.35, delayMix=.15, **ROOM, gain=.9),
    "LEAD - Crying Lead": sound(one(cut=700, res=.45, env=.35, il=.2, al=.7, fa=.08, fd=1.2, a=.03, d=1.0, s=.9, r=.5),
        two(wave=.5, fine=6, cut=900, res=.4, env=.3, il=.2, al=.6, fa=.1, fd=1.2, a=.04, d=1.0, s=.9, r=.5),
        voiceMode=1, legato=1, portamento=.08, atPitch=1.0, atFilter=.6, ribbonRange=1, **VIBRATO,
        delaySync=5, delayFeedback=.4, delayMix=.18, **HALL, gain=.9),
    "LEAD - Twin Saw": sound(one(cut=1600, res=.25, env=.35, il=.2, al=.8, fa=.01, fd=.6, a=.005, d=.8, s=.9, r=.3),
        two(fine=16, cut=1800, res=.2, env=.3, il=.2, al=.75, fa=.01, fd=.7, a=.005, d=.8, s=.9, r=.3),
        voiceMode=1, legato=1, portamento=.04, atFilter=.4, atDrive=.4, voiceDrive=.4, **VIBRATO,
        delaySync=6, delayFeedback=.35, delayMix=.14, **ROOM, gain=.8),
    "LEAD - Ring Lead": sound(one(cut=1400, res=.3, env=.35, il=.2, al=.7, fa=.02, fd=.8, a=.01, d=1.0, s=.9, r=.4),
        two(wave=.66, tune=12, fine=0, cut=1800, env=.3, il=.2, al=.6, fa=.02, fd=.8, a=.01, d=1.0, s=.9, r=.4),
        voiceMode=1, legato=1, portamento=.05, ringDepth=.6, ringSpeed=392, ringKey=1, ringAttack=.6, ribbonRange=2, atFilter=.4, **VIBRATO,
        delaySync=5, delayFeedback=.35, delayMix=.15, **ROOM, gain=.85),
    "BASS - Night Bass": sound(one(octave=2, cut=280, res=.3, env=.55, il=.05, al=.8, fa=.002, fd=.35, a=.002, d=.6, s=.8, r=.15),
        two(wave=.66, octave=2, fine=5, cut=380, res=.2, env=.45, il=.05, al=.7, fa=.002, fd=.45, a=.002, d=.6, s=.8, r=.15),
        mix=.4, vcoSub=.5, voiceMode=1, legato=1, portamento=.03, velFilter=.35, voiceDrive=.45, voiceWidth=.2, gain=.9),
    "BASS - Dual Pluck": sound(one(octave=2, cut=420, res=.4, env=.6, il=0, al=.9, fa=.001, fd=.22, a=.001, d=.5, s=.2, r=.15),
        two(wave=.85, octave=3, fine=0, cut=900, res=.3, env=.5, il=0, al=.8, fa=.001, fd=.12, a=.001, d=.25, s=0, r=.1),
        mix=.35, voiceMode=1, velFilter=.5, voiceDrive=.5, voiceWidth=.2, gain=.95),
    "BASS - Ring Bass": sound(one(octave=2, cut=500, res=.3, env=.45, il=.05, al=.7, fa=.002, fd=.4, a=.002, d=.7, s=.7, r=.15),
        two(wave=.66, octave=2, fine=0, cut=600, env=.4, il=.05, al=.6, fa=.002, fd=.4, a=.002, d=.7, s=.7, r=.15),
        mix=.35, ringDepth=.55, ringSpeed=131, ringKey=1, ringDecay=.6, voiceMode=1, legato=1, voiceDrive=.4, voiceWidth=.2, gain=.95),
    "BASS - Velvet Low": sound(one(wave=.05, octave=2, cut=350, res=.15, env=.3, il=.05, al=.6, fa=.01, fd=.8, a=.01, d=1.0, s=.9, r=.3),
        two(octave=2, fine=4, cut=300, res=.1, env=.3, il=.05, al=.5, fa=.02, fd=.9, a=.02, d=1.0, s=.9, r=.3),
        mix=.4, vcoSub=.4, voiceMode=1, legato=1, portamento=.04, atFilter=.4, voiceWidth=.2, gain=.95),
    # ==== E: textures, effects, sequences and chord memory
    "FX - Night Wind": sound(one(wave=0, cut=900, res=.8, env=.3, il=.2, al=.7, fa=2.0, fd=3.0, a=1.5, d=3.0, s=.85, r=3.5, filterBP=1),
        two(wave=0, fine=0, cut=1800, res=.6, env=.25, il=.2, al=.6, fa=3.0, fd=3.0, a=2.0, d=3.0, s=.85, r=3.5),
        vcoNoise=.9, rate=.07, lfoFilter=1.4, lfoShape=1, atFilter=.6, reverbType=2, reverbSize=.95, reverbMix=.36, gain=.7),
    "FX - Metal Rain": sound(one(wave=.05, octave=4, cut=2500, res=.5, env=.3, il=0, al=.6, fa=.002, fd=.3, a=.002, d=.5, s=0, r=.6),
        two(wave=.66, octave=4, tune=5, fine=0, cut=3000, env=.25, il=0, al=.5, fa=.002, fd=.3, a=.002, d=.5, s=0, r=.6),
        ringDepth=.9, ringSpeed=1170, ringDecay=.4, lfoShape=5, rate=7, lfoFilter=1.0, arpOn=1, arpPattern=3, arpOctaves=1, arpTempo=126, arpDivision=2,
        delaySync=5, delayFeedback=.45, delayMix=.22, reverbType=2, reverbMix=.3, gain=.85),
    "FX - Rising Sweep": sound(one(cut=300, res=.6, env=.6, il=0, al=1, fa=4.0, fd=5.0, a=.5, d=5.0, s=1, r=2.0),
        two(fine=12, cut=400, res=.5, env=.5, il=0, al=1, fa=5.0, fd=5.0, a=.8, d=5.0, s=1, r=2.5),
        phaserOn=1, phaserRate=.2, phaserMix=.35, **HALL, gain=.6),
    "FX - Distant Sirens": sound(one(wave=0, octave=4, cut=2000, env=.1, il=.2, al=.4, fa=1.0, fd=2.0, a=.8, d=2.0, s=.9, r=2.5),
        two(wave=0, octave=4, tune=3, fine=0, cut=2000, env=.1, il=.2, al=.4, fa=1.0, fd=2.0, a=1.0, d=2.0, s=.9, r=2.5),
        ringDepth=.5, ringSpeed=1.3, lfoShape=0, rate=.25, lfoPitch=3, atPitch=.8, voiceMode=1, portamento=.6,
        delaySync=4, delayFeedback=.5, delayMix=.25, reverbType=2, reverbSize=.95, reverbMix=.4, gain=.7),
    "SEQ - Night Pulse": sound(one(octave=2, cut=500, res=.45, env=.55, il=0, al=.8, fa=.001, fd=.18, a=.002, d=.25, s=.2, r=.1),
        two(wave=.66, octave=3, fine=0, cut=800, res=.3, env=.4, il=0, al=.7, fa=.001, fd=.15, a=.002, d=.2, s=.1, r=.1),
        mix=.35, voiceMode=1, arpTempo=118, arpDivision=2, arpGate=.55, voiceDrive=.4, rate=.1, lfoFilter=.5,
        delaySync=5, delayFeedback=.4, delayMix=.16, gain=.95,
        sequence="38;38;50;38;45;38;48;50;38;38;50;38;43;45;48;50"),
    "SEQ - Ring Steps": sound(one(wave=0, cut=2600, env=.2, il=0, al=.6, fa=.002, fd=.6, a=.002, d=.9, s=0, r=.6),
        two(wave=0, octave=4, tune=7, fine=0, cut=3200, env=.2, il=0, al=.5, fa=.002, fd=.5, a=.002, d=.7, s=0, r=.5),
        mix=.35, ringDepth=1, ringSpeed=610, ringKey=1, ringDecay=.7, arpTempo=104, arpDivision=2, arpGate=.4,
        delaySync=5, delayFeedback=.45, delayMix=.2, **HALL, gain=.9,
        sequence="69;r;76;72;r;69;79;r;76;r;72;74;r;69;r;r"),
    "CHORD - Dark Minor": sound(one(cut=600, res=.2, env=.3, il=.15, al=.6, fa=.5, fd=2.0, a=.4, d=2.0, s=.9, r=2.0),
        two(fine=10, cut=800, env=.25, il=.1, al=.55, fa=.7, fd=2.0, a=.6, d=2.0, s=.9, r=2.4),
        chordOn=1, chord="0,3,7,10", atFilter=.4, chorusMode=2, chorus=.35, **HALL, gain=.42),
    "CHORD - Open Fifths": sound(one(cut=480, env=.5, il=.1, al=.8, fa=.12, fd=1.2, a=.03, d=1.2, s=.85, r=.5),
        two(octave=2, fine=6, cut=420, env=.45, il=.1, al=.7, fa=.18, fd=1.3, a=.04, d=1.2, s=.85, r=.5),
        mix=.4, chordOn=1, chord="0,7,12", atFilter=.5, atVolume=.3, voiceDrive=.3, **ROOM, gain=.45),
}


folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Presets", "Sounds")
os.makedirs(folder, exist_ok=True)
for old in glob.glob(os.path.join(folder, "*.orbitpreset")):   # sounds no longer in the list are removed; the others are rewritten
    if os.path.basename(old)[:-len(".orbitpreset")] not in SOUNDS:
        os.remove(old)
for name, settings in SOUNDS.items():
    settings = dict(settings); sequence = settings.pop("sequence", None); chord = settings.pop("chord", None)
    extra = (' sequence=%s' % quoteattr(sequence) if sequence else '') + (' chord=%s' % quoteattr(chord) if chord else '')
    head = '<OrbitState stateVersion="5" program="0" modified="0"%s>' % extra
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', head]
    lines += ['  <PARAM id=%s value="%s"/>' % (quoteattr(key), repr(float(value))) for key, value in settings.items()]
    lines.append('</OrbitState>')
    with open(os.path.join(folder, name + ".orbitpreset"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print("écrit :", name)
