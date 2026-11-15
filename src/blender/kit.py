"""Shared parts for a production's Blender scenes: palette, flat shapes, motion, Pip.

Every scene is built from flat 2D shapes set out in depth, so a moving camera
gives parallax and depth of field softens what is near and far. Every surface
is an emission shader, so colours come out exactly as written and no lights
are needed.

Design units are screen units at depth z = 0, seen from the camera's start
height H0: the frame spans x from -8 to 8 and y from -4.5 to 4.5.
"""
import math
from pathlib import Path

import bpy

FPS = None          # frames a second; render_scene.py sets it from the production's settings
H0 = 20.0
ROOT = Path(__file__).resolve().parents[2]

# Colours (sRGB hex), one palette for every scene.
INK900, INK800, INK700, INK600, INK500 = '#0b1030', '#121a47', '#1b2660', '#27347d', '#3a4aa3'
MINT, MINT_DEEP, AMBER, AMBER_DEEP = '#4fe3c1', '#1fae93', '#ffc24b', '#f09a1f'
CORAL, CORAL_DEEP, VIOLET, VIOLET_DEEP = '#ff6b6b', '#d9434f', '#a78bfa', '#7357e0'
SKY, SKY_DEEP, PAPER, MIST, SLATE = '#5cc8ff', '#2b93e0', '#f4f1ff', '#b9c0ea', '#7c86c2'

state = {'frames': 1, 'zstep': 0.002}


def frames():
    return state['frames']


def lin(hex_colour, a=1.0):
    """sRGB hex to the linear RGBA that Blender's shader nodes expect."""
    h = hex_colour.lstrip('#')
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, a)


# ---------------------------------------------------------------- timing

class Timing:
    """Narration timings for one scene, in seconds, turned into frames."""

    def __init__(self, entry):
        self.duration = entry['duration']
        self.lines = [(ln['start'], ln['end']) for ln in entry['lines']]

    def start(self, i):
        return self.lines[i][0]

    def end(self, i):
        return self.lines[i][1]

    def at(self, i, share):
        """A moment part way through line i (share 0 is its start, 1 its end)."""
        s, e = self.lines[i]
        return s + share * (e - s)


def fr(seconds):
    """The frame shown at a time in seconds (frames count from 1)."""
    return max(1, min(frames(), int(round(seconds * FPS)) + 1))


def sec(frame):
    return (frame - 1) / FPS


def every(step=1, f0=1, f1=None):
    f1 = frames() if f1 is None else f1
    out = list(range(max(1, f0), f1 + 1, step))
    if out and out[-1] != f1:
        out.append(f1)
    return out


# ---------------------------------------------------------------- materials

_materials = {}


def material(top, bottom=None, alpha=1.0, alpha_bottom=None, radial=False, power=1.6):
    """Flat emission colour, optionally a vertical or radial gradient, with alpha.

    Every material also multiplies its alpha by the object's colour (kept grey,
    so any channel works), which is how objects fade in and out.
    """
    key = (top, bottom, alpha, alpha_bottom, radial, power)
    if key in _materials:
        return _materials[key]
    m = bpy.data.materials.new(f'm{len(_materials)}')
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    n = nt.nodes.new
    out = n('ShaderNodeOutputMaterial')
    mix = n('ShaderNodeMixShader')
    clear = n('ShaderNodeBsdfTransparent')
    glow = n('ShaderNodeEmission')
    glow.inputs['Strength'].default_value = 1.0
    nt.links.new(clear.outputs[0], mix.inputs[1])
    nt.links.new(glow.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface'])

    fade = n('ShaderNodeAttribute')
    fade.attribute_type = 'OBJECT'
    fade.attribute_name = 'color'

    coords = n('ShaderNodeTexCoord')
    if radial:
        centred = n('ShaderNodeVectorMath')
        centred.operation = 'MULTIPLY_ADD'
        centred.inputs[1].default_value = (2, 2, 0)     # flat shapes: ignore depth
        centred.inputs[2].default_value = (-1, -1, 0)
        nt.links.new(coords.outputs['Generated'], centred.inputs[0])
        grad = n('ShaderNodeTexGradient')
        grad.gradient_type = 'SPHERICAL'
        nt.links.new(centred.outputs[0], grad.inputs['Vector'])
        t = grad.outputs['Fac']
    else:
        split = n('ShaderNodeSeparateXYZ')
        nt.links.new(coords.outputs['Generated'], split.inputs['Vector'])
        t = split.outputs['Y']

    if bottom is None:
        glow.inputs['Color'].default_value = lin(top)
    else:
        ramp = n('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color = lin(bottom)
        ramp.color_ramp.elements[1].color = lin(top)
        nt.links.new(t, ramp.inputs['Fac'])
        nt.links.new(ramp.outputs['Color'], glow.inputs['Color'])

    a = n('ShaderNodeMath')
    a.operation = 'MULTIPLY'
    if radial:
        shaped = n('ShaderNodeMath')
        shaped.operation = 'POWER'
        shaped.inputs[1].default_value = power
        nt.links.new(t, shaped.inputs[0])
        scaled = n('ShaderNodeMath')
        scaled.operation = 'MULTIPLY'
        scaled.inputs[1].default_value = alpha
        nt.links.new(shaped.outputs[0], scaled.inputs[0])
        nt.links.new(scaled.outputs[0], a.inputs[0])
    elif alpha_bottom is not None:
        rng = n('ShaderNodeMapRange')
        rng.inputs['To Min'].default_value = alpha_bottom
        rng.inputs['To Max'].default_value = alpha
        nt.links.new(t, rng.inputs['Value'])
        nt.links.new(rng.outputs['Result'], a.inputs[0])
    else:
        a.inputs[0].default_value = alpha
    nt.links.new(fade.outputs['Fac'], a.inputs[1])
    nt.links.new(a.outputs[0], mix.inputs['Fac'])
    # Eevee: soft glows blend over what is behind them; everything else is dithered,
    # which writes depth so that depth of field knows how far away each shape is.
    m.surface_render_method = 'BLENDED' if radial else 'DITHERED'
    _materials[key] = m
    return m


def glow_material(colour, alpha=0.5, power=1.6):
    """A soft round glow: bright in the middle, gone at the edge."""
    return material(colour, colour, alpha=alpha, radial=True, power=power)


# ---------------------------------------------------------------- shapes

_order = {}


def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def empty(name, parent=None, loc=(0, 0, 0), scale=1.0, rot=0.0):
    ob = link(bpy.data.objects.new(name, None))
    ob.parent = parent
    ob.location = loc if len(loc) == 3 else (loc[0], loc[1], next_z(parent))
    ob.scale = (scale, scale, scale)
    ob.rotation_euler = (0, 0, rot)
    return ob


def layer(name, z):
    """A depth layer. Its children use screen units at the camera's start position."""
    return empty(name, loc=(0, 0, z), scale=(H0 - z) / H0)


def next_z(parent, lift=0.0):
    """Later shapes sit a hair closer to the camera, so they draw on top."""
    if parent is None:
        return 0.0
    root = parent
    while root.parent is not None:
        root = root.parent
    _order[root.name] = _order.get(root.name, 0) + 1
    return lift + _order[root.name] * state['zstep']


def shape(name, pts, mat, parent, loc=(0, 0), smooth=False, lift=0.0, rot=0.0):
    """A filled 2D shape from points given relative to its own origin at loc."""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '2D'
    cu.fill_mode = 'BOTH'
    cu.resolution_u = 12
    sp = cu.splines.new('BEZIER')
    sp.bezier_points.add(len(pts) - 1)
    for bp, (x, y) in zip(sp.bezier_points, pts):
        bp.co = (x, y, 0)
        bp.handle_left_type = bp.handle_right_type = 'AUTO' if smooth else 'VECTOR'
    sp.use_cyclic_u = True
    cu.materials.append(mat)
    ob = link(bpy.data.objects.new(name, cu))
    ob.parent = parent
    ob.location = (loc[0], loc[1], next_z(parent, lift))
    ob.rotation_euler = (0, 0, rot)
    return ob


def circle_pts(r, rx=None, ry=None, n=40):
    rx, ry = rx or r, ry or r
    return [(rx * math.cos(2 * math.pi * i / n), ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def rrect_pts(w, h, r, n=6):
    r = min(r, w / 2, h / 2)
    if r <= 0:
        return [(w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2), (w / 2, -h / 2)]
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def bar_pts(w, h):
    """A rounded bar whose left end sits at the origin, so scaling x grows it rightward."""
    return [(x + w / 2, y) for x, y in rrect_pts(w, h, h / 2)]


def capsule_pts(length, w, n=10):
    """A rounded bar hanging down from its origin: from (0, 0) to (0, -length)."""
    r = w / 2
    pts = [(r * math.cos(math.pi * i / n), r * math.sin(math.pi * i / n)) for i in range(n + 1)]
    pts += [(r * math.cos(math.pi + math.pi * i / n), -length + r * math.sin(math.pi + math.pi * i / n)) for i in range(n + 1)]
    return pts


def arc_pts(r, w, a0, a1, n=16):
    """A curved band, such as a smile: radius r, width w, from angle a0 to a1 in degrees."""
    outer = [((r + w / 2) * math.cos(math.radians(a0 + (a1 - a0) * i / n)), (r + w / 2) * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    inner = [((r - w / 2) * math.cos(math.radians(a1 - (a1 - a0) * i / n)), (r - w / 2) * math.sin(math.radians(a1 - (a1 - a0) * i / n))) for i in range(n + 1)]
    return outer + inner


def star_pts(r_out, r_in, points=4):
    return [((r_out if i % 2 == 0 else r_in) * math.cos(math.pi * i / points + math.pi / 2),
             (r_out if i % 2 == 0 else r_in) * math.sin(math.pi * i / points + math.pi / 2)) for i in range(points * 2)]


_fonts = {}


def font(name='Figtree'):
    if name not in _fonts:
        _fonts[name] = bpy.data.fonts.load(str(ROOT / f'src/fonts/{name}.ttf'))
    return _fonts[name]


def text(name, body, size, mat, parent, loc, face='Figtree', align='CENTER'):
    cu = bpy.data.curves.new(name, 'FONT')
    cu.body = body
    cu.font = font(face)
    cu.size = size
    cu.align_x = align
    cu.align_y = 'CENTER'
    cu.materials.append(mat)
    ob = link(bpy.data.objects.new(name, cu))
    ob.parent = parent
    ob.location = (loc[0], loc[1], next_z(parent))
    return ob


# ---------------------------------------------------------------- motion

def clamp(p):
    return min(1.0, max(0.0, p))


def smooth(p):
    p = clamp(p)
    return p * p * (3 - 2 * p)


def ease_out(p):
    p = clamp(p)
    return 1 - (1 - p) ** 3


def back_out(p, s=1.9):
    """Overshoots a little and settles: for things that pop in."""
    p = clamp(p) - 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def span(t, t0, t1, ease=smooth):
    """Progress from 0 to 1 as time t (seconds) goes from t0 to t1."""
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return ease(clamp((t - t0) / (t1 - t0)))


def mix(a, b, p):
    if isinstance(a, (tuple, list)):
        return tuple(x + (y - x) * p for x, y in zip(a, b))
    return a + (b - a) * p


def key(ob, path, frame, value):
    setattr(ob, path, value)
    ob.keyframe_insert(data_path=path, frame=frame)


def alpha(ob, frame, a):
    key(ob, 'color', frame, (a, a, a, 1))


def track(ob, path, fn, step=1, f0=1, f1=None):
    """Key a property on every step-th frame from fn(seconds)."""
    for f in every(step, f0, f1):
        key(ob, path, f, fn(sec(f)))


def fade(ob, t_in=None, t_out=None, dur=0.4, step=2):
    """Fade an object in at t_in and out at t_out (seconds); either may be None."""
    def a(t):
        v = 1.0
        if t_in is not None:
            v *= span(t, t_in, t_in + dur)
        if t_out is not None:
            v *= 1 - span(t, t_out, t_out + dur)
        return v
    track(ob, 'color', lambda t: (a(t),) * 3 + (1,), step)


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


# ---------------------------------------------------------------- the stage

def backdrop(seed=3, glow=VIOLET_DEEP):
    """A deep blue field with a soft glow and faint specks at a few depths."""
    import random
    rnd = random.Random(seed)
    back = layer('back', -6.0)
    shape('sky', rrect_pts(28, 16, 0), material(INK800, INK900), back)
    shape('sky-glow', circle_pts(9.0, ry=6.5), glow_material(glow, 0.35, power=1.2), back, (0, 0.5))
    specks = []
    for i in range(70):
        z = -5.0 + rnd.random() * 5.5
        s = (H0 - z) / H0
        x, y = (-9 + rnd.random() * 18) * 1.3, (-5 + rnd.random() * 10) * 1.3
        ob = shape(f'speck{i}', circle_pts(0.03 + rnd.random() * 0.04, n=12), material(MIST, alpha=0.25 + rnd.random() * 0.4), None)
        ob.location = (x * s, y * s, z)
        specks.append((ob, rnd.random() * math.tau))
    for ob, ph in specks:
        for f in every(6):
            a = 0.6 + 0.4 * math.sin(sec(f) * 1.3 + ph)
            alpha(ob, f, a)
    return back


def motes(n=30, seed=5, colour=MINT):
    """Out-of-focus specks close to the camera, drifting slowly upward."""
    import random
    rnd = random.Random(seed)
    for i in range(n):
        z = 3.0 + rnd.random() * 9.0
        s = (H0 - z) / H0
        x, y = -9 + rnd.random() * 18, -5 + rnd.random() * 10
        ob = shape(f'mote{i}', circle_pts(0.03 + rnd.random() * 0.05, n=12), material(colour, alpha=0.25 + rnd.random() * 0.35), None)
        ph, speed = rnd.random() * math.tau, 0.05 + rnd.random() * 0.1
        for f in every(4):
            t = sec(f)
            key(ob, 'location', f, ((x + 0.2 * math.sin(t * 0.5 + ph)) * s, (y + speed * t) * s, z))


def camera(path, focus_z=1.0, fstop=0.3, step=2):
    """A camera that looks straight down the z axis.

    path(t) returns (x, y, height) at time t in seconds; focus stays on depth focus_z.
    """
    data = bpy.data.cameras.new('camera')
    data.sensor_fit = 'HORIZONTAL'
    data.sensor_width = 36
    data.lens = 36 * H0 / 16
    data.clip_start = 1.0                     # finer depth steps between stacked shapes
    data.dof.use_dof = True
    data.dof.aperture_fstop = fstop
    data.dof.focus_object = empty('focus', loc=(0, 0, focus_z))   # depth is all that counts
    cam = link(bpy.data.objects.new('camera', data))
    bpy.context.scene.camera = cam
    for f in every(step):
        key(cam, 'location', f, path(sec(f)))
    return cam


def configure(scene, out, start, end, picture):
    """Set a scene up to render frames start..end with a production's [picture] settings."""
    samples = picture['samples']
    if picture['engine'] == 'eevee':
        names = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
        scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in names else 'BLENDER_EEVEE'
        scene.eevee.taa_render_samples = samples
    else:
        scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 0
    scene.cycles.diffuse_bounces = 0
    scene.cycles.glossy_bounces = 0
    scene.cycles.transmission_bounces = 0
    scene.cycles.volume_bounces = 0
    scene.cycles.transparent_max_bounces = 24
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
    scene.render.use_persistent_data = True
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.world = bpy.data.worlds.new('world')
    scene.world.color = lin(INK900)[:3]
    scene.render.resolution_x, scene.render.resolution_y = picture['width'], picture['height']
    scene.render.resolution_percentage = 100
    scene.render.fps = picture['fps']
    scene.frame_start, scene.frame_end = start, end
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.filepath = str(Path(out).resolve() / 'frame_')


# ---------------------------------------------------------------- people

SKIN, SKIN_SHADE = '#f2c7a5', '#d9a07f'


def person(name, parent, loc=(0, 0), scale=1.0, coat='#5566c2', coat_deep=INK500, hair='#3b2a26', facing=1):
    """A simple standing figure, not anyone's likeness: coat, head, hair, eyes, and one working arm.

    The origin is at the shoulders. facing=1 looks right, -1 looks left. The
    working arm hangs at angle 0 and rotates about the shoulder toward where
    the figure faces.
    """
    root = empty(name, parent, (loc[0], loc[1], next_z(parent)), scale)
    body = empty(f'{name}-body', root, (0, 0, 0))
    shape(f'{name}-legs', [(-0.55, -2.6), (0.55, -2.6), (0.5, -4.3), (0.12, -4.3), (0, -3.0), (-0.12, -4.3), (-0.5, -4.3)], material(INK900, INK800), body)
    shape(f'{name}-coat', [(-0.75, -0.15), (-0.45, 0.08), (0, 0.13), (0.45, 0.08), (0.75, -0.15), (0.85, -1.4), (0.95, -2.8), (-0.95, -2.8), (-0.85, -1.4)],
          material(coat, coat_deep), body, smooth=True)
    shape(f'{name}-collar', [(-0.22, 0.08), (0.22, 0.08), (0, -0.5)], material(PAPER), body)
    shape(f'{name}-neck', rrect_pts(0.28, 0.34, 0.12), material(SKIN_SHADE), body, (0, 0.16))
    head = empty(f'{name}-head', body, (0.05 * facing, 0.68, next_z(body)))
    shape(f'{name}-face', circle_pts(0.44), material(SKIN, SKIN_SHADE), head)
    shape(f'{name}-ear', circle_pts(0.08), material(SKIN_SHADE), head, (-0.4 * facing, -0.02))
    shape(f'{name}-hair', [(-0.47 * facing, 0.02), (-0.44 * facing, 0.32), (-0.12 * facing, 0.52), (0.28 * facing, 0.48), (0.46 * facing, 0.2), (0.3 * facing, 0.26), (-0.2 * facing, 0.22)],
          material(hair), head, smooth=True)
    for side in (-1, 1):
        shape(f'{name}-eye{side}', circle_pts(0.045, ry=0.06), material(INK900), head, (0.1 * facing + side * 0.13, 0.0))
    shape(f'{name}-smile', arc_pts(0.1, 0.035, 210, 330), material(INK900), head, (0.1 * facing, -0.14))
    shoulder = empty(f'{name}-shoulder', body, (0.62 * facing, -0.25, next_z(body)))
    shape(f'{name}-arm', capsule_pts(1.5, 0.3), material(coat, coat_deep), shoulder)
    shape(f'{name}-hand', circle_pts(0.15), material(SKIN, SKIN_SHADE), shoulder, (0, -1.55))
    shape(f'{name}-pen', [(x, y - 1.75) for x, y in rrect_pts(0.06, 0.42, 0.03)], material(INK900), shoulder)
    return {'root': root, 'body': body, 'head': head, 'arm': shoulder, 'facing': facing}


# ---------------------------------------------------------------- families of programs

def pop(ob, t, s=1.0, dur=0.45, t_out=None, out_dur=0.3):
    """Scale an object up from nothing at t, overshooting a little, and back to nothing at t_out."""
    tiny = (0.001, 0.001, 0.001)
    key(ob, 'scale', 1, tiny)
    for f in every(1, fr(t), fr(t + dur)):
        v = max(0.001, s * back_out((sec(f) - t) / dur))
        key(ob, 'scale', f, (v, v, v))
    if t_out is not None:
        key(ob, 'scale', fr(t_out), (s, s, s))
        key(ob, 'scale', fr(t_out + out_dur), tiny)


def appear(ob, t_in=None, t_out=None, dur=0.3, a=1.0):
    """Fade a shape in at t_in and out at t_out, keying only around those moments."""
    alpha(ob, 1, 0.0 if t_in is not None else a)
    if t_in is not None:
        alpha(ob, fr(t_in), 0.0)
        alpha(ob, fr(t_in + dur), a)
    if t_out is not None:
        alpha(ob, fr(t_out), a)
        alpha(ob, fr(t_out + dur), 0.0)


def branch(name, parent, a, b, colour=MIST, w=0.07, opacity=0.55):
    """A straight line from point a to point b. It grows out of a when its x scale goes from 0 to 1."""
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    return shape(name, bar_pts(length, w), material(colour, alpha=opacity), parent, a,
                 rot=math.atan2(b[1] - a[1], b[0] - a[0]))


def grow(ob, t, dur=0.35, t_out=None):
    """Grow a branch out from its start at t (and pull it back in at t_out)."""
    key(ob, 'scale', 1, (0.001, 1, 1))
    key(ob, 'scale', fr(t), (0.001, 1, 1))
    key(ob, 'scale', fr(t + dur), (1, 1, 1))
    if t_out is not None:
        key(ob, 'scale', fr(t_out), (1, 1, 1))
        key(ob, 'scale', fr(t_out + dur), (0.001, 1, 1))


def tag(name, parent, loc, label, colour=PAPER, size=0.26):
    """A score: a number on a small dark pill. Pop its root in to show it."""
    root = empty(name, parent, (loc[0], loc[1], next_z(parent)))
    w = 0.3 + 0.62 * size * len(label)
    pill = shape(f'{name}-pill', rrect_pts(w, size * 1.6, size * 0.8), material(INK900, alpha=0.8), root)
    body = text(f'{name}-text', label, size, material(colour), root, (0, -size * 0.04), face='JetBrainsMono')
    root.scale = (0.001, 0.001, 0.001)
    return {'root': root, 'pill': pill, 'text': body}


def ring(name, parent, loc, r=0.6, colour=AMBER, w=0.08, lift=0.0):
    """A thin circle, hidden at first; light it with flash or appear."""
    ob = shape(name, arc_pts(r, w, 0, 360, n=48), material(colour), parent, loc, lift=lift)
    alpha(ob, 1, 0.0)
    return ob


def flash(ob, t, dur=0.9, grow_by=0.5):
    """Light a ring at t: it swells a little and fades out over dur seconds."""
    for f in every(1, fr(t), fr(t + dur)):
        q = span(sec(f), t, t + dur, lambda v: v)
        s = 1 + grow_by * q
        key(ob, 'scale', f, (s, s, 1))
        alpha(ob, f, math.sin(math.pi * q))


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


def veil(t, dur=1.0, colour=INK900):
    """A sheet in front of everything that fades in at t: the scene's fade to dark."""
    front = layer('veil', 12.5)
    ob = shape('veil-sheet', rrect_pts(30, 18, 0), material(colour), front)
    appear(ob, t, None, dur)
    return ob


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


def screen_stand(name, parent, loc, w=5.6, h=3.6):
    """A large computer screen on a stand. Returns the root and the dark screen face."""
    root = empty(name, parent, (loc[0], loc[1], next_z(parent)))
    shape(f'{name}-foot', rrect_pts(2.4, 0.22, 0.11), material(INK600, INK700), root, (0, -h / 2 - 1.05))
    shape(f'{name}-neck', [(-0.3, -h / 2 + 0.1), (0.3, -h / 2 + 0.1), (0.45, -h / 2 - 1.0), (-0.45, -h / 2 - 1.0)], material(INK600, INK700), root)
    shape(f'{name}-shadow', rrect_pts(w + 0.6, h + 0.6, 0.5), glow_material(INK900, 0.7, power=0.8), root, (0.15, -0.2))
    shape(f'{name}-frame', rrect_pts(w, h, 0.25), material(INK500, INK600), root)
    face = shape(f'{name}-face', rrect_pts(w - 0.36, h - 0.36, 0.14), material('#16205a', INK900), root)
    return {'root': root, 'face': face}
