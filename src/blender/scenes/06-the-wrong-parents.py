"""Scene 06: The wrong parents.

Two programs wait to be picked as parents. The one with the higher score is
picked. Then two other researchers walk up and look further down: the
picked program's children and grandchildren come out weak, while the
lower-scored program's family comes out strong.
"""
import math

import kit
from kit import fr, sec, span, mix, key, alpha, every

SIZE = 0.5
A_AT = (-5.4, 1.7)     # higher score, weak family
B_AT = (-5.4, -1.6)    # lower score, strong family

FAMILY = [  # id, parent, place, score
    ('a1', 'a', (-3.1, 2.6), 30),
    ('a2', 'a', (-3.1, 1.0), 27),
    ('a3', 'a1', (-0.8, 3.0), 26),
    ('a4', 'a2', (-0.8, 1.4), 24),
    ('b1', 'b', (-3.1, -0.9), 38),
    ('b2', 'b', (-3.1, -2.4), 42),
    ('b3', 'b1', (-0.8, -0.3), 46),
    ('b4', 'b2', (-0.8, -1.7), 49),
    ('b5', 'b2', (-0.8, -3.0), 45),
]


def build(T):
    kit.state['zstep'] = 0.0005
    cues = []
    end = sec(kit.frames())
    t_pick = T.at(0, 0.5)
    t_group = T.start(1)
    t_kids = T.at(1, 0.6)
    t_grand = T.at(1, 0.78)
    t_verdict = T.end(1) - 0.4

    kit.backdrop(seed=61, glow=kit.VIOLET_DEEP)
    kit.motes(seed=62, colour=kit.MIST)
    lines = kit.layer('lines', 0.9)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ two would-be parents and their scores
    parents = kit.family('par', stage, lines, [
        {'id': 'a', 'parent': None, 'at': A_AT, 'score': 41, 't': 0.15},
        {'id': 'b', 'parent': None, 'at': B_AT, 'score': 33, 't': 0.3},
    ], SIZE, idle_step=2)
    for n in ('a', 'b'):
        kit.pop(parents[n]['tag']['root'], 0.45, 1.0, 0.3)
    cues.append({'t': 0.15, 'type': 'pop'})
    pick = kit.ring('pick', stage, A_AT, 0.75, kit.AMBER, w=0.1, lift=0.02)
    for f, a in ((fr(t_pick), 0.0), (fr(t_pick + 0.25), 1.0), (fr(t_grand), 1.0), (fr(t_grand + 0.5), 0.35)):
        alpha(pick, f, a)
    zr = pick.location.z
    for f in every(1, fr(t_pick), fr(t_pick + 0.5)):
        s = kit.back_out((sec(f) - t_pick) / 0.5)
        key(pick, 'scale', f, (max(0.001, s),) * 2 + (1,))
    cues.append({'t': t_pick, 'type': 'chime', 'gain': 0.5})
    a_pip = parents['a']['pip']
    kit.pip_eyes(a_pip, t_pick + 0.1, 1.15, 0.65)          # pleased
    kit.pip_eyes(a_pip, t_grand + 0.4, 1.0, 1.0)
    b_pip = parents['b']['pip']
    kit.pip_look(b_pip, t_pick, 0.0, 0.1)

    # ------------------------------------------------------------ a second group looks further down the family
    group = [((5.6, 1.0), 10.5, 0.74, '#4a6fd1', '#33509e', '#d8c7a0'),
             ((7.1, 0.7), 11.5, 0.68, '#c25a9b', '#8f3f72', '#2b1d1a')]
    for k, (at, start_x, s, coat, deep, hair) in enumerate(group):
        who = kit.person(f'group{k}', stage, at, s, coat=coat, coat_deep=deep, hair=hair, facing=-1)
        z = who['root'].location.z
        t_in = t_group + 0.25 * k
        for f in every(1):
            t = sec(f)
            q = span(t, t_in, t_in + 1.1, kit.ease_out)
            bob = 0.06 * abs(math.sin(t * 9)) if 0 < q < 1 else 0.0
            key(who['root'], 'location', f, (mix(start_x, at[0], q), at[1] + bob, z))
            point = span(t, t_kids - 0.4 + 0.3 * k, t_kids + 0.2 * k)
            key(who['arm'], 'rotation_euler', f, (0, 0, -math.radians(mix(8, 65 - 15 * k, point) + 3 * math.sin(t * 1.4 + k))))
            key(who['head'], 'rotation_euler', f, (0, 0, 0.05 * math.sin(t * 0.8 + k) - 0.08 * point))
    floor = kit.shape('floor', kit.rrect_pts(10, 0.06, 0), kit.material(kit.MIST, alpha=0.2), stage, (8.0, -2.35))
    kit.appear(floor, t_group, None, 0.6)
    cues.append({'t': t_group, 'type': 'whoosh', 'gain': 0.4})

    nodes = []
    for n, pa, at, sc in FAMILY:
        gen2 = pa in ('a', 'b')
        t = (t_kids if gen2 else t_grand) + (0.12 if n.startswith('b') else 0.0) + 0.05 * int(n[1])
        nodes.append({'id': n, 'parent': pa, 'at': at, 'score': sc, 't': t})
    fam = kit.family('fam', stage, lines, nodes, SIZE * 0.9, known={'a': A_AT, 'b': B_AT})
    for d in nodes:
        kit.pop(fam[d['id']]['tag']['root'], d['t'] + 0.2, 1.0, 0.3)
    cues.append({'t': t_kids, 'type': 'pop', 'pitch': 0.9, 'gain': 0.6})
    cues.append({'t': t_grand, 'type': 'pop', 'pitch': 1.1, 'gain': 0.6})

    # the strong family glows; the picked parent's family stays dim
    glow = kit.shape('b-glow', kit.rrect_pts(7.0, 4.4, 1.6), kit.glow_material(kit.AMBER, 0.45, power=0.9), stage, (-2.9, -1.6), lift=-0.2)
    kit.appear(glow, t_verdict - 0.8, None, 0.8)
    cues.append({'t': t_verdict - 0.8, 'type': 'rise', 'dur': 0.8, 'pitch': 1.1, 'gain': 0.5})
    kit.pip_look(b_pip, t_grand + 0.3, 0.12, -0.04)

    def path(t):
        q = kit.smooth(t / end)
        look = span(t, t_group - 0.3, t_group + 1.5)
        return (mix(-3.2, 0.0, look) + 0.2 * q, 0.1, mix(15.5, kit.H0, look) - 0.3 * q)

    kit.camera(path, focus_z=1.0)
    return cues
