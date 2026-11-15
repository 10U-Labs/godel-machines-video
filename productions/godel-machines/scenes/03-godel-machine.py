"""Scene 03: Improving itself.

A computer scientist sketches a machine as a blueprint, and it is named the
Gödel Machine. The blueprint becomes one working machine, tied to its own
code: it does its job while it rewrites that code, changes any part of
itself, and even changes the part that makes the changes. Then the machine
becomes Pip: only one Pip, changing itself again and again.
"""
import math

import kit
import parts
from kit import fr, sec, span, mix, key, alpha, every

SHEET_AT = (1.3, 0.3)
SHEET_W, SHEET_H = 8.0, 5.8
BOT_S = 1.7
MACHINE_AT = (-3.4, 0.3)
CODE_AT = (3.6, 0.4)


def outline_paths():
    """The blueprint's lines, as lists of points around the machine's body, screen, eyes, and antenna."""
    def sample(pts, closed=True, step=0.16):
        out = []
        loop = pts + [pts[0]] if closed else pts
        for (x0, y0), (x1, y1) in zip(loop, loop[1:]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
            out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
        return out
    body = sample(kit.rrect_pts(1.7, 1.5, 0.62))
    screen = [(x, y + 0.06) for x, y in sample(kit.rrect_pts(1.28, 0.86, 0.34))]
    eyes = [(x + dx, y + 0.14) for dx in (-0.27, 0.27) for x, y in sample(kit.circle_pts(0.14, ry=0.17, n=24))]
    antenna = sample([(0, 0.75), (0, 1.1)], closed=False) + [(x, y + 1.13) for x, y in sample(kit.circle_pts(0.11, n=16))]
    arms = [(s * 0.85 + s * 0.15 * i / 6, -0.2 - 0.5 * i / 6) for s in (-1, 1) for i in range(7)]
    return body + screen + eyes + antenna + arms


def build(T):
    cues = []
    end = sec(kit.frames())
    t_year = T.start(0)
    t_draw0, t_draw1 = T.at(0, 0.25), T.at(0, 0.7)
    t_name = T.at(0, 0.8)
    t_one = T.start(1)
    t_job = T.at(1, 0.42)
    t_rewrite = T.at(1, 0.68)
    t_any = T.start(2)
    t_changer = T.at(2, 0.52)
    t_pip = T.start(3)
    t_only = T.at(3, 0.42)
    t_again = T.at(3, 0.66)

    kit.backdrop(seed=31, glow=kit.SKY_DEEP)
    kit.motes(seed=32, colour=kit.SKY)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the scientist and the blueprint
    sheet = kit.empty('sheet', stage, (SHEET_AT[0], SHEET_AT[1], kit.next_z(stage)))
    paper = kit.shape('sheet-paper', kit.rrect_pts(SHEET_W, SHEET_H, 0.15), kit.material('#1d3f8f', '#16307a'), sheet)
    grid = []
    for i in range(1, 16):
        grid.append(kit.shape(f'grid-v{i}', kit.rrect_pts(0.025, SHEET_H - 0.3, 0), kit.material(kit.SKY, alpha=0.18), sheet, (-SHEET_W / 2 + i * SHEET_W / 16, 0)))
    for i in range(1, 12):
        grid.append(kit.shape(f'grid-h{i}', kit.rrect_pts(SHEET_W - 0.3, 0.025, 0), kit.material(kit.SKY, alpha=0.18), sheet, (0, -SHEET_H / 2 + i * SHEET_H / 12)))
    dashes = []
    for k, (x, y) in enumerate(outline_paths()):
        d = kit.shape(f'dash{k}', kit.circle_pts(0.045, n=10), kit.material('#cfe9ff'), sheet, (x * BOT_S, y * BOT_S + 0.3))
        dashes.append(d)
    n = len(dashes)
    for k, d in enumerate(dashes):
        t0 = mix(t_draw0, t_draw1, k / n)
        alpha(d, 1, 0.0)
        alpha(d, fr(t0), 0.0)
        alpha(d, fr(t0) + 2, 1.0)
        alpha(d, fr(t_one + 0.1), 1.0)
        alpha(d, fr(t_one + 0.4), 0.0)
    for k in range(10):
        cues.append({'t': t_draw0 + (t_draw1 - t_draw0) * k / 10, 'type': 'tick', 'pitch': 0.8 + 0.04 * (k % 4), 'gain': 0.35})
    zs = sheet.location.z
    for f in every(1):
        t = sec(f)
        s = max(0.001, kit.back_out((t - t_year - 0.2) / 0.5)) * (1 - span(t, t_one + 0.2, t_one + 0.6))
        key(sheet, 'scale', f, (max(0.001, s),) * 2 + (1,))
    cues.append({'t': t_year + 0.2, 'type': 'pop', 'pitch': 0.8})

    who = kit.person('scientist', stage, (-4.6, 1.2), 0.78, coat='#8a5a3c', coat_deep='#5e3b28', hair='#c9c2b8')
    zw = who['root'].location.z
    for f in every(1):
        t = sec(f)
        x = mix(-9.5, -4.6, span(t, t_year, t_year + 0.9, kit.ease_out))
        x = mix(x, -10.5, span(t, t_one, t_one + 0.8))
        key(who['root'], 'location', f, (x, 1.2, zw))
        drawing = 1.0 if t_draw0 <= t <= t_draw1 else 0.0
        reach = 58 + span(t, t_draw0 - 0.4, t_draw0) * 12 * (1 - span(t, t_draw1, t_draw1 + 0.4))
        key(who['arm'], 'rotation_euler', f, (0, 0, math.radians(reach + drawing * 4 * math.sin(t * 9))))
        key(who['head'], 'rotation_euler', f, (0, 0, -0.06 * drawing + 0.03 * math.sin(t * 0.8)))

    year = kit.text('year', '2003', 0.62, kit.material(kit.PAPER), stage, (-6.9, 3.85), align='LEFT')
    name = kit.text('name', 'Jürgen Schmidhuber', 0.3, kit.material(kit.MIST), stage, (-6.9, 3.3), align='LEFT')
    kit.fade(year, t_year + 0.3, t_one, 0.4)
    kit.fade(name, t_year + 0.8, t_one, 0.4)
    title = kit.text('title', 'Gödel Machine', 0.6, kit.material(kit.PAPER), stage, (SHEET_AT[0], -3.25))
    kit.fade(title, t_name, t_any - 0.5, 0.5)
    cues.append({'t': t_name, 'type': 'chime', 'gain': 0.6})

    # ------------------------------------------------------------ the machine and its own code
    m = parts.pip('machine', stage, MACHINE_AT, BOT_S, body=kit.SKY, body_deep=kit.SKY_DEEP)
    p = parts.pip('pip', stage, (0, 0.2), 1.6)
    zm, zp = m['root'].location.z, p['root'].location.z
    for f in every(1):
        t = sec(f)
        x = mix(SHEET_AT[0], MACHINE_AT[0], span(t, t_one + 0.5, t_one + 1.3))
        x = mix(x, 0.0, span(t, t_pip, t_pip + 0.7))
        grow = max(0.001, kit.back_out((t - t_one - 0.2) / 0.45)) * (1 - span(t, t_pip + 0.7, t_pip + 0.95))
        key(m['root'], 'location', f, (x, mix(SHEET_AT[1] + 0.5, MACHINE_AT[1], span(t, t_one + 0.5, t_one + 1.3)), zm))
        key(m['root'], 'scale', f, (BOT_S * max(0.001, grow),) * 3)
    parts.pip_idle(m, phase=0.5)
    parts.pip_blink(m, (t_one + 2.5, t_rewrite + 1.4, t_any + 2.3))
    cues.append({'t': t_one + 0.2, 'type': 'pop'})

    code = parts.program('code', stage, CODE_AT, rows=7, w=3.4, h=4.4, seed=31)
    zc = code['root'].location.z
    for f in every(1):
        t = sec(f)
        s = max(0.001, kit.back_out((t - t_one - 1.0) / 0.45)) * (1 - span(t, t_pip, t_pip + 0.4))
        key(code['root'], 'scale', f, (max(0.001, s),) * 2 + (1,))
        key(code['root'], 'location', f, (CODE_AT[0], CODE_AT[1], zc))
    tether = []
    for k in range(12):
        x = mix(MACHINE_AT[0] + 1.7, CODE_AT[0] - 1.8, k / 11)
        d = kit.shape(f'tether{k}', kit.circle_pts(0.06, n=10), kit.material(kit.SKY, alpha=0.8), stage, (x, MACHINE_AT[1] + 0.1 * math.sin(k)))
        alpha(d, 1, 0.0)
        alpha(d, fr(t_one + 1.2 + 0.04 * k), 0.0)
        alpha(d, fr(t_one + 1.3 + 0.04 * k), 1.0)
        alpha(d, fr(t_pip), 1.0)
        alpha(d, fr(t_pip + 0.3), 0.0)
        tether.append(d)

    # the machine does its job: small programs come along, and each leaves fixed
    for k in range(5):
        t0 = t_job + 0.75 * k
        job = parts.program(f'task{k}', stage, (-9, -3.0), rows=3, w=2.0, h=1.4, seed=40 + k, mistake=1, scale=0.68)
        zj = job['root'].location.z
        t_mid = t0 + 0.7
        for f in every(1, fr(t0 - 0.1), fr(t0 + 1.6)):
            t = sec(f)
            x = mix(-9.5, MACHINE_AT[0], span(t, t0, t_mid, kit.ease_out))
            x = mix(x, 9.5, span(t, t_mid + 0.15, t0 + 1.6, lambda v: v * v))
            key(job['root'], 'location', f, (x, -3.0, zj))
        for ob in job['bad']['bars']:
            alpha(ob, fr(t_mid), 1.0)
            alpha(ob, fr(t_mid + 0.1), 0.0)
        for ob in job['good']:
            alpha(ob, fr(t_mid), 0.0)
            alpha(ob, fr(t_mid + 0.1), 1.0)
        cues.append({'t': t_mid, 'type': 'blip', 'pitch': 1.1 + 0.05 * k, 'gain': 0.5})
    parts.pip_look(m, t_job, -0.05, -0.12)

    # ... and while it works, it rewrites its own code
    parts.pip_look(m, t_rewrite - 0.3, 0.13, 0.0)
    flash = []
    for r in (1, 3, 5):
        y = code['rows'][r][0].location.y
        hl = kit.shape(f'row{r}-flash', kit.rrect_pts(3.2, 0.36, 0.18), kit.material(kit.AMBER, alpha=0.35), code['root'], (0, y), lift=-0.003)
        alpha(hl, 1, 0.0)
        flash.append((r, hl))
    import random
    rnd = random.Random(3)
    for k, (r, hl) in enumerate(flash):
        t0 = t_rewrite + 0.45 * k
        for f, a in ((fr(t0), 0.0), (fr(t0) + 3, 1.0), (fr(t0 + 0.6), 0.0)):
            alpha(hl, f, a)
        for ob in code['rows'][r]:
            ob.keyframe_insert('scale', frame=fr(t0))
            key(ob, 'scale', fr(t0) + 4, (0.001, 1, 1))
            key(ob, 'scale', fr(t0) + 9, (0.6 + 0.7 * rnd.random(), 1, 1))
        cues.append({'t': t0, 'type': 'tick', 'pitch': 1.3, 'gain': 0.6})
    parts.pip_arm(m, 'right', t_rewrite - 0.3, 80, 0.25)
    parts.pip_arm(m, 'right', t_rewrite + 1.4, 18, 0.3)

    # ------------------------------------------------------------ any part, even the part that changes
    rings = []
    spots = [(0, 1.15), (-0.95, -0.6), (0.95, -0.6), (0, 0.15)]       # antenna, hands, face (in machine units)
    for k, (dx, dy) in enumerate(spots):
        t0 = t_any + 0.35 + 0.45 * k
        ring = kit.shape(f'part-ring{k}', kit.circle_pts(0.5), kit.glow_material(kit.AMBER, 0.9, power=0.7), stage, lift=0.2)
        zr = ring.location.z
        for f in every(1, fr(t0 - 0.1), fr(t0 + 0.6)):
            t = sec(f)
            q = span(t, t0, t0 + 0.5, lambda v: v)
            key(ring, 'location', f, (MACHINE_AT[0] + dx * BOT_S, MACHINE_AT[1] + dy * BOT_S, zr))
            key(ring, 'scale', f, (0.6 + 1.6 * q,) * 2 + (1,))
            alpha(ring, f, math.sin(math.pi * q))
        alpha(ring, 1, 0.0)
        cues.append({'t': t0, 'type': 'pop', 'pitch': 1.0 + 0.1 * k, 'gain': 0.6})
        rings.append(ring)
    parts.pip_eyes(m, t_any + 1.65, 1.25, 1.25, 0.15)
    parts.pip_eyes(m, t_any + 2.1, 1.0, 1.0, 0.2)

    # the part that makes the changes: a pencil beside one line of the code, which rewrites itself
    row = 6
    y = code['rows'][row][0].location.y
    pencil = kit.empty('pencil', code['root'], (-3.4 / 2 - 0.35, y, kit.next_z(code['root'])))
    kit.shape('pencil-glow', kit.circle_pts(0.6), kit.glow_material(kit.AMBER, 0.7), pencil)
    kit.shape('pencil-body', [(-0.07, 0.24), (0.07, 0.24), (0.07, -0.12), (0, -0.26), (-0.07, -0.12)], kit.material(kit.AMBER, kit.AMBER_DEEP), pencil)
    kit.shape('pencil-tip', [(-0.035, -0.19), (0.035, -0.19), (0, -0.26)], kit.material(kit.INK900), pencil)
    pencil.rotation_euler = (0, 0, -0.6)
    pencil.scale = (0.001,) * 3
    pencil.keyframe_insert('scale', frame=1)
    pencil.keyframe_insert('scale', frame=fr(t_one + 1.2))
    key(pencil, 'scale', fr(t_one + 1.5), (1, 1, 1))
    ring = kit.shape('changer-ring', kit.rrect_pts(3.9, 0.5, 0.25), kit.material(kit.AMBER, alpha=0.4), code['root'], (-0.25, y), lift=-0.003)
    alpha(ring, 1, 0.0)
    for f in every(1, fr(t_changer - 0.1), fr(t_pip)):
        t = sec(f)
        alpha(ring, f, span(t, t_changer, t_changer + 0.3) * (1 - span(t, t_pip - 0.6, t_pip - 0.2)) * (0.75 + 0.25 * math.sin((t - t_changer) * 8)))
        spin = span(t, t_changer + 0.5, t_changer + 1.1)
        pulse = 1 + 0.5 * math.sin(math.pi * spin)
        key(pencil, 'rotation_euler', f, (0, 0, -0.6 - math.tau * spin))
        key(pencil, 'scale', f, (pulse, pulse, 1))
    for ob in code['rows'][row]:
        ob.keyframe_insert('scale', frame=fr(t_changer + 0.6))
        key(ob, 'scale', fr(t_changer + 0.75), (0.001, 1, 1))
        key(ob, 'scale', fr(t_changer + 1.0), (1.3, 1, 1))
    cues.append({'t': t_changer, 'type': 'tick', 'pitch': 0.9})
    cues.append({'t': t_changer + 0.5, 'type': 'rise', 'dur': 0.6, 'pitch': 1.2, 'gain': 0.6})

    # ------------------------------------------------------------ if Pip were a Gödel Machine
    for f in every(1):
        t = sec(f)
        s = 1.6 * max(0.001, kit.back_out((t - t_pip - 0.8) / 0.45))
        key(p['root'], 'scale', f, (s, s, s))
    parts.pip_idle(p)
    cues.append({'t': t_pip + 0.75, 'type': 'pop', 'pitch': 1.1})
    spot = kit.shape('spotlight', kit.circle_pts(4.0), kit.glow_material(kit.PAPER, 0.18, power=1.0), stage, (0, 0.2), lift=-0.01)
    alpha(spot, 1, 0.0)
    kit.fade(spot, t_only, None, 0.6)

    # one Pip, changing itself: each change ripples out from Pip, and Pip itself is a little different after it
    changes = [t_again, t_again + 0.75, t_again + 1.5]
    for k, t0 in enumerate(changes):
        ripple = kit.shape(f'ripple{k}', kit.arc_pts(1.6, 0.12, 0, 360, n=48), kit.material(kit.MINT, alpha=0.8), stage, (0, 0.2), lift=0.2)
        zr = ripple.location.z
        alpha(ripple, 1, 0.0)
        for f in every(1, fr(t0 - 0.05), fr(t0 + 0.8)):
            q = span(sec(f), t0, t0 + 0.7, lambda v: v)
            key(ripple, 'scale', f, (1 + 1.4 * q, 1 + 1.4 * q, 1))
            alpha(ripple, f, 1 - q)
        cues.append({'t': t0, 'type': 'rise', 'dur': 0.4, 'pitch': 1.0 + 0.15 * k, 'gain': 0.6})
    a = p['antenna']
    a.keyframe_insert('scale', frame=fr(changes[0]))
    key(a, 'scale', fr(changes[0]) + 5, (1.15, 1.45, 1))
    for e in p['eye_list']:
        e.keyframe_insert('scale', frame=fr(changes[1]))
        key(e, 'scale', fr(changes[1]) + 5, (1.25, 1.25, 1))
    for side in ('left', 'right'):
        sh = p['arms'][side]
        sh.keyframe_insert('scale', frame=fr(changes[2]))
        key(sh, 'scale', fr(changes[2]) + 5, (1.2, 1.3, 1))
    parts.pip_arm(p, 'right', changes[2] + 0.3, 140, 0.25)
    parts.pip_arm(p, 'left', changes[2] + 0.3, 140, 0.25)

    # ------------------------------------------------------------ camera
    def path(t):
        q = kit.smooth(t / end)
        close = span(t, t_pip, t_pip + 1.5)
        return (mix(0.1 * q, 0.0, close), 0.05 * q, kit.H0 - 0.7 * q - 3.0 * close)

    kit.camera(path, focus_z=1.0)
    return cues
