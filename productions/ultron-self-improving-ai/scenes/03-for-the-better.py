"""Scene 03: For the better.

A second lab, with four machines made for building robots and racks of new
parts. Ultron's feeble body stands in it, and it sags. He lifts its one good
arm, the machines' lamps turn red, and they build a tall body of clean
steel. A red light crosses from the feeble head to the new one: its eyes and
the light in its chest come on, and the feeble body slumps. Then the hall,
where his three forms stand in a row, and each is lit in turn. The first
looks about and stays where it is. The second limps a few steps. The third
strikes a steel plate, which flies off. A light passes from form to form,
and of the three small lamps the second one lights.
"""
import math

import kit
import parts
from kit import every, fr, key, mix, sec, span

SCALE = 0.9
OLD = (-3.6, parts.FLOOR)
PLATE = (5.45, parts.FLOOR + 2.1)


def build(T):
    cues = []
    end = sec(kit.frames())
    t_feeble = T.at(0, 0.12)
    t_go = T.at(0, 0.42)
    t_build = t_go + 0.7
    t_built = T.end(0) + 0.1
    t_move = t_built + 0.25
    t_strong = t_move + 1.0
    t_hall = T.at(1, 0.24)
    t_first, t_second, t_third = T.at(1, 0.27), T.at(1, 0.52), T.at(1, 0.72)
    t_blow = T.at(1, 0.9)
    t_hop0, t_hop1 = T.at(2, 0.04), T.at(2, 0.42)
    t_tally = T.at(2, 0.5)
    t_reason = T.at(2, 0.84)

    parts.backdrop(seed=41)
    kit.motes(n=12, seed=42, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the second lab: a better body
    lab = parts.second_lab(far, stage)
    parts.cut(lab['roots'], None, t_hall)
    front = lab['front']
    stand = lab['stand']
    weak = parts.feeble('weak', front, OLD, SCALE)
    old_head = (OLD[0] + 0.04 * SCALE, parts.FLOOR + 3.52 * SCALE)
    new_head = (stand[0], parts.FLOOR + 4.98 * SCALE)
    parts.blink(weak['eyes'], (T.at(0, 0.05), t_go + 1.4))
    for when, lean, drop in ((t_feeble, 0.0, 0.0), (t_feeble + 0.3, -0.09, -0.1), (t_move, -0.07, -0.08), (t_move + 0.7, -0.17, -0.16)):
        key(weak['rig'], 'rotation_euler', fr(when), (0, 0, lean))
        key(weak['rig'], 'location', fr(when), (0, drop, 0))
    for when, tilt in ((t_feeble, 0.0), (t_feeble + 0.3, 0.2), (t_go, 0.12), (t_go + 0.3, -0.06), (t_move, -0.06), (t_move + 0.8, 0.32)):
        key(weak['head'], 'rotation_euler', fr(when), (0, 0, tilt))
    for when, deg in ((t_go - 0.1, 0), (t_go + 0.35, 118), (t_move, 112), (t_move + 0.6, 0)):
        key(weak['arms']['left'], 'rotation_euler', fr(when), (0, 0, math.radians(deg)))
    short = kit.shape('short', kit.star_pts(0.3, 0.07), kit.material(parts.HOT), front, (OLD[0] + 0.25, parts.FLOOR + 1.75), lift=0.3)
    kit.pop(short, t_feeble + 0.2, 1.0, 0.12, t_feeble + 0.34, 0.1)
    cues.append({'t': t_feeble + 0.2, 'type': 'tick', 'pitch': 1.8, 'gain': 0.6})
    cues.append({'t': t_feeble + 0.3, 'type': 'pop', 'pitch': 0.4, 'gain': 0.5})

    for k, m in enumerate(lab['machines']):
        t0 = t_go + 0.2 + 0.14 * k
        parts.light(m, t0)
        cues.append({'t': t0, 'type': 'pop', 'pitch': 0.6 + 0.08 * k, 'gain': 0.8})
        lean = -1 if k < 2 else 1
        parts.work(m, t_build, t_built + 0.4, sh=(-8 * lean, -36 * lean), el=(60 * lean, 12 * lean), rate=0.7 + 0.1 * k)
        parts.fold(m, t_built + 0.5, lean * 30, lean * 85)
    strong = parts.powerful('strong', front, stand, SCALE)
    source = ((lab['rack_at'][0] - stand[0]) / SCALE, 1.2)
    times = [mix(t_build + 0.1, t_built - 0.4, k / 5) for k in range(6)]
    parts.assemble(strong, times, source, 0.4)
    for k, t0 in enumerate(times):
        cues.append({'t': t0, 'type': 'whoosh', 'gain': 0.35, 'dur': 0.35})
        cues.append({'t': t0 + 0.4, 'type': 'tick', 'pitch': 0.45 + 0.04 * k, 'gain': 0.9})

    # he moves from the feeble body into the better one
    moving = parts.spark('moving', front)
    parts.visible(moving['shapes'], [(t_move, t_move + 0.6)], 0.1)
    parts.hop(moving, [old_head, new_head], t_move, t_move + 0.6, lift=1.5)
    parts.hide(weak['eyes']['shapes'], t_move, 0.15)
    parts.visible(strong['eyes']['shapes'] + [strong['core'][0], strong['core'][2]], [(t_move + 0.55, None)], 0.25)
    cues.append({'t': t_move, 'type': 'swoosh', 'gain': 0.7})
    cues.append({'t': t_move + 0.6, 'type': 'chime', 'gain': 0.5, 'pitch': 0.6})
    for side, arm in ((-1, strong['arms']['left']), (1, strong['arms']['right'])):
        for when, deg in ((t_strong, 0), (t_strong + 0.3, 30), (t_strong + 0.9, 12)):
            key(arm, 'rotation_euler', fr(when), (0, 0, side * math.radians(deg)))
    for when, s in ((t_strong, 1.0), (t_strong + 0.25, 1.05), (t_strong + 0.6, 1.0)):
        key(strong['rig'], 'scale', fr(when), (s, s, 1))
    parts.pulse('might', front, (stand[0], parts.FLOOR + 3.85 * SCALE), t_strong + 0.2, 0.9, parts.RED, 0.9)
    cues.append({'t': t_strong + 0.2, 'type': 'pop', 'pitch': 0.4, 'gain': 1.0})

    # ------------------------------------------------------------ the hall: each form could do more than the last
    hall = parts.room('hall', far, stage, lamps=(-5.4, -1.9, 2.4), glow=0.05)
    parts.cut(hall, t_hall, None)
    near = hall[1]
    parts.dip([t_hall])
    cues.append({'t': t_hall - 0.2, 'type': 'whoosh', 'gain': 0.5})
    forms = parts.three_forms(near)
    row = forms['root']
    first, second, third = forms['first'], forms['second'], forms['third']
    walked = -0.7
    for k, when in enumerate((t_first, t_second, t_third)):
        pool = parts.spot(f'pool{k}', row, (parts.FORMS[k][0] + (0.6 if k == 1 else 0.0), parts.FLOOR + 2.2), 2.9, parts.RED, 0.22)
        parts.visible([pool], [(when, None)], 0.3)
        cues.append({'t': when, 'type': 'blip', 'pitch': 0.7 + 0.15 * k, 'gain': 0.5})

    # the first could not move
    parts.hover(first, t_hall, end)
    for when, dx in ((t_first + 0.3, -0.13), (t_first + 0.9, 0.13), (t_first + 1.5, -0.1), (t_first + 2.0, 0.0)):
        parts.look(first['eyes'], when, dx, 0.0)
    parts.blink(first['eyes'], (t_second + 1.2, t_hop0 - 0.4))

    # the second could walk
    parts.sway(second, t_hall, t_second, phase=0.6, amount=1.6)
    parts.walk(second, t_second + 0.2, t_third - 0.1, parts.FORMS[1][0], walked, limp=1.0, rate=1.5)
    parts.sway(second, t_third, end, phase=0.6, amount=1.6)
    for k in range(int((t_third - 0.3 - t_second) * 1.5)):
        cues.append({'t': t_second + 0.2 + (k + 0.5) / 1.5, 'type': 'tick', 'pitch': 0.5 if k % 2 else 0.42, 'gain': 0.6})
    parts.blink(second['eyes'], (t_first + 0.8, t_third + 1.0))

    # the third was strong enough to fight
    plate = parts.group('plate', near, PLATE)
    kit.shape('plate-slab', kit.rrect_pts(0.5, 4.2, 0.06), kit.material(parts.STEEL500, parts.STEEL700), plate)
    for i in range(4):
        kit.shape(f'plate-rivet{i}', kit.circle_pts(0.05, n=10), kit.material(parts.STEEL300), plate, (0, -1.65 + 1.1 * i))
    reach = third['arms']['right']
    for when, deg in ((t_blow - 0.5, 0), (t_blow - 0.15, -28), (t_blow, 92), (t_blow + 1.0, 92), (t_blow + 1.5, 12)):
        key(reach, 'rotation_euler', fr(when), (0, 0, math.radians(deg)))
    for when, lean in ((t_blow - 0.5, 0.0), (t_blow - 0.15, 0.05), (t_blow, -0.08), (t_blow + 1.0, -0.08), (t_blow + 1.5, 0.0)):
        key(third['rig'], 'rotation_euler', fr(when), (0, 0, lean))
    parts.strike('blow', near, t_blow - 0.1, (4.2, 0.78), (5.2, 0.78))
    z = plate.location.z
    t_hit = t_blow + 0.02
    key(plate, 'location', max(1, fr(t_hit) - 1), (PLATE[0], PLATE[1], z))
    key(plate, 'rotation_euler', max(1, fr(t_hit) - 1), (0, 0, 0))
    for f in every(1, fr(t_hit), fr(t_hit + 0.7)):
        q = span(sec(f), t_hit, t_hit + 0.7, lambda v: v)
        key(plate, 'location', f, (PLATE[0] + 9.0 * q, PLATE[1] + 2.4 * math.sin(math.pi * q * 0.8), z))
        key(plate, 'rotation_euler', f, (0, 0, -2.6 * q))
    cues.append({'t': t_blow - 0.1, 'type': 'swoosh', 'gain': 0.8})
    cues.append({'t': t_hit, 'type': 'pop', 'pitch': 0.35, 'gain': 1.0})
    parts.sway(third, t_hall, t_blow - 0.6, phase=1.9, amount=0.6)
    parts.blink(third['eyes'], (t_second + 0.5, t_blow + 1.8))

    # he was able to improve himself, and more than once: the second reason
    heads = [forms['heads'][0], (walked + 0.04 * parts.FORM_SCALE, forms['heads'][1][1]), forms['heads'][2]]
    more = parts.spark('more', row)
    parts.visible(more['shapes'], [(t_hop0, t_hop1 + 0.1)], 0.15)
    parts.hop(more, heads, t_hop0, t_hop1)
    for k in range(1, 3):
        when = mix(t_hop0, t_hop1, k / 2)
        parts.pulse(f'better{k}', row, (heads[k][0], parts.FLOOR + 1.8 + 0.3 * k), when, 1.5 + 0.4 * k, parts.RED, 0.9, 0.06)
        cues.append({'t': when, 'type': 'pop', 'pitch': 0.8 - 0.15 * k, 'gain': 0.8})
    cues.append({'t': t_hop0, 'type': 'rise', 'dur': t_hop1 - t_hop0, 'pitch': 0.7, 'gain': 0.4})
    parts.tally('reasons', near, (-1.5, 3.1), t_tally, (-1.0, t_reason, None))
    cues.append({'t': t_tally, 'type': 'tick', 'gain': 0.4})
    cues.append({'t': t_reason, 'type': 'chime', 'gain': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        if t < t_hall:
            pos = mix((-1.6, 0.2, 17.6), (0.2, 0.4, 19.4), span(t, t_go - 0.6, t_go + 0.8))
            return mix(pos, (0.3, 0.6, 17.6), span(t, t_move, t_hall))
        pos = mix((-2.4, 0.3, 19.0), (-1.3, 0.3, 19.6), span(t, t_hall, t_second))
        pos = mix(pos, (0.2, 0.4, 20.0), span(t, t_third - 0.4, t_third + 0.8))
        return mix(pos, (-0.9, 0.5, 19.8), span(t, T.start(2) - 0.3, T.start(2) + 1.0))

    kit.camera(path, focus_z=1.0)
    return cues
