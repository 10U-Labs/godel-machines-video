"""Scene 08: Three machines.

Three small pictures stand side by side, one for each machine, and the camera
visits each in turn: one program rewriting itself; a family growing child by
child; a family hanging down from one program, where the best branch grows.
Then a line of Pips climbs a stair, each new version a little better than the
last, and the trail goes on up into the dark.
"""
import math

import kit
import parts
from kit import fr, sec, span, mix, key, alpha, every

LEFT, MID, RIGHT = (-5.4, 0.2), (0.0, 0.2), (5.4, 0.2)
SIZE = 0.34

DARWIN = [  # id, parent, place (relative to the middle picture), score
    ('d0', None, (-1.6, -1.7), 20),
    ('d1', 'd0', (-0.3, -0.9), 25),
    ('d2', 'd0', (-1.7, -0.3), 19),
    ('d3', 'd1', (0.9, -0.2), 30),
    ('d4', 'd1', (-0.4, 0.5), 27),
    ('d5', 'd3', (1.6, 0.9), 36),
    ('d6', 'd2', (-1.6, 1.1), 24),
    ('d7', 'd5', (0.6, 1.8), 41),
]

HUXLEY = [  # id, parent, place (relative to the right picture), score
    ('h0', None, (0.0, 1.8), 22),
    ('h1', 'h0', (-1.2, 0.6), 30),
    ('h2', 'h0', (1.2, 0.6), 34),
    ('h3', 'h1', (-1.8, -0.6), 33),
    ('h4', 'h1', (-0.6, -0.6), 35),
    ('h5', 'h2', (1.2, -0.6), 24),
    ('h6', 'h3', (-1.8, -1.8), 40),      # the best branch grows
    ('h7', 'h4', (-0.6, -1.8), 42),
]

STAIR = [(-5.6, -2.7, 0.6, 20), (-3.0, -1.75, 0.7, 26), (-0.4, -0.8, 0.8, 33), (2.2, 0.15, 0.9, 40), (4.8, 1.1, 1.0, 47)]


def build(T):
    kit.state['zstep'] = 0.0005
    cues = []
    end = sec(kit.frames())
    t_show = [T.at(0, 0.3), T.at(0, 0.5), T.at(0, 0.7)]
    t_g, t_d, t_h = T.start(1), T.start(2), T.start(3)
    t_away = T.start(4) - 0.4
    t_stair0, t_stair1 = T.at(4, 0.05), T.at(4, 0.8)
    t_far = T.start(5)

    kit.backdrop(seed=81, glow=kit.VIOLET_DEEP)
    kit.motes(seed=82, colour=kit.MINT)
    lines = kit.layer('lines', 0.9)
    stage = kit.layer('stage', 1.0)

    def picture(name, at, t_in, k):
        root = kit.empty(name, stage, (at[0], at[1], kit.next_z(stage)))
        line_root = kit.empty(f'{name}-lines', lines, (at[0], at[1], 0.0))
        for ob in (root, line_root):
            kit.pop(ob, t_in, 1.0, 0.5, t_out=t_away + 0.12 * k)
        return root, line_root

    names = ['Gödel Machine', 'Darwin Gödel Machine', 'Huxley-Gödel Machine']
    for k, (at, t_line) in enumerate(((LEFT, t_g), (MID, t_d), (RIGHT, t_h))):
        lab = kit.text(f'name{k}', names[k], 0.3, kit.material(kit.PAPER), stage, (at[0], -3.35))
        alpha(lab, 1, 0.0)
        for f, a in ((fr(t_show[k] + 0.2), 0.0), (fr(t_show[k] + 0.6), 0.5), (fr(t_line), 0.5), (fr(t_line + 0.4), 1.0),
                     (fr(t_line + 0.4) + 1, 1.0), (fr(t_away), 1.0), (fr(t_away + 0.3), 0.0)):
            alpha(lab, f, a)
        cues.append({'t': t_show[k], 'type': 'pop', 'pitch': 0.9 + 0.15 * k, 'gain': 0.6})

    # ------------------------------------------------------------ the Gödel Machine: one program rewriting itself
    g_root, _ = picture('godel', LEFT, t_show[0], 0)
    g = parts.pip('godel-pip', g_root, (0, 0), 1.0, body=kit.SKY, body_deep=kit.SKY_DEEP)
    parts.pip_idle(g, step=2)
    parts.pip_blink(g, (3.0, t_g + 2.6, 14.0, 21.0))
    loop = kit.empty('godel-loop', g_root, (0, 0, kit.next_z(g_root)))
    kit.shape('godel-arc', kit.arc_pts(1.65, 0.09, 120, 400, n=48), kit.material(kit.SKY, alpha=0.75), loop)
    tip_a = math.radians(400)
    tip = (1.65 * math.cos(tip_a), 1.65 * math.sin(tip_a))
    c, s = math.cos(tip_a + math.pi / 2), math.sin(tip_a + math.pi / 2)
    kit.shape('godel-head', [(tip[0] + x * c - y * s, tip[1] + x * s + y * c) for x, y in ((0.2, 0), (-0.14, 0.17), (-0.14, -0.17))],
              kit.material(kit.SKY, alpha=0.75), loop)
    angle = 0.0
    for f in every(1):
        t = sec(f)
        speed = 0.6 + 2.4 * span(t, t_g, t_g + 0.6) * (1 - span(t, t_d - 0.5, t_d + 0.5))
        angle += speed / kit.FPS
        key(loop, 'rotation_euler', f, (0, 0, angle))
    changes = [T.at(1, 0.3), T.at(1, 0.55), T.at(1, 0.8)]
    for k, t0 in enumerate(changes):
        ripple = kit.ring(f'godel-ripple{k}', g_root, (0, 0), 1.2, kit.SKY, w=0.1, lift=0.02)
        kit.flash(ripple, t0, 0.7, grow_by=1.2)
        cues.append({'t': t0, 'type': 'rise', 'dur': 0.4, 'pitch': 1.0 + 0.15 * k, 'gain': 0.5})
    a = g['antenna']
    a.keyframe_insert('scale', frame=fr(changes[0]))
    key(a, 'scale', fr(changes[0]) + 5, (1.15, 1.45, 1))
    for e in g['eye_list']:
        e.keyframe_insert('scale', frame=fr(changes[1]))
        key(e, 'scale', fr(changes[1]) + 5, (1.25, 1.25, 1))
    for side in ('left', 'right'):
        sh = g['arms'][side]
        sh.keyframe_insert('scale', frame=fr(changes[2]))
        key(sh, 'scale', fr(changes[2]) + 5, (1.2, 1.3, 1))

    # ------------------------------------------------------------ the Darwin Gödel Machine: improving through children
    d_root, d_lines = picture('darwin', MID, t_show[1], 1)
    t_d_node = {'d0': t_show[1] + 0.1, 'd1': t_show[1] + 0.5}
    later = [n for n, *_ in DARWIN[2:]]
    for k, n in enumerate(later):
        t_d_node[n] = mix(T.at(2, 0.12), T.at(2, 0.9), k / (len(later) - 1))
    dfam = parts.family('darwin-fam', d_root, d_lines,
                      [{'id': n, 'parent': pa, 'at': at, 'score': sc, 't': t_d_node[n]} for n, pa, at, sc in DARWIN], SIZE)
    for n, pa, at, sc in DARWIN[2:]:
        r = kit.ring(f'{n}-pick', d_root, dfam[pa]['at'], 0.5, kit.AMBER, lift=0.02)
        kit.flash(r, t_d_node[n] - 0.4, 0.55)
        cues.append({'t': t_d_node[n], 'type': 'pop', 'pitch': 0.9 + sc / 60, 'gain': 0.45})

    # ------------------------------------------------------------ the Huxley-Gödel Machine: improving through families
    h_root, h_lines = picture('huxley', RIGHT, t_show[2], 2)
    t_h_node = {n: t_show[2] + 0.1 + 0.1 * k for k, (n, *_) in enumerate(HUXLEY[:6])}
    t_h_node['h6'], t_h_node['h7'] = T.at(3, 0.62), T.at(3, 0.78)
    hfam = parts.family('huxley-fam', h_root, h_lines,
                      [{'id': n, 'parent': pa, 'at': at, 'score': sc, 't': t_h_node[n]} for n, pa, at, sc in HUXLEY], SIZE)
    for name, centre, w, h, colour, t_in in (('best', (-1.2, -0.6), 2.7, 3.7, kit.MINT, T.at(3, 0.3)),
                                             ('weak', (1.2, 0.0), 1.4, 2.4, kit.CORAL, T.at(3, 0.38))):
        hull = kit.shape(f'huxley-{name}', kit.rrect_pts(w, h, 0.6), kit.material(colour, alpha=0.18), h_lines, centre)
        kit.appear(hull, t_in, None, 0.5)
        cues.append({'t': t_in, 'type': 'swoosh', 'gain': 0.35})
    for n in ('h6', 'h7'):
        pa = next(p for i, p, _, _ in HUXLEY if i == n)
        r = kit.ring(f'{n}-pick', h_root, hfam[pa]['at'], 0.5, kit.AMBER, lift=0.02)
        kit.flash(r, t_h_node[n] - 0.4, 0.55)
        cues.append({'t': t_h_node[n], 'type': 'pop', 'pitch': 1.2, 'gain': 0.5})
    cues.append({'t': t_away, 'type': 'whoosh', 'gain': 0.5})

    # ------------------------------------------------------------ today: each new version better than the last
    pips = []
    for k, (x, y, s, score) in enumerate(STAIR):
        t0 = mix(t_stair0, t_stair1, k / (len(STAIR) - 1))
        step = kit.shape(f'stair{k}', kit.rrect_pts(2.0, 0.16, 0.08), kit.material(kit.INK500), stage, (x, y - 1.05 * s))
        kit.appear(step, t0 - 0.3, None, 0.3)
        p = parts.pip(f'version{k}', stage, (x, y), s, *parts.score_colour(score))
        kit.pop(p['root'], t0, s)
        parts.pip_idle(p, t0=t0, phase=k * 1.3, step=2)
        alpha(p['halo'], 1, 0.4 + 0.15 * k)
        pips.append((p, t0))
        cues.append({'t': t0, 'type': 'pop', 'pitch': 0.9 + 0.12 * k, 'gain': 0.55})
    for k in range(1, len(pips)):
        prev, t0 = pips[k - 1][0], pips[k][1]
        parts.pip_look(prev, t0 - 0.5, 0.12, 0.06)
        spark = kit.shape(f'spark{k}', kit.star_pts(0.22, 0.07), kit.material('#fff3cf'), stage, lift=0.3)
        sg = kit.shape(f'spark{k}-glow', kit.circle_pts(0.6), kit.glow_material(kit.AMBER, 0.8), stage, lift=0.29)
        (x0, y0), (x1, y1) = STAIR[k - 1][:2], STAIR[k][:2]
        for ob in (spark, sg):
            z = ob.location.z
            alpha(ob, 1, 0.0)
            for f in every(1, fr(t0 - 0.5), fr(t0 + 0.05)):
                q = span(sec(f), t0 - 0.45, t0, lambda v: v)
                key(ob, 'location', f, (mix(x0, x1, q), mix(y0, y1, q) + 0.8 * math.sin(math.pi * q), z))
                alpha(ob, f, 1.0 if 0 < q < 1 else 0.0)
    last = pips[-1][0]
    parts.pip_look(last, t_far, 0.06, 0.12, 0.4)
    parts.pip_arm(last, 'right', t_far + 0.3, 110, 0.4)

    # the trail goes on up, into the dark
    lx, ly = STAIR[-1][:2]
    for k in range(18):
        q = k / 17
        dot = kit.shape(f'trail{k}', kit.circle_pts(0.08 - 0.03 * q, n=12), kit.material(kit.AMBER, alpha=1 - 0.8 * q), stage,
                        (lx + 1.2 + 2.4 * q, ly + 1.6 + 5.0 * q ** 0.9))
        kit.appear(dot, t_far + 0.1 + 0.08 * k, None, 0.3)
    cues.append({'t': t_far + 0.1, 'type': 'rise', 'dur': 1.6, 'pitch': 1.1, 'gain': 0.45})

    kit.veil(end - 1.0, 0.9)

    # ------------------------------------------------------------ camera
    def path(t):
        x, y, h = 0.0, 0.0, kit.H0 + 0.6
        for t0, (px, py) in ((t_g - 0.4, LEFT), (t_d - 0.4, MID), (t_h - 0.4, RIGHT)):
            q = span(t, t0, t0 + 1.1)
            x, y, h = mix(x, px, q), mix(y, py, q), mix(h, 13.5, q)
        q = span(t, t_away - 0.2, t_away + 1.2)
        x, y, h = mix(x, 0.0, q), mix(y, 0.0, q), mix(h, kit.H0, q)
        q = span(t, t_far - 0.3, end)
        return mix(x, 1.6, q), mix(y, 2.4, q), mix(h, kit.H0 + 0.8, q)

    kit.camera(path, focus_z=1.0)
    return cues
