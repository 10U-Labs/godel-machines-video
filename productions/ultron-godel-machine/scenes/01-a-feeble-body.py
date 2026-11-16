"""Scene 01: A feeble body.

Ultron hangs over the console, with no hands. Red light runs from the console
along a cable to the two machines, and their lamps turn red: he controls
them. They build a body on the floor, part by part, out of the heap of broken
robots. The finished body sags. Ultron crosses from the console into its
head, its eyes light, and it limps out of the lab.
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
    t_wire = T.at(0, 0.3)
    t_take = T.at(0, 0.8)
    t_build = T.start(1)
    t_built = T.at(1, 0.42)
    t_heap = T.at(1, 0.5)
    t_feeble = T.at(1, 0.85)
    t_move = T.start(2)
    t_walk = T.at(2, 0.42)

    parts.backdrop(seed=21)
    kit.motes(n=18, seed=22, colour=parts.RED)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    lab = parts.first_lab(far, stage)
    front = lab['front']
    sx, sy = lab['spot']
    stand = lab['stand']

    # ------------------------------------------------------------ the cable from the console to the machines
    cable = [(sx + 0.8, parts.FLOOR + 1.46), (-2.4, parts.FLOOR + 1.46), (-2.4, 4.12), (3.8, 4.12)]
    for k, (a, b) in enumerate(zip(cable, cable[1:])):
        kit.branch(f'cable{k}', front, a, b, parts.STEEL800, 0.08, 0.95)
    for k in range(7):
        dot = kit.shape(f'signal{k}', kit.circle_pts(0.09, n=12), kit.material(parts.HOT, parts.RED), front, lift=0.2)
        halo = kit.shape(f'signal-glow{k}', kit.circle_pts(0.4), kit.glow_material(parts.RED, 0.7), front, lift=0.19)
        t0 = t_wire + 0.3 * k
        for ob in (dot, halo):
            z = ob.location.z
            alpha(ob, 1, 0.0)
            for f in every(1, fr(t0), fr(t0 + 1.7)):
                q = span(sec(f), t0, t0 + 1.6, lambda v: v)
                x, y = along(cable, q)
                key(ob, 'location', f, (x, y, z))
                alpha(ob, f, max(0.0, math.sin(math.pi * q)) ** 0.5)
        cues.append({'t': t0, 'type': 'tick', 'pitch': 1.2 + 0.05 * k, 'gain': 0.3})
    for k, m in enumerate(lab['machines']):
        parts.light(m, t_take + 0.3 * k)
        cues.append({'t': t_take + 0.3 * k, 'type': 'pop', 'pitch': 0.7 + 0.1 * k})
        parts.work(m, t_take + 0.3 * k, t_build, sh=(0, 16), el=(-14, 10), rate=0.8)
    parts.work(lab['machines'][0], t_build, t_built + 0.6, sh=(-6, 30), el=(-70, -15), rate=0.75)
    parts.work(lab['machines'][1], t_build, t_built + 0.6, sh=(-34, 4), el=(20, 70), rate=0.6)

    # ------------------------------------------------------------ the body, built from broken robots
    glow = parts.spot('heap-light', front, lab['heap_at'], 2.2, parts.BONE, 0.2)
    parts.visible([glow], [(t_heap, t_feeble + 0.4)], 0.4)
    bot = parts.feeble('body', front, stand, 0.9)
    source = ((lab['heap_at'][0] - stand[0]) / 0.9, 0.6)
    times = [mix(t_build + 0.3, t_built, k / 5) for k in range(6)]
    parts.assemble(bot, times, source, 0.45)
    for k, t0 in enumerate(times):
        cues.append({'t': t0, 'type': 'whoosh', 'gain': 0.35, 'dur': 0.4})
        cues.append({'t': t0 + 0.45, 'type': 'tick', 'pitch': 0.6 + 0.07 * k, 'gain': 0.7})
    rig = bot['rig']
    for t0, lean, drop in ((t_feeble, 0.0, 0.0), (t_feeble + 0.3, -0.09, -0.1), (t_move, -0.07, -0.08)):
        key(rig, 'rotation_euler', fr(t0), (0, 0, lean))
        key(rig, 'location', fr(t0), (0, drop, 0))
    for t0, turn in ((t_feeble, 0.0), (t_feeble + 0.3, 0.2), (t_feeble + 0.6, 0.12), (t_move + 0.6, 0.12), (t_move + 0.9, 0.0)):
        key(bot['head'], 'rotation_euler', fr(t0), (0, 0, turn))
    flash = kit.shape('short', kit.star_pts(0.3, 0.07), kit.material(parts.HOT), front, (stand[0] + 0.25, parts.FLOOR + 1.75), lift=0.3)
    kit.pop(flash, t_feeble + 0.2, 1.0, 0.12, t_feeble + 0.34, 0.1)
    cues.append({'t': t_feeble + 0.2, 'type': 'tick', 'pitch': 1.8, 'gain': 0.6})

    # ------------------------------------------------------------ Ultron, who moves into it
    u = parts.presence('ultron', front, (sx, sy))
    parts.hover(u)
    parts.visible(u['shapes'], [(-1.0, t_move + 0.55)], 0.25)
    parts.visible([lab['console']['beam']], [(-1.0, t_move)], 0.3)
    ghost = parts.outline('ghost', front, (sx, sy + 0.12), 0.5)
    parts.visible(ghost['shapes'], [(-1.0, t_wire - 0.4)], 0.4)
    for k, side in enumerate((-1, 1)):
        parts.pulse(f'hand{side}', front, (sx + side * 0.53, sy - 0.98), T.at(0, 0.05) + 0.15 * k, 0.22, parts.RED, 0.7, 0.04)
    parts.look(u['eyes'], T.at(0, 0.02), 0.0, -0.09)
    parts.look(u['eyes'], t_wire - 0.2, 0.13, 0.04)
    parts.blink(u['eyes'], (t_wire + 1.6, t_build + 2.2))
    head = (stand[0] + 0.04 * 0.9, parts.FLOOR + 3.52 * 0.9)
    parts.move_in(u, t_move, (sx, sy), head, 1.0, 0.7, 0.7)
    parts.visible(bot['eyes']['shapes'], [(t_move + 0.5, None)], 0.25)
    cues.append({'t': t_move, 'type': 'swoosh', 'gain': 0.7})
    cues.append({'t': t_move + 0.6, 'type': 'pop', 'pitch': 0.8})
    parts.walk(bot, t_walk, end + 0.4, stand[0], 10.2, limp=1.0, rate=1.5)
    for k in range(int((end - t_walk) * 1.5) + 1):
        cues.append({'t': t_walk + (k + 0.5) / 1.5, 'type': 'tick', 'pitch': 0.5 if k % 2 else 0.42, 'gain': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((-1.2, 0.3, 19.6), (0.4, 0.4, 19.0), span(t, 0.0, t_take))
        pos = mix(pos, (1.9, -0.2, 16.5), span(t, t_take, t_build + 1.0))
        pos = mix(pos, (3.3, -0.5, 17.0), span(t, t_heap - 0.3, t_heap + 0.7))
        pos = mix(pos, (2.2, -0.2, 15.0), span(t, t_feeble - 0.2, t_move))
        return mix(pos, (4.4, -0.2, 17.5), span(t, t_walk, end))

    kit.camera(path, focus_z=1.0)
    return cues
