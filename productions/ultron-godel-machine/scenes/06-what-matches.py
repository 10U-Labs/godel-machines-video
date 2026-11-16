"""Scene 06: What matches.

A hall. Ultron stands on the left in his powerful body, and the Gödel
Machine floats on the right, a program drawn as its code. A person stands by
each. The one by the Gödel Machine reaches for it, but it rewrites lines of
its own code first, and the person steps back. The one by Ultron steps back
too: a machine with a red lamp, one that Ultron controls, does the work on
his body.
"""
import kit
import parts
from kit import alpha, mix, sec, span

SCALE = 0.82
ULTRON = (-3.4, parts.FLOOR)
PAGE = (3.6, 0.9)


def build(T):
    cues = []
    end = sec(kit.frames())
    t_turn = T.at(0, 0.12)
    t_self = T.at(1, 0.08)
    t_no_one = T.at(1, 0.55)
    t_same = T.at(2, 0.02)
    t_bodies = T.at(2, 0.3)
    t_he = T.at(2, 0.8)

    parts.backdrop(seed=71)
    kit.motes(n=16, seed=72, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    front = parts.room('hall', far, stage, lamps=(-3.4, 3.6), glow=0.1)[1]
    for ob in (parts.spot('red-pool', front, (ULTRON[0], parts.FLOOR + 2.4), 3.2, parts.RED, 0.14),
               parts.spot('blue-pool', front, PAGE, 3.4, parts.ICE, 0.12)):
        alpha(ob, 1, 1.0)

    # ------------------------------------------------------------ the Gödel Machine, and the person beside it
    pg = parts.page('machine', front, PAGE, rows=8, seed=5)
    parts.drift(pg['root'])
    parts.pen('pen', pg['root'], (-pg['w'] / 2 - 0.35, pg['ys'][7]))
    parts.blink(pg['eyes'], (t_turn + 1.4, t_no_one + 1.2, t_bodies + 1.5))
    parts.look(pg['eyes'], t_turn, -0.08)
    who = parts.figure('scientist', front, (6.9, parts.FLOOR), coat='#56707e', coat_deep='#3b505c', hair='#c9c2b8', facing=-1)
    parts.nod(who, phase=0.4)
    parts.reach(who, t_self - 0.6, 66)
    for k, r in enumerate((2, 5)):
        parts.rewrite(pg, r, t_self + 0.75 * k)
        parts.pulse(f'self{k}', front, PAGE, t_self + 0.75 * k, 2.3, parts.FROST, 0.8, 0.05)
        cues.append({'t': t_self + 0.75 * k, 'type': 'blip', 'pitch': 1.2 + 0.15 * k, 'gain': 0.6})
    parts.reach(who, t_no_one, 0, 0.4)
    parts.stroll(who, t_no_one + 0.2, t_no_one + 0.9, 6.9, 7.6)
    parts.rewrite(pg, 0, t_no_one + 1.1)
    cues.append({'t': t_no_one + 1.1, 'type': 'blip', 'pitch': 1.5, 'gain': 0.6})

    # ------------------------------------------------------------ Ultron, and the person beside him
    bot = parts.powerful('ultron', front, ULTRON, SCALE)
    parts.sway(bot, phase=1.1, amount=0.6)
    parts.blink(bot['eyes'], (t_turn + 2.2, t_same + 1.9))
    parts.look(bot['eyes'], t_turn, 0.08)
    maker = parts.figure('maker', front, (-6.5, parts.FLOOR), coat='#7d3b3b', coat_deep='#552525')
    parts.nod(maker, phase=1.7)
    parts.reach(maker, t_bodies - 0.7, 62)
    parts.reach(maker, t_bodies + 0.2, 0, 0.4)
    parts.stroll(maker, t_bodies + 0.4, t_bodies + 1.1, -6.5, -7.4)
    fit = parts.machine('fitter', front, (ULTRON[0] + 2.1, 4.25), 1.5, 1.3)
    head = (ULTRON[0], parts.FLOOR + 4.98 * SCALE)
    order = parts.spark('order', front)
    parts.visible(order['shapes'], [(t_he - 0.45, t_he)], 0.12)
    parts.slide(order['root'], t_he - 0.45, t_he + 0.05, head, (ULTRON[0] + 2.1, 4.15))
    parts.light(fit, t_he)
    parts.work(fit, t_he, end + 0.5, sh=(-8, -36), el=(60, 12), rate=0.8)
    parts.pulse('his-work', front, (ULTRON[0] + 0.9, parts.FLOOR + 4.1 * SCALE), t_he + 0.7, 0.5, parts.RED, 0.7)
    cues.append({'t': t_he - 0.45, 'type': 'swoosh', 'gain': 0.5})
    cues.append({'t': t_he, 'type': 'pop', 'pitch': 0.7})
    cues.append({'t': t_he + 0.7, 'type': 'tick', 'pitch': 0.6, 'gain': 0.7})

    # ------------------------------------------------------------ the two are alike in this
    cues.append({'t': t_turn, 'type': 'whoosh', 'gain': 0.4})
    parts.pulse('same-ultron', front, (ULTRON[0], parts.FLOOR + 2.4), t_same, 2.2, parts.BONE, 1.0, 0.05)
    parts.pulse('same-machine', front, PAGE, t_same, 2.2, parts.BONE, 1.0, 0.05)
    cues.append({'t': t_same, 'type': 'chime', 'gain': 0.5})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((0.0, 0.3, 20.0), (0.2, 0.3, 19.2), span(t, 0.0, T.end(0)))
        pos = mix(pos, (1.9, 0.4, 17.0), span(t, T.start(1) - 0.3, T.start(1) + 1.0))
        pos = mix(pos, (-1.7, 0.4, 17.0), span(t, t_same - 0.3, t_same + 1.1))
        return mix(pos, (-0.6, 0.3, 18.6), span(t, t_he + 0.6, end))

    kit.camera(path, focus_z=1.0)
    return cues
