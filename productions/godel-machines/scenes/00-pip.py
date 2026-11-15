"""Scene 00: A program that fixes programs.

Pip pops in and waves. A program with a red mistake slides in; Pip spots the
mistake and fixes it. Other programs like Pip appear all around, then go. A
new program drops in, and its title bar shows Pip's own face.
"""
import math

import kit
import parts
from kit import fr, sec, span, mix, key, alpha, every

HOME = (0.0, -0.3)
WORK = (-3.7, -0.3)
CARD = (2.9, 0.15)
PIP_SCALE = 1.35

CROWD = [  # x, y, depth, scale, colour, deep colour
    (-6.3, 2.6, -2.5, 0.55, kit.SKY, kit.SKY_DEEP),
    (-3.1, 3.2, -4.0, 0.45, kit.VIOLET, kit.VIOLET_DEEP),
    (3.4, 3.1, -3.2, 0.5, kit.AMBER, kit.AMBER_DEEP),
    (6.4, 2.2, -1.5, 0.6, kit.CORAL, kit.CORAL_DEEP),
    (-6.8, -1.0, -1.0, 0.65, kit.VIOLET, kit.VIOLET_DEEP),
    (6.7, -1.4, -3.6, 0.5, kit.SKY, kit.SKY_DEEP),
    (-4.6, -3.3, 0.3, 0.6, kit.AMBER, kit.AMBER_DEEP),
    (4.4, -3.4, -0.6, 0.62, kit.MIST, kit.SLATE),
    (-0.6, 3.6, -5.0, 0.4, kit.CORAL, kit.CORAL_DEEP),
    (0.9, -3.9, -4.5, 0.42, kit.SKY, kit.SKY_DEEP),
    (-8.4, 0.9, -4.8, 0.4, kit.AMBER, kit.AMBER_DEEP),
    (8.6, 0.6, -5.2, 0.4, kit.VIOLET, kit.VIOLET_DEEP),
]


def build(T):
    cues = []
    end = sec(kit.frames())
    t_hello = T.start(0)
    t_job = T.start(1)
    t_find = T.at(1, 0.5)
    t_fix = T.at(1, 0.84)
    t_made_up = T.start(2)
    t_real = T.at(2, 0.4)
    t_crowd_out = T.end(2) + 0.05
    t_new = T.start(3)
    t_own = T.at(3, 0.56)

    kit.backdrop()
    kit.motes()
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ Pip
    p = parts.pip('pip', stage, HOME, PIP_SCALE)
    label = kit.text('pip-name', 'Pip', 0.55, kit.material(kit.PAPER), stage, (0, -2.25))
    kit.fade(label, t_hello + 0.5, t_job - 0.5)

    def pip_place(t):
        x, y = HOME
        for t0, dest in ((t_job, WORK), (t_made_up + 0.1, HOME), (t_new, WORK)):
            q = span(t, t0, t0 + 0.8)
            x, y = mix(x, dest[0], q), mix(y, dest[1], q)
        x -= 0.25 * span(t, t_own, t_own + 0.25, kit.ease_out) * (1 - 0.6 * span(t, t_own + 0.4, t_own + 1.2))
        return (x, y, p['root'].location.z)

    z_root = p['root'].location.z
    for f in every(1):
        t = sec(f)
        x, y, _ = pip_place(t)
        key(p['root'], 'location', f, (x, y, z_root))
        s = PIP_SCALE * max(0.001, kit.back_out((t - t_hello) / 0.5))
        key(p['root'], 'scale', f, (s, s, s))
    parts.pip_idle(p)
    cues.append({'t': t_hello, 'type': 'pop'})

    parts.pip_wave(p, t_hello + 0.7, t_hello + 2.6)
    parts.pip_blink(p, (3.6, t_job + 1.3, t_made_up + 1.6, t_real + 2.0, t_new + 1.1))

    # ------------------------------------------------------------ a program with a mistake
    a = parts.program('job', stage, (14, CARD[1]), rows=7, seed=4, mistake=3)
    zc = a['root'].location.z
    for f in every(1):
        t = sec(f)
        x = mix(14.0, CARD[0], span(t, t_job, t_job + 0.9, kit.ease_out))
        x = mix(x, 15.0, span(t, t_made_up, t_made_up + 0.8, lambda q: q * q))
        key(a['root'], 'location', f, (x, CARD[1], zc))
    cues.append({'t': t_job, 'type': 'whoosh'})
    cues.append({'t': t_made_up, 'type': 'whoosh', 'gain': 0.7})

    parts.pip_look(p, t_job + 0.5, 0.13, 0.0)
    for f in every(1, fr(t_job), fr(t_fix)):  # the mistake twitches until it is fixed
        t = sec(f)
        jig = 0.035 * math.sin(t * 31) * (0.5 + 0.5 * math.sin(t * 5.3))
        for ob in a['bad']['bars']:
            key(ob, 'rotation_euler', f, (0, 0, jig))
    for ob in a['bad']['bars']:
        key(ob, 'rotation_euler', fr(t_fix) + 1, (0, 0, 0))

    ring = a['bad']['ring']
    for f in every(1, fr(t_find), fr(t_fix + 0.6)):
        t = sec(f)
        on = span(t, t_find, t_find + 0.25) * (1 - span(t, t_fix, t_fix + 0.5))
        alpha(ring, f, on * (0.75 + 0.25 * math.sin((t - t_find) * 9)))
    cues.append({'t': t_find, 'type': 'tick'})
    cues.append({'t': t_find + 0.12, 'type': 'tick', 'pitch': 1.2})

    # Pip reaches out, a spark flies to the mistake, and the red bars turn mint.
    parts.pip_arm(p, 'right', t_fix - 0.55, 82, 0.25)
    hand = (WORK[0] + PIP_SCALE * 1.3, WORK[1] + PIP_SCALE * -0.27)
    target = (CARD[0] + a['bad']['x'], CARD[1] + a['bad']['y'])
    spark = kit.shape('spark', kit.star_pts(0.32, 0.08), kit.material('#eafff9'), stage, lift=0.3)
    spark_glow = kit.shape('spark-glow', kit.circle_pts(0.9), kit.glow_material(kit.MINT, 0.8), stage, lift=0.29)
    zs, zg = spark.location.z, spark_glow.location.z
    t_fly = t_fix - 0.3
    for f in every(1):
        t = sec(f)
        q = span(t, t_fly, t_fix, lambda v: v)
        x, y = mix(hand[0], target[0], q), mix(hand[1], target[1], q) + 0.9 * math.sin(math.pi * q)
        flying = 1.0 if t_fly <= t <= t_fix else 0.0
        burst = span(t, t_fix, t_fix + 0.5, kit.ease_out)
        bursting = 1.0 if t_fix < t <= t_fix + 0.6 else 0.0
        if bursting:
            x, y = target
        s = 0.001 + flying * 0.6 + bursting * (0.6 + 1.6 * burst)
        a_s = flying + bursting * (1 - burst)
        key(spark, 'location', f, (x, y, zs))
        key(spark, 'scale', f, (s, s, 1))
        key(spark, 'rotation_euler', f, (0, 0, t * 4))
        alpha(spark, f, a_s)
        key(spark_glow, 'location', f, (x, y, zg))
        key(spark_glow, 'scale', f, (s * 1.3, s * 1.3, 1))
        alpha(spark_glow, f, a_s)
    for ob in a['bad']['bars']:
        alpha(ob, fr(t_fix), 1.0)
        alpha(ob, fr(t_fix + 0.2), 0.0)
    for ob in a['good']:
        alpha(ob, fr(t_fix), 0.0)
        alpha(ob, fr(t_fix + 0.2), 1.0)
    cues.append({'t': t_fly, 'type': 'rise', 'dur': 0.3, 'pitch': 1.5, 'gain': 0.6})
    cues.append({'t': t_fix, 'type': 'chime'})

    parts.pip_arm(p, 'right', t_fix + 0.35, 150, 0.2)       # a small cheer
    parts.pip_eyes(p, t_fix + 0.1, 1.1, 0.55)                # happy squint
    parts.pip_arm(p, 'right', t_made_up - 0.2, 18, 0.35)
    parts.pip_eyes(p, t_made_up - 0.1, 1.0, 1.0)
    parts.pip_look(p, t_made_up + 0.2, 0.0, 0.0)

    # ------------------------------------------------------------ other programs like Pip
    for i, (x, y, z, sc, col, deep) in enumerate(CROWD):
        lay = kit.layer(f'crowd{i}', z)
        bot = parts.pip(f'bot{i}', lay, (x, y), sc, body=col, body_deep=deep)
        t_in = t_real + 0.09 * i
        zb = bot['root'].location.z
        for f in every(1, fr(t_real - 0.2), fr(t_crowd_out + 0.8)):
            t = sec(f)
            grow = kit.back_out((t - t_in) / 0.45) * (1 - span(t, t_crowd_out + 0.04 * i, t_crowd_out + 0.04 * i + 0.35))
            s = sc * max(0.001, grow)
            key(bot['root'], 'scale', f, (s, s, s))
        bot['root'].scale = (0.001,) * 3
        bot['root'].keyframe_insert('scale', frame=1)
        key(bot['root'], 'location', fr(t_real), (x, y, zb))
        key(bot['root'], 'location', fr(t_crowd_out + 0.8), (x + 0.25 * (1 if x > 0 else -1), y + 0.15, zb))
        parts.pip_idle(bot, t_real - 0.2, t_crowd_out + 0.8, phase=i * 0.7, step=3)
        parts.pip_look(bot, t_in + 0.5, -0.06 if x > 0 else 0.06, -0.03 if y > 0 else 0.03)
        if i % 3 == 1:
            parts.pip_wave(bot, t_in + 0.6, t_in + 1.8, rate=8 + i % 4)
        cues.append({'t': t_in, 'type': 'blip', 'pitch': 0.8 + 0.06 * (i % 7), 'gain': 0.45})
    parts.pip_look(p, t_real + 0.5, -0.12, 0.05)
    parts.pip_look(p, t_real + 1.6, 0.12, 0.05)
    parts.pip_look(p, t_crowd_out, 0.0, 0.0)

    # ------------------------------------------------------------ a new program: Pip's own code
    b = parts.program('own', stage, (CARD[0], 10), rows=7, seed=9, tab_icon=True)
    zb = b['root'].location.z
    for f in every(1):
        t = sec(f)
        y = mix(10.0, CARD[1], span(t, t_new, t_new + 0.9, kit.back_out))
        key(b['root'], 'location', f, (CARD[0], y, zb))
    cues.append({'t': t_new, 'type': 'whoosh'})
    parts.pip_look(p, t_new + 0.6, 0.13, 0.03)

    icon = b['icon']
    for f in every(1):
        t = sec(f)
        s = max(0.001, kit.back_out((t - t_own) / 0.45))
        pulse = 1 + 0.12 * math.sin((t - t_own) * 5) * span(t, t_own + 0.5, t_own + 1.0)
        key(icon, 'scale', f, (s * pulse,) * 3)
    cues.append({'t': t_own, 'type': 'pop', 'pitch': 1.3})
    cues.append({'t': t_own + 0.15, 'type': 'rise', 'dur': 1.2, 'pitch': 0.8, 'gain': 0.7})

    parts.pip_eyes(p, t_own + 0.15, 1.35, 1.35, 0.15)        # Pip sees its own face
    parts.pip_look(p, t_own + 0.15, 0.15, 0.06, 0.15)
    for f in every(1, fr(t_own), fr(t_own + 0.8)):
        t = sec(f)
        flash = 1 + 0.9 * math.sin(math.pi * span(t, t_own + 0.1, t_own + 0.7, lambda v: v))
        key(p['bulb_glow'], 'scale', f, (flash, flash, 1))
    key(p['mouth'], 'scale', fr(t_own + 0.1), (1, 1, 1))
    key(p['mouth'], 'scale', fr(t_own + 0.3), (0.6, 0.6, 1))

    # ------------------------------------------------------------ camera
    def path(t):
        p_all = kit.smooth(t / end)
        push = span(t, t_own, end + 0.5)
        x = -0.25 + 0.4 * p_all + mix(0, -0.5, push)
        y = 0.05 * p_all
        z = kit.H0 - 0.8 * p_all - 3.2 * push
        return (x, y, z)

    kit.camera(path, focus_z=1.0)
    return cues
