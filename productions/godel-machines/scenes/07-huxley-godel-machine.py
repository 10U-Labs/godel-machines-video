"""Scene 07: Improving through families.

A family of programs hangs down from one program at the top. One program,
then its children, then theirs, light up, and a soft boundary closes around
them all: a clade. Each clade is rated as a whole, and the best clade gets
more children. The best single program sits in a weak clade; the program
that starts the best family is picked instead. Last, the two machines stand
on columns as tall as their scores, beside clocks of the computer time they
used.
"""
import math

import kit
import parts
from kit import fr, sec, span, mix, key, alpha, every

SIZE = 0.42

TREE = [  # id, parent, place, score
    ('r', None, (0.0, 3.3), 22),
    ('a', 'r', (-5.0, 1.7), 26),
    ('b', 'r', (0.0, 1.7), 29),
    ('c', 'r', (5.0, 1.7), 44),
    ('a1', 'a', (-6.3, 0.1), 28),
    ('a2', 'a', (-3.7, 0.1), 25),
    ('b1', 'b', (-1.3, 0.1), 33),
    ('b2', 'b', (1.3, 0.1), 31),
    ('c1', 'c', (5.0, 0.1), 23),
    ('a3', 'a1', (-6.3, -1.5), 27),
    ('a4', 'a2', (-3.7, -1.5), 24),
    ('b3', 'b1', (-1.9, -1.5), 37),
    ('b4', 'b1', (-0.6, -1.5), 35),
    ('b5', 'b2', (0.7, -1.5), 36),
    ('b6', 'b2', (1.9, -1.5), 38),
    ('c2', 'c1', (5.0, -1.5), 21),
    ('b7', 'b3', (-1.9, -3.0), 40),
    ('b8', 'b6', (1.9, -3.0), 39),
    ('b9', 'b4', (-0.6, -3.0), 42),       # the best clade's new children
    ('b10', 'b5', (0.7, -3.0), 41),
]

CLADES = {  # centre, width, height, colour, rating (share of the meter)
    'a': ((-5.0, -0.1), 4.0, 4.4, kit.SKY, 0.45),
    'b': ((0.0, -0.55), 5.0, 5.3, kit.MINT, 0.9),
    'c': ((5.0, -0.1), 2.6, 4.4, kit.CORAL, 0.22),
}


def clock(name, parent, loc, lit, t0, rate, colour):
    """A clock face whose rim lights segment by segment from t0, one segment every rate seconds."""
    root = kit.empty(name, parent, (loc[0], loc[1], kit.next_z(parent)))
    kit.shape(f'{name}-face', kit.circle_pts(0.72), kit.material(kit.INK700, kit.INK800), root)
    segs = []
    for i in range(24):
        a = math.pi / 2 - math.tau * (i + 0.5) / 24
        at = (0.6 * math.cos(a), 0.6 * math.sin(a))
        kit.shape(f'{name}-slot{i}', kit.rrect_pts(0.07, 0.17, 0.03), kit.material(kit.INK500), root, at, rot=a - math.pi / 2)
        if i < lit:
            on = kit.shape(f'{name}-seg{i}', kit.rrect_pts(0.08, 0.19, 0.03), kit.material(colour), root, at, rot=a - math.pi / 2)
            t = t0 + rate * i
            alpha(on, 1, 0.0)
            alpha(on, fr(t), 0.0)
            alpha(on, fr(t) + 1, 1.0)
            segs.append(on)
    hand = kit.shape(f'{name}-hand', [(-0.03, 0), (0.03, 0), (0.02, 0.45), (-0.02, 0.45)], kit.material(kit.PAPER), root)
    kit.shape(f'{name}-hub', kit.circle_pts(0.06), kit.material(kit.PAPER), root)
    for f in every(1, fr(t0), fr(t0 + rate * lit) + 1):
        q = min(lit, (sec(f) - t0) / rate) / 24
        key(hand, 'rotation_euler', f, (0, 0, -math.tau * q))
    return root


def build(T):
    kit.state['zstep'] = 0.0005
    cues = []
    end = sec(kit.frames())
    t_tree0 = 0.15
    t_one = T.at(1, 0.04)
    t_kids = T.at(1, 0.19)
    t_grand = T.at(1, 0.31)
    t_down = T.at(1, 0.43)
    t_clade = T.at(1, 0.56)
    t_name = T.at(1, 0.76)
    t_rate = T.start(2) + 0.2
    t_meters = T.at(2, 0.25)
    t_more = T.at(2, 0.62)
    t_best = T.start(3) + 0.3
    t_starts = T.at(3, 0.52)
    t_clear = T.start(4) - 0.35
    t_cols = T.at(4, 0.08)
    t_clocks = T.at(4, 0.6)

    kit.backdrop(seed=71, glow=kit.VIOLET_DEEP)
    kit.motes(seed=72, colour=kit.VIOLET)
    lines = kit.layer('lines', 0.9)
    hulls = kit.layer('hulls', 0.8)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the family, built quickly from the top
    t_node = {}
    order = [n for n, *_ in TREE[:18]]
    for k, n in enumerate(order):
        t_node[n] = t_tree0 + 0.12 * k
    t_node['b9'], t_node['b10'] = t_more + 0.45, t_more + 1.2
    nodes = [{'id': n, 'parent': pa, 'at': at, 'score': sc, 't': t_node[n],
              't_out': t_clear + 0.02 * i} for i, (n, pa, at, sc) in enumerate(TREE)]
    fam = parts.family('fam', stage, lines, nodes, SIZE)
    places = {n: at for n, _, at, _ in TREE}
    cues.append({'t': t_tree0, 'type': 'rise', 'dur': 2.0, 'pitch': 0.9, 'gain': 0.4})
    for n in ('r', 'a', 'b', 'c'):
        cues.append({'t': t_node[n], 'type': 'pop', 'pitch': 0.9 + 0.05 * len(cues), 'gain': 0.4})

    # ------------------------------------------------------------ a program, its children, theirs, and so on down
    lights = [(t_one, ['b']), (t_kids, ['b1', 'b2']), (t_grand, ['b3', 'b4', 'b5', 'b6']), (t_down, ['b7', 'b8'])]
    for k, (t, ids) in enumerate(lights):
        for n in ids:
            r = kit.ring(f'{n}-light', stage, places[n], 0.58, kit.MINT, w=0.09, lift=0.02)
            for f, a in ((fr(t), 0.0), (fr(t + 0.2), 1.0), (fr(t_clade + 0.3), 1.0), (fr(t_clade + 0.9), 0.0)):
                alpha(r, f, a)
        cues.append({'t': t, 'type': 'blip', 'pitch': 1.0 + 0.12 * k, 'gain': 0.55})

    hull = {}
    for c, (centre, w, h, colour, _) in CLADES.items():
        ob = kit.shape(f'{c}-hull', kit.rrect_pts(w, h, 0.9), kit.material(colour, alpha=0.16), hulls, centre)
        t_in = t_clade if c == 'b' else t_rate
        alpha(ob, 1, 0.0)
        alpha(ob, fr(t_in), 0.0)
        alpha(ob, fr(t_in + 0.5), 1.0)
        alpha(ob, fr(t_clear), 1.0)
        alpha(ob, fr(t_clear + 0.4), 0.0)
        if c == 'b':                             # the best family lights up brighter
            bright = kit.shape('b-hull-bright', kit.rrect_pts(w, h, 0.9), kit.material(colour, alpha=0.2), hulls, centre)
            kit.appear(bright, t_starts, t_clear, 0.4)
        hull[c] = ob
    word = kit.text('clade-word', 'clade', 0.4, kit.material(kit.MINT), stage, (CLADES['b'][0][0] + 1.9, CLADES['b'][0][1] + 2.95))
    kit.appear(word, t_clade + 0.2, t_rate, 0.4)
    cues.append({'t': t_clade, 'type': 'swoosh', 'gain': 0.5})
    title = kit.text('title', 'Huxley-Gödel Machine', 0.55, kit.material(kit.PAPER), stage, (0, -4.05))
    kit.appear(title, t_name, t_rate - 0.3, 0.5)
    cues.append({'t': t_name, 'type': 'chime', 'gain': 0.6})

    # ------------------------------------------------------------ each clade gets a rating; the best grows
    for k, (c, (centre, w, h, colour, share)) in enumerate(CLADES.items()):
        at = (centre[0] - 1.6, -4.15)
        track_ob = kit.shape(f'{c}-track', kit.bar_pts(3.2, 0.22), kit.material(kit.INK600), stage, at)
        fill = kit.shape(f'{c}-fill', kit.bar_pts(3.2, 0.22), kit.material(colour), stage, at)
        kit.appear(track_ob, t_rate, t_clear, 0.4)
        t0 = t_meters + 0.25 * k
        key(fill, 'scale', 1, (0.001, 1, 1))
        key(fill, 'scale', fr(t0), (0.001, 1, 1))
        key(fill, 'scale', fr(t0 + 0.9), (share, 1, 1))
        kit.appear(fill, t_rate, t_clear, 0.4)
        cues.append({'t': t0, 'type': 'rise', 'dur': 0.9, 'pitch': 0.8 + share * 0.6, 'gain': 0.4})
    for n in ('b9', 'b10'):
        pa = next(p for i, p, _, _ in TREE if i == n)
        r = kit.ring(f'{n}-pick', stage, places[pa], 0.6, kit.AMBER, lift=0.02)
        kit.flash(r, t_node[n] - 0.45, 0.6)
        cues.append({'t': t_node[n], 'type': 'pop', 'pitch': 1.2, 'gain': 0.5})

    # ------------------------------------------------------------ not the best Pip, the Pip that starts the best family
    c_tag = fam['c']['tag']
    kit.pop(c_tag['root'], t_best, 1.3, 0.35, t_out=t_starts)
    c_ring = kit.ring('c-best', stage, places['c'], 0.62, kit.AMBER, w=0.1, lift=0.02)
    for f, a in ((fr(t_best), 0.0), (fr(t_best + 0.25), 1.0), (fr(t_starts - 0.2), 1.0), (fr(t_starts + 0.2), 0.0)):
        alpha(c_ring, f, a)
    cues.append({'t': t_best, 'type': 'pop', 'pitch': 1.3, 'gain': 0.6})
    b_tag = fam['b']['tag']
    kit.pop(b_tag['root'], t_starts, 1.3, 0.35, t_out=t_clear)
    b_ring = kit.ring('b-best', stage, places['b'], 0.62, kit.MINT, w=0.12, lift=0.02)
    for f, a in ((fr(t_starts), 0.0), (fr(t_starts + 0.25), 1.0), (fr(t_clear - 0.1), 1.0), (fr(t_clear + 0.2), 0.0)):
        alpha(b_ring, f, a)
    cues.append({'t': t_starts, 'type': 'chime', 'gain': 0.6})
    for n in ('b', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10'):
        parts.pip_eyes(fam[n]['pip'], t_starts + 0.1, 1.12, 0.7)
    parts.pip_look(fam['c']['pip'], t_starts, -0.1, -0.05)

    # ------------------------------------------------------------ the two machines: score and computer time
    cues.append({'t': t_clear, 'type': 'whoosh', 'gain': 0.5})
    base = -3.0
    machines = [('dgm', -3.4, 2.4, (kit.VIOLET, kit.VIOLET_DEEP), 'Darwin Gödel Machine', 24),
                ('hgm', 3.4, 3.4, (kit.MINT, kit.MINT_DEEP), 'Huxley-Gödel Machine', 10)]
    for k, (name, x, height, (body, deep), label, lit) in enumerate(machines):
        col = kit.shape(f'{name}-column', [(0.75, 0), (0.75, 1), (-0.75, 1), (-0.75, 0)], kit.material(body, deep), stage, (x, base))
        p = parts.pip(f'{name}-pip', stage, (x, base + 0.95), 0.9, body=body, body_deep=deep)
        parts.pip_idle(p, phase=k * 1.7, step=2)
        parts.pip_blink(p, (t_cols + 2.0 + k * 0.6,))
        z = p['root'].location.z
        t0 = t_cols + 0.35 * k
        for f in every(1):
            t = sec(f)
            q = span(t, t0, t0 + 1.4, kit.ease_out)
            h = 0.001 + height * q
            key(col, 'scale', f, (1, h, 1))
            key(p['root'], 'location', f, (x, base + h + 0.95, z))
        kit.pop(p['root'], t0, 0.9)
        kit.appear(col, t0, None, 0.2)
        lab = kit.text(f'{name}-label', label, 0.32, kit.material(kit.PAPER), stage, (x, base - 0.45))
        kit.appear(lab, t0 + 0.2, None, 0.4)
        cues.append({'t': t0, 'type': 'rise', 'dur': 1.4, 'pitch': 0.8 + 0.25 * k, 'gain': 0.45})
        clock(f'{name}-clock', stage, (x + 2.0, base + height * 0.5 + 0.3), lit, t_clocks, 0.11, body)
    for k in range(0, 24, 3):
        cues.append({'t': t_clocks + 0.11 * k, 'type': 'tick', 'pitch': 1.0, 'gain': 0.3})
    cues.append({'t': t_clocks + 0.11 * 10, 'type': 'chime', 'gain': 0.5, 'pitch': 1.2})

    # ------------------------------------------------------------ camera
    def path(t):
        x, y, h = 0.0, 2.4, 13.5
        wide = span(t, 0.6, T.end(0))
        x, y, h = mix(x, 0.0, wide), mix(y, -0.3, wide), mix(h, kit.H0 + 1.4, wide)
        near = span(t, t_one - 0.3, t_one + 1.2) * (1 - span(t, t_rate - 0.6, t_rate + 0.6))
        x, y, h = mix(x, 0.0, near), mix(y, -0.4, near), mix(h, 17.0, near)
        end_q = span(t, t_clear, t_clear + 1.2)
        return mix(x, 0.0, end_q), mix(y, 0.3, end_q), mix(h, kit.H0 - 0.5, end_q) - 0.3 * span(t, t_clear, end)

    kit.camera(path, focus_z=1.0)
    return cues
