"""Scene 04: The question.

Three pools of red light, and into them come Ultron's three forms, in a row:
the eyes with no body, the feeble robot, and the powerful one. A red light
passes from each to the next, since each change was his own doing. Then the
row moves aside, and a computer scientist walks in to a board with a design
drawn on it: a program, with eyes. It is named the Gödel Machine. Ultron
turns to look at it.
"""
import math

import kit
import parts
from kit import every, fr, key, mix, sec, span

SCALE = 0.82
AT = [(-5.4, parts.FLOOR + 3.0), (-1.9, parts.FLOOR), (2.4, parts.FLOOR)]
SHIFT = -2.7
BOARD = (4.6, parts.FLOOR + 3.4)


def build(T):
    cues = []
    end = sec(kit.frames())
    t_three = T.at(0, 0.02)
    t_forms = [T.at(0, 0.28), T.at(0, 0.58), T.at(0, 0.82)]
    t_made = T.start(1)
    t_better = T.start(2)
    t_design = T.at(2, 0.36)
    t_named = T.at(2, 0.78)
    t_ask = T.at(3, 0.35)

    parts.backdrop(seed=51)
    kit.motes(n=12, seed=52, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    front = parts.room('hall', far, stage, lamps=(-5.4, -1.9, 2.4), glow=0.05)[1]

    # ------------------------------------------------------------ the three forms
    row = kit.empty('row', front)
    heads = [AT[0], (AT[1][0] + 0.04 * SCALE, parts.FLOOR + 3.52 * SCALE), (AT[2][0], parts.FLOOR + 4.98 * SCALE)]
    for k, (x, y) in enumerate(AT):
        pool = parts.spot(f'pool{k}', row, (x, parts.FLOOR + 2.2), 2.8, parts.RED, 0.2)
        parts.visible([pool], [(t_three + 0.25 * k, None)], 0.5)
        cues.append({'t': t_three + 0.25 * k, 'type': 'tick', 'pitch': 0.7 + 0.1 * k, 'gain': 0.4})
        cues.append({'t': t_forms[k], 'type': 'pop', 'pitch': 1.0 - 0.2 * k})
    parts.console('stand', row, (AT[0][0], parts.FLOOR), 0.9)
    u = parts.presence('no-body', row, AT[0], 0.9)
    parts.hover(u)
    parts.visible(u['shapes'], [(t_forms[0], None)], 0.4)
    weak = parts.feeble('feeble', row, AT[1], SCALE)
    kit.pop(weak['root'], t_forms[1], SCALE)
    parts.sway(weak, phase=0.6, amount=1.6)
    strong = parts.powerful('powerful', row, AT[2], SCALE)
    kit.pop(strong['root'], t_forms[2], SCALE)
    parts.sway(strong, 0.0, t_ask - 0.2, phase=1.9, amount=0.6)
    parts.blink(u['eyes'], (t_forms[0] + 1.8, t_better + 2.0))
    parts.blink(weak['eyes'], (t_forms[1] + 1.5, t_made + 2.6, t_design + 1.0))
    parts.blink(strong['eyes'], (t_forms[2] + 1.6, t_design + 2.2))

    # each change was his own: one light goes from form to form
    same = parts.spark('same', row)
    zs = same['root'].location.z
    t0, t1 = t_made + 0.2, T.end(1)
    parts.visible(same['shapes'], [(t0, t1 + 0.1)], 0.15)
    for f in every(1, fr(t0), fr(t1 + 0.2)):
        s = span(sec(f), t0, t1, lambda v: v) * 2
        i = min(1, int(s))
        q = kit.smooth(s - i)
        x, y = mix(heads[i], heads[i + 1], q)
        key(same['root'], 'location', f, (x, y + 1.3 * math.sin(math.pi * q), zs))
    for k in range(3):
        when = mix(t0, t1, k / 2)
        parts.pulse(f'own{k}', row, heads[k], when, 0.5, parts.RED, 0.8)
        cues.append({'t': when, 'type': 'blip', 'pitch': 0.8 + 0.2 * k, 'gain': 0.6})
    cues.append({'t': t0, 'type': 'rise', 'dur': t1 - t0, 'pitch': 0.7, 'gain': 0.4})
    parts.slide(row, t_design - 0.9, t_design + 0.3, (0, 0), (SHIFT, 0))
    cues.append({'t': t_design - 0.9, 'type': 'swoosh', 'gain': 0.5})

    # ------------------------------------------------------------ the design, and the one who shows it
    cool = parts.spot('cool', front, (BOARD[0] + 0.6, parts.FLOOR + 2.6), 3.6, parts.ICE, 0.14)
    parts.visible([cool], [(t_design, None)], 0.8)
    board = parts.blueprint('design', front, BOARD)
    kit.pop(board['root'], t_design, 1.0)
    parts.draw(board['dots'], t_design + 0.4, t_named)
    cues.append({'t': t_design, 'type': 'pop', 'pitch': 1.2})
    for k in range(6):
        cues.append({'t': mix(t_design + 0.5, t_named, k / 6), 'type': 'tick', 'pitch': 1.1 + 0.05 * (k % 3), 'gain': 0.3})
    who = parts.figure('scientist', front, (11.0, parts.FLOOR), coat='#56707e', coat_deep='#3b505c', hair='#c9c2b8', facing=-1)
    parts.stroll(who, t_design - 0.6, t_design + 0.5, 11.0, 7.3)
    parts.nod(who, t_design + 0.5, end, 0.4)
    parts.reach(who, t_design + 0.6, 70)
    parts.reach(who, t_named + 0.4, 15, 0.5)
    name = kit.text('name', 'Gödel Machine', 0.42, kit.material(parts.FROST), front, (BOARD[0], parts.FLOOR + 0.75))
    kit.fade(name, t_named, None, 0.5)
    cues.append({'t': t_named, 'type': 'chime', 'gain': 0.6})

    # ------------------------------------------------------------ the question
    for t0, turn in ((t_ask - 0.2, 0.0), (t_ask + 0.2, -0.14)):
        key(strong['head'], 'rotation_euler', fr(t0), (0, 0, turn))
    parts.look(strong['eyes'], t_ask - 0.1, 0.06, 0.0)
    mark = kit.text('mark', '?', 1.5, kit.material(parts.BONE), front, (1.75, parts.FLOOR + 4.2))
    kit.pop(mark, t_ask, 1.0)
    parts.pulse('wonder', front, (1.75, parts.FLOOR + 4.2), t_ask + 0.1, 0.9, parts.BONE, 1.0, 0.05)
    cues.append({'t': t_ask, 'type': 'pop', 'pitch': 1.3})
    cues.append({'t': t_ask + 0.1, 'type': 'rise', 'dur': 1.2, 'pitch': 0.8, 'gain': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((-1.8, 0.3, 20.0), (-1.3, 0.3, 19.2), span(t, 0.0, t_better))
        pos = mix(pos, (0.4, 0.3, 20.0), span(t, t_design - 0.9, t_design + 0.6))
        return mix(pos, (3.0, 0.5, 15.8), span(t, T.start(3), end))

    kit.camera(path, focus_z=1.0)
    return cues
