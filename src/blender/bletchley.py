"""Test shot in Blender: I. J. Good and Alan Turing at Bletchley Park, 1941.

    blender -b --factory-startup -P src/blender/bletchley.py -- \
        --root . --out out/shot/frames --start 1 --end 450

Builds the shot from flat 2D shapes set out in depth (wall, people, desk,
foreground), so a moving camera gives parallax and depth of field blurs what
is near and far. Every surface is an emission shader, so colours come out
exactly as written and no lights are needed. Renders frames start..end as PNG.
"""
import argparse
import math
import random
import sys
from pathlib import Path

import bpy

FPS = 30
FRAMES = 450                # 15 seconds
H0 = 20.0                   # camera height at the start; design units are screen units at z = 0
FOCUS_Z = 1.9               # depth of the people, kept in focus

# Colours (sRGB hex), shared with the film's palette where they overlap.
INK900, INK800, INK700, INK600, INK500 = '#0b1030', '#121a47', '#1b2660', '#27347d', '#3a4aa3'
AMBER, AMBER_DEEP, PAPER, MIST, CORAL = '#ffc24b', '#f09a1f', '#f4f1ff', '#b9c0ea', '#ff6b6b'
MINT_DEEP, VIOLET_DEEP, CORAL_DEEP = '#1fae93', '#7357e0', '#d9434f'
CREAM, SKIN, SKIN_SHADE = '#f3e9d2', '#f2c7a5', '#d9a07f'


def args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path('.'))
    ap.add_argument('--out', type=Path, default=Path('out/shot/frames'))
    ap.add_argument('--start', type=int, default=1)
    ap.add_argument('--end', type=int, default=FRAMES)
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    return ap.parse_args(argv)


def lin(hex_colour, a=1.0):
    """sRGB hex to the linear RGBA that Blender's shader nodes expect."""
    h = hex_colour.lstrip('#')
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, a)


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
        centred.inputs[1].default_value = (2, 2, 2)
        centred.inputs[2].default_value = (-1, -1, -1)
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
        span = n('ShaderNodeMapRange')
        span.inputs['To Min'].default_value = alpha_bottom
        span.inputs['To Max'].default_value = alpha
        nt.links.new(t, span.inputs['Value'])
        nt.links.new(span.outputs['Result'], a.inputs[0])
    else:
        a.inputs[0].default_value = alpha
    nt.links.new(fade.outputs['Fac'], a.inputs[1])
    nt.links.new(a.outputs[0], mix.inputs['Fac'])
    _materials[key] = m
    return m


# ---------------------------------------------------------------- shapes

_order = {}


def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def empty(name, parent=None, loc=(0, 0, 0), scale=1.0, rot=0.0):
    ob = link(bpy.data.objects.new(name, None))
    ob.parent = parent
    ob.location = loc
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
    return lift + _order[root.name] * 0.004


def shape(name, pts, mat, parent, loc=(0, 0), smooth=False, lift=0.0, rot=0.0):
    """A filled 2D shape from points given relative to its own origin at loc."""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '2D'
    cu.fill_mode = 'BOTH'
    cu.resolution_u = 16
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


def circle_pts(r, rx=None, ry=None, n=48):
    rx, ry = rx or r, ry or r
    return [(rx * math.cos(2 * math.pi * i / n), ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def rrect_pts(w, h, r, n=8):
    r = min(r, w / 2, h / 2)
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def capsule_pts(length, w, n=10):
    """A rounded bar hanging down from its origin: from (0, 0) to (0, -length)."""
    r = w / 2
    pts = [(r * math.cos(math.pi * i / n), r * math.sin(math.pi * i / n)) for i in range(n + 1)]
    pts += [(r * math.cos(math.pi + math.pi * i / n), -length + r * math.sin(math.pi + math.pi * i / n)) for i in range(n + 1)]
    return pts


def text(name, body, size, mat, parent, loc, font, align='LEFT'):
    cu = bpy.data.curves.new(name, 'FONT')
    cu.body = body
    cu.font = font
    cu.size = size
    cu.align_x = align
    cu.materials.append(mat)
    ob = link(bpy.data.objects.new(name, cu))
    ob.parent = parent
    ob.location = (loc[0], loc[1], next_z(parent))
    return ob


# ---------------------------------------------------------------- animation

def smooth(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def span(f, f0, f1):
    return smooth((f - f0) / (f1 - f0))


def key(ob, path, frame, value):
    setattr(ob, path, value)
    ob.keyframe_insert(data_path=path, frame=frame)


def fade(ob, f0, f1, a0=0.0, a1=1.0):
    for f, a in ((1, a0), (f0, a0), (f1, a1)):
        key(ob, 'color', f, (a, a, a, 1))


def every(step=2):
    return range(1, FRAMES + 1, step)


# ---------------------------------------------------------------- people

def person(name, parent, loc, jacket, jacket_lit, hair, hair_pts, tie=None, rot=0.0, scale=1.0):
    """A simple round figure: body, head, hair, eyes, and two two-part arms.

    The origin is the top of the shoulders. Arms hang straight down at angle 0;
    each arm is (shoulder pivot, elbow pivot).
    """
    root = empty(name, parent, (loc[0], loc[1], 0), scale, rot)
    body = shape(f'{name}-body', [(-0.8, -0.18), (-0.55, 0.06), (0, 0.12), (0.55, 0.06), (0.8, -0.18), (0.86, -1.3), (0.9, -2.7), (-0.9, -2.7), (-0.86, -1.3)],
                 material(jacket_lit, jacket), root, smooth=True)
    shape(f'{name}-neck', rrect_pts(0.3, 0.34, 0.12), material(SKIN_SHADE), root, (0, 0.14))
    shape(f'{name}-shirt', [(-0.24, 0.08), (0.24, 0.08), (0, -0.58)], material('#e8e4f5'), root)
    if tie:
        shape(f'{name}-tie', [(-0.06, 0.02), (0.06, 0.02), (0.1, -0.48), (0, -0.6), (-0.1, -0.48)], material(tie), root)
    head = empty(f'{name}-head', root, (0, 0.66, next_z(root)))
    shape(f'{name}-face', circle_pts(0.46), material(SKIN, SKIN_SHADE), head)
    shape(f'{name}-ear', circle_pts(0.09), material(SKIN_SHADE), head, (-0.44, -0.02))
    shape(f'{name}-hair', hair_pts, material(hair), head, smooth=True)
    for side in (-1, 1):
        shape(f'{name}-cheek{side}', circle_pts(0.07), material(CORAL, alpha=0.35), head, (side * 0.24, -0.16))
    eyes = empty(f'{name}-eyes', head, (0, -0.02, next_z(root)))
    for side in (-1, 1):
        shape(f'{name}-eye{side}', circle_pts(0.05, ry=0.06), material(INK900), eyes, (side * 0.15, 0))

    def arm(side):
        shoulder = empty(f'{name}-shoulder{side}', root, (side * 0.66, -0.26, 1.0))
        shape(f'{name}-upper{side}', capsule_pts(0.95, 0.34), material(jacket_lit, jacket), shoulder)
        elbow = empty(f'{name}-elbow{side}', shoulder, (0, -0.95, 0))
        shape(f'{name}-fore{side}', capsule_pts(0.85, 0.3), material(jacket_lit, jacket), elbow)
        shape(f'{name}-hand{side}', circle_pts(0.15), material(SKIN, SKIN_SHADE), elbow, (0, -0.88))
        return shoulder, elbow

    return {'root': root, 'body': body, 'head': head, 'eyes': eyes, 'left': arm(-1), 'right': arm(1)}


def pose(arm, frame, upper_deg, fore_deg):
    shoulder, elbow = arm
    key(shoulder, 'rotation_euler', frame, (0, 0, math.radians(upper_deg)))
    key(elbow, 'rotation_euler', frame, (0, 0, math.radians(fore_deg)))


def blink(p, frames):
    for f0 in frames:
        for f, s in ((f0 - 3, 1.0), (f0, 0.1), (f0 + 3, 1.0)):
            key(p['eyes'], 'scale', f, (1, s, 1))


def look(p, frame, dx, dy=0.0):
    key(p['eyes'], 'location', frame, (dx, -0.02 + dy, p['eyes'].location.z))


# ---------------------------------------------------------------- the shot

def build(root):
    random.seed(7)
    font = bpy.data.fonts.load(str((root / 'src/scenes/fonts/Figtree.ttf').resolve()))

    # -- the back wall of the hut, at night
    wall = layer('wall', 0.0)
    shape('wall', rrect_pts(19, 11, 0), material(INK700, INK800), wall)
    for i in range(16):
        y = -4.6 + i * 0.68
        shape(f'plank{i}', rrect_pts(19, 0.05, 0), material(INK900, alpha=0.35), wall, (0, y))
    pool = shape('lamp-pool', circle_pts(5.2), material(AMBER, AMBER_DEEP, alpha=0.30, radial=True), wall, (0.9, 0.2))

    # window with blackout curtain, moon, and stars
    shape('window-frame', rrect_pts(3.4, 2.6, 0.12), material('#2a2050'), wall, (4.6, 1.9))
    shape('window-sky', rrect_pts(3.0, 2.2, 0.06), material('#22307a', INK900), wall, (4.6, 1.9))
    stars = []
    for i in range(20):
        x, y = 3.2 + random.random() * 2.8, 0.9 + random.random() * 2.0
        stars.append(shape(f'star{i}', circle_pts(0.025 + random.random() * 0.025), material(PAPER), wall, (x, y)))
    shape('moon-glow', circle_pts(0.9), material(PAPER, MIST, alpha=0.35, radial=True), wall, (5.35, 2.5))
    shape('moon', circle_pts(0.28), material(PAPER, MIST), wall, (5.35, 2.5))
    shape('mullion', rrect_pts(0.1, 2.2, 0), material('#2a2050'), wall, (4.6, 1.9))
    shape('transom', rrect_pts(3.0, 0.1, 0), material('#2a2050'), wall, (4.6, 1.9))
    shape('curtain', [(-0.15, 1.45), (1.25, 1.45), (1.1, 0.3), (1.3, -0.8), (0.95, -1.5), (-0.15, -1.5)], material('#3a2660', '#24173f'), wall, (2.9, 1.9), smooth=True)

    # cork board of intercepted messages
    shape('board-frame', rrect_pts(3.5, 2.5, 0.1), material('#4a2f3a'), wall, (-4.8, 1.7))
    shape('board', rrect_pts(3.2, 2.2, 0.06), material('#9a6448', '#7a4e3a'), wall, (-4.8, 1.7))
    for i, (x, y, r) in enumerate(((-5.8, 2.0, 4), (-4.7, 1.9, -3), (-3.75, 2.1, 6), (-5.3, 1.05, -5), (-4.1, 1.15, 2))):
        sheet = empty(f'sheet{i}', wall, (x, y, next_z(wall)), rot=math.radians(r))
        shape(f'sheet{i}-paper', rrect_pts(0.85, 0.75, 0.03), material(CREAM, '#ddd0b4'), sheet)
        for row in range(4):
            for g in range(3):
                shape(f'sheet{i}-r{row}g{g}', rrect_pts(0.18, 0.06, 0.03), material(INK600, alpha=0.6), sheet, (-0.25 + g * 0.25, 0.22 - row * 0.14))
        shape(f'sheet{i}-pin', circle_pts(0.05), material([CORAL, AMBER, MINT_DEEP][i % 3]), sheet, (0, 0.3))

    # clock, with a ticking second hand
    shape('clock-rim', circle_pts(0.5), material(INK600), wall, (0.3, 3.35))
    shape('clock-face', circle_pts(0.42), material(CREAM, '#ddd0b4'), wall, (0.3, 3.35))
    minute = empty('minute', wall, (0.3, 3.35, next_z(wall)))
    shape('minute-hand', capsule_pts(0.32, 0.05), material(INK900), minute, rot=math.pi)
    second = empty('second', wall, (0.3, 3.35, next_z(wall)))
    shape('second-hand', capsule_pts(0.36, 0.025), material(CORAL_DEEP), second, rot=math.pi)

    # caption
    words = layer('words', 2.0)
    title = text('title', 'Bletchley Park, 1941', 0.42, material(PAPER), words, (-7.4, 3.75), font)
    sub = text('subtitle', 'Hut 8: reading the German navy’s coded messages', 0.25, material(MIST), words, (-7.4, 3.3), font)

    # -- the people, behind the desk
    people = layer('people', 1.6)
    turing = person('turing', people, (-2.7, 0.25), '#7a5236', '#a8714a', '#3b2a26',
                    [(-0.5, 0.0), (-0.44, 0.36), (-0.1, 0.56), (0.32, 0.5), (0.5, 0.18), (0.46, 0.02), (0.22, 0.3), (-0.3, 0.26)], rot=-0.1)
    good = person('good', people, (3.0, -0.45), INK500, '#5566c2', '#1e1630',
                  [(-0.5, 0.02), (-0.46, 0.34), (-0.14, 0.56), (0.3, 0.52), (0.5, 0.22), (0.48, 0.04), (0.1, 0.28), (-0.36, 0.22)], tie=CORAL_DEEP, rot=0.07)
    turing_name = text('turing-name', 'Alan Turing', 0.3, material(PAPER), people, (-2.6, 1.75), font, align='CENTER')
    good_name = text('good-name', 'I. J. Good', 0.3, material(PAPER), people, (3.0, 1.05), font, align='CENTER')
    pen = shape('pen', rrect_pts(0.05, 0.36, 0.02), material(INK900), good['left'][1], (0.05, -0.95), rot=-0.5)

    # -- the desk and what is on it
    desk = layer('desk', 2.1)
    shape('desk-top', [(-7.6, -2.35), (7.6, -2.35), (6.7, -1.5), (-6.7, -1.5)], material('#7a4a5e', '#4c2f5c'), desk)
    shape('desk-pool', circle_pts(3.4, ry=1.0), material(AMBER, AMBER_DEEP, alpha=0.45, radial=True), desk, (0.7, -1.95))
    shape('paper1', [(-1.35, -2.25), (0.25, -2.2), (0.35, -1.68), (-1.05, -1.72)], material(CREAM, '#e6d8b8'), desk)
    for row in range(3):
        for g in range(4):
            shape(f'paper1-r{row}g{g}', rrect_pts(0.24, 0.05, 0.025), material(INK600, alpha=0.6), desk, (-0.95 + g * 0.33, -1.83 - row * 0.12))
    shape('paper2', [(-2.3, -2.28), (-1.1, -2.3), (-1.0, -1.85), (-2.05, -1.8)], material('#e9dfc6', '#d6c7a6'), desk)
    shape('notebook', [(2.0, -2.27), (3.45, -2.27), (3.32, -1.76), (2.1, -1.76)], material(PAPER, '#dcd6ee'), desk)
    ink = shape('ink-line', rrect_pts(1.0, 0.04, 0.02), material(INK600), desk, (2.25, -2.0))
    # teacup and steam
    shape('saucer', circle_pts(0.45, ry=0.1), material('#e8e4f5', MIST), desk, (-3.8, -1.98))
    shape('cup', [(-0.3, 0.32), (0.3, 0.32), (0.22, -0.02), (-0.22, -0.02)], material('#f4f1ff', MIST), desk, (-3.8, -1.95))
    shape('cup-handle', circle_pts(0.12), material(MIST), desk, (-3.47, -1.8))
    steam = [shape(f'steam{i}', [(0, 0), (0.08, 0.2), (-0.04, 0.42), (0.06, 0.62), (0.02, 0.64), (-0.08, 0.42), (0.04, 0.2), (-0.04, 0.0)],
                   material(PAPER, alpha=0.35), desk, (-3.9 + i * 0.1, -1.55), smooth=True) for i in range(3)]
    # books
    for i, (w, c) in enumerate(((1.5, VIOLET_DEEP), (1.3, CORAL_DEEP), (1.6, INK500))):
        shape(f'book{i}', rrect_pts(w, 0.22, 0.05), material(c), desk, (5.9, -1.85 + i * 0.23))
    # the lamp, its glow, and the cone of light
    shape('lamp-base', circle_pts(0.5, ry=0.14), material('#178a73', '#0f5e50'), desk, (1.75, -1.82))
    shape('lamp-stem', capsule_pts(2.25, 0.12), material('#178a73'), desk, (1.75, -1.75), rot=math.radians(186))
    cone = shape('lamp-cone', [(0.45, 0.5), (1.2, 0.26), (2.7, -1.92), (-1.5, -1.92)], material(AMBER, AMBER, alpha=0.26, alpha_bottom=0.05), desk)
    shape('lamp-shade', [(0.3, 0.6), (0.68, 0.95), (1.25, 1.02), (1.6, 0.74), (1.25, 0.28), (0.55, 0.36)], material(MINT_DEEP, '#0f5e50'), desk, smooth=True)
    glows = [shape('bulb-halo', circle_pts(1.4), material(AMBER, AMBER_DEEP, alpha=0.6, radial=True), desk, (0.85, 0.42)),
             shape('bulb-halo-wide', circle_pts(3.2), material(AMBER, AMBER_DEEP, alpha=0.2, radial=True), desk, (0.85, 0.42))]
    shape('bulb', circle_pts(0.13), material('#fff6d8'), desk, (0.85, 0.42))
    shape('desk-front', rrect_pts(15.4, 3.2, 0), material('#33224d', '#24183c'), layer('desk-front', 2.8), (0, -3.95))

    # -- out-of-focus foreground
    near = layer('near', 12.0)
    shape('chair', rrect_pts(3.4, 4.2, 0.7), material('#0d1237'), near, (-7.4, -3.4))
    shape('typewriter', rrect_pts(3.8, 2.2, 0.5), material('#0d1237'), near, (7.6, -4.1))

    # -- dust in the lamp light, at many depths
    motes = []
    for i in range(46):
        z = 2.4 + random.random() * 6.5
        s = (H0 - z) / H0
        x, y = -2.5 + random.random() * 5.5, -1.6 + random.random() * 3.6
        ob = shape(f'mote{i}', circle_pts(0.03 + random.random() * 0.035, n=16), material('#fff1c9', alpha=0.5 + random.random() * 0.4), None)
        ob.location = (x * s, y * s, z)
        motes.append((ob, x * s, y * s, z, random.random() * math.tau, 0.1 + random.random() * 0.15))

    # ------------------------------------------------------------ motion
    cam_data = bpy.data.cameras.new('camera')
    cam_data.sensor_fit = 'HORIZONTAL'
    cam_data.sensor_width = 36
    cam_data.lens = 36 * H0 / 16
    cam_data.dof.use_dof = True
    cam_data.dof.aperture_fstop = 0.06
    cam = link(bpy.data.objects.new('camera', cam_data))
    bpy.context.scene.camera = cam
    for f in every(3):
        p = smooth((f - 1) / (FRAMES - 1))
        z = H0 - 1.5 * p
        key(cam, 'location', f, (-0.35 + 0.7 * p, -0.1 + 0.25 * p, z))
        cam_data.dof.focus_distance = z - FOCUS_Z
        cam_data.dof.keyframe_insert('focus_distance', frame=f)

    fade(title, 15, 40)
    fade(sub, 35, 60)
    fade(turing_name, 75, 100)
    fade(good_name, 140, 165)

    # Turing: arm hangs, rises to point at the message, taps it twice, then turns to Good
    pose(turing['right'], 1, 6, 4)
    pose(turing['right'], 60, 6, 4)
    pose(turing['right'], 95, 36, 12)
    for k, f in enumerate((120, 128, 136, 144)):
        pose(turing['right'], f, 36 + (2 if k % 2 == 0 else 0), 12 + (8 if k % 2 == 0 else 0))
    pose(turing['right'], 450, 38, 14)
    pose(turing['left'], 1, -8, -4)
    for f in every(6):
        key(turing['root'], 'rotation_euler', f, (0, 0, -0.1 + 0.015 * math.sin(f / 40)))
        key(turing['body'], 'scale', f, (1, 1 + 0.012 * math.sin(f / 22), 1))
        key(good['body'], 'scale', f, (1, 1 + 0.012 * math.sin(f / 25 + 1), 1))
    look(turing, 1, 0.05, -0.03)
    look(turing, 215, 0.05, -0.03)
    look(turing, 230, 0.1, 0.0)
    key(turing['head'], 'rotation_euler', 215, (0, 0, 0))
    key(turing['head'], 'rotation_euler', 235, (0, 0, -0.08))
    blink(turing, (110, 290, 410))

    # Good: writes, looks up at Turing, then goes back to writing
    for f in every(2):
        writing = 1.0 if f < 200 or f > 340 else 0.0
        w = writing * math.sin(f * 0.6)
        pose(good['left'], f, -20 + 2 * w, 95 + 5 * w)
    pose(good['right'], 1, 18, -62)
    look(good, 1, -0.04, -0.05)
    look(good, 200, -0.04, -0.05)
    look(good, 215, -0.12, 0.02)
    look(good, 335, -0.12, 0.02)
    look(good, 350, -0.04, -0.05)
    key(good['head'], 'rotation_euler', 200, (0, 0, 0))
    key(good['head'], 'rotation_euler', 218, (0, 0, 0.09))
    key(good['head'], 'rotation_euler', 335, (0, 0, 0.09))
    key(good['head'], 'rotation_euler', 352, (0, 0, 0))
    blink(good, (60, 250, 380))
    for f in every(3):
        done = 0.15 + 0.85 * (0.6 * span(f, 1, 200) + 0.4 * span(f, 340, 450))
        key(ink, 'scale', f, (done, 1, 1))
        key(ink, 'location', f, (2.25 - 0.5 * (1 - done), -2.0, ink.location.z))

    # the room: clock, lamp flicker, stars, steam, dust
    for f in every(30):  # one tick a second: hold, then jump in one frame
        angle = (0, 0, -math.radians(6 * (f // 30)))
        key(second, 'rotation_euler', f, angle)
        key(second, 'rotation_euler', f + 29, angle)
    key(minute, 'rotation_euler', 1, (0, 0, -math.radians(130)))
    key(minute, 'rotation_euler', FRAMES, (0, 0, -math.radians(131.5)))
    for f in every(4):
        flicker = 1 + 0.05 * math.sin(f * 1.7) * math.sin(f * 0.31)
        for ob in glows + [pool, cone]:
            key(ob, 'color', f, (flicker, flicker, flicker, 1))
    for i, st in enumerate(stars):
        for f in every(6):
            a = 0.55 + 0.45 * math.sin(f / 18 + i * 1.3)
            key(st, 'color', f, (a, a, a, 1))
    for i, st in enumerate(steam):
        x0, y0, z0 = st.location
        for f in every(2):
            p = ((f / FPS) / 2.6 + i / 3) % 1
            key(st, 'location', f, (x0 + 0.08 * math.sin(p * 5 + i), y0 + 0.7 * p, z0))
            a = math.sin(math.pi * p)
            key(st, 'color', f, (a, a, a, 1))
    for ob, x, y, z, ph, speed in motes:
        for f in every(3):
            t = f / FPS
            key(ob, 'location', f, (x + 0.15 * math.sin(t * 0.7 + ph), y + speed * t - 0.25, z))
            a = 0.5 + 0.5 * math.sin(t * 1.9 + ph)
            key(ob, 'color', f, (a, a, a, 1))


def configure(scene, out, start, end):
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 64
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 4
    scene.cycles.diffuse_bounces = 0
    scene.cycles.glossy_bounces = 0
    scene.cycles.transmission_bounces = 0
    scene.cycles.volume_bounces = 0
    scene.cycles.transparent_max_bounces = 64
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.world = bpy.data.worlds.new('world')
    scene.world.color = lin(INK900)[:3]
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = start, end
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.filepath = str(out.resolve() / 'frame_')


def main():
    a = args()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    a.out.mkdir(parents=True, exist_ok=True)
    build(a.root)
    configure(bpy.context.scene, a.out, a.start, a.end)
    bpy.ops.render.render(animation=True)


main()
