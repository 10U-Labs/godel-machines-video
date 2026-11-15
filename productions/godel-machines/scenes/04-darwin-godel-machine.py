"""Scene 04: Improving through children.

The Gödel Machine's blueprint fades, unbuilt. A team of researchers gathers
at a screen, and a machine appears on it: the Darwin Gödel Machine. Pip does
not change in place; it writes a changed copy of its code, and the copy
becomes its child. The child solves problems and gets a score. Parents are
picked, mostly the ones with high scores, and a family grows generation by
generation. An old program from early on becomes a parent again.
"""
import math

import kit
import parts
from kit import fr, sec, span, mix, key, alpha, every

SHEET_W, SHEET_H = 6.4, 4.6
SCREEN_AT = (1.2, 0.6)
PIP_AT = (-4.4, 0.2)
CODE_AT = (-0.6, 0.3)
CHILD_AT = (3.8, 0.2)
SIZE = 0.45

# The family: id, parent, place, score. Higher scores have more children.
TREE = [
    ('n0', None, (-6.5, -0.2), 20),
    ('n1', 'n0', (-4.4, 0.9), 23),
    ('n2', 'n0', (-4.4, -1.4), 18),
    ('n3', 'n1', (-2.3, 1.8), 27),
    ('n4', 'n1', (-2.3, 0.3), 25),
    ('n5', 'n3', (-0.2, 2.6), 31),
    ('n6', 'n3', (-0.2, 1.4), 29),
    ('n7', 'n4', (-0.2, 0.0), 24),
    ('n8', 'n5', (1.9, 3.1), 36),
    ('n9', 'n5', (1.9, 2.0), 33),
    ('n10', 'n6', (1.9, 0.9), 30),
    ('n11', 'n8', (4.0, 3.4), 41),
    ('n12', 'n8', (4.0, 2.4), 38),
    ('n13', 'n9', (4.0, 1.4), 35),
    ('n14', 'n11', (6.1, 3.2), 47),
    ('n15', 'n11', (6.1, 2.2), 44),
    ('n16', 'n2', (-2.3, -1.9), 26),
    ('n17', 'n7', (1.9, -0.4), 32),
]


def build(T):
    kit.state['zstep'] = 0.0005
    cues = []
    end = sec(kit.frames())
    t_dim = T.at(0, 0.1)
    t_2025 = T.at(0, 0.22)
    t_team = T.at(0, 0.28)
    t_built = T.at(0, 0.47)
    t_name = T.at(0, 0.78)
    t_out0 = T.start(1) - 0.4
    t_pip = T.start(1) + 0.05
    t_place = T.at(1, 0.08)
    t_code = T.at(1, 0.38)
    t_copy = T.at(1, 0.5)
    t_change = T.at(1, 0.64)
    t_child = T.at(1, 0.82)
    t_tests = T.start(2) + 0.2
    t_score = T.at(2, 0.4)
    t_move = T.at(2, 0.55)
    t_again = T.at(2, 0.86)
    t_grow0, t_grow1 = T.at(3, 0.04), T.at(3, 0.92)
    t_old = T.at(4, 0.3)

    kit.backdrop(seed=41, glow=kit.MINT_DEEP)
    kit.motes(seed=42, colour=kit.MINT)
    lines = kit.layer('lines', 0.9)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the blueprint, never built
    sheet = kit.empty('sheet', stage, (0, 0.3, kit.next_z(stage)))
    paper = kit.shape('sheet-paper', kit.rrect_pts(SHEET_W, SHEET_H, 0.15), kit.material('#1d3f8f', '#16307a'), sheet)
    drawn = [paper]
    for i in range(1, 12):
        drawn.append(kit.shape(f'grid-v{i}', kit.rrect_pts(0.025, SHEET_H - 0.3, 0), kit.material(kit.SKY, alpha=0.18), sheet, (-SHEET_W / 2 + i * SHEET_W / 12, 0)))
    for i in range(1, 9):
        drawn.append(kit.shape(f'grid-h{i}', kit.rrect_pts(SHEET_W - 0.3, 0.025, 0), kit.material(kit.SKY, alpha=0.18), sheet, (0, -SHEET_H / 2 + i * SHEET_H / 9)))
    for k, (x, y) in enumerate(parts.machine_outline()):
        drawn.append(kit.shape(f'dash{k}', kit.circle_pts(0.04, n=10), kit.material('#cfe9ff'), sheet, (x * 1.4, y * 1.4 - 0.1)))
    for ob in drawn:
        alpha(ob, 1, 1.0)
        alpha(ob, fr(t_dim), 1.0)
        alpha(ob, fr(t_dim + 0.8), 0.35)
    zs = sheet.location.z
    for f in every(1, 1, fr(t_team + 0.4)):
        t = sec(f)
        q = span(t, t_2025 - 0.2, t_team + 0.4)
        key(sheet, 'location', f, (mix(0.0, -10.5, q), 0.3 - 0.4 * q, zs))
        key(sheet, 'rotation_euler', f, (0, 0, 0.02 * math.sin(t * 0.7) + 0.25 * q))
    cues.append({'t': t_2025 - 0.2, 'type': 'whoosh', 'gain': 0.5})

    # ------------------------------------------------------------ the team and their screen
    floor = kit.shape('floor', kit.rrect_pts(30, 0.06, 0), kit.material(kit.MIST, alpha=0.2), stage, (0, -2.35))
    kit.appear(floor, t_team, t_out0, 0.5)
    screen = kit.screen_stand('screen', stage, SCREEN_AT)
    kit.pop(screen['root'], t_team, 1.0, 0.5, t_out=t_out0)
    cues.append({'t': t_team, 'type': 'pop', 'pitch': 0.8})

    team = [  # where they stand, where they come from, facing, scale, coat, coat shade, hair
        ((-3.4, 0.9), -10.5, 1, 0.72, '#d9604f', '#a8413a', '#2b1d1a'),
        ((5.4, 1.0), 10.5, -1, 0.75, '#3f8f6f', '#2b6b52', '#5a3a22'),
        ((6.9, 0.6), 11.5, -1, 0.66, kit.AMBER_DEEP, '#b86c12', '#141414'),
    ]
    for k, (at, start_x, facing, s, coat, deep, hair) in enumerate(team):
        who = kit.person(f'researcher{k}', stage, at, s, coat=coat, coat_deep=deep, hair=hair, facing=facing)
        z = who['root'].location.z
        t_in = t_team + 0.15 + 0.3 * k
        for f in every(1):
            t = sec(f)
            x = mix(start_x, at[0], span(t, t_in, t_in + 1.0, kit.ease_out))
            x = mix(x, start_x, span(t, t_out0 - 0.3, t_out0 + 0.5))
            walk = span(t, t_in, t_in + 1.0) < 1 or span(t, t_out0 - 0.3, t_out0 + 0.5) > 0
            bob = 0.06 * abs(math.sin(t * 9)) if walk else 0.0
            key(who['root'], 'location', f, (x, at[1] + bob, z))
            point = span(t, t_built - 0.3 + 0.2 * k, t_built + 0.1 + 0.2 * k) * (1 - span(t, t_name + 1.0, t_name + 1.5))
            deg = mix(8, 75 if k == 0 else 50, point) + 3 * math.sin(t * 1.3 + k)
            key(who['arm'], 'rotation_euler', f, (0, 0, facing * math.radians(deg)))
            key(who['head'], 'rotation_euler', f, (0, 0, 0.04 * math.sin(t * 0.9 + k * 2)))

    year = kit.text('year', '2025', 0.62, kit.material(kit.PAPER), stage, (-6.9, 3.85), align='LEFT')
    kit.appear(year, t_2025, t_out0, 0.4)
    m = parts.pip('machine', stage, (SCREEN_AT[0], SCREEN_AT[1] + 0.05), 1.0)
    kit.pop(m['root'], t_built, 1.0, t_out=t_out0 - 0.1)
    parts.pip_idle(m, step=2)
    parts.pip_blink(m, (t_built + 1.5, t_name + 0.8))
    cues.append({'t': t_built, 'type': 'pop', 'pitch': 1.2})
    title = kit.text('title', 'Darwin Gödel Machine', 0.55, kit.material(kit.PAPER), stage, (SCREEN_AT[0], 3.25))
    kit.appear(title, t_name, t_out0 - 0.2, 0.5)
    cues.append({'t': t_name, 'type': 'chime', 'gain': 0.6})

    # ------------------------------------------------------------ Pip writes a changed copy: its child
    n0 = parts.pip('n0', stage, PIP_AT, 1.3)
    parts.pip_idle(n0, step=2)
    parts.pip_blink(n0, (t_pip + 1.2, t_copy + 1.0, t_tests + 2.0, t_move + 3.0, t_grow1 + 1.0))
    alpha(n0['halo'], 1, 0.6)
    cues.append({'t': t_pip, 'type': 'pop'})

    # not in place: a loop around Pip shows up and fades, and Pip shakes its eyes no
    loop = kit.shape('in-place', kit.arc_pts(1.6, 0.1, 110, 410, n=48), kit.material(kit.MIST, alpha=0.7), stage, PIP_AT, lift=0.05)
    kit.appear(loop, t_place, t_place + 1.4, 0.3)
    for f in every(1, fr(t_place), fr(t_place + 1.8)):
        key(loop, 'rotation_euler', f, (0, 0, -(sec(f) - t_place) * 2.5))
    for k, dx in enumerate((0.1, -0.1, 0.1, 0.0)):
        parts.pip_look(n0, t_place + 0.5 + 0.22 * k, dx, 0.0, 0.18)

    code = parts.program('code', stage, CODE_AT, rows=6, w=3.0, h=3.6, seed=44, tab_icon=True, scale=0.8)
    kit.pop(code['root'], t_code, 0.8, t_out=t_child - 0.1)
    cues.append({'t': t_code, 'type': 'pop', 'pitch': 0.9})
    copy = parts.program('copy', stage, CODE_AT, rows=6, w=3.0, h=3.6, seed=44, tab_icon=True, scale=0.8)
    zc = copy['root'].location.z
    for f in every(1, 1, fr(t_child + 0.4)):
        t = sec(f)
        q = span(t, t_copy, t_copy + 0.8, kit.ease_out)
        key(copy['root'], 'location', f, (mix(CODE_AT[0], CHILD_AT[0], q), mix(CODE_AT[1], CHILD_AT[1] + 0.1, q) + 0.3 * math.sin(math.pi * q), zc))
        s = 0.8 * (1.0 if t >= t_copy else 0.001) * (1 - span(t, t_child, t_child + 0.25)) + 0.001
        key(copy['root'], 'scale', f, (s, s, s))
    cues.append({'t': t_copy, 'type': 'whoosh', 'gain': 0.5})
    parts.pip_look(n0, t_copy - 0.3, 0.13, 0.0)
    row = 2
    y = copy['rows'][row][0].location.y
    hl = kit.shape('changed-row', kit.rrect_pts(2.8, 0.36, 0.18), kit.material(kit.AMBER, alpha=0.4), copy['root'], (0, y), lift=-0.0015)
    alpha(hl, 1, 0.0)
    for f, a in ((fr(t_change), 0.0), (fr(t_change) + 3, 1.0), (fr(t_child - 0.2), 1.0), (fr(t_child), 0.0)):
        alpha(hl, f, a)
    for ob in copy['rows'][row]:
        ob.keyframe_insert('scale', frame=fr(t_change))
        key(ob, 'scale', fr(t_change) + 4, (0.001, 1, 1))
        key(ob, 'scale', fr(t_change) + 10, (1.25, 1, 1))
    cues.append({'t': t_change, 'type': 'tick', 'pitch': 1.3, 'gain': 0.7})

    child = parts.pip('n1', stage, CHILD_AT, 1.0, *parts.score_colour(23))
    kit.pop(child['root'], t_child, 1.0)
    parts.pip_idle(child, phase=1.3, step=2)
    parts.pip_blink(child, (t_child + 1.0, t_score + 0.6, t_move + 2.4))
    alpha(child['halo'], 1, 0.6)
    cues.append({'t': t_child, 'type': 'pop', 'pitch': 1.3})
    first_line = kit.branch('first-line', lines, PIP_AT, CHILD_AT, kit.MIST)
    kit.grow(first_line, t_child - 0.1, 0.4, t_out=t_move - 0.2)
    parts.pip_look(n0, t_child + 0.3, 0.14, 0.0)

    # ------------------------------------------------------------ the child is tested and gets a score
    parts.pip_look(child, t_tests - 0.2, 0.12, -0.05)
    for k in range(4):
        t0 = t_tests + 0.55 * k
        job = parts.program(f'task{k}', stage, (9.5, -2.6), rows=3, w=2.0, h=1.4, seed=50 + k, mistake=1, scale=0.6)
        zj = job['root'].location.z
        t_hit = t0 + 0.55
        for f in every(1, fr(t0 - 0.1), fr(t0 + 1.7)):
            t = sec(f)
            x = mix(9.5, CHILD_AT[0] + 0.3, span(t, t0, t_hit, kit.ease_out))
            x = mix(x, -9.5, span(t, t_hit + 0.2, t0 + 1.7, lambda v: v * v))
            key(job['root'], 'location', f, (x, -2.4 + 0.15 * math.sin(math.pi * span(t, t0, t_hit)), zj))
        if k != 2:                          # one problem stays unsolved
            for ob in job['bad']['bars']:
                alpha(ob, fr(t_hit), 1.0)
                alpha(ob, fr(t_hit + 0.1), 0.0)
            for ob in job['good']:
                alpha(ob, fr(t_hit), 0.0)
                alpha(ob, fr(t_hit + 0.1), 1.0)
            cues.append({'t': t_hit, 'type': 'blip', 'pitch': 1.1 + 0.05 * k, 'gain': 0.5})
        else:
            cues.append({'t': t_hit, 'type': 'tick', 'pitch': 0.7, 'gain': 0.5})
    big = kit.tag('n1-big-tag', stage, (CHILD_AT[0], CHILD_AT[1] + 2.05), '23', size=0.42)
    kit.pop(big['root'], t_score, 1.0, t_out=t_move - 0.3)
    cues.append({'t': t_score, 'type': 'chime', 'gain': 0.5, 'pitch': 1.2})

    # ------------------------------------------------------------ parents are picked, and the family grows
    for p, at, s0, dest in ((n0, PIP_AT, 1.3, TREE[0][2]), (child, CHILD_AT, 1.0, TREE[1][2])):
        z = p['root'].location.z
        for f in every(1, fr(t_move - 0.05), fr(t_move + 1.0)):
            q = span(sec(f), t_move, t_move + 1.0)
            key(p['root'], 'location', f, (mix(at[0], dest[0], q), mix(at[1], dest[1], q), z))
            key(p['root'], 'scale', f, (mix(s0, SIZE, q),) * 3)
        alpha(p['halo'], fr(t_move), 0.6)
        alpha(p['halo'], fr(t_move + 1.0), 0.35)
    cues.append({'t': t_move, 'type': 'whoosh', 'gain': 0.4})
    n1_line = kit.branch('n1-line', lines, TREE[0][2], TREE[1][2])
    kit.grow(n1_line, t_move + 0.9, 0.3)

    # when each node pops in, and who was picked to be its parent just before
    t_tree = {'n2': t_move + 1.5, 'n3': t_again + 0.4}
    later = [n for n, *_ in TREE[4:16]]
    for k, n in enumerate(later):
        t_tree[n] = mix(t_grow0, t_grow1, k / (len(later) - 1))
    t_tree['n16'] = t_old + 0.45
    t_tree['n17'] = t_old + 1.6
    nodes = [{'id': n, 'parent': pa, 'at': at, 'score': sc, 't': t_tree[n]} for n, pa, at, sc in TREE[2:]]
    places = {n: at for n, _, at, _ in TREE}
    fam = parts.family('fam', stage, lines, nodes, SIZE, known=places)
    for n, pa, at, sc in TREE[2:]:
        r = kit.ring(f'{n}-pick', stage, places[pa], 0.62, kit.AMBER, lift=0.02)
        kit.flash(r, t_tree[n] - 0.45, 0.6)
        kit.pop(fam[n]['tag']['root'], t_tree[n] + 0.25, 1.0, 0.3)
        cues.append({'t': t_tree[n], 'type': 'pop', 'pitch': 0.9 + sc / 60, 'gain': 0.45})
    for n, s in (('n0', 20), ('n1', 23)):
        tg = kit.tag(f'{n}-tag', stage, (places[n][0] + 0.8, places[n][1] + 0.3), str(s))
        kit.pop(tg['root'], t_move + 1.0, 1.0, 0.3)
    cues.append({'t': t_grow0, 'type': 'rise', 'dur': t_grow1 - t_grow0, 'pitch': 0.9, 'gain': 0.35})

    # the old ones stay, and an early program becomes a parent again
    old = kit.ring('old-glow', stage, places['n2'], 0.75, kit.MINT, w=0.12, lift=0.02)
    for f, a in ((fr(t_old - 0.3), 0.0), (fr(t_old), 1.0), (fr(t_old + 1.2), 1.0), (fr(t_old + 1.8), 0.0)):
        alpha(old, f, a)
    cues.append({'t': t_old, 'type': 'chime', 'gain': 0.45, 'pitch': 0.9})

    # ------------------------------------------------------------ camera
    def path(t):
        q = kit.smooth(t / end)
        x, y, h = 0.1 * q, 0.05 * q, kit.H0 - 0.4 * q
        tree = span(t, t_move, t_move + 1.4)
        x, y, h = mix(x, -4.2, tree), mix(y, 0.1, tree), mix(h, 15.0, tree)
        wide = span(t, t_grow0 - 0.5, t_grow0 + 3.0)
        x, y, h = mix(x, 0.0, wide), mix(y, 0.6, wide), mix(h, kit.H0 + 1.0, wide)
        back = span(t, T.start(4) - 0.2, T.start(4) + 1.6)
        return mix(x, -2.6, back), mix(y, -0.6, back), mix(h, 16.5, back)

    kit.camera(path, focus_z=1.0)
    return cues
