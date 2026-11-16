"""Scene 05: The Gödel Machine.

A study in cold light. A computer scientist draws the design on a board, in
2003. The design comes off the board as a program: a sheet with eyes, on
which lines of text appear one by one. Small programs with a mistake in them
come past, and each leaves fixed: that is its job. While it works it rewrites
lines of its own text, and then the programs come past faster. A pen marks
the line that does the rewriting, and that line is rewritten too.
"""
import math

import kit
import parts
from kit import alpha, every, fr, key, mix, sec, span

BOARD = (-3.5, parts.FLOOR + 3.4)
PAGE = (2.9, 1.0)
LANE = parts.FLOOR + 0.85


def build(T):
    cues = []
    end = sec(kit.frames())
    t_draw0, t_draw1 = T.at(1, 0.1), T.end(1)
    t_program = T.start(2)
    t_text0, t_text1 = T.at(2, 0.42), T.at(2, 0.82)
    t_code = T.at(2, 0.9)
    t_can = T.at(3, 0.03)
    t_job = T.at(3, 0.26)
    t_own = T.at(3, 0.56)
    t_any = T.start(4)
    t_even = T.at(4, 0.55)

    parts.backdrop(seed=61, glow=parts.ICE_DEEP, strength=0.22)
    kit.motes(n=18, seed=62, colour=parts.ICE)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    front = parts.room('study', far, stage, light=parts.ICE, glow=0.13)[1]

    # ------------------------------------------------------------ the scientist and the design
    board = parts.blueprint('design', front, BOARD)
    parts.draw(board['dots'], t_draw0, t_draw1)
    who = parts.figure('scientist', front, (-9.5, parts.FLOOR), coat='#56707e', coat_deep='#3b505c', hair='#c9c2b8')
    parts.stroll(who, 0.2, T.end(0), -9.5, -6.2)
    parts.nod(who, T.end(0), end, 0.4)
    parts.reach(who, t_draw0 - 0.4, 72)
    for f in every(2, fr(t_draw0), fr(t_draw1)):
        key(who['arm'], 'rotation_euler', f, (0, 0, math.radians(72 + 9 * math.sin(sec(f) * 7.0))))
    parts.reach(who, t_draw1 + 0.1, 12, 0.5)
    for k in range(8):
        cues.append({'t': mix(t_draw0, t_draw1, k / 8), 'type': 'tick', 'pitch': 0.9 + 0.05 * (k % 4), 'gain': 0.35})
    year = kit.text('year', '2003', 0.6, kit.material(parts.BONE), front, (-7.3, 3.5), align='LEFT')
    name = kit.text('name', 'Jürgen Schmidhuber', 0.3, kit.material(parts.ASH), front, (-7.3, 2.97), align='LEFT')
    kit.fade(year, T.start(1) + 0.2, t_program - 0.3)
    kit.fade(name, T.at(1, 0.45), t_program - 0.3)

    # ------------------------------------------------------------ the design as a program: its text
    pg = parts.page('machine', front, PAGE, rows=8, seed=5)
    z = pg['root'].location.z
    for f in every(1, fr(t_program), fr(t_program + 1.0)):
        q = span(sec(f), t_program, t_program + 0.9)
        s = max(0.001, 0.45 + 0.55 * q) * max(0.001, kit.back_out((sec(f) - t_program) / 0.4))
        x, y = mix((BOARD[0], BOARD[1]), PAGE, q)
        key(pg['root'], 'location', f, (x, y, z))
        key(pg['root'], 'scale', f, (s, s, s))
    key(pg['root'], 'scale', 1, parts.TINY)
    key(pg['root'], 'scale', max(1, fr(t_program) - 1), parts.TINY)
    parts.open_eyes(pg['eyes'], t_program + 0.9)
    parts.blink(pg['eyes'], (t_text1 + 0.8, t_job + 1.6, t_any + 1.2))
    cues.append({'t': t_program, 'type': 'whoosh', 'gain': 0.7})
    cues.append({'t': t_program + 0.9, 'type': 'pop', 'pitch': 1.2})
    for r, row in enumerate(pg['rows']):
        t0 = mix(t_text0, t_text1, r / 7)
        for ob in row:
            key(ob, 'scale', 1, (0.001, 1, 1))
            key(ob, 'scale', fr(t0), (0.001, 1, 1))
            key(ob, 'scale', fr(t0 + 0.25), (1, 1, 1))
        cues.append({'t': t0, 'type': 'tick', 'pitch': 1.4 - 0.05 * r, 'gain': 0.5})
    parts.pulse('code', front, PAGE, t_code, 2.4, parts.ICE, 0.9, 0.06)
    cues.append({'t': t_code, 'type': 'chime', 'gain': 0.5})

    # ------------------------------------------------------------ its job, and rewriting its own text
    parts.rewrite(pg, 1, t_can)
    cues.append({'t': t_can, 'type': 'blip', 'pitch': 1.2, 'gain': 0.6})
    arrivals, when = [], t_job
    while when < end - 1.0:
        arrivals.append(when)
        when += 1.25 if when < t_own + 1.0 else 0.62
    for k, t0 in enumerate(arrivals):
        card = parts.task(f'task{k}', front, (10.5, LANE), 0.7, seed=k)
        zc = card['root'].location.z
        for f in every(1, fr(t0), fr(t0 + 1.4)):
            t = sec(f)
            x = mix(10.5, PAGE[0], span(t, t0, t0 + 0.5, kit.ease_out))
            x = mix(x, -0.4, span(t, t0 + 0.75, t0 + 1.3, lambda v: v * v))
            s = 0.7 * (1 - span(t, t0 + 1.0, t0 + 1.35))
            key(card['root'], 'location', f, (x, LANE, zc))
            key(card['root'], 'scale', f, (max(0.001, s),) * 3)
        parts.fix(card, t0 + 0.55)
        cues.append({'t': t0 + 0.55, 'type': 'blip', 'pitch': 1.0 + 0.04 * k, 'gain': 0.4})
    for k, r in enumerate((3, 5, 2)):
        parts.rewrite(pg, r, t_own + 0.4 * k)
        cues.append({'t': t_own + 0.4 * k, 'type': 'tick', 'pitch': 1.3 + 0.1 * k, 'gain': 0.6})
    parts.pulse('better', front, PAGE, t_own + 1.3, 2.4, parts.FROST, 0.9, 0.05)

    # ------------------------------------------------------------ any part, even the part that rewrites
    for r in range(8):
        lit = parts.band(pg, r, parts.FROST, 0.28)
        t0 = t_any + 0.14 * r
        for when, a in ((t0, 0.0), (t0 + 0.1, 1.0), (t0 + 0.45, 0.0)):
            alpha(lit, fr(when), a)
        cues.append({'t': t0, 'type': 'tick', 'pitch': 0.9 + 0.06 * r, 'gain': 0.3})
    quill = parts.pen('pen', pg['root'], (-pg['w'] / 2 - 0.35, pg['ys'][7]))
    kit.pop(quill, t_own - 0.3, 1.0)
    last = parts.band(pg, 7, parts.BONE, 0.34)
    for when, a in ((t_even - 0.1, 0.0), (t_even + 0.2, 1.0), (end - 0.4, 0.6)):
        alpha(last, fr(when), a)
    for f in every(1, fr(t_even + 0.3), fr(t_even + 1.0)):
        q = span(sec(f), t_even + 0.3, t_even + 0.95)
        s = 1 + 0.5 * math.sin(math.pi * q)
        key(quill, 'rotation_euler', f, (0, 0, -0.6 - math.tau * q))
        key(quill, 'scale', f, (s, s, s))
    parts.rewrite(pg, 7, t_even + 0.6)
    cues.append({'t': t_even, 'type': 'tick', 'pitch': 0.9})
    cues.append({'t': t_even + 0.3, 'type': 'rise', 'dur': 0.7, 'pitch': 1.2, 'gain': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((-4.4, 0.4, 16.5), (-3.6, 0.5, 16.0), span(t, 0.0, t_draw1))
        pos = mix(pos, (0.3, 0.3, 19.6), span(t, t_program - 0.2, t_program + 1.4))
        return mix(pos, (1.9, 0.2, 16.8), span(t, t_can, t_own + 1.5))

    kit.camera(path, focus_z=1.0)
    return cues
