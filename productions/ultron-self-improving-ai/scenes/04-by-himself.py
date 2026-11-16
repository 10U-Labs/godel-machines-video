"""Scene 04: By himself.

A workshop. A person stands at a computer and fits it with two arms, one
after the other, by hand. The computer waves its new arms; it did nothing to
get them. A light comes up on the person, who made the change. Then the
hall, with nobody in it: Ultron's three forms in a row, and over the two
bodies the machines that built them, their lamps red. A red light runs from
his first form up to one machine and down into the feeble body, then up to
the next machine and down into the powerful one. Of the three small lamps,
the third one lights.
"""
import kit
import parts
from kit import mix, sec, span

MAKER = (-1.7, parts.FLOOR)
BOX = (1.5, parts.FLOOR)
LAMPS = [(-3.3, 4.15), (0.6, 4.15)]


def build(T):
    cues = []
    end = sec(kit.frames())
    t_fit = T.at(0, 0.16)
    t_not = T.at(0, 0.58)
    t_who = T.at(1, 0.1)
    t_hall = T.at(1, 0.3)
    t_did = T.at(1, 0.78)
    t_done = T.start(2) + 0.1
    t_tally = T.start(2) - 0.1
    t_reason = T.at(2, 0.72)

    parts.backdrop(seed=51)
    kit.motes(n=12, seed=52, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ a person makes a machine better
    shop = parts.room('shop', far, stage, lamps=(-1.7, 1.5), light=parts.STEEL100, glow=0.07)
    parts.cut(shop, None, t_hall)
    front = shop[1]
    parts.desk('bench', front, (-4.6, parts.FLOOR), 2.4)
    for i in range(3):
        kit.shape(f'spare{i}', kit.capsule_pts(0.7, 0.18), kit.material(parts.STEEL500, parts.STEEL700), front,
                  (-5.2 + 0.55 * i, parts.FLOOR + 1.62), rot=1.45)
    light = parts.spot('maker-light', shop[0], (MAKER[0] - 0.7, parts.FLOOR + 2.0), 3.0, parts.BONE, 0.2)
    parts.visible([light], [(t_not, None)], 0.5)
    box = parts.console('computer', front, BOX, 1.0, parts.ICE)
    who = parts.figure('maker', front, MAKER, coat='#6f6a78', coat_deep='#4b4754', hair='#2a2320')
    parts.nod(who, 0.0, t_hall, 0.2)
    hand = (MAKER[0] + 1.2, parts.FLOOR + 2.3)
    fitted = parts.arms('fitted', box, BOX, front, t_fit, gap=1.25, source=hand, t1=t_hall)
    for when in fitted:
        parts.reach(who, when - 0.95, 78, 0.25)
        parts.reach(who, when + 0.1, 30, 0.3)
        cues.append({'t': when - 0.45, 'type': 'swoosh', 'gain': 0.4})
        cues.append({'t': when, 'type': 'tick', 'pitch': 0.7, 'gain': 0.8})
    parts.reach(who, fitted[1] + 0.6, 4, 0.5)
    parts.stroll(who, t_not - 0.3, t_not + 0.7, MAKER[0], MAKER[0] - 0.9)
    cues.append({'t': t_not, 'type': 'blip', 'pitch': 0.7, 'gain': 0.4})
    parts.pulse('who', front, (MAKER[0] - 0.9, parts.FLOOR + 1.6), t_who, 1.9, parts.BONE, 1.0, 0.06)
    cues.append({'t': t_who, 'type': 'pop', 'pitch': 1.0})

    # ------------------------------------------------------------ nobody built Ultron's bodies: he did
    hall = parts.room('hall', far, stage, lamps=(-5.4, -1.9, 2.4), glow=0.05)
    parts.cut(hall, t_hall, None)
    near = hall[1]
    parts.dip([t_hall])
    cues.append({'t': t_hall - 0.2, 'type': 'whoosh', 'gain': 0.5})
    builders = [parts.machine('builder0', near, (LAMPS[0][0], 4.25)),
                parts.machine('builder1', near, (LAMPS[1][0], 4.25), 1.5, 1.3)]
    forms = parts.three_forms(near)
    row = forms['root']
    for k, (x, _) in enumerate(parts.FORMS):
        pool = parts.spot(f'pool{k}', row, (x, parts.FLOOR + 2.2), 2.8, parts.RED, 0.2)
        parts.visible([pool], [(-1.0, None)], 0.3)
    parts.hover(forms['first'], t_hall, end)
    parts.sway(forms['second'], t_hall, end, phase=0.6, amount=1.6)
    parts.sway(forms['third'], t_hall, end, phase=1.9, amount=0.6)
    parts.blink(forms['first']['eyes'], (t_hall + 1.3, t_done + 1.2))
    parts.blink(forms['second']['eyes'], (t_hall + 2.1, t_reason + 0.6))
    parts.blink(forms['third']['eyes'], (t_hall + 0.8, t_done + 0.7))
    for k, m in enumerate(builders):
        for ob in m['lamp']:
            kit.alpha(ob, 1, 1.0)
        parts.work(m, t_hall - 0.5, t_did + 0.2, sh=(4, 32) if k == 0 else (2, 36), el=(-62, -14) if k == 0 else (-48, 0), rate=0.7 + 0.15 * k)
        away = -1 if k == 0 else 1
        parts.fold(m, t_did + 0.3, away * 32, away * 84)

    path_of_light = [forms['heads'][0], LAMPS[0], forms['heads'][1], LAMPS[1], forms['heads'][2]]
    did = parts.spark('did', near)
    parts.visible(did['shapes'], [(t_did, t_done + 0.1)], 0.15)
    parts.run(did, path_of_light, t_did, t_done)
    for k, at in enumerate(path_of_light):
        when = mix(t_did, t_done, k / 4)
        parts.pulse(f'did{k}', near, at, when, 0.5 if k % 2 else 0.7, parts.RED, 0.8)
        cues.append({'t': when, 'type': 'blip', 'pitch': 0.7 + 0.12 * k, 'gain': 0.6})
    cues.append({'t': t_did, 'type': 'rise', 'dur': t_done - t_did, 'pitch': 0.7, 'gain': 0.4})

    # that he built them himself: the third reason
    parts.tally('reasons', near, (-1.35, 3.3), t_tally, (-1.0, -1.0, t_reason))
    cues.append({'t': t_tally, 'type': 'tick', 'gain': 0.4})
    cues.append({'t': t_reason, 'type': 'chime', 'gain': 0.6})

    # ------------------------------------------------------------ camera
    def path(t):
        if t < t_hall:
            pos = mix((0.2, 0.2, 16.4), (0.0, 0.2, 15.6), span(t, 0.0, t_not))
            return mix(pos, (-1.0, 0.2, 15.0), span(t, t_not, t_hall))
        pos = mix((-1.9, 0.5, 19.2), (-1.3, 0.6, 19.8), span(t, t_hall, t_did))
        return mix(pos, (-1.3, 0.7, 19.4), span(t, t_done, end))

    kit.camera(path, focus_z=1.0)
    return cues
