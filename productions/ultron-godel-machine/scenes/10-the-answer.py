"""Scene 10: The answer.

The hall. Ultron and the Gödel Machine face each other, joined by a line of
dots with a question mark over it. The mark drops away and the line parts in
the middle: they look away from each other. Then what the answer rests on.
Behind Ultron his earlier forms light in turn, and a red light passes along
them to him. A ring goes round his body, and beside his head his own program
hangs with no line changed. A proof's mark shines beside the Gödel Machine,
and beside Ultron there is a ring of dots with nothing in it.
"""
import kit
import parts
from kit import alpha, mix, span

SCALE = 0.82
ULTRON = (-3.4, parts.FLOOR)
PAGE = (4.0, 0.9)
LINK = 14


def build(T):
    cues = []
    t_ask = T.at(0, 0.08)
    t_no = T.at(0, 0.8)
    t_improve = T.start(1)
    t_body = T.at(1, 0.3)
    t_code = T.at(1, 0.45)
    t_proof = T.at(1, 0.57)

    parts.backdrop(seed=111)
    kit.motes(n=16, seed=112, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    front = parts.room('hall', far, stage, lamps=(-3.4, 4.0), glow=0.1)[1]
    for ob in (parts.spot('red-pool', front, (ULTRON[0], parts.FLOOR + 2.4), 3.2, parts.RED, 0.14),
               parts.spot('blue-pool', front, PAGE, 3.4, parts.ICE, 0.12)):
        alpha(ob, 1, 1.0)

    # ------------------------------------------------------------ the two, and the question between them
    earlier = parts.presence('no-body', front, (-7.3, parts.FLOOR + 1.3), 0.4)
    second = parts.outline('feeble', front, (-5.75, parts.FLOOR + 2.2), 0.55, parts.ASH, 0.8)
    bot = parts.powerful('ultron', front, ULTRON, SCALE)
    parts.sway(bot, phase=1.1, amount=0.6)
    parts.blink(bot['eyes'], (t_ask + 1.0, t_improve + 2.4, t_proof + 2.0))
    head = (ULTRON[0], parts.FLOOR + 4.98 * SCALE)
    pg = parts.page('machine', front, PAGE, rows=8, seed=5)
    parts.drift(pg['root'])
    parts.pen('pen', pg['root'], (-pg['w'] / 2 - 0.4, pg['ys'][7]))
    parts.blink(pg['eyes'], (t_ask + 1.5, t_body + 0.6, t_proof + 2.9))
    who = parts.figure('scientist', front, (7.4, parts.FLOOR), coat='#56707e', coat_deep='#3b505c', hair='#c9c2b8', facing=-1)
    parts.nod(who, phase=0.4)

    a, b = (ULTRON[0] + 1.0, 1.35), (PAGE[0] - 1.95, 1.35)
    for k in range(LINK):
        dot = kit.shape(f'link{k}', kit.circle_pts(0.05, n=10), kit.material(parts.BONE), front, mix(a, b, k / (LINK - 1)))
        t_in = t_ask + 0.04 * min(k, LINK - 1 - k)
        t_out = t_no + 0.05 * (LINK / 2 - 0.5 - min(k, LINK - 1 - k))
        kit.appear(dot, t_in, t_out, 0.15)
    mark = kit.text('mark', '?', 1.3, kit.material(parts.BONE), front, ((a[0] + b[0]) / 2, 2.35))
    kit.pop(mark, t_ask + 0.2, 1.0, 0.45, t_no, 0.25)
    parts.look(bot['eyes'], t_ask, 0.08)
    parts.look(pg['eyes'], t_ask, -0.08)
    parts.look(bot['eyes'], t_no + 0.1, -0.08, 0.0, 0.4)
    parts.look(pg['eyes'], t_no + 0.1, 0.08, 0.0, 0.4)
    cues.append({'t': t_ask, 'type': 'rise', 'dur': 1.0, 'pitch': 0.8, 'gain': 0.5})
    cues.append({'t': t_no, 'type': 'pop', 'pitch': 0.42, 'gain': 1.0})
    cues.append({'t': t_no + 0.15, 'type': 'tick', 'pitch': 0.5, 'gain': 0.7})

    # ------------------------------------------------------------ he does improve himself
    parts.hover(earlier)
    parts.visible(earlier['shapes'] + second['shapes'], [(t_improve, t_proof - 0.2)], 0.4)
    stops = [(-7.3, parts.FLOOR + 1.35), (-5.75, parts.FLOOR + 2.2), head]
    own_light = parts.spark('own-light', front)
    t0, t1 = t_improve + 0.5, t_body - 0.5
    parts.visible(own_light['shapes'], [(t0, t1)], 0.15)
    parts.run(own_light, stops, t0, t1 + 0.1)
    for k, at in enumerate(stops):
        when = mix(t0, t1, k / 2)
        parts.pulse(f'own{k}', front, at, when, 0.45, parts.RED, 0.8)
        cues.append({'t': when, 'type': 'blip', 'pitch': 0.8 + 0.2 * k, 'gain': 0.6})

    # ------------------------------------------------------------ his body, not his code
    parts.pulse('his-body', front, (ULTRON[0], parts.FLOOR + 2.4), t_body, 2.3, parts.BONE, 1.0, 0.06)
    cues.append({'t': t_body, 'type': 'pop', 'pitch': 0.6})
    mine = parts.own_program('own', front, (ULTRON[0] + 2.35, 2.05), 0.45)
    kit.pop(mine['root'], t_code, 0.45)
    parts.blink(mine['eyes'], (t_code + 1.3, t_proof + 2.4))
    cues.append({'t': t_code, 'type': 'pop', 'pitch': 0.9, 'gain': 0.6})

    # ------------------------------------------------------------ and no proof
    proof = parts.seal('proof', front, (PAGE[0] - 2.5, 0.15), 0.8)
    kit.pop(proof, t_proof + 0.3, 0.8)
    cues.append({'t': t_proof + 0.3, 'type': 'chime', 'gain': 0.5})
    none = parts.dotted_ring('no-proof', front, (ULTRON[0] + 2.35, 0.15), 0.42)
    parts.visible(none['shapes'], [(t_proof + 1.6, None)], 0.5)
    cues.append({'t': t_proof + 1.6, 'type': 'tick', 'pitch': 0.5, 'gain': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((0.2, 0.3, 20.2), (0.2, 0.4, 19.0), span(t, 0.0, t_no))
        pos = mix(pos, (-2.3, 0.4, 17.8), span(t, t_improve - 0.3, t_improve + 1.0))
        return mix(pos, (0.2, 0.4, 19.4), span(t, t_proof - 0.3, t_proof + 1.0))

    kit.camera(path, focus_z=1.0)
    return cues
