"""Scene 03: A powerful body.

The city at night: a red light runs along the wire. Then a second lab. The
light comes down a cable into a console, and Ultron's eyes open over it. One
by one the lamps of four machines turn red: machines made for building
robots. They build a tall body out of new steel parts. Ultron crosses into
it: its eyes and the light in its chest come on, and it stands over the
dotted outline of the first, smaller body.
"""
import math

import kit
import parts
from kit import fr, key, mix, sec, span


def build(T):
    cues = []
    end = sec(kit.frames())
    t_lab = T.at(0, 0.3)
    t_arrive = T.at(0, 0.42)
    t_lights = T.at(0, 0.58)
    t_build = T.start(1)
    t_built = T.at(1, 0.5)
    t_wake = T.at(1, 0.56)
    t_strong = T.at(1, 0.8)

    parts.backdrop(seed=41)
    kit.motes(n=18, seed=42, colour=parts.RED)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the city: Ultron on his way
    town = parts.city('city', stage)
    sent = parts.spark('sent', town['root'])
    parts.visible(sent['shapes'], [(0.0, t_lab)], 0.15)
    parts.run(sent, town['masts'][:5], 0.0, t_lab + 0.2)
    for k in range(1, 4):
        when = (t_lab + 0.2) * k / 4
        parts.pulse(f'relay{k}', town['root'], town['masts'][k], when, 0.25, parts.RED, 0.6, 0.05)
        cues.append({'t': when, 'type': 'blip', 'pitch': 0.9 + 0.12 * k, 'gain': 0.5})
    parts.cut([town['root']], None, t_lab)
    parts.dip([t_lab])
    cues.append({'t': t_lab - 0.2, 'type': 'whoosh', 'gain': 0.5})

    # ------------------------------------------------------------ the second lab
    lab = parts.second_lab(far, stage)
    parts.cut(lab['roots'], t_lab, None)
    front = lab['front']
    sx, sy = lab['spot']
    stand = lab['stand']
    scale = 0.9
    cable = [(-10.5, 3.7), (-7.7, 2.4), (sx - 0.5, parts.FLOOR + 1.46 * 0.85)]
    for k, (a, b) in enumerate(zip(cable, cable[1:])):
        kit.branch(f'cable{k}', front, a, b, parts.STEEL800, 0.07, 0.95)

    for k, m in enumerate(lab['machines']):
        t0 = t_lights + 0.3 + 0.24 * k
        parts.light(m, t0)
        cues.append({'t': t0, 'type': 'pop', 'pitch': 0.6 + 0.08 * k, 'gain': 0.8})
        lean = -1 if k < 2 else 1
        parts.work(m, t0, t_build, sh=(0, -12 * lean), el=(-8, 10), rate=0.8)
        parts.work(m, t_build, t_built + 0.5, sh=(-8 * lean, -36 * lean), el=(60 * lean, 12 * lean), rate=0.7 + 0.1 * k)
    first = parts.outline('first', front, (stand[0] - 3.0, parts.FLOOR + 3.17), 0.8, parts.ASH, 0.6)
    parts.visible(first['shapes'], [(t_built + 0.2, None)], 0.5)
    bot = parts.powerful('body', front, stand, scale)
    source = ((lab['rack_at'][0] - stand[0]) / scale, 1.2)
    times = [mix(t_build + 0.2, t_built, k / 5) for k in range(6)]
    parts.assemble(bot, times, source, 0.4)
    for k, t0 in enumerate(times):
        cues.append({'t': t0, 'type': 'whoosh', 'gain': 0.35, 'dur': 0.35})
        cues.append({'t': t0 + 0.4, 'type': 'tick', 'pitch': 0.45 + 0.04 * k, 'gain': 0.9})
    parts.visible(bot['eyes']['shapes'] + [bot['core'][0], bot['core'][2]], [(t_wake + 0.45, None)], 0.3)
    for side, arm in ((-1, bot['arms']['left']), (1, bot['arms']['right'])):
        for t0, deg in ((t_strong, 0), (t_strong + 0.3, 30), (t_strong + 0.9, 12)):
            key(arm, 'rotation_euler', fr(t0), (0, 0, side * math.radians(deg)))
    for t0, s in ((t_strong, 1.0), (t_strong + 0.25, 1.05), (t_strong + 0.6, 1.0)):
        key(bot['rig'], 'scale', fr(t0), (s, s, 1))
    parts.pulse('might', front, (stand[0], parts.FLOOR + 3.85 * scale), t_strong + 0.2, 0.9, parts.RED, 0.9)
    cues.append({'t': t_strong + 0.2, 'type': 'pop', 'pitch': 0.4, 'gain': 1.0})

    # ------------------------------------------------------------ Ultron arrives, and moves into the body
    came = parts.spark('came', front)
    parts.visible(came['shapes'], [(t_lab, t_arrive)], 0.12)
    parts.run(came, cable, t_lab + 0.05, t_arrive)
    u = parts.presence('ultron', front, (sx, sy), 0.85)
    parts.hover(u, 0.0, t_wake + 1.0)
    parts.visible(u['shapes'], [(t_arrive, t_wake + 0.5)], 0.3)
    parts.visible([lab['console']['beam']], [(t_arrive, t_wake)], 0.3)
    parts.open_eyes(u['eyes'], t_arrive + 0.1)
    parts.look(u['eyes'], t_lights, 0.13, 0.03)
    parts.blink(u['eyes'], (t_lights + 1.7,))
    cues.append({'t': t_arrive, 'type': 'rise', 'dur': 0.8, 'pitch': 0.7, 'gain': 0.6})
    head = (stand[0], parts.FLOOR + 4.98 * scale)
    parts.move_in(u, t_wake, (sx, sy), head, 0.85, 0.6)
    cues.append({'t': t_wake, 'type': 'swoosh', 'gain': 0.7})
    cues.append({'t': t_wake + 0.5, 'type': 'chime', 'gain': 0.5, 'pitch': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        if t < t_lab:
            return mix((-2.4, 0.5, 19.6), (0.2, 0.5, 19.0), span(t, 0.0, t_lab))
        pos = mix((-4.4, 0.5, 16.4), (0.0, 0.5, 20.0), span(t, t_lights - 0.3, t_lights + 1.3))
        pos = mix(pos, (0.8, 0.3, 18.2), span(t, t_build, t_built))
        return mix(pos, (0.6, 0.9, 16.2), span(t, t_wake, end))

    kit.camera(path, focus_z=1.0)
    return cues
