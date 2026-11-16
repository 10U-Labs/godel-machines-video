"""The cast, the sets, and the colours of the Ultron film, built from the shared kit.

Ultron in his three forms: a program with no body, drawn as a pair of eyes in
a glow; a feeble robot; and a powerful one. They are original designs, and
copy nothing of Marvel's. With them: the people of the story, the labs, the
machines that build a body, a program drawn as a page of its code, and the
moves the scenes share.

The film's colours are steel greys and reds on near-black, with a cold blue
for the computer scientist's study and for a program that is not Ultron.
"""
import math
import random

import kit
from kit import (
    alpha, arc_pts, bar_pts, capsule_pts, circle_pts, empty, every, fr, glow_material, key, layer, material,
    mix, next_z, rrect_pts, sec, shape, span,
)

NIGHT900, NIGHT800, NIGHT700, NIGHT600, NIGHT500 = '#07070b', '#0d0e14', '#15161e', '#1f212b', '#2c2f3b'
STEEL100, STEEL300, STEEL500, STEEL700, STEEL800 = '#d7dce4', '#a4acb9', '#707888', '#474d59', '#30353f'
RED, RED_DEEP, BLOOD, HOT = '#ff3d3d', '#b3161f', '#4a0d14', '#ffd9d2'
ICE, ICE_DEEP, FROST = '#9fdcec', '#4a9fb5', '#e6f8fc'
BONE, ASH = '#efe9df', '#8b8e99'
RUST, RUST_DEEP = '#8a5a44', '#5c3a2c'

FLOOR = -2.7        # the height feet stand at, in screen units
SOFT = 2.6          # how fast a wide pool of light falls away from its middle

# The kit sets each new shape a little closer to the camera than the last, and
# a scene of this film has hundreds of shapes. At the kit's own step the last
# of them would stand far enough forward to look bigger than they are drawn,
# and lower than the floor they stand on. A smaller step keeps them in place.
kit.state['zstep'] = 0.0008
TINY = (0.001, 0.001, 0.001)


def scene_end():
    return sec(kit.frames())


_depth = {}


def group(name, parent, loc=(0, 0), scale=1.0):
    """An empty to hang shapes from, set at the depth that keeps its shapes in the order they are made.

    The kit sets each new shape a hair closer to the camera than the one made
    before it, counted in its parent's units. Hung from a parent that is set
    forward too, a shape would be set forward twice, and under a small parent
    its step would shrink with it. So a group is set forward by only what its
    own scale takes from its shapes' steps, which at full size is nothing.
    """
    step = next_z(parent)
    _depth[name] = step
    return empty(name, parent, (loc[0], loc[1], step * (1 - scale)), scale)


def move_in(p, t, a, b, s0, s1, dur=0.6):
    """Send a program with no body from point a to point b, changing its size from s0 to s1 on the way.

    It is how Ultron goes into a body: he shrinks to fit its head. His depth
    is corrected as he shrinks, so he stays in front of what was made before
    him.
    """
    root = p['root']
    step = _depth[root.name]
    last = fr(t + dur)
    for f in every(1, fr(t), last):
        q = 1.0 if f == last else span(sec(f), t, t + dur)
        size = mix(s0, s1, q)
        key(root, 'location', f, (mix(a[0], b[0], q), mix(a[1], b[1], q), step * (1 - size)))
        key(root, 'scale', f, (size, size, size))


def glow(name, parent, loc=(0, 0), r=0.5, colour=RED, a=0.75, lift=0.0):
    """A round light with no edge: brightest in the middle, and a tenth as bright at distance r.

    The kit's glow fades with the distance from a shape's middle, and counts
    that distance against the shape's size with 1 more added on every side:
    a curve's texture space reaches out to the radius of its points, which is
    1. A small round shape has hardly faded where it ends, and shows as a
    disc. So this light is drawn three times as wide as r, and it fades fast
    enough to be at nothing where the shape ends.
    """
    wide = 3 * r
    power = math.log(0.1) / math.log(1 - r / (wide + 1))
    return shape(name, circle_pts(wide), glow_material(colour, a, power=power), parent, loc, lift=lift)


# ---------------------------------------------------------------- the stage

def backdrop(seed=3, glow=RED_DEEP, strength=0.3):
    """A near-black field with a soft glow and faint specks at a few depths. Returns the back layer."""
    rnd = random.Random(seed)
    back = layer('back', -6.0)
    shape('sky', rrect_pts(30, 17, 0), material(NIGHT800, NIGHT900), back)
    shape('sky-glow', circle_pts(11.0, ry=7.5), glow_material(glow, strength, power=SOFT), back, (0, 0.5))
    for i in range(45):
        z = -5.0 + rnd.random() * 5.5
        s = (kit.H0 - z) / kit.H0
        x, y = (-9 + rnd.random() * 18) * 1.3, (-5 + rnd.random() * 10) * 1.3
        ob = shape(f'speck{i}', circle_pts(0.03 + rnd.random() * 0.04, n=12), material(ASH, alpha=0.2 + rnd.random() * 0.3), None)
        ob.location = (x * s, y * s, z)
        ph = rnd.random() * math.tau
        for f in every(6):
            alpha(ob, f, 0.6 + 0.4 * math.sin(sec(f) * 1.3 + ph))
    return back


def room(name, far, stage, lamps=(-4.6, 0.0, 4.6), light=STEEL300, glow=0.07):
    """A lab at night: wall panels and hanging lamps behind, and a floor to stand on.

    Returns the two roots that hold it, one on each layer, so that a scene can
    show and hide the whole room with cut.
    """
    behind = empty(f'{name}-far', far)
    front = empty(f'{name}-near', stage)
    for i in range(8):
        x = -11.55 + i * 3.3
        shape(f'{name}-panel{i}', rrect_pts(3.0, 5.8, 0.12), material(NIGHT600, NIGHT700), behind, (x, 1.0))
        shape(f'{name}-seam{i}', rrect_pts(2.6, 0.05, 0), material(STEEL800, alpha=0.7), behind, (x, 2.4))
    shape(f'{name}-rail', rrect_pts(30, 0.14, 0), material(STEEL800), behind, (0, 4.05))
    for i, x in enumerate(lamps):
        shape(f'{name}-lamp-light{i}', circle_pts(3.0, ry=4.2), glow_material(light, glow, power=SOFT), behind, (x, 1.6))
        shape(f'{name}-lamp{i}', rrect_pts(0.9, 0.16, 0.08), material(STEEL700), behind, (x, 3.95))
    shape(f'{name}-floor', rrect_pts(30, 3.2, 0), material(NIGHT600, NIGHT800), front, (0, FLOOR - 1.6))
    shape(f'{name}-floor-edge', rrect_pts(30, 0.05, 0), material(STEEL700, alpha=0.8), front, (0, FLOOR))
    return [behind, front]


def cut(roots, t_in=None, t_out=None):
    """Show what hangs from each root from t_in to t_out, and at no other time. A hidden root is shrunk to nothing."""
    for root in roots:
        full = tuple(root.scale)
        gone = tuple(v * 1e-5 for v in full)
        key(root, 'scale', 1, gone if t_in is not None else full)
        if t_in is not None:
            key(root, 'scale', max(1, fr(t_in) - 1), gone)
            key(root, 'scale', fr(t_in), full)
        if t_out is not None:
            key(root, 'scale', max(1, fr(t_out) - 1), full)
            key(root, 'scale', fr(t_out), gone)


def dip(times, dur=0.35, colour=NIGHT900):
    """Go dark for a moment at each of the times: a sheet in front of everything fades in and out again.

    The dark lasts through the frame before each time and the frame after it,
    so that what a scene changes at that time, with cut or with a jump of the
    camera, is not seen changing.
    """
    front = layer('dip', 12.4)
    sheet = shape('dip-sheet', rrect_pts(30, 18, 0), material(colour), front)
    alpha(sheet, 1, 0.0)
    for t in times:
        f = fr(t)
        alpha(sheet, max(1, min(f - 2, fr(t - dur))), 0.0)
        alpha(sheet, max(1, f - 1), 1.0)
        alpha(sheet, f + 1, 1.0)
        alpha(sheet, max(f + 2, fr(t + dur)), 0.0)
    return sheet


# ---------------------------------------------------------------- eyes, and a program with no body

def eyes(name, parent, loc=(0, 0), scale=1.0, colour=RED, hot=HOT, slant=True, gap=0.3):
    """A pair of glowing eyes. Ultron's slant inward; a round pair is for other programs."""
    root = group(name, parent, loc, scale)
    pair, shapes = [], []
    for side in (-1, 1):
        e = group(f'{name}-eye{side}', root, (side * gap, 0))
        shapes.append(glow(f'{name}-glow{side}', e, (0, 0), 0.7, colour, 0.9))
        pair.append(e)
    # Both lights are made before either lens, so that neither light lies over the other eye's lens.
    for side, e in zip((-1, 1), pair):
        if slant:
            pts = [(-0.2 * side, -0.03), (-0.03 * side, 0.1), (0.22 * side, 0.09), (0.05 * side, -0.08)]
        else:
            pts = circle_pts(0.12, ry=0.15, n=20)
        shapes.append(shape(f'{name}-lens{side}', pts, material(hot, colour), e, smooth=slant))
    return {'root': root, 'pair': pair, 'shapes': shapes, 'home': (loc[0], loc[1])}


def blink(e, times):
    for t in times:
        f = fr(t)
        for df, s in ((-2, 1.0), (0, 0.1), (2, 1.0)):
            for ob in e['pair']:
                key(ob, 'scale', max(1, f + df), (1, s, 1))


def look(e, t, dx, dy=0.0, dur=0.25):
    """Slide a pair of eyes to (dx, dy) from where they rest, by t + dur."""
    root = e['root']
    z = root.location.z
    root.keyframe_insert('location', frame=fr(t))
    key(root, 'location', fr(t + dur), (e['home'][0] + dx, e['home'][1] + dy, z))


def presence(name, parent, loc=(0, 0), scale=1.0, colour=RED, hot=HOT, slant=True):
    """A program with no body: a pair of eyes in a glow, over a row of bars that jump when it talks."""
    root = group(name, parent, loc, scale)
    rig = empty(f'{name}-rig', root, (0, 0, 0))
    halo = glow(f'{name}-halo', rig, (0, 0), 1.9, colour, 0.42)
    e = eyes(f'{name}-eyes', rig, (0, 0.12), 1.0, colour, hot, slant)
    bars = []
    for i in range(9):
        b = shape(f'{name}-bar{i}', rrect_pts(0.07, 0.34, 0.035), material(colour, alpha=0.85), rig, ((i - 4) * 0.14, -0.55))
        b.scale = (1, 0.15, 1)
        bars.append(b)
    return {'root': root, 'rig': rig, 'halo': halo, 'eyes': e, 'bars': bars, 'shapes': [halo] + e['shapes'] + bars}


def hover(p, t0=0.0, t1=None, phase=0.0, step=2):
    """Let a program with no body drift a little, and its glow swell and shrink."""
    t1 = scene_end() if t1 is None else t1
    for f in every(step, fr(t0), fr(t1)):
        t = sec(f) + phase
        key(p['rig'], 'location', f, (0.05 * math.sin(t * 0.9), 0.07 * math.sin(t * 1.7), 0))
        s = 1 + 0.06 * math.sin(t * 2.3)
        key(p['halo'], 'scale', f, (s, s, 1))


def talk(p, t0, t1, seed=0, step=2):
    """Make the bars under a program's eyes jump between t0 and t1: it is talking."""
    rnd = random.Random(seed)
    for b in p['bars']:
        key(b, 'scale', max(1, fr(t0) - 1), (1, 0.15, 1))
        for f in every(step, fr(t0), fr(t1)):
            key(b, 'scale', f, (1, 0.25 + 1.1 * rnd.random(), 1))
        key(b, 'scale', fr(t1) + 2, (1, 0.15, 1))


def spark(name, parent, colour=RED, hot=HOT):
    """A point of light: Ultron on his way from one computer to another. Hidden until the scene shows it."""
    root = empty(name, parent)
    shapes = [glow(f'{name}-glow', root, (0, 0), 0.55, colour, 0.9),
              shape(f'{name}-core', circle_pts(0.1), material(hot, colour), root)]
    for ob in shapes:
        alpha(ob, 1, 0.0)
    return {'root': root, 'shapes': shapes}


# ---------------------------------------------------------------- Ultron's two bodies

def _part(name, rig, at):
    return group(name, rig, at)


def feeble(name, parent, loc=(0, FLOOR), scale=1.0):
    """Ultron's first body: a feeble robot, put together from the damaged parts of other robots.

    The origin is on the ground between its feet. Its legs, arms, and head
    turn about the points they hang from. 'parts' lists them in the order
    they are built.
    """
    root = group(name, parent, loc, scale)
    rig = empty(f'{name}-rig', root, (0, 0, 0))
    grey, deep, rust = material(STEEL500, STEEL700), material(STEEL700, STEEL800), material(RUST, RUST_DEEP)
    leg_l = _part(f'{name}-leg-l', rig, (-0.3, 1.5))
    shape(f'{name}-leg-l-bar', capsule_pts(1.42, 0.3), grey, leg_l)
    shape(f'{name}-leg-l-knee', circle_pts(0.13), deep, leg_l, (0, -0.7))
    shape(f'{name}-leg-l-foot', rrect_pts(0.6, 0.16, 0.06), deep, leg_l, (0.08, -1.42))
    leg_r = _part(f'{name}-leg-r', rig, (0.32, 1.5))
    shape(f'{name}-leg-r-bar', capsule_pts(1.1, 0.2), rust, leg_r)
    shape(f'{name}-leg-r-peg', capsule_pts(0.36, 0.1), deep, leg_r, (0, -1.08))
    torso = _part(f'{name}-torso', rig, (0, 1.5))
    shape(f'{name}-shell', [(-0.55, -0.05), (0.5, 0.0), (0.64, 0.7), (0.5, 1.4), (-0.62, 1.32), (-0.72, 0.55)], grey, torso)
    shape(f'{name}-patch', [(-0.5, 0.75), (0.1, 0.85), (0.05, 1.25), (-0.52, 1.18)], rust, torso)
    shape(f'{name}-hole', circle_pts(0.2, ry=0.24, n=20), material(NIGHT900), torso, (0.28, 0.42))
    for i, (x, drop) in enumerate(((0.2, 0.5), (0.3, 0.72), (0.38, 0.4))):
        shape(f'{name}-wire{i}', capsule_pts(drop, 0.035, n=4), material(RED_DEEP if i == 1 else ASH), torso, (x, 0.36), rot=(i - 1) * 0.25)
    for i, (x, y) in enumerate(((-0.45, 0.2), (0.42, 1.2), (-0.5, 1.15))):
        shape(f'{name}-rivet{i}', circle_pts(0.035, n=10), material(STEEL300), torso, (x, y))
    arm_l = _part(f'{name}-arm-l', rig, (-0.72, 2.72))
    shape(f'{name}-arm-l-bar', capsule_pts(1.25, 0.22), grey, arm_l)
    shape(f'{name}-arm-l-hand', circle_pts(0.13, n=16), deep, arm_l, (0, -1.3))
    arm_r = _part(f'{name}-arm-r', rig, (0.62, 2.78))
    shape(f'{name}-arm-r-bar', capsule_pts(0.55, 0.2), rust, arm_r)
    shape(f'{name}-arm-r-wire', capsule_pts(0.3, 0.035, n=4), material(ASH), arm_r, (0.02, -0.55), rot=0.3)
    head = _part(f'{name}-head', rig, (0.04, 2.92))
    shape(f'{name}-neck', rrect_pts(0.2, 0.3, 0.05), deep, head, (0, 0.08))
    shape(f'{name}-skull', rrect_pts(0.95, 0.78, 0.2), material(STEEL300, STEEL500), head, (0, 0.6), rot=0.1)
    shape(f'{name}-chip', [(0.2, 1.03), (0.52, 1.06), (0.5, 0.74)], material(NIGHT700), head)
    e = eyes(f'{name}-eyes', head, (0, 0.6), 0.7)
    return {'root': root, 'rig': rig, 'parts': [leg_l, leg_r, torso, arm_l, arm_r, head], 'torso': torso, 'head': head,
            'legs': {'left': leg_l, 'right': leg_r}, 'arms': {'left': arm_l, 'right': arm_r}, 'eyes': e, 'height': 3.95}


def powerful(name, parent, loc=(0, FLOOR), scale=1.0):
    """Ultron's second body: a tall, strong robot of clean steel, with a red light in its chest.

    Built like the feeble one: the origin is on the ground between its feet,
    and 'parts' lists its legs, torso, arms, and head in the order they are
    built.
    """
    root = group(name, parent, loc, scale)
    rig = empty(f'{name}-rig', root, (0, 0, 0))
    steel, dark = material(STEEL300, STEEL500), material(STEEL500, STEEL700)
    legs = {}
    for side, tag in ((-1, 'l'), (1, 'r')):
        leg = _part(f'{name}-leg-{tag}', rig, (side * 0.42, 2.3))
        shape(f'{name}-leg-{tag}-bar', [(-0.3, 0.1), (0.3, 0.1), (0.24, -1.0), (0.3, -1.15), (0.22, -2.2), (-0.22, -2.2), (-0.3, -1.15), (-0.24, -1.0)], steel, leg)
        shape(f'{name}-leg-{tag}-knee', circle_pts(0.2, n=20), dark, leg, (0, -1.08))
        shape(f'{name}-leg-{tag}-foot', rrect_pts(0.8, 0.22, 0.08), dark, leg, (side * 0.06, -2.19))
        legs['left' if side < 0 else 'right'] = leg
    torso = _part(f'{name}-torso', rig, (0, 2.3))
    shape(f'{name}-hips', rrect_pts(1.2, 0.4, 0.14), dark, torso, (0, 0.05))
    shape(f'{name}-waist', [(-0.5, 0.2), (0.5, 0.2), (0.62, 1.0), (-0.62, 1.0)], dark, torso)
    for i in range(3):
        shape(f'{name}-slit{i}', rrect_pts(0.74 + 0.08 * i, 0.05, 0), material(NIGHT800), torso, (0, 0.42 + 0.2 * i))
    shape(f'{name}-chest', [(-0.66, 0.95), (0.66, 0.95), (1.12, 1.75), (0.98, 2.1), (-0.98, 2.1), (-1.12, 1.75)], steel, torso)
    core = [glow(f'{name}-core-glow', torso, (0, 1.55), 0.6, RED, 0.75),
            shape(f'{name}-core-rim', circle_pts(0.3, n=24), dark, torso, (0, 1.55)),
            shape(f'{name}-core', circle_pts(0.2, n=24), material(HOT, RED), torso, (0, 1.55))]
    arms = {}
    for side, tag in ((-1, 'l'), (1, 'r')):
        arm = _part(f'{name}-arm-{tag}', rig, (side * 1.18, 4.2))
        shape(f'{name}-arm-{tag}-upper', capsule_pts(1.0, 0.4), dark, arm)
        shape(f'{name}-arm-{tag}-fore', [(-0.27, -0.9), (0.27, -0.9), (0.22, -1.95), (-0.22, -1.95)], steel, arm)
        shape(f'{name}-arm-{tag}-fist', rrect_pts(0.44, 0.4, 0.12), dark, arm, (0, -2.12))
        shape(f'{name}-arm-{tag}-pad', circle_pts(0.46, n=24), steel, arm)
        arms['left' if side < 0 else 'right'] = arm
    head = _part(f'{name}-head', rig, (0, 4.42))
    shape(f'{name}-neck', rrect_pts(0.36, 0.3, 0.08), dark, head, (0, 0.05))
    shape(f'{name}-helmet', [(-0.4, 0.15), (0.4, 0.15), (0.52, 0.62), (0.3, 1.02), (-0.3, 1.02), (-0.52, 0.62)], steel, head)
    shape(f'{name}-crest', rrect_pts(0.08, 0.5, 0.03), dark, head, (0, 0.84))
    shape(f'{name}-visor', rrect_pts(0.86, 0.26, 0.1), material(NIGHT900), head, (0, 0.56))
    e = eyes(f'{name}-eyes', head, (0, 0.56), 0.62)
    return {'root': root, 'rig': rig, 'parts': [legs['left'], legs['right'], torso, arms['left'], arms['right'], head],
            'torso': torso, 'head': head, 'legs': legs, 'arms': arms, 'eyes': e, 'core': core, 'height': 5.45}


def assemble(bot, times, source=None, dur=0.35):
    """Build a robot part by part: part i arrives at times[i], from the point source if one is given.

    source is in the robot's own units, measured from the ground between its feet.
    """
    for part, t in zip(bot['parts'], times):
        home = tuple(part.location)
        kit.pop(part, t, 1.0, dur)
        if source is not None:
            key(part, 'location', fr(t), (source[0], source[1], home[2]))
            key(part, 'location', fr(t + dur), home)


def walk(bot, t0, t1, x0, x1, y=FLOOR, rate=1.6, swing=24, limp=0.0, step=1):
    """Walk a robot from x0 to x1 between t0 and t1, at rate steps a second.

    A limp from 0 to 1 makes it sag and lean on every other step.
    """
    root, rig = bot['root'], bot['rig']
    z = root.location.z
    for f in every(step, fr(t0), fr(t1)):
        t = sec(f)
        q = kit.clamp((t - t0) / max(1e-6, t1 - t0))
        go = kit.clamp(min((t - t0) / 0.3, (t1 - t) / 0.3))
        s = math.sin((t - t0) * rate * math.pi)
        a = math.radians(swing) * s * go
        key(root, 'location', f, (mix(x0, x1, q), y, z))
        key(bot['legs']['left'], 'rotation_euler', f, (0, 0, a))
        key(bot['legs']['right'], 'rotation_euler', f, (0, 0, -a))
        key(bot['arms']['left'], 'rotation_euler', f, (0, 0, -0.6 * a))
        key(bot['arms']['right'], 'rotation_euler', f, (0, 0, 0.6 * a))
        sag = limp * max(0.0, s)
        key(rig, 'location', f, (0, (0.06 * abs(s) - 0.16 * sag) * go, 0))
        key(rig, 'rotation_euler', f, (0, 0, -0.12 * sag * go))


def sway(bot, t0=0.0, t1=None, phase=0.0, amount=1.0, step=3):
    """Keep a standing robot from being still: its head turns a little, and its arms hang loose."""
    t1 = scene_end() if t1 is None else t1
    for f in every(step, fr(t0), fr(t1)):
        t = sec(f) + phase
        key(bot['head'], 'rotation_euler', f, (0, 0, 0.05 * amount * math.sin(t * 0.9)))
        key(bot['arms']['left'], 'rotation_euler', f, (0, 0, 0.04 * amount * math.sin(t * 1.3)))
        key(bot['arms']['right'], 'rotation_euler', f, (0, 0, -0.04 * amount * math.sin(t * 1.3 + 0.7)))


# ---------------------------------------------------------------- people

def figure(name, parent, loc=(0, FLOOR), scale=0.62, coat=STEEL500, coat_deep=STEEL700, hair='#2a2320',
           skin=kit.SKIN, shade=kit.SKIN_SHADE, facing=1):
    """A simple standing person, nobody's likeness.

    The origin is on the ground between the feet. facing=1 looks right, -1
    looks left. The working arm hangs at angle 0 and turns about the shoulder
    toward where the figure faces.
    """
    root = group(name, parent, loc, scale)
    body = empty(f'{name}-body', root, (0, 4.3, 0))
    shape(f'{name}-legs', [(-0.55, -2.6), (0.55, -2.6), (0.5, -4.3), (0.12, -4.3), (0, -3.0), (-0.12, -4.3), (-0.5, -4.3)],
          material(NIGHT500, NIGHT600), body)
    shape(f'{name}-coat', [(-0.75, -0.15), (-0.45, 0.08), (0, 0.13), (0.45, 0.08), (0.75, -0.15), (0.85, -1.4), (0.95, -2.8), (-0.95, -2.8), (-0.85, -1.4)],
          material(coat, coat_deep), body, smooth=True)
    shape(f'{name}-collar', [(-0.22, 0.08), (0.22, 0.08), (0, -0.5)], material(BONE), body)
    shape(f'{name}-neck', rrect_pts(0.28, 0.34, 0.12), material(shade), body, (0, 0.16))
    head = group(f'{name}-head', body, (0.05 * facing, 0.68))
    shape(f'{name}-face', circle_pts(0.44), material(skin, shade), head)
    shape(f'{name}-ear', circle_pts(0.08, n=12), material(shade), head, (-0.4 * facing, -0.02))
    shape(f'{name}-hair', [(-0.47 * facing, 0.02), (-0.44 * facing, 0.32), (-0.12 * facing, 0.52), (0.28 * facing, 0.48), (0.46 * facing, 0.2), (0.3 * facing, 0.26), (-0.2 * facing, 0.22)],
          material(hair), head, smooth=True)
    for side in (-1, 1):
        shape(f'{name}-eye{side}', circle_pts(0.045, ry=0.06, n=12), material(NIGHT900), head, (0.1 * facing + side * 0.13, 0.0))
    shape(f'{name}-mouth', arc_pts(0.1, 0.035, 210, 330, n=8), material(NIGHT900), head, (0.1 * facing, -0.14))
    shoulder = group(f'{name}-shoulder', body, (0.62 * facing, -0.25))
    shape(f'{name}-arm', capsule_pts(1.5, 0.3), material(coat, coat_deep), shoulder)
    shape(f'{name}-hand', circle_pts(0.15, n=16), material(skin, shade), shoulder, (0, -1.55))
    return {'root': root, 'body': body, 'head': head, 'arm': shoulder, 'facing': facing}


def stroll(who, t0, t1, x0, x1, y=FLOOR, step=1):
    """Walk a person from x0 to x1 between t0 and t1, with a small bob at each step."""
    root, body = who['root'], who['body']
    z = root.location.z
    for f in every(step, fr(t0), fr(t1)):
        t = sec(f)
        q = span(t, t0, t1)
        go = kit.clamp(min((t - t0) / 0.25, (t1 - t) / 0.25))
        key(root, 'location', f, (mix(x0, x1, q), y, z))
        key(body, 'location', f, (0, 4.3 + 0.07 * abs(math.sin((t - t0) * 7.0)) * go, 0))


def reach(who, t, deg, dur=0.3):
    """Turn a person's working arm to deg (0 hangs down, 90 points ahead) by t + dur."""
    arm = who['arm']
    arm.keyframe_insert('rotation_euler', frame=fr(t))
    key(arm, 'rotation_euler', fr(t + dur), (0, 0, who['facing'] * math.radians(deg)))


def nod(who, t0=0.0, t1=None, phase=0.0, step=3):
    """Keep a standing person from being still: the head tips a little, now and then."""
    t1 = scene_end() if t1 is None else t1
    for f in every(step, fr(t0), fr(t1)):
        key(who['head'], 'rotation_euler', f, (0, 0, 0.05 * math.sin((sec(f) + phase) * 1.1)))


# ---------------------------------------------------------------- machines

def console(name, parent, loc=(0, FLOOR), scale=1.0, colour=RED):
    """A lab computer: a desk with a dish on it, and above the dish a program with no body can show itself.

    The origin is on the ground. 'spot' is where the program floats, in the
    console's own units, and 'beam' is the light the dish throws up at it.
    """
    root = group(name, parent, loc, scale)
    for side in (-1, 1):
        shape(f'{name}-leg{side}', rrect_pts(0.14, 1.0, 0.03), material(STEEL800), root, (side * 1.05, 0.5))
    shape(f'{name}-top', rrect_pts(2.8, 0.24, 0.08), material(STEEL700, STEEL800), root, (0, 1.1))
    shape(f'{name}-box', rrect_pts(1.5, 0.5, 0.1), material(NIGHT500, NIGHT600), root, (0, 1.46))
    for i in range(3):
        shape(f'{name}-dot{i}', circle_pts(0.04, n=10), material(ASH), root, (-0.5 + 0.16 * i, 1.46))
    shape(f'{name}-dish', [(-0.5, 1.72), (0.5, 1.72), (0.32, 1.9), (-0.32, 1.9)], material(STEEL500, STEEL700), root)
    beam = shape(f'{name}-beam', [(-0.3, 1.9), (0.3, 1.9), (1.2, 4.1), (-1.2, 4.1)], material(colour, alpha=0.0, alpha_bottom=0.22), root)
    alpha(beam, 1, 0.0)
    return {'root': root, 'beam': beam, 'spot': (0, 3.2)}


def machine(name, parent, base, l1=1.7, l2=1.5, colour=STEEL500, deep=STEEL700):
    """A lab machine that builds things: an arm of two parts with a claw, hanging from base.

    Turn 'shoulder' and 'elbow' to move it. Its lamp is grey until light turns it red.
    """
    root = group(name, parent, base)
    shape(f'{name}-mount', rrect_pts(0.9, 0.3, 0.1), material(STEEL700, STEEL800), root)
    shoulder = group(f'{name}-shoulder', root, (0, -0.1))
    shape(f'{name}-upper', capsule_pts(l1, 0.26), material(colour, deep), shoulder)
    elbow = group(f'{name}-elbow', shoulder, (0, -l1))
    shape(f'{name}-lower', capsule_pts(l2, 0.2), material(colour, deep), elbow)
    for side in (-1, 1):
        shape(f'{name}-finger{side}', [(0, 0.04), (side * 0.2, -0.1), (side * 0.14, -0.42), (side * 0.05, -0.28)], material(deep), elbow, (0, -l2))
    shape(f'{name}-joint', circle_pts(0.17, n=20), material(STEEL300, STEEL500), elbow)
    shape(f'{name}-hub', circle_pts(0.2, n=20), material(STEEL300, STEEL500), shoulder)
    shape(f'{name}-lamp-off', circle_pts(0.08, n=12), material(ASH), shoulder)
    lamp = [glow(f'{name}-lamp-glow', shoulder, (0, 0), 0.4, RED, 0.8),
            shape(f'{name}-lamp-on', circle_pts(0.08, n=12), material(HOT, RED), shoulder)]
    for ob in lamp:
        alpha(ob, 1, 0.0)
    return {'root': root, 'shoulder': shoulder, 'elbow': elbow, 'lamp': lamp}


def light(m, t, dur=0.2):
    """Turn a machine's lamp red at t: Ultron has taken control of it."""
    for ob in m['lamp']:
        alpha(ob, fr(t), 0.0)
        alpha(ob, fr(t + dur), 1.0)


def work(m, t0, t1, sh=(10, 50), el=(-75, -15), rate=1.2, step=2):
    """Have a machine work between t0 and t1: its two joints swing between the given angles, in degrees."""
    for f in every(step, fr(t0), fr(t1)):
        t = sec(f)
        on = span(t, t0, t0 + 0.4) * (1 - span(t, t1 - 0.4, t1))
        w = 0.5 + 0.5 * math.sin((t - t0) * rate * math.tau)
        key(m['shoulder'], 'rotation_euler', f, (0, 0, math.radians(mix(sh[0], sh[1], w)) * on))
        key(m['elbow'], 'rotation_euler', f, (0, 0, math.radians(mix(el[0], el[1], w * w)) * on))


def fold(m, t, sh=35, el=80, dur=0.7):
    """Fold a machine's arm up and out of the way at t, once its work is done. The angles are in degrees."""
    for when, a, b in ((t, 0, 0), (t + dur, sh, el)):
        key(m['shoulder'], 'rotation_euler', fr(when), (0, 0, math.radians(a)))
        key(m['elbow'], 'rotation_euler', fr(when), (0, 0, math.radians(b)))


def heap(name, parent, loc=(0, FLOOR), seed=4, n=9):
    """A pile of parts from broken robots, lying on the ground."""
    rnd = random.Random(seed)
    root = group(name, parent, loc)
    for i in range(n):
        x = (rnd.random() - 0.5) * 2.4
        y = 0.12 + 0.75 * rnd.random() * (1 - abs(x) / 1.4)
        mat = material(*rnd.choice(((STEEL500, STEEL700), (STEEL700, STEEL800), (RUST, RUST_DEEP))))
        if i % 3 == 0:
            shape(f'{name}-rod{i}', capsule_pts(0.7 + 0.5 * rnd.random(), 0.2), mat, root, (x, y), rot=1.2 + rnd.random() * 0.8)
        elif i % 3 == 1:
            shape(f'{name}-plate{i}', rrect_pts(0.6 + 0.4 * rnd.random(), 0.34, 0.08), mat, root, (x, y), rot=rnd.uniform(-0.5, 0.5))
        else:
            shape(f'{name}-skull{i}', rrect_pts(0.5, 0.42, 0.12), mat, root, (x, y), rot=rnd.uniform(-0.8, 0.8))
    return root


# ---------------------------------------------------------------- a program as its code

def _bars(name, root, x, y, right, rnd, colours, thick=0.13):
    row = []
    while right - x > 0.3 and len(row) < 5:
        ln = min(right - x, 0.3 + rnd.random() * 0.9)
        row.append(shape(f'{name}w{len(row)}', bar_pts(ln, thick), material(rnd.choice(colours)), root, (x, y)))
        x += ln + 0.14
        if rnd.random() < 0.25:
            break
    return row


def page(name, parent, loc=(0, 0), rows=8, w=3.4, h=4.2, seed=1, colour=ICE, deep=ICE_DEEP, hot=FROST, scale=1.0, face=True, slant=False):
    """A program drawn as its code: a sheet with rows of bars for its lines of text.

    With face, a pair of eyes sits at the top of the sheet, so the program can
    be followed as a character. Returns the root, the rows (each a list of
    bars), and where each row sits.
    """
    rnd = random.Random(seed)
    root = group(name, parent, loc, scale)
    glow = shape(f'{name}-glow', circle_pts(w * 0.5 + 1.9, ry=h * 0.5 + 1.9), glow_material(colour, 0.5, power=4.0), root)
    shape(f'{name}-sheet', rrect_pts(w, h, 0.18), material(NIGHT500, NIGHT600), root)
    shape(f'{name}-rule', rrect_pts(w - 0.5, 0.03, 0), material(STEEL700), root, (0, h / 2 - 0.62))
    e = eyes(f'{name}-eyes', root, (0, h / 2 - 0.32), 0.55, colour, hot, slant, gap=0.26) if face else None
    top = h / 2 - 0.95
    gap = (h - 1.3) / rows
    out, ys, x0s = [], [], []
    for r in range(rows):
        x = -w / 2 + 0.32 + (rnd.choice((0, 1, 1, 2)) if r else 0) * 0.32
        y = top - r * gap
        out.append(_bars(f'{name}-r{r}', root, x, y, w / 2 - 0.3, rnd, [colour, deep, STEEL300, STEEL500]))
        ys.append(y)
        x0s.append(x)
    return {'root': root, 'rows': out, 'ys': ys, 'x0s': x0s, 'eyes': e, 'w': w, 'h': h, 'glow': glow, 'name': name, 'made': 0}


def rewrite(pg, r, t, colours=(BONE, FROST), dur=0.45):
    """Rewrite row r of a page at t: its bars close up, and new ones of other lengths open in their place."""
    pg['made'] += 1
    rnd = random.Random(pg['made'] * 31 + r)
    for ob in pg['rows'][r]:
        ob.keyframe_insert('scale', frame=fr(t))
        key(ob, 'scale', fr(t + dur * 0.35), (0.001, 1, 1))
    new = _bars(f'{pg["name"]}-r{r}v{pg["made"]}', pg['root'], pg['x0s'][r], pg['ys'][r], pg['w'] / 2 - 0.3, rnd, list(colours))
    for ob in new:
        key(ob, 'scale', 1, (0.001, 1, 1))
        key(ob, 'scale', fr(t + dur * 0.35), (0.001, 1, 1))
        key(ob, 'scale', fr(t + dur), (1, 1, 1))
    pg['rows'][r] = new
    return new


def band(pg, r, colour=BONE, a=0.3):
    """A soft bar of light along row r of a page, hidden until the scene shows it."""
    pg['made'] += 1
    ob = shape(f'{pg["name"]}-band{pg["made"]}', rrect_pts(pg['w'] - 0.3, 0.36, 0.18), material(colour, alpha=a), pg['root'], (0, pg['ys'][r]))
    alpha(ob, 1, 0.0)
    return ob


def pen(name, parent, loc=(0, 0), scale=1.0, colour=ICE, hot=FROST):
    """A small pen: the mark of the part of a program that does the rewriting."""
    root = group(name, parent, loc, scale)
    shape(f'{name}-glow', circle_pts(0.55), glow_material(colour, 0.7), root)
    shape(f'{name}-body', [(-0.07, 0.26), (0.07, 0.26), (0.07, -0.1), (0, -0.26), (-0.07, -0.1)], material(hot, colour), root)
    shape(f'{name}-tip', [(-0.035, -0.18), (0.035, -0.18), (0, -0.26)], material(NIGHT900), root)
    root.rotation_euler = (0, 0, -0.6)
    return root


def seal(name, parent, loc=(0, 0), scale=1.0, colour=ICE, hot=FROST):
    """A proof's mark: a tick in a ring. It is shrunk to nothing until the scene pops it."""
    root = group(name, parent, loc, scale)
    glow(f'{name}-glow', root, (0, 0), 0.9, colour, 0.7)
    shape(f'{name}-disc', circle_pts(0.5), material(NIGHT700), root)
    shape(f'{name}-ring', arc_pts(0.5, 0.07, 0, 360, n=40), material(colour), root)
    shape(f'{name}-tick', [(-0.26, 0.06), (-0.08, -0.06), (0.24, 0.3), (0.32, 0.22), (-0.08, -0.22), (-0.32, 0.0)], material(hot), root)
    root.scale = TINY
    return root


def desk(name, parent, loc=(0, FLOOR), w=3.0):
    """A plain desk, seen from the side. The origin is on the ground; its top is 1.45 above it."""
    root = group(name, parent, loc)
    for side in (-1, 1):
        shape(f'{name}-leg{side}', rrect_pts(0.14, 1.35, 0.03), material(STEEL800), root, (side * (w / 2 - 0.2), 0.68))
    shape(f'{name}-top', rrect_pts(w, 0.2, 0.06), material(STEEL700, STEEL800), root, (0, 1.4))
    return root


def task(name, parent, loc=(0, 0), scale=1.0, seed=0):
    """A small program with a mistake in it: a card with three lines, one of them red.

    Returns the card's root, the red line, and the line that takes its place once the mistake is fixed.
    """
    rnd = random.Random(seed)
    root = group(name, parent, loc, scale)
    shape(f'{name}-card', rrect_pts(1.3, 1.0, 0.12), material(NIGHT500, NIGHT600), root)
    bad = good = None
    for r in range(3):
        ln = 0.5 + 0.4 * rnd.random()
        y = 0.26 - 0.26 * r
        if r == 1:
            bad = shape(f'{name}-bad', bar_pts(ln, 0.11), material(RED), root, (-0.45, y))
            good = shape(f'{name}-good', bar_pts(ln, 0.11), material(ICE), root, (-0.45, y))
            alpha(good, 1, 0.0)
        else:
            shape(f'{name}-line{r}', bar_pts(ln, 0.11), material(STEEL500), root, (-0.45, y))
    return {'root': root, 'bad': bad, 'good': good}


def fix(card, t, dur=0.15):
    """Fix a small program's mistake at t: its red line turns blue."""
    lit(card['bad'], [(0.0, 1.0), (t, 1.0), (t + dur, 0.0)])
    lit(card['good'], [(0.0, 0.0), (t, 0.0), (t + dur, 1.0)])


# ---------------------------------------------------------------- marks and moves

def outline(name, parent, loc=(0, 0), scale=1.0, colour=RED, a=1.0):
    """The dotted outline of a body that is not there: a head, shoulders, arms, and legs.

    The origin is between where its eyes would be. Hidden until the scene shows it.
    """
    root = group(name, parent, loc, scale)
    pts = [(0.62 * math.cos(math.tau * i / 14), 0.05 + 0.62 * math.sin(math.tau * i / 14)) for i in range(14)]
    path = [(-0.3, -0.6), (-1.0, -0.85), (-1.05, -2.2), (-0.7, -2.25), (-0.65, -3.9), (-0.1, -3.9), (0, -2.6),
            (0.1, -3.9), (0.65, -3.9), (0.7, -2.25), (1.05, -2.2), (1.0, -0.85), (0.3, -0.6)]
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 0.24))
        pts += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
    dots = [shape(f'{name}-dot{i}', circle_pts(0.045, n=8), material(colour, alpha=a), root, p) for i, p in enumerate(pts)]
    for ob in dots:
        alpha(ob, 1, 0.0)
    return {'root': root, 'shapes': dots}


def strike(name, parent, t, a, b, colour=BONE, dur=0.12):
    """A blow: a streak of light from point a to point b at t, and a flash where it lands."""
    streak = shape(f'{name}-streak', bar_pts(math.hypot(b[0] - a[0], b[1] - a[1]), 0.14), material(colour), parent, a,
                   lift=0.3, rot=math.atan2(b[1] - a[1], b[0] - a[0]))
    key(streak, 'scale', 1, (0.001, 1, 1))
    key(streak, 'scale', fr(t), (0.001, 1, 1))
    key(streak, 'scale', max(fr(t) + 1, fr(t + dur)), (1, 1, 1))
    lit(streak, [(0.0, 0.0), (t - 0.04, 0.0), (t, 1.0), (t + dur, 1.0), (t + dur + 0.15, 0.0)])
    flash = glow(f'{name}-flash', parent, b, 0.9, colour, 0.9, lift=0.31)
    lit(flash, [(0.0, 0.0), (t + dur, 0.0), (t + dur + 0.04, 1.0), (t + dur + 0.35, 0.0)])
    return streak, flash


def pulse(name, parent, loc, t, r=0.7, colour=BONE, dur=0.8, width=0.07):
    """A ring of light that swells and fades at t."""
    ob = kit.ring(name, parent, loc, r, colour, width, lift=0.25)
    kit.flash(ob, t, dur)
    return ob


def spot(name, parent, loc, r=2.4, colour=BONE, a=0.14):
    """A soft pool of light behind something, about r across at its brightest part. Hidden until the scene shows it."""
    ob = glow(name, parent, loc, 0.8 * r, colour, a)
    alpha(ob, 1, 0.0)
    return ob


# ---------------------------------------------------------------- the two labs

def first_lab(far, stage, name='lab'):
    """The lab Ultron starts up in: a console on the left, two machines hanging on the right, and a heap of broken robots."""
    roots = room(name, far, stage)
    front = roots[1]
    c = console(f'{name}-console', front, (-4.6, FLOOR))
    pile = heap(f'{name}-heap', front, (6.3, FLOOR))
    ms = [machine(f'{name}-machine{i}', front, (x, 4.25)) for i, x in enumerate((1.0, 3.8))]
    return {'roots': roots, 'front': front, 'console': c, 'machines': ms, 'heap': pile,
            'spot': (-4.6, FLOOR + 3.2), 'stand': (2.4, FLOOR), 'heap_at': (6.3, FLOOR + 0.5)}


def second_lab(far, stage, name='works'):
    """The lab Ultron goes to: four machines made for building robots, and racks of new parts."""
    roots = room(name, far, stage, lamps=(-6.0, -2.0, 2.0, 6.0), light=STEEL100, glow=0.06)
    front = roots[1]
    for i, x in enumerate((6.0, 7.3)):
        for j in range(4):
            shape(f'{name}-rack{i}-{j}', rrect_pts(1.05, 0.34, 0.06), material(STEEL300, STEEL500), front, (x, FLOOR + 0.3 + 0.48 * j))
    c = console(f'{name}-console', front, (-6.2, FLOOR), 0.85)
    ms = [machine(f'{name}-machine{i}', front, (x, 4.25), 1.5, 1.3) for i, x in enumerate((-2.6, -0.9, 2.9, 4.6))]
    return {'roots': roots, 'front': front, 'console': c, 'machines': ms,
            'spot': (-6.2, FLOOR + 3.2 * 0.85), 'stand': (1.0, FLOOR), 'rack_at': (6.6, FLOOR + 1.0)}


# ---------------------------------------------------------------- the study, and an AI that is not Ultron

def scientist(name, parent, loc=(0, FLOOR), facing=1):
    """The computer scientist: a person in a grey-blue coat, with grey hair. Nobody's likeness."""
    return figure(name, parent, loc, coat='#56707e', coat_deep='#3b505c', hair='#c9c2b8', facing=facing)


def paper(who, name='paper'):
    """A sheet of paper in a person's working hand. It hangs at their side until the arm is raised."""
    root = group(name, who['arm'], (0, -1.95))
    shape(f'{name}-sheet', rrect_pts(0.7, 0.9, 0.04), material(BONE, STEEL100), root)
    for i in range(4):
        shape(f'{name}-line{i}', bar_pts(0.46 - 0.1 * (i % 2), 0.05), material(STEEL500), root, (-0.24, 0.27 - 0.18 * i))
    return root


def write(who, t0, t1, deg=36):
    """Have a person write at a desk between t0 and t1: the working arm reaches down to the paper, and the hand moves."""
    reach(who, t0 - 0.4, deg)
    for f in every(2, fr(t0), fr(t1)):
        key(who['arm'], 'rotation_euler', f, (0, 0, who['facing'] * math.radians(deg + 5 * math.sin(sec(f) * 7.0))))
    reach(who, t1 + 0.1, 8, 0.5)


def thinker(name, parent, loc=(0, FLOOR), scale=0.72, seed=5):
    """An AI that is not Ultron: a computer, and above it the program that runs on it, a sheet of its code with eyes.

    'at' is where the computer stands, and 'bench' is the point small
    programs are brought to, for the program to work on.
    """
    box = console(f'{name}-computer', parent, loc, 1.0, ICE)
    pg = page(f'{name}-program', parent, (loc[0], loc[1] + 4.3), rows=6, w=3.0, h=3.4, seed=seed, scale=scale)
    return {'computer': box, 'program': pg, 'size': scale, 'at': loc, 'bench': (loc[0] + 2.9, loc[1] + 4.3)}


def arms(name, box, at, parent, t, gap=0.5, source=None, t1=None):
    """Fit a computer with a pair of arms, the first at t and the second gap seconds later.

    box is the console, and at is where it stands, in parent's units. With a
    source, each arm is carried to its place from that point, as if by a
    hand; without one it grows where it is. Once an arm is on, it lifts and
    waves. Returns the times the two are on.
    """
    t1 = scene_end() if t1 is None else t1
    times = []
    for k, side in enumerate((-1, 1)):
        when = t + gap * k
        home = (side * 1.5, 1.2)
        arm = group(f'{name}{side}', box['root'], home)
        shape(f'{name}{side}-bar', capsule_pts(1.1, 0.22), material(STEEL300, STEEL500), arm)
        for tip in (-1, 1):
            shape(f'{name}{side}-claw{tip}', [(0, 0.04), (tip * 0.2, -0.1), (tip * 0.14, -0.42), (tip * 0.05, -0.28)],
                  material(STEEL500), arm, (0, -1.1))
        shape(f'{name}{side}-hub', circle_pts(0.17, n=20), material(ICE, ICE_DEEP), arm)
        z = arm.location.z
        if source is None:
            kit.pop(arm, when, 1.0, 0.35)
        else:
            start = (source[0] - at[0], source[1] - at[1])
            kit.pop(arm, when - 0.7, 1.0, 0.2)
            key(arm, 'location', 1, (start[0], start[1], z))
            last = fr(when)
            for f in every(1, fr(when - 0.45), last):
                q = 1.0 if f == last else span(sec(f), when - 0.45, when)
                x, y = mix(start, home, q)
                key(arm, 'location', f, (x, y + 0.6 * math.sin(math.pi * q), z))
        for f in every(2, fr(when), fr(t1)):
            s = sec(f)
            up = 2.2 * (1.0 if source is None else span(s, when, when + 0.4))
            wave = 0.35 * math.sin((s - when) * 2.6 + k) * (1 - span(s, when + 2.2, when + 3.0))
            key(arm, 'rotation_euler', f, (0, 0, side * (up + wave)))
        pulse(f'{name}-ring{side}', parent, (at[0] + side * 1.9, at[1] + 1.9), when + 0.1, 0.8, ICE, 0.7, 0.05)
        times.append(when)
    return times


def dotted_sheet(name, parent, loc=(0, 0), w=3.0, h=3.4, scale=1.0, colour=FROST):
    """The dotted outline of a sheet of code: a program that is not there yet. Hidden until the scene shows it."""
    root = group(name, parent, loc, scale)
    edge = rrect_pts(w, h, 0.18, n=3)
    pts = []
    for (x0, y0), (x1, y1) in zip(edge, edge[1:] + edge[:1]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 0.2))
        pts += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
    dots = [shape(f'{name}-dot{i}', circle_pts(0.045, n=8), material(colour), root, p) for i, p in enumerate(pts)]
    for ob in dots:
        alpha(ob, 1, 0.0)
    return {'root': root, 'shapes': dots}


def study(far, stage, name='study'):
    """The computer scientist's study, in cold light.

    On the left he stands at the desk he writes at. On the right is the AI
    he writes about: a computer, and above it the program that runs on it.
    """
    roots = room(name, far, stage, lamps=(-5.4, 1.6), light=ICE, glow=0.06)
    front = roots[1]
    desk(f'{name}-desk', front, (-5.3, FLOOR), 2.6)
    shape(f'{name}-paper', rrect_pts(0.9, 0.06, 0.02), material(BONE), front, (-6.1, FLOOR + 1.53))
    who = scientist(f'{name}-scientist', front, (-7.4, FLOOR))
    return {'roots': roots, 'front': front, 'who': who, 'ai': thinker(name, front, (1.6, FLOOR))}


def dark(parent, t, dur=0.25, name='dark'):
    """Put out every light at t: a black sheet in front of all that was made before it.

    Returns an empty set in front of the sheet. What hangs from it shows in
    the dark.
    """
    sheet = shape(f'{name}-sheet', rrect_pts(40, 24, 0), material('#000000'), parent, lift=0.3)
    lit(sheet, [(0.0, 0.0), (t, 0.0), (t + dur, 1.0)])
    return empty(f'{name}-front', parent, (0, 0, 0.35))


# ---------------------------------------------------------------- what the scenes share

FORMS = [(-5.4, FLOOR + 3.0), (-1.9, FLOOR), (2.4, FLOOR)]
FORM_SCALE = 0.82


def three_forms(parent, name='forms'):
    """Ultron's three forms in a row: the program with no body over its computer, the feeble robot, and the powerful one.

    'heads' is where his eyes are in each.
    """
    row = empty(name, parent)
    stand = console(f'{name}-stand', row, (FORMS[0][0], FLOOR), 0.9)
    alpha(stand['beam'], 1, 1.0)
    first = presence(f'{name}-first', row, FORMS[0], 0.9)
    second = feeble(f'{name}-second', row, FORMS[1], FORM_SCALE)
    third = powerful(f'{name}-third', row, FORMS[2], FORM_SCALE)
    heads = [FORMS[0], (FORMS[1][0] + 0.04 * FORM_SCALE, FLOOR + 3.52 * FORM_SCALE), (FORMS[2][0], FLOOR + 4.98 * FORM_SCALE)]
    return {'root': row, 'first': first, 'second': second, 'third': third, 'heads': heads}


def tally(name, parent, loc, t_show, times, gap=0.7):
    """Three lamps in a row, one for each reason the film gives. They show from t_show.

    Lamp k lights at times[k]. A time of None leaves it dark, and a time
    before t_show has it lit when the lamps first show.
    """
    root = group(name, parent, loc)
    for k, t in enumerate(times):
        x = (k - 1) * gap
        off = [shape(f'{name}-rim{k}', circle_pts(0.2, n=24), material(STEEL500), root, (x, 0)),
               shape(f'{name}-well{k}', circle_pts(0.14, n=24), material(NIGHT800), root, (x, 0))]
        visible(off, [(t_show, None)], 0.3)
        if t is not None:
            on = [glow(f'{name}-glow{k}', root, (x, 0), 0.32, RED, 0.85),
                  shape(f'{name}-lamp{k}', circle_pts(0.14, n=24), material(HOT, RED), root, (x, 0))]
            visible(on, [(max(t_show, t), None)], 0.2)
    return root


def errand(name, parent, t, at, fixed=True, pace=1.0, seed=0, scale=0.7, away=12.5):
    """Bring a small program with a mistake in it from the right to the point at, at t, and take it back out.

    With fixed, its red line has turned blue before it leaves: the program
    it was brought to did its job. A pace above 1 is a quicker turn. Returns
    the time the mistake is fixed, or would have been.
    """
    card = task(name, parent, (away, at[1]), scale, seed)
    root = card['root']
    z = root.location.z
    t_fix, t_go, t_gone = t + 0.75 / pace, t + 1.05 / pace, t + 1.6 / pace
    key(root, 'location', max(1, fr(t) - 1), (away, at[1], z))
    for f in every(1, fr(t), fr(t_gone) + 1):
        s = sec(f)
        x = mix(away, at[0], span(s, t, t + 0.5 / pace, kit.ease_out))
        x = mix(x, away, span(s, t_go, t_gone, lambda v: v * v))
        key(root, 'location', f, (x, at[1], z))
    if fixed:
        fix(card, t_fix)
    return t_fix


def hop(sp, points, t0, t1, lift=1.3):
    """Send a point of light from each point to the next in an arc, between t0 and t1."""
    root = sp['root']
    z = root.location.z
    hops = len(points) - 1
    for f in every(1, fr(t0), fr(t1) + 1):
        along = span(sec(f), t0, t1, lambda v: v) * hops
        i = min(hops - 1, int(along))
        q = kit.smooth(along - i)
        x, y = mix(points[i], points[i + 1], q)
        key(root, 'location', f, (x, y + lift * math.sin(math.pi * q), z))


def lit(ob, steps):
    """Set how much a shape shows at each (time, share) step, in turn.

    Two steps that are closer together than one frame are still keyed on two
    frames, one after the other, so that neither is lost and a shape meant to
    be hidden until a moment does not show before it.
    """
    last = 0
    for t, a in steps:
        last = max(fr(t), last + 1)
        alpha(ob, last, a)


def visible(shapes, spans, dur=0.3):
    """Show a group of shapes during each (t_in, t_out) span, and hide it between them.

    A t_out of None lasts to the end, and a span that begins before the scene
    does is showing from the first frame.
    """
    for ob in shapes:
        steps = [(0.0, 0.0)]
        for t_in, t_out in spans:
            steps = [(0.0, 1.0)] if t_in + dur <= 0 else steps + [(t_in, 0.0), (t_in + dur, 1.0)]
            if t_out is not None:
                steps += [(t_out, 1.0), (t_out + dur, 0.0)]
        lit(ob, steps)


def open_eyes(e, t, dur=0.4):
    """Open a pair of eyes at t: they are slits before it."""
    for ob in e['pair']:
        key(ob, 'scale', max(1, fr(t - 0.5)), (1, 1, 1))
        key(ob, 'scale', max(1, fr(t) - 1), (1, 0.08, 1))
        key(ob, 'scale', fr(t + dur), (1, 1, 1))


def hide(shapes, t, dur=0.3):
    """Fade out, at t, a group of shapes that has been showing since the scene began."""
    for ob in shapes:
        lit(ob, [(0.0, 1.0), (t, 1.0), (t + dur, 0.0)])


def drift(ob, t0=0.0, t1=None, amount=0.08, phase=0.0, step=2):
    """Let something that floats rise and sink a little, about where it is."""
    t1 = scene_end() if t1 is None else t1
    x, y, z = ob.location
    for f in every(step, fr(t0), fr(t1)):
        key(ob, 'location', f, (x, y + amount * math.sin((sec(f) + phase) * 1.4), z))


def resize(ob, t, s0, s1, dur=0.3):
    """Change an object's size from s0 to s1 at t."""
    key(ob, 'scale', fr(t), (s0, s0, s0))
    key(ob, 'scale', fr(t + dur), (s1, s1, s1))


def own_program(name, parent, loc=(0, 0), scale=0.5):
    """Ultron's program, drawn as its code: a small red sheet with his eyes at the top."""
    return page(name, parent, loc, rows=6, w=2.6, h=3.0, seed=9, colour=RED, deep=RED_DEEP, hot=HOT, scale=scale, slant=True)


def run(sp, points, t0, t1):
    """Send a point of light along a line through the points between t0 and t1, slowing at each one."""
    root = sp['root']
    z = root.location.z
    hops = len(points) - 1
    for f in every(1, fr(t0), fr(t1)):
        along = span(sec(f), t0, t1, lambda v: v) * hops
        i = min(hops - 1, int(along))
        x, y = mix(points[i], points[i + 1], kit.smooth(along - i))
        key(root, 'location', f, (x, y, z))
