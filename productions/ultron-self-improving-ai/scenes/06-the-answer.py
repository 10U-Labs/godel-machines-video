"""Scene 06: The answer.

The hall where the question was asked. Ultron's three forms stand in a row,
and the computer scientist looks at them. The question mark shows over them
again, and this time it turns into a tick. Under the tick are the three
small lamps, dark, and they light one at a time. At the first, a red light
passes from form to form. At the second, the powerful body lifts its arms.
At the third, a ring of red lights around each form.
"""
import math

import kit
import parts
from kit import fr, key, mix, sec, span

MARK = (0.6, 3.15)


def build(T):
    cues = []
    end = sec(kit.frames())
    t_ask = T.at(0, 0.12)
    t_yes = T.at(0, 0.84)
    t_tally = T.start(1) - 0.3
    t_changed, t_more, t_himself = T.at(1, 0.04), T.at(1, 0.3), T.at(1, 0.74)

    parts.backdrop(seed=71)
    kit.motes(n=12, seed=72, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    near = parts.room('hall', far, stage, lamps=(-5.4, -1.9, 2.4), glow=0.05)[1]
    forms = parts.three_forms(near)
    row = forms['root']
    first, second, third = forms['first'], forms['second'], forms['third']
    for k, (x, _) in enumerate(parts.FORMS):
        pool = parts.spot(f'pool{k}', row, (x, parts.FLOOR + 2.2), 2.8, parts.RED, 0.2)
        parts.visible([pool], [(-1.0, None)], 0.3)
    parts.hover(first)
    parts.sway(second, phase=0.6, amount=1.6)
    parts.sway(third, 0.0, t_more - 0.1, phase=1.9, amount=0.6)
    parts.blink(first['eyes'], (t_ask + 0.9, t_more + 0.5))
    parts.blink(second['eyes'], (t_ask + 1.6, t_himself - 0.6))
    parts.blink(third['eyes'], (t_ask + 0.4, t_yes + 1.1))
    who = parts.scientist('scientist', near, (7.0, parts.FLOOR), facing=-1)
    parts.nod(who, phase=0.4)
    parts.reach(who, t_ask, 66)
    parts.reach(who, t_yes + 0.4, 12, 0.5)

    # ------------------------------------------------------------ the question, and the answer
    mark = kit.text('mark', '?', 1.5, kit.material(parts.BONE), near, MARK)
    kit.pop(mark, t_ask, 1.0, 0.45, t_yes, 0.2)
    cues.append({'t': t_ask, 'type': 'pop', 'pitch': 1.3})
    yes = parts.seal('yes', near, MARK, 1.25, parts.RED, parts.HOT)
    kit.pop(yes, t_yes + 0.15, 1.25)
    for k in range(2):
        parts.pulse(f'yes-ring{k}', near, MARK, t_yes + 0.25 + 0.25 * k, 1.0 + 0.5 * k, parts.RED, 1.0, 0.06)
    cues.append({'t': t_yes + 0.15, 'type': 'chime', 'gain': 0.7})
    cues.append({'t': t_yes + 0.15, 'type': 'pop', 'pitch': 0.6, 'gain': 0.8})

    # ------------------------------------------------------------ the three reasons, one lamp each
    parts.tally('reasons', near, (MARK[0], 1.8), t_tally, (t_changed, t_more, t_himself))
    for k, when in enumerate((t_changed, t_more, t_himself)):
        cues.append({'t': when, 'type': 'blip', 'pitch': 0.8 + 0.2 * k, 'gain': 0.7})

    # he changed himself
    same = parts.spark('same', row)
    parts.visible(same['shapes'], [(t_changed, t_more - 0.1)], 0.12)
    parts.hop(same, forms['heads'], t_changed, t_more - 0.15)

    # the changes left him able to do more
    for side, arm in ((-1, third['arms']['left']), (1, third['arms']['right'])):
        for when, deg in ((t_more, 0), (t_more + 0.3, 30), (t_more + 1.2, 12)):
            key(arm, 'rotation_euler', fr(when), (0, 0, side * math.radians(deg)))
    for when, s in ((t_more, 1.0), (t_more + 0.25, 1.05), (t_more + 0.6, 1.0)):
        key(third['rig'], 'scale', fr(when), (s, s, 1))
    parts.pulse('more', row, (parts.FORMS[2][0], parts.FLOOR + 3.85 * parts.FORM_SCALE), t_more + 0.2, 0.9, parts.RED, 0.9)
    cues.append({'t': t_more + 0.2, 'type': 'pop', 'pitch': 0.4, 'gain': 0.9})

    # and he made them himself
    for k, (x, _) in enumerate(parts.FORMS):
        parts.pulse(f'himself{k}', row, (x, parts.FLOOR + 1.9 + 0.3 * k), t_himself + 0.12 * k, 1.2 + 0.4 * k, parts.RED, 1.0, 0.06)
    cues.append({'t': t_himself, 'type': 'chime', 'gain': 0.5, 'pitch': 0.8})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((0.6, 0.5, 19.8), (0.6, 0.6, 19.2), span(t, 0.0, t_yes))
        return mix(pos, (0.6, 0.6, 18.9), span(t, t_yes, end))

    kit.camera(path, focus_z=1.0)
    return cues
