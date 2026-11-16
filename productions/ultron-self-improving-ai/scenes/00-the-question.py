"""Scene 00: The question.

A lab at night, with nobody in it. Over a computer a pair of red eyes opens:
an artificial intelligence has started up. It talks, and beside it stands the
dotted outline of the body it does not have. Then a hall, later on: the eyes
are still there, and next to them stand a feeble robot and then a powerful
one. A red light passes from each form to the next, since he built them
himself. A computer scientist walks in and looks at the three, and a question
mark hangs over them.
"""
import kit
import parts
from kit import mix, sec, span


def build(T):
    cues = []
    end = sec(kit.frames())
    t_on = T.at(0, 0.06)
    t_talk0, t_talk1 = T.at(0, 0.5), T.at(0, 0.72)
    t_nobody = T.at(0, 0.8)
    t_later = T.start(2) - 0.2
    t_forms = [T.at(2, 0.22), T.at(2, 0.42)]
    t_own0, t_own1 = T.at(2, 0.6), T.end(2) + 0.2
    t_science = T.start(3) - 0.3
    t_term = T.at(3, 0.72)
    t_ask = T.at(4, 0.3)

    parts.backdrop(seed=11)
    kit.motes(n=12, seed=12, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the lab he starts up in
    lab = parts.first_lab(far, stage)
    parts.cut(lab['roots'], None, t_later)
    front = lab['front']
    sx, sy = lab['spot']
    u = parts.presence('ultron', front, (sx, sy))
    parts.hover(u, 0.0, t_later)
    parts.visible(u['shapes'] + [lab['console']['beam']], [(t_on, None)], 0.5)
    parts.open_eyes(u['eyes'], t_on + 0.1)
    parts.blink(u['eyes'], (t_on + 2.4, T.at(1, 0.3), T.at(1, 0.85)))
    parts.talk(u, t_talk0, t_talk1, seed=1)
    cues.append({'t': t_on, 'type': 'rise', 'dur': 1.0, 'pitch': 0.7, 'gain': 0.7})
    for k in range(3):
        cues.append({'t': mix(t_talk0, t_talk1, k / 3), 'type': 'tick', 'pitch': 0.8 + 0.1 * k, 'gain': 0.35})
    ghost = parts.outline('ghost', front, (sx + 2.7, parts.FLOOR + 3.2), 0.8, parts.ASH, 1.0)
    parts.visible(ghost['shapes'], [(t_nobody, None)], 0.4)
    parts.look(u['eyes'], t_nobody + 0.3, 0.13, -0.03)
    parts.look(u['eyes'], T.at(1, 0.15), 0.0, 0.0)
    cues.append({'t': t_nobody, 'type': 'tick', 'gain': 0.5})

    # ------------------------------------------------------------ later: his three forms
    hall = parts.room('hall', far, stage, lamps=(-5.4, -1.9, 2.4), glow=0.05)
    parts.cut(hall, t_later, None)
    near = hall[1]
    parts.dip([t_later])
    cues.append({'t': t_later - 0.2, 'type': 'whoosh', 'gain': 0.6})
    forms = parts.three_forms(near)
    row = forms['root']
    for k, (x, _) in enumerate(parts.FORMS):
        pool = parts.spot(f'pool{k}', row, (x, parts.FLOOR + 2.2), 2.8, parts.RED, 0.2)
        parts.visible([pool], [(-1.0, None)], 0.3)
    first, second, third = forms['first'], forms['second'], forms['third']
    parts.hover(first, t_later, end)
    kit.pop(second['root'], t_forms[0], parts.FORM_SCALE)
    kit.pop(third['root'], t_forms[1], parts.FORM_SCALE)
    parts.sway(second, t_forms[0], end, phase=0.6, amount=1.6)
    parts.sway(third, t_forms[1], end, phase=1.9, amount=0.6)
    parts.blink(first['eyes'], (t_later + 1.4, t_term + 0.4))
    parts.blink(second['eyes'], (t_forms[0] + 1.5, t_science + 2.4))
    parts.blink(third['eyes'], (t_forms[1] + 1.6, t_science + 1.2, t_ask + 1.4))
    for k, t0 in enumerate(t_forms):
        cues.append({'t': t0, 'type': 'pop', 'pitch': 0.8 - 0.2 * k})

    # he built them himself: one light goes from form to form
    same = parts.spark('same', row)
    parts.visible(same['shapes'], [(t_own0, t_own1 + 0.1)], 0.15)
    parts.hop(same, forms['heads'], t_own0, t_own1)
    for k in range(3):
        when = mix(t_own0, t_own1, k / 2)
        parts.pulse(f'own{k}', row, forms['heads'][k], when, 0.5, parts.RED, 0.8)
        cues.append({'t': when, 'type': 'blip', 'pitch': 0.8 + 0.2 * k, 'gain': 0.6})
    cues.append({'t': t_own0, 'type': 'rise', 'dur': t_own1 - t_own0, 'pitch': 0.7, 'gain': 0.4})

    # ------------------------------------------------------------ the computer scientist, and the question
    who = parts.figure('scientist', near, (12.0, parts.FLOOR), coat='#56707e', coat_deep='#3b505c', hair='#c9c2b8', facing=-1)
    parts.stroll(who, t_science, t_science + 1.6, 12.0, 7.0)
    parts.nod(who, t_science + 1.6, end, 0.4)
    parts.reach(who, T.at(3, 0.3), 66)
    parts.reach(who, T.end(3), 14, 0.5)
    cues.append({'t': t_science, 'type': 'swoosh', 'gain': 0.4})
    for k in range(3):
        parts.pulse(f'term{k}', row, (parts.FORMS[k][0], parts.FLOOR + 1.9 + 0.35 * k), t_term + 0.22 * k, 1.5 + 0.35 * k, parts.BONE, 0.9, 0.05)
    cues.append({'t': t_term, 'type': 'chime', 'gain': 0.5})
    mark = kit.text('mark', '?', 1.5, kit.material(parts.BONE), near, (0.6, 3.0))
    kit.pop(mark, t_ask, 1.0)
    parts.pulse('wonder', near, (0.6, 3.0), t_ask + 0.1, 0.9, parts.BONE, 1.0, 0.05)
    cues.append({'t': t_ask, 'type': 'pop', 'pitch': 1.3})
    cues.append({'t': t_ask + 0.1, 'type': 'rise', 'dur': 1.2, 'pitch': 0.8, 'gain': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        if t < t_later:
            return mix((-1.5, 0.2, 19.5), (-3.4, 0.5, 15.2), span(t, 0.0, T.end(1)))
        pos = mix((-1.8, 0.3, 19.6), (-1.3, 0.3, 19.2), span(t, t_later, T.end(2)))
        pos = mix(pos, (0.6, 0.4, 20.4), span(t, t_science - 0.2, t_science + 1.6))
        return mix(pos, (0.6, 0.5, 19.8), span(t, T.start(4), end))

    kit.camera(path, focus_z=1.0)
    return cues
