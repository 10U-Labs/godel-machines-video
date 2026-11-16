"""Scene 05: Physical self-improvement.

The hall. On the left stand Ultron's two bodies: the feeble one, with his
eyes lit in it, and the powerful one, still dark. His program comes out of
the feeble head as a small red sheet of code. A light passes down its lines,
and not one of them changes. It goes into the powerful head, whose eyes
light, and the feeble body slumps. Then, on the right, the AI from the
study: it rewrites a line of its program, and then its computer grows arms.
Those are the two ways. A red ring lights around Ultron's new body: his was
the second way. At the far right the computer scientist lifts his paper.
"""
import math

import kit
import parts
from kit import alpha, every, fr, key, mix, sec, span

SCALE = 0.82
OLD = (-6.3, parts.FLOOR)
NEW = (-3.0, parts.FLOOR)
ABOVE = (-4.7, 2.75)
OTHER = (3.3, parts.FLOOR)


def build(T):
    cues = []
    end = sec(kit.frames())
    t_out = T.at(0, 0.22)
    t_scan0, t_scan1 = T.at(0, 0.4), T.at(0, 0.63)
    t_in = T.at(0, 0.72)
    t_other = T.at(1, 0.18)
    t_code = T.at(1, 0.38)
    t_machine = T.at(1, 0.62)
    t_his = T.at(1, 0.84)
    t_paper = T.at(2, 0.08)
    t_name = T.at(2, 0.58)

    parts.backdrop(seed=61)
    kit.motes(n=12, seed=62, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    front = parts.room('hall', far, stage, lamps=(-4.6, 3.3), glow=0.05)[1]
    pool = parts.spot('red-pool', front, (-4.6, parts.FLOOR + 2.4), 3.8, parts.RED, 0.13)
    alpha(pool, 1, 1.0)

    # ------------------------------------------------------------ the same program, moved from one body to the next
    weak = parts.feeble('feeble', front, OLD, SCALE)
    strong = parts.powerful('powerful', front, NEW, SCALE)
    old_head = (OLD[0] + 0.04 * SCALE, parts.FLOOR + 3.52 * SCALE)
    new_head = (NEW[0], parts.FLOOR + 4.98 * SCALE)
    parts.blink(weak['eyes'], (T.at(0, 0.08),))
    parts.hide(weak['eyes']['shapes'], t_out, 0.3)
    parts.visible(strong['eyes']['shapes'] + [strong['core'][0], strong['core'][2]], [(t_in + 0.6, None)], 0.3)
    parts.blink(strong['eyes'], (t_other + 0.6, t_machine + 1.0, t_paper + 1.3))
    for when, lean, drop in ((t_in + 0.6, 0.0, 0.0), (t_in + 1.3, -0.1, -0.1)):
        key(weak['rig'], 'rotation_euler', fr(when), (0, 0, lean))
        key(weak['rig'], 'location', fr(when), (0, drop, 0))
    for when, tilt in ((t_in + 0.6, 0.0), (t_in + 1.4, 0.3)):
        key(weak['head'], 'rotation_euler', fr(when), (0, 0, tilt))

    own = parts.own_program('own', front, ABOVE, 0.5)
    z = own['root'].location.z
    key(own['root'], 'scale', 1, parts.TINY)
    key(own['root'], 'scale', max(1, fr(t_out) - 1), parts.TINY)
    for f in every(1, fr(t_out), fr(t_out + 0.8)):
        q = span(sec(f), t_out, t_out + 0.75)
        s = mix(0.04, 0.5, q)
        x, y = mix(old_head, ABOVE, q)
        key(own['root'], 'location', f, (x, y, z))
        key(own['root'], 'scale', f, (s, s, s))
    for f in every(1, fr(t_in), fr(t_in + 0.8)):
        q = span(sec(f), t_in, t_in + 0.75)
        s = mix(0.5, 0.04, q)
        x, y = mix(ABOVE, new_head, q)
        key(own['root'], 'location', f, (x, y, z))
        key(own['root'], 'scale', f, (s, s, s))
    key(own['root'], 'scale', fr(t_in + 0.8) + 1, parts.TINY)
    parts.blink(own['eyes'], (t_out + 1.3, t_scan1 + 0.3))
    cues.append({'t': t_out, 'type': 'whoosh', 'gain': 0.6})
    cues.append({'t': t_in, 'type': 'swoosh', 'gain': 0.7})
    cues.append({'t': t_in + 0.7, 'type': 'pop', 'pitch': 0.5, 'gain': 0.9})

    # a light goes down its lines, and none of them changes
    rows = len(own['rows'])
    step = (t_scan1 - t_scan0) / rows
    for r in range(rows):
        when = t_scan0 + step * r
        bar = parts.band(own, r, parts.HOT, 0.28)
        parts.lit(bar, [(0.0, 0.0), (when, 0.0), (when + step * 0.5, 1.0), (when + step * 1.3, 0.0)])
        cues.append({'t': when, 'type': 'tick', 'pitch': 0.8, 'gain': 0.3})

    # ------------------------------------------------------------ the two ways: its program, or its machine
    side = kit.empty('other', front)
    parts.cut([side], t_other, None)
    blue = parts.spot('blue-pool', side, (OTHER[0], parts.FLOOR + 3.0), 3.6, parts.ICE, 0.1)
    alpha(blue, 1, 1.0)
    ai = parts.thinker('ai', side, OTHER)
    pg, box = ai['program'], ai['computer']
    alpha(box['beam'], 1, 1.0)
    parts.drift(pg['root'])
    parts.blink(pg['eyes'], (t_other + 1.1, t_machine + 0.4, t_name))
    parts.pulse('other-ring', front, (OTHER[0], parts.FLOOR + 3.0), t_other + 0.1, 2.6, parts.FROST, 0.9, 0.05)
    cues.append({'t': t_other, 'type': 'pop', 'pitch': 1.2, 'gain': 0.7})
    quill = parts.pen('pen', pg['root'], (-pg['w'] / 2 - 0.35, pg['ys'][2]))
    kit.pop(quill, t_code - 0.3, 1.0, 0.3, t_machine - 0.4)
    for k, r in enumerate((2, 4)):
        when = t_code + 0.7 * k
        bar = parts.band(pg, r, parts.FROST, 0.3)
        parts.lit(bar, [(0.0, 0.0), (when - 0.1, 0.0), (when + 0.1, 1.0), (when + 0.8, 0.0)])
        parts.rewrite(pg, r, when)
        cues.append({'t': when, 'type': 'tick', 'pitch': 1.3 + 0.1 * k, 'gain': 0.6})
    for k, when in enumerate(parts.arms('new-arm', box, OTHER, front, t_machine, gap=0.4)):
        cues.append({'t': when, 'type': 'pop', 'pitch': 0.7 + 0.15 * k})

    # Ultron changed the machine
    for k in range(2):
        parts.pulse(f'his{k}', front, (NEW[0], parts.FLOOR + 2.3), t_his + 0.35 * k, 2.2 + 0.4 * k, parts.RED, 1.0, 0.07)
    for arm_side, arm in ((-1, strong['arms']['left']), (1, strong['arms']['right'])):
        for when, deg in ((t_his, 0), (t_his + 0.3, 28), (t_his + 1.0, 10)):
            key(arm, 'rotation_euler', fr(when), (0, 0, arm_side * math.radians(deg)))
    cues.append({'t': t_his, 'type': 'pop', 'pitch': 0.45, 'gain': 1.0})

    # ------------------------------------------------------------ the paper's name for it
    who = parts.scientist('scientist', front, (7.8, parts.FLOOR), facing=-1)
    parts.paper(who)
    parts.nod(who, phase=0.4)
    parts.reach(who, t_paper, 104, 0.5)
    cues.append({'t': t_paper, 'type': 'swoosh', 'gain': 0.4})
    for k in range(3):
        parts.pulse(f'name{k}', front, (NEW[0], parts.FLOOR + 2.3), t_name + 0.3 * k, 1.6 + 0.6 * k, parts.RED, 1.1, 0.07)
    for when, s in ((t_name, 1.0), (t_name + 0.3, 1.05), (t_name + 0.8, 1.0)):
        key(strong['rig'], 'scale', fr(when), (s, s, 1))
    cues.append({'t': t_name, 'type': 'chime', 'gain': 0.6})
    cues.append({'t': t_name, 'type': 'pop', 'pitch': 0.4, 'gain': 0.8})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((-3.9, 0.6, 16.6), (-3.7, 0.7, 15.6), span(t, 0.0, t_in))
        pos = mix(pos, (0.5, 0.4, 20.6), span(t, t_other - 1.2, t_other + 0.4))
        pos = mix(pos, (1.6, 0.4, 19.2), span(t, t_code - 0.6, t_code + 0.6))
        pos = mix(pos, (0.5, 0.4, 20.6), span(t, t_his - 0.8, t_his + 0.2))
        return mix(pos, (0.5, 0.5, 20.2), span(t, t_paper, end))

    kit.camera(path, focus_z=1.0)
    return cues
