"""Synthesized music bed and sound effects. Everything is generated from
numbers here; there are no samples or recordings, so nothing needs a licence."""
import numpy as np
from scipy.signal import butter, lfilter

SR = 48000


def midi(note):
    return 440.0 * 2 ** ((note - 69) / 12)


def lowpass(x, cutoff, order=2):
    b, a = butter(order, cutoff / (SR / 2), btype="low")
    return lfilter(b, a, x, axis=0)


def bandpass(x, lo, hi, order=2):
    b, a = butter(order, [lo / (SR / 2), hi / (SR / 2)], btype="band")
    return lfilter(b, a, x, axis=0)


def pan(mono, position=0.0):
    """Mono to stereo. position runs from -1 (left) to 1 (right)."""
    angle = (position + 1) * np.pi / 4
    return np.stack([mono * np.cos(angle), mono * np.sin(angle)], axis=1)


def place(buf, clip, t):
    """Add a stereo clip into a stereo buffer starting at time t (seconds)."""
    i = int(round(t * SR))
    if i >= len(buf) or i + len(clip) <= 0:
        return
    j0 = max(0, -i)
    i = max(0, i)
    n = min(len(clip) - j0, len(buf) - i)
    buf[i:i + n] += clip[j0:j0 + n]


def _times(dur):
    return np.arange(int(dur * SR)) / SR


def _swell(n, attack, release):
    """Envelope that rises over `attack` seconds and falls over `release`."""
    env = np.ones(n)
    a = min(n, int(attack * SR))
    r = min(n, int(release * SR))
    env[:a] = np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    env[n - r:] *= np.cos(np.linspace(0, np.pi / 2, r)) ** 2
    return env


# ---------------------------------------------------------------- music

BPM = 80
BEAT = 60 / BPM
CHORD_LEN = 8 * BEAT  # two bars per chord

# Dm9, Bbmaj7, Fmaj9, Cadd9: bass note and chord tones as MIDI numbers.
CHORDS = [
    {"bass": 38, "notes": [57, 60, 64, 65, 69]},
    {"bass": 34, "notes": [58, 62, 65, 69]},
    {"bass": 41, "notes": [57, 60, 64, 67]},
    {"bass": 36, "notes": [55, 60, 62, 64, 67]},
]
ARP_PATTERN = [0, 2, 1, 3, 2, 4, 3, 2, 0, 2, 1, 3, 4, 3, 2, 1]


def _pad_note(freq, dur):
    t = _times(dur)
    out = np.zeros((len(t), 2))
    for side, cents in ((0, -5), (1, 5)):
        f = freq * 2 ** (cents / 1200)
        wave = np.sin(2 * np.pi * f * t)
        for k in range(2, 6):
            wave += np.sin(2 * np.pi * f * k * t) / (k * 1.6)
        out[:, side] = wave
    out = lowpass(out, 1100)
    return out * _swell(len(t), 1.6, 2.2)[:, None]


def _bass_note(freq, dur):
    t = _times(dur)
    wave = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2 * t)
    return pan(wave * _swell(len(t), 0.35, 1.2))


def _pluck(freq, dur=1.3):
    t = _times(dur)
    wave = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t)
    env = np.exp(-t / 0.26) * np.minimum(1, t / 0.004)
    return wave * env


def _bell(freq, dur=3.0):
    t = _times(dur)
    mod = 1.6 * np.exp(-t * 3.0) * np.sin(2 * np.pi * freq * 3.5 * t)
    wave = np.sin(2 * np.pi * freq * t + mod)
    return wave * np.exp(-t / 0.9) * np.minimum(1, t / 0.005)


def _ping_pong(x, delay, feedback=0.32, mix=0.35, repeats=5):
    out = x.copy()
    d = int(delay * SR)
    gain = mix
    for k in range(1, repeats + 1):
        shifted = np.zeros_like(x)
        if k * d >= len(x):
            break
        src = x[: len(x) - k * d]
        # alternate sides on each repeat
        if k % 2:
            shifted[k * d:, 0] = src[:, 1]
            shifted[k * d:, 1] = src[:, 0] * 0.4
        else:
            shifted[k * d:, 1] = src[:, 1]
            shifted[k * d:, 0] = src[:, 0] * 0.4
        out += shifted * gain
        gain *= feedback / mix * mix
    return out


def music(duration, arp_from=6.0):
    """Calm bed: pad chords, soft bass, a plucked arpeggio that enters at
    `arp_from` seconds, and an occasional bell. Returns stereo float array."""
    n = int(duration * SR)
    pad = np.zeros((n, 2))
    bass = np.zeros((n, 2))
    arp = np.zeros((n, 2))
    bells = np.zeros((n, 2))

    t0 = 0.0
    index = 0
    while t0 < duration:
        chord = CHORDS[index % len(CHORDS)]
        for note in chord["notes"]:
            place(pad, _pad_note(midi(note), CHORD_LEN + 2.0) * 0.05, t0 - 0.4)
        place(bass, _bass_note(midi(chord["bass"]), CHORD_LEN + 0.6) * 0.2, t0)

        ladder = chord["notes"] + [chord["notes"][0] + 12]
        for step, pick in enumerate(ARP_PATTERN):
            when = t0 + step * BEAT / 2
            note = ladder[pick % len(ladder)] + 12
            side = 0.35 if step % 2 else -0.35
            place(arp, pan(_pluck(midi(note)) * 0.085, side), when)

        if index % 2 == 1:
            top = chord["notes"][-1] + 12
            place(bells, pan(_bell(midi(top)) * 0.05, 0.2), t0 + 2 * BEAT)
        t0 += CHORD_LEN
        index += 1

    arp = _ping_pong(arp, BEAT * 0.75)
    t = np.arange(n) / SR
    arp_gain = np.clip((t - arp_from) / 6.0, 0, 1)[:, None]
    mix = pad + bass + arp * arp_gain + bells * arp_gain

    fade_in = np.clip(t / 1.5, 0, 1)
    fade_out = np.clip((duration - t) / 3.0, 0, 1)
    mix *= (fade_in * fade_out)[:, None]
    return np.tanh(mix * 1.2) / 1.2


# ---------------------------------------------------------------- effects

def _noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


def sfx(kind, seed=0, pitch=1.0, dur=None):
    """One sound effect as a stereo clip. `pitch` scales its frequency."""
    if kind == "pop":
        t = _times(0.12)
        f = np.linspace(300, 620, len(t)) * pitch
        wave = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035)
        return pan(wave * 0.5)
    if kind == "tick":
        t = _times(0.03)
        click = bandpass(_noise(len(t), seed), 2500, 6000) * np.exp(-t / 0.004)
        blip = np.sin(2 * np.pi * 1700 * pitch * t) * np.exp(-t / 0.006)
        return pan((click * 0.6 + blip * 0.5) * 0.3, (seed % 5 - 2) * 0.08)
    if kind == "blip":
        t = _times(0.14)
        wave = np.sin(2 * np.pi * 880 * pitch * t) * np.exp(-t / 0.04)
        return pan(wave * 0.3)
    if kind == "rise":
        t = _times(dur or 0.5)
        f = 440 * pitch * (1 + 0.5 * (t / t[-1]) ** 1.5)
        phase = 2 * np.pi * np.cumsum(f) / SR
        wave = np.sin(phase) + 0.4 * np.sin(2 * phase)
        return pan(wave * _swell(len(t), 0.05, 0.25) * 0.22)
    if kind in ("whoosh", "swoosh"):
        length = dur or (0.55 if kind == "whoosh" else 1.2)
        t = _times(length)
        lo, hi = (300, 1800) if kind == "whoosh" else (900, 4200)
        noise = bandpass(_noise(len(t), seed + 11), lo, hi)
        env = np.sin(np.pi * (t / t[-1]) ** (0.7 if kind == "whoosh" else 1.4)) ** 2
        mono = noise * env * (0.22 if kind == "whoosh" else 0.12)
        sweep = np.linspace(-0.5, 0.5, len(t))
        return np.stack([mono * np.cos((sweep + 1) * np.pi / 4), mono * np.sin((sweep + 1) * np.pi / 4)], axis=1)
    if kind == "chime":
        t = _times(dur or 2.4)
        wave = np.zeros(len(t))
        for note, gain in ((74, 1.0), (81, 0.8), (88, 0.6)):  # D5, A5, E6
            f = midi(note) * pitch
            for ratio, amp, decay in ((1, 1.0, 0.9), (2.76, 0.35, 0.35), (5.4, 0.15, 0.2)):
                wave += gain * amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / decay)
        wave *= np.minimum(1, t / 0.004)
        return pan(wave * 0.11)
    raise ValueError(f"Unknown sound effect: {kind}")
