"""Scene 08: Better at getting better.

The Gödel Machine's code, close. Its lines light up in turn, and a pen marks
the one that does the rewriting. Lines are rewritten, and then the pen's own
line is rewritten, and the pen grows. After that it rewrites more lines at
once, and faster, and grows again. Then the hall's other side: a hero
strikes Ultron's powerful body, and the blow does nothing. But beside him his
own program hangs as it was, with no line changed.
"""
import kit
import parts
from kit import alpha, fr, key, mix, sec, span

SCALE = 0.82
ULTRON = (-3.9, parts.FLOOR)
PAGE = (3.3, 0.9)
ROUNDS = [  # the lines each round rewrites, the time between them, and the pen's size once its own line is rewritten
    ((2, 4), 0.42, 1.35),
    ((0, 3, 5), 0.22, 1.75),
    ((1, 2, 4, 6, 0), 0.13, 2.2),
]


def build(T):
    cues = []
    end = sec(kit.frames())
    t_many = T.at(0, 0.03)
    t_one = T.at(0, 0.34)
    t_rounds = [T.at(0, 0.6), T.at(1, 0.03), T.at(1, 0.55)]
    t_pens = [T.at(0, 0.85), T.at(1, 0.03) + 0.85, T.at(1, 0.55) + 0.85]
    t_body = T.start(2)
    t_blow = T.at(2, 0.4)
    t_not = T.at(2, 0.58)

    parts.backdrop(seed=91)
    kit.motes(n=16, seed=92, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    front = parts.room('hall', far, stage, lamps=(-3.9, 3.3), glow=0.1)[1]
    for ob in (parts.spot('red-pool', front, (ULTRON[0], parts.FLOOR + 2.4), 3.2, parts.RED, 0.14),
               parts.spot('blue-pool', front, PAGE, 3.4, parts.ICE, 0.12)):
        alpha(ob, 1, 1.0)

    # ------------------------------------------------------------ the Gödel Machine's code, and the line that rewrites
    pg = parts.page('machine', front, PAGE, rows=8, seed=5)
    parts.blink(pg['eyes'], (t_one + 1.2, t_rounds[1] + 0.4, t_body + 0.6))
    for r in range(7):
        lit = parts.band(pg, r, parts.FROST, 0.28)
        when = mix(t_many, t_one - 0.5, r / 6)
        for dt, a in ((0.0, 0.0), (0.12, 1.0), (0.5, 0.0)):
            alpha(lit, fr(when + dt), a)
        cues.append({'t': when, 'type': 'tick', 'pitch': 0.9 + 0.06 * r, 'gain': 0.35})
    own = parts.band(pg, 7, parts.BONE, 0.34)
    for when, a in ((t_one, 0.0), (t_one + 0.25, 1.0), (end, 1.0)):
        alpha(own, fr(when), a)
    quill = parts.pen('pen', pg['root'], (-pg['w'] / 2 - 0.4, pg['ys'][7]))
    kit.pop(quill, t_one + 0.15, 1.0)
    cues.append({'t': t_one + 0.15, 'type': 'pop', 'pitch': 1.3})
    size = 1.0
    for k, ((rows, gap, grown), t0, t_pen) in enumerate(zip(ROUNDS, t_rounds, t_pens)):
        for j, r in enumerate(rows):
            parts.rewrite(pg, r, t0 + gap * j, dur=min(0.45, gap * 1.6))
            cues.append({'t': t0 + gap * j, 'type': 'tick', 'pitch': 1.0 + 0.2 * k + 0.05 * j, 'gain': 0.55})
        parts.rewrite(pg, 7, t_pen)
        parts.resize(quill, t_pen + 0.15, size, grown)
        parts.pulse(f'grown{k}', front, (PAGE[0] - pg['w'] / 2 - 0.4, PAGE[1] + pg['ys'][7]), t_pen + 0.15, 0.35 * grown, parts.FROST, 0.8, 0.05)
        cues.append({'t': t_pen + 0.15, 'type': 'rise', 'dur': 0.5, 'pitch': 0.9 + 0.25 * k, 'gain': 0.55})
        size = grown
    for when, s in ((t_rounds[0], 1.0), (t_pens[2] + 0.6, 1.25)):
        key(pg['glow'], 'scale', fr(when), (s, s, 1))
    who = parts.figure('scientist', front, (7.3, parts.FLOOR), coat='#56707e', coat_deep='#3b505c', hair='#c9c2b8', facing=-1)
    parts.nod(who, phase=0.4)

    # ------------------------------------------------------------ Ultron: a body that is harder to smash, and no more
    bot = parts.powerful('ultron', front, ULTRON, SCALE)
    parts.sway(bot, phase=1.1, amount=0.6)
    parts.blink(bot['eyes'], (t_body + 1.1, t_not + 1.6))
    parts.pulse('stronger', front, (ULTRON[0], parts.FLOOR + 2.4), t_body + 0.3, 2.2, parts.RED, 0.9, 0.06)
    hero = parts.figure('hero', front, (-11.0, parts.FLOOR), coat='#3d5a80', coat_deep='#2a3f5c', hair='#c9b27a')
    parts.stroll(hero, t_body + 0.3, t_blow - 0.3, -11.0, -6.7)
    parts.reach(hero, t_blow - 0.4, 100, 0.2)
    mark = (ULTRON[0] - 1.05, parts.FLOOR + 3.0)
    parts.strike('blow', front, t_blow - 0.12, (-6.1, parts.FLOOR + 2.3), mark)
    parts.pulse('held', front, mark, t_blow, 0.5, parts.BONE, 0.6, 0.06)
    for when, lean in ((t_blow, 0.0), (t_blow + 0.1, -0.03), (t_blow + 0.5, 0.0)):
        key(bot['rig'], 'rotation_euler', fr(when), (0, 0, lean))
    parts.stroll(hero, t_blow + 0.15, t_blow + 0.8, -6.7, -7.7)
    parts.reach(hero, t_blow + 0.2, 25, 0.4)
    cues.append({'t': t_blow - 0.3, 'type': 'whoosh', 'gain': 0.8})
    cues.append({'t': t_blow, 'type': 'tick', 'pitch': 1.7, 'gain': 0.9})
    cues.append({'t': t_blow, 'type': 'pop', 'pitch': 0.45, 'gain': 0.8})
    mine = parts.own_program('own', front, (ULTRON[0] + 2.6, 1.7), 0.5)
    kit.pop(mine['root'], t_not, 0.5)
    parts.drift(mine['root'], t_not + 0.5, end, 0.06)
    parts.blink(mine['eyes'], (t_not + 1.4, t_not + 2.6))
    cues.append({'t': t_not, 'type': 'pop', 'pitch': 0.9, 'gain': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((3.3, 0.5, 15.0), (3.1, 0.5, 14.0), span(t, 0.0, T.end(1)))
        pos = mix(pos, (-3.6, 0.5, 16.6), span(t, t_body - 0.4, t_body + 1.0))
        return mix(pos, (-2.9, 0.5, 15.8), span(t, t_not, end))

    kit.camera(path, focus_z=1.0)
    return cues
