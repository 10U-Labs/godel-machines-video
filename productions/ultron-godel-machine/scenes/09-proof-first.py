"""Scene 09: Proof first.

A study. On the Gödel Machine's code one line is rewritten badly, and turns
the colour of rust. Then the pen's own line goes the same way, and after it
line after line. The picture starts again with the code whole. A change
waits beside it: a new line that tries to go in and is held back. Next to it
a proof is written, step by step, and the line is held back once more. Only
when the proof has its mark does the new line go in. Then the second lab:
Ultron's body is put together in a moment, and he walks out in it.
"""
import math

import kit
import parts
from kit import alpha, every, fr, key, mix, sec, span

PAGE = (0.4, 0.9)
SHEET = (5.7, 0.9)
ROW = 3
WORSE = (parts.RUST, parts.RED_DEEP)
STEPS = (1.5, 1.1, 1.7, 0.9, 1.4, 1.2, 0.8)


def bump(t, t0, dur):
    """Rises from 0 to 1 and falls back, between t0 and t0 + dur."""
    return math.sin(math.pi * kit.clamp((t - t0) / dur))


def build(T):
    cues = []
    end = sec(kit.frames())
    t_bad = T.at(0, 0.1)
    t_then = T.at(0, 0.5)
    t_reset = T.start(1) - 0.15
    t_guess = T.at(1, 0.04)
    t_prove = T.at(1, 0.27)
    t_again = T.at(1, 0.78)
    t_proved = T.end(1) + 0.15
    t_change = t_proved + 0.5
    t_film = T.at(2, 0.4) - 0.1
    t_walk = t_film + 1.6

    parts.backdrop(seed=101, glow=parts.ICE_DEEP, strength=0.2)
    kit.motes(n=16, seed=102, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    study = parts.room('study', far, stage, light=parts.ICE, glow=0.13)
    side = study[1]
    who = parts.figure('scientist', side, (-4.0, parts.FLOOR), coat='#56707e', coat_deep='#3b505c', hair='#c9c2b8')
    parts.nod(who, 0.0, t_film, 0.4)
    parts.reach(who, t_bad + 0.4, 58)
    parts.reach(who, t_reset - 0.2, 0, 0.3)
    parts.reach(who, t_proved + 0.1, 40)

    # ------------------------------------------------------------ a change for the worse, and what follows it
    spoiled = parts.page('spoiled', side, PAGE, rows=8, seed=5)
    quill = parts.pen('spoiled-pen', spoiled['root'], (-spoiled['w'] / 2 - 0.4, spoiled['ys'][7]))
    rusty = parts.pen('rusty-pen', spoiled['root'], (-spoiled['w'] / 2 - 0.4, spoiled['ys'][7]), 1.0, parts.RUST, parts.RUST)
    parts.rewrite(spoiled, ROW, t_bad, WORSE)
    parts.pulse('harm', side, (PAGE[0], PAGE[1] + spoiled['ys'][ROW]), t_bad + 0.2, 0.9, parts.RED, 0.7)
    cues.append({'t': t_bad, 'type': 'blip', 'pitch': 0.6, 'gain': 0.7})
    parts.rewrite(spoiled, 7, t_then, WORSE)
    parts.resize(quill, t_then + 0.2, 1.0, 0.001, 0.2)
    kit.pop(rusty, t_then + 0.3, 1.0, 0.3)
    cues.append({'t': t_then, 'type': 'blip', 'pitch': 0.5, 'gain': 0.7})
    for k, r in enumerate((1, 5, 0, 2, 6, 4)):
        when = t_then + 0.7 + 0.3 * k
        parts.rewrite(spoiled, r, when, WORSE, 0.35)
        cues.append({'t': when, 'type': 'blip', 'pitch': 0.46 - 0.03 * k, 'gain': 0.6})
    for when, a in ((t_bad, 1.0), (t_then + 2.4, 0.15)):
        alpha(spoiled['glow'], fr(when), a)
    for ob in spoiled['eyes']['pair']:
        key(ob, 'scale', fr(t_then), (1, 1, 1))
        key(ob, 'scale', fr(t_then + 1.6), (1, 0.4, 1))
    parts.cut([spoiled['root']], None, t_reset)

    # ------------------------------------------------------------ the same code, whole, and a change that has to wait
    pg = parts.page('machine', side, PAGE, rows=8, seed=5)
    parts.pen('pen', pg['root'], (-pg['w'] / 2 - 0.4, pg['ys'][7]))
    parts.cut([pg['root']], t_reset, None)
    parts.blink(pg['eyes'], (t_guess + 2.0, t_prove + 3.0, t_again + 1.6))
    parts.look(pg['eyes'], t_guess + 0.2, 0.08)
    edge = (PAGE[0] + pg['w'] / 2, PAGE[1] + pg['ys'][ROW])
    hold = (edge[0] + 1.3, edge[1])
    change = parts.group('change', side, (hold[0] + 0.9, hold[1]))
    kit.shape('change-glow', kit.rrect_pts(2.6, 1.1, 0.5), kit.glow_material(parts.BONE, 0.3, power=1.0), change)
    kit.shape('change-card', kit.rrect_pts(1.8, 0.44, 0.14), kit.material(parts.NIGHT500, parts.NIGHT600), change)
    x = -0.72
    for k, ln in enumerate((0.5, 0.34, 0.42)):
        kit.shape(f'change-bar{k}', kit.bar_pts(ln, 0.13), kit.material(parts.FROST if k == 1 else parts.BONE), change, (x, 0))
        x += ln + 0.1
    kit.pop(change, t_guess, 1.0)
    z = change.location.z
    for f in every(1, fr(t_guess), fr(t_change + 0.4)):
        t = sec(f)
        cx = hold[0] + 0.9 * (1 - span(t, t_guess + 0.2, t_guess + 0.6))
        cx -= 0.4 * (bump(t, t_guess + 0.7, 0.8) + bump(t, t_again, 0.8))
        cx -= (hold[0] - PAGE[0] - 0.3) * span(t, t_change, t_change + 0.35)
        key(change, 'location', f, (cx, hold[1] + 0.05 * math.sin(t * 2.0), z))
    parts.resize(change, t_change + 0.1, 1.0, 0.001, 0.25)
    for k, when in enumerate((t_guess + 1.1, t_again + 0.4)):
        parts.pulse(f'held{k}', side, edge, when, 0.4, parts.BONE, 0.6, 0.05)
        cues.append({'t': when, 'type': 'tick', 'pitch': 0.6, 'gain': 0.7})
    cues.append({'t': t_guess, 'type': 'pop', 'pitch': 1.1})

    # ------------------------------------------------------------ the proof
    sheet = parts.group('proof', side, SHEET)
    kit.shape('proof-glow', kit.rrect_pts(3.6, 4.8, 1.0), kit.glow_material(parts.ICE, 0.16, power=1.0), sheet)
    kit.shape('proof-paper', kit.rrect_pts(2.4, 3.6, 0.1), kit.material('#16283a', '#101d2b'), sheet)
    for k, ln in enumerate(STEPS):
        step = kit.shape(f'proof-step{k}', kit.bar_pts(ln, 0.1), kit.material(parts.FROST if k % 2 else parts.ICE), sheet, (-0.95, 1.35 - 0.34 * k))
        when = mix(t_prove + 0.3, t_proved - 0.8, k / (len(STEPS) - 1))
        kit.grow(step, when, 0.5)
        cues.append({'t': when, 'type': 'tick', 'pitch': 1.1 + 0.05 * k, 'gain': 0.4})
    kit.pop(sheet, t_prove - 0.2, 1.0)
    mark = parts.seal('proof-mark', sheet, (0.45, -1.2), 0.7)
    kit.pop(mark, t_proved, 0.7)
    parts.pulse('proved', side, (SHEET[0] + 0.45, SHEET[1] - 1.2), t_proved + 0.1, 0.5, parts.FROST, 0.8)
    cues.append({'t': t_proved, 'type': 'chime', 'gain': 0.6})
    parts.rewrite(pg, ROW, t_change + 0.2)
    parts.pulse('changed', side, PAGE, t_change + 0.3, 2.3, parts.FROST, 0.8, 0.05)
    cues.append({'t': t_change, 'type': 'swoosh', 'gain': 0.5})
    cues.append({'t': t_change + 0.3, 'type': 'blip', 'pitch': 1.4, 'gain': 0.6})

    # ------------------------------------------------------------ the film: a body, and out
    lab = parts.second_lab(far, stage)
    stand, scale = lab['stand'], 0.9
    for k, m in enumerate(lab['machines']):
        for ob in m['lamp']:
            alpha(ob, 1, 1.0)
        lean = -1 if k < 2 else 1
        parts.work(m, t_film, t_film + 1.5, sh=(-8 * lean, -36 * lean), el=(60 * lean, 12 * lean), rate=1.3 + 0.1 * k)
    bot = parts.powerful('body', lab['front'], stand, scale)
    times = [t_film + 0.2 + 0.15 * k for k in range(6)]
    parts.assemble(bot, times, ((lab['rack_at'][0] - stand[0]) / scale, 1.2), 0.3)
    for k, t0 in enumerate(times):
        cues.append({'t': t0 + 0.3, 'type': 'tick', 'pitch': 0.45 + 0.04 * k, 'gain': 0.9})
    parts.visible(bot['eyes']['shapes'] + [bot['core'][0], bot['core'][2]], [(t_film + 1.25, None)], 0.2)
    cues.append({'t': t_film + 1.25, 'type': 'pop', 'pitch': 0.5})
    parts.walk(bot, t_walk, end + 0.6, stand[0], 12.5, rate=2.0, swing=26)
    for k in range(int((end - t_walk) * 2.0) + 1):
        cues.append({'t': min(end, t_walk + (k + 0.5) / 2.0), 'type': 'tick', 'pitch': 0.38, 'gain': 0.8})
    parts.cut(study, None, t_film)
    parts.cut(lab['roots'], t_film, None)
    parts.dip([t_reset, t_film])
    cues.append({'t': t_film - 0.2, 'type': 'whoosh', 'gain': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        if t >= t_film:
            return mix((1.2, 0.5, 19.2), (3.2, 0.4, 18.6), span(t, t_film, end))
        if t >= t_reset:
            return mix((1.5, 0.4, 19.2), (1.9, 0.4, 18.2), span(t, t_reset, t_film))
        return mix((0.1, 0.4, 16.8), (0.3, 0.4, 16.0), span(t, 0.0, t_reset))

    kit.camera(path, focus_z=1.0)
    return cues
