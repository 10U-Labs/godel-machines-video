"""The cast and props of the Gödel machines film, built from the shared kit.

Pip, the film's made-up program, and how it moves; a program drawn as a file
and as a page of code; a family of programs drawn as small Pips joined by
branches; and Pip's shape as a blueprint drawing.
"""
import math

from kit import (
    AMBER, AMBER_DEEP, CORAL, INK500, INK600, INK700, INK800, INK900, MINT, MINT_DEEP, MIST, PAPER, SKY,
    VIOLET, alpha, arc_pts, bar_pts, branch, capsule_pts, circle_pts, empty, every, fr, frames,
    glow_material, grow, key, material, next_z, pop, rrect_pts, sec, shape, tag, text,
)


# ---------------------------------------------------------------- Pip

def pip(name, parent, loc=(0, 0), scale=1.0, body=MINT, body_deep=MINT_DEEP):
    """Pip: a small round program with a screen for a face, two arms, and an antenna.

    The origin is the middle of the body. Arms hang down at angle 0 and rotate
    about the shoulder; positive angles swing the right arm outward and up.
    """
    root = empty(name, parent, (loc[0], loc[1], next_z(parent)), scale)
    rig = empty(f'{name}-rig', root, (0, 0, 0))          # bobbing and squash live here
    halo = shape(f'{name}-halo', circle_pts(2.0), glow_material(body, 0.3, power=2.2), rig, (0, 0.1))
    arms = {}
    for side in (-1, 1):
        shoulder = empty(f'{name}-shoulder{side}', rig, (side * 0.8, -0.18, next_z(rig)))
        shape(f'{name}-arm{side}', capsule_pts(0.5, 0.22), material(body, body_deep), shoulder)
        shape(f'{name}-hand{side}', circle_pts(0.15), material(body, body_deep), shoulder, (0, -0.52))
        shoulder.rotation_euler = (0, 0, side * math.radians(18))
        arms['left' if side < 0 else 'right'] = shoulder
    antenna = empty(f'{name}-antenna', rig, (0, 0.72, next_z(rig)))
    shape(f'{name}-stem', capsule_pts(0.34, 0.07), material(body_deep), antenna, (0, 0.34))
    bulb_glow = shape(f'{name}-bulb-glow', circle_pts(0.45), glow_material(AMBER, 0.55), antenna, (0, 0.38))
    shape(f'{name}-bulb', circle_pts(0.11), material('#fff2c4', AMBER), antenna, (0, 0.38))
    shape(f'{name}-body', rrect_pts(1.7, 1.5, 0.62), material(body, body_deep), rig)
    shape(f'{name}-shine', circle_pts(0.2, ry=0.1), material(PAPER, alpha=0.45), rig, (-0.48, 0.5), rot=0.5)
    shape(f'{name}-screen', rrect_pts(1.28, 0.86, 0.34), material(INK800, INK900), rig, (0, 0.06))
    face = empty(f'{name}-face', rig, (0, 0.06, next_z(rig)))
    eyes = empty(f'{name}-eyes', face, (0, 0.08, next_z(face)))
    eye_list = []
    for side in (-1, 1):
        e = empty(f'{name}-eye{side}', eyes, (side * 0.27, 0, next_z(face)))
        shape(f'{name}-eyeglow{side}', circle_pts(0.3), glow_material(body, 0.4), e)
        shape(f'{name}-eyeball{side}', circle_pts(0.12, ry=0.16), material('#d9fff5', body), e)
        shape(f'{name}-spark{side}', circle_pts(0.035), material(PAPER), e, (0.04, 0.06))
        eye_list.append(e)
    mouth = shape(f'{name}-mouth', arc_pts(0.13, 0.05, 200, 340), material(body), face, (0, -0.1))
    return {'root': root, 'rig': rig, 'halo': halo, 'arms': arms, 'eyes': eyes, 'eye_list': eye_list,
            'mouth': mouth, 'antenna': antenna, 'bulb_glow': bulb_glow, 'face': face}


def pip_idle(p, t0=0.0, t1=None, phase=0.0, step=2):
    """Bob gently, with a slight squash, and let the antenna sway."""
    t1 = sec(frames()) if t1 is None else t1
    for f in every(step, fr(t0), fr(t1)):
        t = sec(f) + phase
        b = math.sin(t * 2.2)
        key(p['rig'], 'location', f, (0, 0.08 * b, 0))
        key(p['rig'], 'scale', f, (1 - 0.015 * b, 1 + 0.015 * b, 1))
        key(p['antenna'], 'rotation_euler', f, (0, 0, 0.12 * math.sin(t * 2.2 - 0.9)))
        g = 0.8 + 0.2 * math.sin(t * 3.1)
        alpha(p['bulb_glow'], f, g)


def pip_blink(p, times):
    for t in times:
        f = fr(t)
        for df, s in ((-3, 1.0), (0, 0.08), (3, 1.0)):
            for e in p['eye_list']:
                key(e, 'scale', f + df, (1, s, 1))


def pip_look(p, t, dx, dy=0.0, dur=0.25):
    """Glance: the eyes slide across the screen within dur seconds, ending at time t + dur."""
    eyes = p['eyes']
    z = eyes.location.z
    eyes.keyframe_insert('location', frame=fr(t))
    key(eyes, 'location', fr(t + dur), (dx, 0.08 + dy, z))


def pip_arm(p, side, t, deg, dur=0.3):
    """Swing an arm to deg (0 hangs down, 90 points sideways, 160 straight up) by t + dur."""
    shoulder = p['arms'][side]
    s = 1 if side == 'right' else -1
    shoulder.keyframe_insert('rotation_euler', frame=fr(t))
    key(shoulder, 'rotation_euler', fr(t + dur), (0, 0, s * math.radians(deg)))


def pip_wave(p, t0, t1, rate=7.0):
    shoulder = p['arms']['right']
    shoulder.keyframe_insert('rotation_euler', frame=fr(t0))
    for f in every(2, fr(t0) + 4, fr(t1)):
        key(shoulder, 'rotation_euler', f, (0, 0, math.radians(135 + 22 * math.sin((sec(f) - t0) * rate))))
    key(shoulder, 'rotation_euler', fr(t1 + 0.35), (0, 0, math.radians(18)))


def pip_eyes(p, t, sx, sy, dur=0.2):
    """Widen (above 1) or narrow (below 1) both eyes by time t + dur."""
    for e in p['eye_list']:
        e.keyframe_insert('scale', frame=fr(t))
        key(e, 'scale', fr(t + dur), (sx, sy, 1))


# ---------------------------------------------------------------- programs

CODE = [MINT, VIOLET, SKY, AMBER, MIST]


def badge(name, parent, loc=(0, 0), scale=1.0):
    """Pip's face in miniature, marking something as Pip's own."""
    icon = empty(name, parent, (loc[0], loc[1], next_z(parent)), scale)
    shape(f'{name}-glow', circle_pts(0.7), glow_material(MINT, 0.6), icon)
    shape(f'{name}-body', rrect_pts(0.42, 0.36, 0.14), material(MINT, MINT_DEEP), icon)
    shape(f'{name}-screen', rrect_pts(0.3, 0.2, 0.08), material(INK900), icon, (0, 0.01))
    for side in (-1, 1):
        shape(f'{name}-eye{side}', circle_pts(0.03, ry=0.04), material('#d9fff5'), icon, (side * 0.06, 0.02))
    return icon


def file_icon(name, parent, loc=(0, 0), scale=1.0, mine=False, seed=0):
    """A file: a page with a folded corner and a few lines of text on it."""
    import random
    rnd = random.Random(seed)
    root = empty(name, parent, (loc[0], loc[1], next_z(parent)), scale)
    glow = shape(f'{name}-glow', rrect_pts(1.9, 2.2, 0.8), glow_material(MINT if mine else SKY, 0.5, power=1.0), root)
    alpha(glow, 1, 0.0)
    shape(f'{name}-page', [(-0.5, 0.65), (0.22, 0.65), (0.5, 0.37), (0.5, -0.65), (-0.5, -0.65)], material(INK600, INK700), root)
    shape(f'{name}-fold', [(0.22, 0.65), (0.22, 0.37), (0.5, 0.37)], material(INK500), root)
    for r in range(5):
        ln = 0.3 + rnd.random() * 0.4 if r else 0.35
        shape(f'{name}-line{r}', bar_pts(ln, 0.07), material(MIST, alpha=0.8), root, (-0.34, 0.38 - r * 0.2 - (0.08 if r else 0)))
    icon = badge(f'{name}-badge', root, (0.12, -0.42), 0.9) if mine else None
    return {'root': root, 'glow': glow, 'badge': icon}


def program(name, parent, loc=(0, 0), rows=8, w=3.6, h=4.2, seed=1, mistake=None, label=None, scale=1.0, tab_icon=False):
    """A program shown as a page of code: a window with a title bar and rows of coloured bars.

    Returns the root, the list of row bars, and, if mistake is a row number,
    the red bar on that row and the fixed bar that replaces it.
    """
    import random
    rnd = random.Random(seed)
    root = empty(name, parent, (loc[0], loc[1], next_z(parent)), scale)
    shape(f'{name}-shadow', rrect_pts(w + 0.5, h + 0.5, 0.5), glow_material(INK900, 0.7, power=0.8), root, (0.15, -0.2))
    shape(f'{name}-page', rrect_pts(w, h, 0.22), material(INK700, INK800), root)
    shape(f'{name}-bar', [(x, y + h / 2 - 0.3) for x, y in rrect_pts(w, 0.6, 0.22)], material(INK600), root)
    shape(f'{name}-bar-fill', [(x, y + h / 2 - 0.45) for x, y in rrect_pts(w, 0.3, 0)], material(INK600), root)
    for i, c in enumerate((CORAL, AMBER, MINT)):
        shape(f'{name}-dot{i}', circle_pts(0.08), material(c), root, (-w / 2 + 0.3 + i * 0.25, h / 2 - 0.3))
    icon = badge(f'{name}-icon', root, (w / 2 - 0.45, h / 2 - 0.3)) if tab_icon else None
    if label:
        text(f'{name}-label', label, 0.2, material(MIST), root, (0, h / 2 - 0.3), face='JetBrainsMono')
    bars, bad, good = [], None, None
    top = h / 2 - 0.95
    gap = (h - 1.4) / rows
    for r in range(rows):
        indent = [0, 1, 1, 2, 2, 1, 0][rnd.randrange(7)] if r else 0
        x = -w / 2 + 0.35 + indent * 0.35
        y = top - r * gap
        left = w - 0.7 - indent * 0.35
        words = []
        while left > 0.35:
            ln = min(left, 0.35 + rnd.random() * 1.0)
            words.append(ln)
            left -= ln + 0.15
            if rnd.random() < 0.3:
                break
        row = []
        for j, ln in enumerate(words):
            col = CODE[rnd.randrange(len(CODE))]
            if r == mistake:
                col = CORAL
            ob = shape(f'{name}-r{r}w{j}', bar_pts(ln, 0.14), material(col), root, (x, y))
            row.append(ob)
            if r == mistake:
                fix = shape(f'{name}-r{r}w{j}-fixed', bar_pts(ln, 0.14), material(MINT), root, (x, y))
                alpha(fix, 1, 0.0)
                good = (good or []) + [fix]
            x += ln + 0.15
        if r == mistake:
            bad = row
            span_w = x - 0.15 - (-w / 2 + 0.35 + indent * 0.35)
            ring = shape(f'{name}-ring', rrect_pts(span_w + 0.3, 0.42, 0.21), material(CORAL, alpha=0.25), root,
                         (-w / 2 + 0.35 + indent * 0.35 + span_w / 2, y), lift=-0.0015)
            alpha(ring, 1, 0.0)
            bad = {'bars': row, 'ring': ring, 'y': y, 'x': -w / 2 + 0.35 + indent * 0.35 + span_w / 2}
        bars.append(row)
    return {'root': root, 'rows': bars, 'bad': bad, 'good': good, 'icon': icon}


# ---------------------------------------------------------------- families of programs

SCORE_COLOURS = [(18, ('#5aa59b', '#3c7a73')), (24, (MINT, MINT_DEEP)), (32, ('#9af7d8', MINT)), (40, (AMBER, AMBER_DEEP))]


def score_colour(score):
    """Pip's colours for a program with a score: dull for low scores, warm for high ones."""
    out = SCORE_COLOURS[0][1]
    for floor, c in SCORE_COLOURS:
        if score >= floor:
            out = c
    return out


def family(name, stage, lines, nodes, size=0.45, line_colour=MIST, idle_step=3, known=None):
    """A family of programs drawn as small Pips joined by branches.

    nodes is a list of dicts with id, parent (an id, or None), at (x, y), t
    (when it pops in), and optionally score, colour (body, deep), and
    t_out. Branches go in the lines layer, which sits just behind the stage.
    known maps ids of parents drawn elsewhere to their places.
    Returns id -> {'pip', 'line', 'at', 'tag'}.
    """
    import random
    rnd = random.Random(len(nodes))
    out = {}
    for n in nodes:
        at = n['at']
        body, deep = n.get('colour') or score_colour(n.get('score', 24))
        line = None
        if n.get('parent') is not None:
            pa = out[n['parent']]['at'] if n['parent'] in out else known[n['parent']]
            line = branch(f'{name}-{n["id"]}-line', lines, pa, at, line_colour)
            grow(line, n['t'] - 0.3, 0.3, n.get('t_out'))
        p = pip(f'{name}-{n["id"]}', stage, at, size, body=body, body_deep=deep)
        alpha(p['halo'], 1, 0.35)
        pop(p['root'], n['t'], size, t_out=n.get('t_out'))
        pip_idle(p, phase=rnd.random() * 6, step=idle_step)
        tg = None
        if 'score' in n:
            tg = tag(f'{name}-{n["id"]}-tag', stage, (at[0] + 0.8 * size / 0.45, at[1] + 0.3 * size / 0.45), str(n['score']),
                     colour=AMBER if n['score'] >= 40 else PAPER)
        out[n['id']] = {'pip': p, 'line': line, 'at': at, 'tag': tg}
    return out


def machine_outline(step=0.16):
    """Points along the lines of Pip's shape (body, screen, eyes, antenna, arms), for a blueprint drawing."""
    def sample(pts, closed=True):
        out = []
        loop = pts + [pts[0]] if closed else pts
        for (x0, y0), (x1, y1) in zip(loop, loop[1:]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
            out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
        return out
    body = sample(rrect_pts(1.7, 1.5, 0.62))
    screen = [(x, y + 0.06) for x, y in sample(rrect_pts(1.28, 0.86, 0.34))]
    eyes = [(x + dx, y + 0.14) for dx in (-0.27, 0.27) for x, y in sample(circle_pts(0.14, ry=0.17, n=24))]
    antenna = sample([(0, 0.75), (0, 1.1)], closed=False) + [(x, y + 1.13) for x, y in sample(circle_pts(0.11, n=16))]
    arms = [(s * 0.85 + s * 0.15 * i / 6, -0.2 - 0.5 * i / 6) for s in (-1, 1) for i in range(7)]
    return body + screen + eyes + antenna + arms
