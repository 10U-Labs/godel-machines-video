"""Scene 11: A real program.

A study: the Gödel Machine is still a design on a board, and the stand beside
it holds nothing. Then an office in 2025, where two researchers stand at a
screen. A program comes up on it. Small programs with a mistake in them come
past it and leave fixed, and then it rewrites its own lines. On the wall a
board of a hundred squares lights two rows, and after many rewrites, five.
Beside the screen the dotted outline of a body shows and fades: the program
has none. Then the researchers are gone, and Ultron's eyes hang over a
console as they did at the start. A feeble body is built beside him and he
moves into it, while the program on the screen goes on rewriting itself.
"""
import math

import kit
import parts
from kit import alpha, every, fr, key, mix, sec, span

BOARD = (0.8, parts.FLOOR + 3.4)
SCREEN = (3.0, parts.FLOOR)
GRID = (-5.9, 1.0)
CONSOLE = (-5.2, parts.FLOOR)
BODY = (-1.7, parts.FLOOR)
SCALE = 0.8


def build(T):
    cues = []
    end = sec(kit.frames())
    t_real = T.start(1) - 0.1
    t_program = T.at(1, 0.2)
    t_fixes = T.at(1, 0.36)
    t_rewrites = T.at(1, 0.62)
    t_first = T.at(2, 0.1)
    t_rounds = T.at(2, 0.48)
    t_best = T.at(2, 0.8)
    t_no_body = T.start(3)
    t_code = T.at(3, 0.5)
    t_was = T.start(4) - 0.1
    t_builds = T.start(5)
    t_into = T.at(5, 0.34)
    t_itself = T.at(5, 0.52)

    parts.backdrop(seed=121, glow=parts.ICE_DEEP, strength=0.2)
    kit.motes(n=16, seed=122, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the design that was never built
    study = parts.room('study', far, stage, light=parts.ICE, glow=0.13)
    design = parts.blueprint('design', study[1], BOARD)
    for i, ob in enumerate(design['dots']):
        for f in every(4, 1, fr(t_real)):
            alpha(ob, f, 0.6 + 0.4 * math.sin(sec(f) * 5.0 + i * 0.7))
    author = parts.figure('scientist', study[1], (-2.6, parts.FLOOR), coat='#56707e', coat_deep='#3b505c', hair='#c9c2b8')
    parts.nod(author, 0.0, t_real, 0.4)
    parts.reach(author, 0.3, 45)
    parts.console('unbuilt', study[1], (5.0, parts.FLOOR), 1.0, parts.ICE)
    gap = parts.dotted_ring('gap', study[1], (5.0, parts.FLOOR + 3.2), 0.8, parts.ASH, 20)
    parts.visible(gap['shapes'], [(T.at(0, 0.3), None)], 0.4)
    cues.append({'t': T.at(0, 0.3), 'type': 'tick', 'pitch': 0.5, 'gain': 0.6})
    parts.cut(study, None, t_real)

    # ------------------------------------------------------------ 2025: researchers, and a program on their screen
    office = parts.room('office', far, stage, light=parts.STEEL100, glow=0.18)
    side = office[1]
    parts.cut(office, t_real, None)
    screen = parts.monitor('screen', side, SCREEN)
    centre = (SCREEN[0], SCREEN[1] + screen['centre'][1])
    prog = parts.page('program', side, centre, rows=8, seed=12, scale=0.66)
    kit.pop(prog['root'], t_program, 0.66)
    parts.pen('pen', prog['root'], (-prog['w'] / 2 - 0.35, prog['ys'][7]))
    parts.open_eyes(prog['eyes'], t_program + 0.3)
    parts.blink(prog['eyes'], (t_fixes + 1.2, t_first + 1.0, t_no_body + 0.8, t_was + 2.0, t_itself + 1.2))
    cues.append({'t': t_program, 'type': 'pop', 'pitch': 1.2})

    crew = kit.empty('crew', side)
    one = parts.figure('researcher-one', crew, (-3.3, parts.FLOOR), coat='#3f6b6b', coat_deep='#2b4a4a', skin='#c98f6b', shade='#a8704f')
    two = parts.figure('researcher-two', crew, (-1.6, parts.FLOOR), 0.6, coat='#7a6a3a', coat_deep='#564a28', hair='#7a3b24')
    parts.nod(one, t_real, t_was, 0.0)
    parts.nod(two, t_real, t_was, 1.3)
    parts.reach(one, t_program - 0.5, 58)
    parts.reach(one, t_fixes, 15, 0.5)
    parts.reach(two, t_rewrites - 0.3, 62)
    parts.reach(two, T.end(1), 10, 0.5)
    year = kit.text('year', '2025', 0.6, kit.material(parts.BONE), crew, (-5.0, 3.5), align='LEFT')
    kit.fade(year, t_real + 0.5, T.end(1))

    spot = (centre[0] + 1.55, centre[1])
    for k in range(3):
        t0 = t_fixes + 0.6 * k
        card = parts.task(f'task{k}', side, (10.5, 2.2), 0.5, seed=k)
        zc = card['root'].location.z
        for f in every(1, fr(t0), fr(t0 + 1.3)):
            t = sec(f)
            x, y = mix((10.5, 2.2), spot, span(t, t0, t0 + 0.45, kit.ease_out))
            y += 3.4 * span(t, t0 + 0.8, t0 + 1.25, lambda v: v * v)
            s = 0.5 * (1 - span(t, t0 + 0.95, t0 + 1.25))
            key(card['root'], 'location', f, (x, y, zc))
            key(card['root'], 'scale', f, (max(0.001, s),) * 3)
        key(card['root'], 'scale', 1, parts.TINY)
        key(card['root'], 'scale', max(1, fr(t0) - 1), parts.TINY)
        parts.fix(card, t0 + 0.55)
        cues.append({'t': t0 + 0.55, 'type': 'blip', 'pitch': 1.0 + 0.1 * k, 'gain': 0.5})
    for k, r in enumerate((2, 5, 1, 6, 3, 7)):
        when = t_rewrites + 0.3 + 0.5 * k
        parts.rewrite(prog, r, when)
        cues.append({'t': when, 'type': 'tick', 'pitch': 1.1 + 0.07 * k, 'gain': 0.55})

    # ------------------------------------------------------------ what it fixed: 20 in a hundred, then 50
    results = parts.group('results', crew, GRID)
    kit.shape('results-board', kit.rrect_pts(3.5, 3.5, 0.15), kit.material(parts.NIGHT500, parts.NIGHT600), results)
    for i in range(100):
        row, col = divmod(i, 10)
        at = (-1.35 + 0.3 * col, 1.35 - 0.3 * row)
        kit.shape(f'cell{i}', kit.rrect_pts(0.2, 0.2, 0.04), kit.material(parts.STEEL700), results, at)
        if i < 50:
            lit = kit.shape(f'fixed{i}', kit.rrect_pts(0.2, 0.2, 0.04), kit.material(parts.FROST, parts.ICE), results, at)
            when = mix(t_first, t_first + 1.0, i / 19) if i < 20 else mix(t_best, t_best + 1.1, (i - 20) / 29)
            alpha(lit, 1, 0.0)
            alpha(lit, fr(when), 0.0)
            alpha(lit, fr(when) + 2, 1.0)
    kit.pop(results, T.start(2) - 0.3, 1.0)
    cues.append({'t': T.start(2) - 0.3, 'type': 'pop', 'pitch': 1.0})
    for k in range(4):
        cues.append({'t': t_first + 0.25 * k, 'type': 'tick', 'pitch': 1.2, 'gain': 0.4})
        cues.append({'t': t_best + 0.25 * k, 'type': 'tick', 'pitch': 1.5, 'gain': 0.4})
    cues.append({'t': t_best + 1.1, 'type': 'chime', 'gain': 0.5})
    for k in range(12):
        parts.rewrite(prog, (k * 3) % 8, t_rounds + 0.13 * k, dur=0.2)
    cues.append({'t': t_rounds, 'type': 'rise', 'dur': 1.6, 'pitch': 1.0, 'gain': 0.5})

    # ------------------------------------------------------------ no body: only its code got better
    ghost = parts.outline('no-body', crew, (6.9, parts.FLOOR + 3.1), 0.78, parts.ICE, 0.7)
    parts.visible(ghost['shapes'], [(t_no_body + 0.1, t_code - 0.3)], 0.4)
    cues.append({'t': t_no_body + 0.1, 'type': 'tick', 'gain': 0.5})
    parts.pulse('its-code', side, centre, t_code, 1.6, parts.FROST, 1.0, 0.05)
    cues.append({'t': t_code, 'type': 'chime', 'gain': 0.4, 'pitch': 1.2})
    parts.cut([crew], None, t_was)

    # ------------------------------------------------------------ what Ultron was, and what each does next
    then = kit.empty('then', side)
    parts.cut([then], t_was, None)
    stand = parts.console('console', then, CONSOLE)
    at = (CONSOLE[0], parts.FLOOR + 3.2)
    u = parts.presence('ultron', then, at)
    parts.hover(u, t_was, end)
    parts.open_eyes(u['eyes'], t_was + 0.3)
    parts.blink(u['eyes'], (t_was + 2.6,))
    parts.look(u['eyes'], T.at(4, 0.5), 0.13)
    parts.look(prog['eyes'], T.at(4, 0.5), -0.07)
    was = parts.outline('his-body', then, (at[0], at[1] + 0.12), 0.5)
    parts.visible(was['shapes'], [(t_was + 0.5, t_into)], 0.4)
    parts.visible([stand['beam']], [(t_was, t_into + 0.2)], 0.3)
    cues.append({'t': t_was + 0.3, 'type': 'rise', 'dur': 1.0, 'pitch': 0.7, 'gain': 0.6})

    bot = parts.feeble('body', then, BODY, SCALE)
    times = [t_builds + 0.25 + 0.22 * k for k in range(6)]
    parts.assemble(bot, times, ((CONSOLE[0] - BODY[0]) / SCALE, 1.6), 0.3)
    for k, t0 in enumerate(times):
        cues.append({'t': t0 + 0.3, 'type': 'tick', 'pitch': 0.6 + 0.07 * k, 'gain': 0.7})
    head = (BODY[0] + 0.04 * SCALE, parts.FLOOR + 3.52 * SCALE)
    parts.move_in(u, t_into, at, head, 1.0, 0.62, 0.5)
    parts.hide(u['shapes'], t_into + 0.45, 0.2)
    parts.visible(bot['eyes']['shapes'], [(t_into + 0.45, None)], 0.2)
    cues.append({'t': t_into, 'type': 'swoosh', 'gain': 0.7})
    k, when = 0, t_itself
    while when < end - 0.4:
        parts.rewrite(prog, (k * 5 + 1) % 8, when, dur=0.3)
        cues.append({'t': when, 'type': 'tick', 'pitch': 1.1 + 0.05 * (k % 6), 'gain': 0.5})
        k, when = k + 1, when + 0.32
    parts.pulse('itself', side, centre, t_itself, 1.6, parts.FROST, 1.0, 0.05)

    parts.dip([t_real, t_was])
    cues.append({'t': t_real - 0.2, 'type': 'whoosh', 'gain': 0.6})
    cues.append({'t': t_was - 0.2, 'type': 'whoosh', 'gain': 0.6})
    kit.veil(end - 1.0, 0.9, parts.NIGHT900)

    # ------------------------------------------------------------ camera
    def path(t):
        if t < t_real:
            return mix((1.8, 0.4, 17.8), (2.4, 0.4, 17.0), span(t, 0.0, t_real))
        if t < t_was:
            pos = mix((1.4, 0.4, 17.4), (0.6, 0.4, 18.2), span(t, t_real, T.end(1)))
            pos = mix(pos, (-0.9, 0.4, 20.0), span(t, T.start(2) - 0.6, T.start(2) + 0.8))
            return mix(pos, (3.6, 0.5, 16.2), span(t, t_no_body - 0.4, t_no_body + 1.0))
        pos = mix((-0.9, 0.4, 19.8), (-0.9, 0.4, 19.2), span(t, t_was, t_builds))
        return mix(pos, (0.6, 0.5, 18.2), span(t, t_itself - 0.3, end))

    kit.camera(path, focus_z=1.0)
    return cues
