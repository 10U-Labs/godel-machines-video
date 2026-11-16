"""Scene 02: Only a body.

A party room in warm light, with four heroes in it. The feeble robot limps in
from the left. One hero steps up and strikes it, and it falls to pieces. As
it breaks, a red light leaves its head for a box on the wall, whose lamps
turn red: Ultron was sent on before the body fell. Then a city at night: the
red light runs along a wire from mast to mast, and is gone.
"""
import math

import kit
import parts
from kit import alpha, every, fr, key, mix, sec, span

HEROES = [  # x, coat, deep coat, hair, skin, skin in shade
    (1.7, '#3d5a80', '#2a3f5c', '#c9b27a', kit.SKIN, kit.SKIN_SHADE),
    (3.3, '#8a3a3a', '#5e2626', '#2a2320', '#c98f6b', '#a8704f'),
    (4.9, '#4d6b4a', '#344a32', '#7a3b24', kit.SKIN, kit.SKIN_SHADE),
    (6.5, '#6a5a8a', '#4a3f63', '#2a2320', '#8d5a3c', '#70442b'),
]
BOX = (-6.4, 1.3)


def build(T):
    cues = []
    end = sec(kit.frames())
    t_face = T.at(0, 0.33)
    t_smash = T.at(0, 0.84)
    t_box = T.at(1, 0.3)
    t_city = T.at(1, 0.55)
    t_left = T.start(2)

    parts.backdrop(seed=31)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the party
    party = parts.room('party', far, stage, light=parts.WARM, glow=0.12)
    behind, front = party
    for k in range(15):
        u = k / 14
        bulb = kit.shape(f'bulb{k}', kit.circle_pts(0.07, n=12), kit.material('#fff3d6', parts.WARM), behind, (-8 + 16 * u, 3.45 - 0.5 * math.sin(math.pi * u)))
        for f in every(8):
            alpha(bulb, f, 0.75 + 0.25 * math.sin(sec(f) * 2.0 + k))
    kit.shape('box', kit.rrect_pts(0.9, 0.6, 0.08), kit.material(parts.STEEL700, parts.STEEL800), front, BOX)
    kit.branch('box-cable', front, (BOX[0], BOX[1] + 0.3), (BOX[0], 4.6), parts.STEEL800, 0.07, 0.95)
    lamps = []
    for k in range(3):
        kit.shape(f'box-off{k}', kit.circle_pts(0.05, n=10), kit.material(parts.ASH), front, (BOX[0] - 0.22 + 0.22 * k, BOX[1]))
        lamps.append(kit.shape(f'box-on{k}', kit.circle_pts(0.05, n=10), kit.material(parts.HOT, parts.RED), front, (BOX[0] - 0.22 + 0.22 * k, BOX[1])))
    lamps.append(kit.shape('box-glow', kit.circle_pts(1.2), kit.glow_material(parts.RED, 0.7, power=2.2), front, BOX))
    parts.visible(lamps, [(t_smash + 0.3, None)], 0.2)

    heroes = []
    for k, (x, coat, deep, hair, skin, shade) in enumerate(HEROES):
        who = parts.figure(f'hero{k}', front, (x, parts.FLOOR), 0.6 + 0.03 * (k % 2), coat, deep, hair, skin, shade, facing=-1)
        parts.nod(who, 0.0, end, k * 0.9)
        parts.reach(who, t_face + 0.12 * k, 35 + 10 * k)
        heroes.append(who)
    first = heroes[0]
    parts.stroll(first, t_smash - 0.75, t_smash - 0.15, HEROES[0][0], -0.5)
    parts.reach(first, t_smash - 0.4, 100, 0.2)
    parts.reach(first, t_smash + 0.5, 20, 0.5)

    bot = parts.feeble('body', front, (-10.0, parts.FLOOR), 0.9)
    parts.walk(bot, 0.2, t_face + 0.7, -10.0, -2.5, limp=1.0, rate=1.5)
    for k in range(int((t_face + 0.5) * 1.5)):
        cues.append({'t': 0.2 + (k + 0.5) / 1.5, 'type': 'tick', 'pitch': 0.5 if k % 2 else 0.42, 'gain': 0.6})
    parts.strike('blow', front, t_smash - 0.12, (-0.9, parts.FLOOR + 2.3), (-2.4, parts.FLOOR + 2.0))
    parts.scatter(bot, t_smash, seed=5)
    parts.hide(bot['eyes']['shapes'], t_smash, 0.25)
    cues.append({'t': t_smash - 0.3, 'type': 'whoosh', 'gain': 0.8})
    cues.append({'t': t_smash, 'type': 'pop', 'pitch': 0.55, 'gain': 1.0})
    for k in range(4):
        cues.append({'t': t_smash + 0.45 + 0.13 * k, 'type': 'tick', 'pitch': 0.6 + 0.12 * k, 'gain': 0.6})

    # Ultron, sent from the body to the box on the wall as the body breaks
    gone = parts.spark('sent', front)
    zs = gone['root'].location.z
    for f in every(1, fr(t_smash - 0.1), fr(t_smash + 0.4)):
        q = span(sec(f), t_smash - 0.05, t_smash + 0.3)
        x, y = mix((-2.4, parts.FLOOR + 3.0), BOX, q)
        key(gone['root'], 'location', f, (x, y + 0.9 * math.sin(math.pi * q), zs))
    for ob in gone['shapes']:
        parts.lit(ob, [(0.0, 0.0), (t_smash - 0.1, 0.0), (t_smash - 0.05, 1.0), (t_smash + 0.3, 1.0), (t_smash + 0.4, 0.0)])
    cues.append({'t': t_smash, 'type': 'rise', 'dur': 0.35, 'pitch': 1.5, 'gain': 0.5})
    cues.append({'t': t_box, 'type': 'blip', 'pitch': 0.8, 'gain': 0.5})

    # ------------------------------------------------------------ the city, and the wire out of it
    town = parts.city('city', stage)
    masts = town['masts']
    run = parts.spark('run', town['root'])
    parts.visible(run['shapes'], [(t_city + 0.1, None)], 0.15)
    hops = len(masts) - 1
    t0, t1 = t_city + 0.2, end - 0.2
    parts.run(run, masts, t0, t1)
    for k in range(1, hops):
        cues.append({'t': t0 + (t1 - t0) * k / hops, 'type': 'blip', 'pitch': 1.0 + 0.12 * k, 'gain': 0.5})
        parts.pulse(f'relay{k}', town['root'], masts[k], t0 + (t1 - t0) * k / hops, 0.25, parts.RED, 0.6, 0.05)
    cues.append({'t': t_left, 'type': 'swoosh', 'gain': 0.6})

    parts.cut(party, None, t_city)
    parts.cut([town['root']], t_city, None)
    parts.dip([t_city])

    # ------------------------------------------------------------ camera
    def path(t):
        if t >= t_city:
            return mix((-1.6, 0.4, 19.6), (2.6, 0.6, 18.6), span(t, t_city, end))
        pos = mix((-1.4, 0.1, 19.8), (0.0, 0.0, 19.6), span(t, 0.0, t_face + 1.0))
        return mix(pos, (-3.2, -0.3, 16.0), span(t, t_smash + 0.5, T.start(1) + 1.4))

    kit.camera(path, focus_z=1.0)
    return cues
