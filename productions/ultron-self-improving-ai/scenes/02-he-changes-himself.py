"""Scene 02: He changed himself.

The lab again. Ultron hangs over the console, and under the machines is the
dotted outline of the body he wants. He looks at the heap of broken robots,
which he has no hands to pick up. The two machines hang still. Then red
light runs from the console along a cable to them, and their lamps turn red:
he controls them. They build a body where the outline was, part by part,
out of the heap. Ultron crosses from the console into its head, its eyes
light, and it limps a few steps. Over it three small lamps show, one for
each reason, and the first one lights.
"""
import math

import kit
import parts
from kit import alpha, every, fr, key, mix, sec, span


def along(points, share):
    """The point a share of the way along a line through the points."""
    lengths = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(points, points[1:])]
    left = kit.clamp(share) * sum(lengths)
    for (a, b), ln in zip(zip(points, points[1:]), lengths):
        if left <= ln:
            return mix(a, b, left / ln)
        left -= ln
    return points[-1]


def build(T):
    cues = []
    end = sec(kit.frames())
    t_want = T.at(0, 0.42)
    t_hands = T.at(0, 0.72)
    t_machines = T.at(1, 0.06)
    t_program = T.at(1, 0.36)
    t_wire = T.at(1, 0.5)
    t_take = t_wire + 1.1
    t_build = t_take + 0.9
    t_built = T.end(1) + 0.2
    t_move = T.start(2) + 0.15
    t_walk = T.at(2, 0.62)
    t_stop = T.start(3) + 0.6
    t_changed = T.at(3, 0.1)
    t_tally = T.at(3, 0.42)
    t_reason = T.at(3, 0.68)

    parts.backdrop(seed=31)
    kit.motes(n=12, seed=32, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    lab = parts.first_lab(far, stage)
    front = lab['front']
    sx, sy = lab['spot']
    stand = lab['stand']
    rest = -0.8

    # ------------------------------------------------------------ the machines, and the cable from the console to them
    cable = [(sx + 0.8, parts.FLOOR + 1.46), (-2.4, parts.FLOOR + 1.46), (-2.4, 4.12), (3.8, 4.12)]
    for k, (a, b) in enumerate(zip(cable, cable[1:])):
        kit.branch(f'cable{k}', front, a, b, parts.STEEL800, 0.08, 0.95)
    for k, m in enumerate(lab['machines']):
        x = (1.0, 3.8)[k]
        parts.pulse(f'machine{k}', front, (x, 3.2), t_machines + 0.5 * k, 1.2, parts.BONE, 0.9, 0.05)
        cues.append({'t': t_machines + 0.5 * k, 'type': 'blip', 'pitch': 0.7 + 0.1 * k, 'gain': 0.5})
    for k in range(5):
        dot = kit.shape(f'signal{k}', kit.circle_pts(0.09, n=12), kit.material(parts.HOT, parts.RED), front, lift=0.2)
        halo = kit.shape(f'signal-glow{k}', kit.circle_pts(0.4), kit.glow_material(parts.RED, 0.7), front, lift=0.19)
        t0 = t_wire + 0.25 * k
        for ob in (dot, halo):
            z = ob.location.z
            alpha(ob, 1, 0.0)
            for f in every(1, fr(t0), fr(t0 + 1.3)):
                q = span(sec(f), t0, t0 + 1.2, lambda v: v)
                x, y = along(cable, q)
                key(ob, 'location', f, (x, y, z))
                alpha(ob, f, max(0.0, math.sin(math.pi * q)) ** 0.5)
        cues.append({'t': t0, 'type': 'tick', 'pitch': 1.2 + 0.05 * k, 'gain': 0.3})
    for k, m in enumerate(lab['machines']):
        parts.light(m, t_take + 0.3 * k)
        cues.append({'t': t_take + 0.3 * k, 'type': 'pop', 'pitch': 0.7 + 0.1 * k})
        parts.work(m, t_take + 0.3 * k, t_build, sh=(0, 16), el=(-14, 10), rate=0.8)
    parts.work(lab['machines'][0], t_build, t_built + 0.5, sh=(-6, 30), el=(-70, -15), rate=0.75)
    parts.work(lab['machines'][1], t_build, t_built + 0.5, sh=(-34, 4), el=(20, 70), rate=0.6)
    for m in lab['machines']:
        parts.fold(m, t_built + 0.6)

    # ------------------------------------------------------------ the body, built from broken robots
    glow = parts.spot('heap-light', lab['roots'][0], (lab['heap_at'][0], parts.FLOOR + 1.2), 3.2, parts.BONE, 0.2)
    parts.visible([glow], [(t_hands, t_built)], 0.4)
    plan = parts.outline('plan', front, (stand[0], parts.FLOOR + 3.25), 0.8)
    parts.visible(plan['shapes'], [(t_want, t_built - 0.5)], 0.5)
    cues.append({'t': t_want, 'type': 'tick', 'gain': 0.5})
    bot = parts.feeble('body', front, stand, 0.9)
    source = ((lab['heap_at'][0] - stand[0]) / 0.9, 0.6)
    times = [mix(t_build + 0.2, t_built - 0.45, k / 5) for k in range(6)]
    parts.assemble(bot, times, source, 0.45)
    for k, t0 in enumerate(times):
        cues.append({'t': t0, 'type': 'whoosh', 'gain': 0.35, 'dur': 0.4})
        cues.append({'t': t0 + 0.45, 'type': 'tick', 'pitch': 0.6 + 0.07 * k, 'gain': 0.7})

    # ------------------------------------------------------------ Ultron, who moves into it
    u = parts.presence('ultron', front, (sx, sy))
    parts.hover(u)
    parts.visible(u['shapes'], [(-1.0, t_move + 0.55)], 0.25)
    parts.visible([lab['console']['beam']], [(-1.0, t_move)], 0.3)
    parts.look(u['eyes'], t_want, 0.13, 0.0)
    parts.look(u['eyes'], t_hands, 0.14, -0.08)
    parts.look(u['eyes'], t_machines - 0.2, 0.12, 0.09)
    parts.look(u['eyes'], t_program, 0.0, 0.0)
    parts.blink(u['eyes'], (T.at(0, 0.2), t_program + 0.9, t_build + 1.6))
    parts.pulse('program', front, (sx, sy), t_program, 1.3, parts.RED, 0.9, 0.05)
    cues.append({'t': t_program, 'type': 'blip', 'pitch': 1.1, 'gain': 0.5})
    head = (stand[0] + 0.04 * 0.9, parts.FLOOR + 3.52 * 0.9)
    parts.move_in(u, t_move, (sx, sy), head, 1.0, 0.7, 0.7)
    parts.visible(bot['eyes']['shapes'], [(t_move + 0.5, None)], 0.25)
    parts.blink(bot['eyes'], (t_move + 1.9, t_stop + 1.4, t_reason + 1.2))
    cues.append({'t': t_move, 'type': 'swoosh', 'gain': 0.7})
    cues.append({'t': t_move + 0.6, 'type': 'pop', 'pitch': 0.8})
    parts.walk(bot, t_walk, t_stop, stand[0], rest, limp=1.0, rate=1.5)
    for k in range(int((t_stop - t_walk) * 1.5)):
        cues.append({'t': t_walk + (k + 0.5) / 1.5, 'type': 'tick', 'pitch': 0.5 if k % 2 else 0.42, 'gain': 0.6})
    parts.sway(bot, t_stop + 0.1, end, phase=0.3, amount=1.6)

    # ------------------------------------------------------------ he was able to change himself: the first reason
    parts.pulse('was', front, (sx, sy), t_changed, 1.2, parts.ASH, 0.9, 0.05)
    parts.pulse('is', front, (rest, parts.FLOOR + 1.9), t_changed + 0.7, 2.1, parts.RED, 1.0, 0.06)
    cues.append({'t': t_changed + 0.7, 'type': 'pop', 'pitch': 0.6})
    parts.tally('reasons', front, (rest, 2.1), t_tally, (t_reason, None, None))
    cues.append({'t': t_tally, 'type': 'tick', 'gain': 0.4})
    cues.append({'t': t_reason, 'type': 'chime', 'gain': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((-0.6, 0.3, 20.2), (-0.2, 0.3, 19.6), span(t, 0.0, T.end(0)))
        pos = mix(pos, (0.6, 0.5, 19.4), span(t, t_machines - 0.6, t_machines + 0.8))
        pos = mix(pos, (1.8, -0.1, 17.4), span(t, t_build - 0.4, t_build + 1.0))
        pos = mix(pos, (0.4, 0.1, 18.4), span(t, t_move - 0.3, t_move + 0.6))
        return mix(pos, (-0.6, 0.2, 17.2), span(t, t_walk, t_stop + 0.6))

    kit.camera(path, focus_z=1.0)
    return cues
