"""Scene 02: Better at getting better.

Pip and its own code sit at the two ends of a loop. An idea travels from Pip
into the code, and the better code comes back as a better Pip. Each lap runs
faster and lifts the meter under Pip by more than the last one.
"""
import math

import kit
import parts
from kit import fr, sec, span, mix, key, alpha, every

PIP_AT = (-4.4, 0.2)
CODE_AT = (4.4, 0.2)
R = 2.84                       # radius of both arcs of the loop
TOP_C = (0.0, 0.16)            # centre of the upper arc (Pip to code)
BOT_C = (0.0, 0.24)            # centre of the lower arc (code back to Pip)
A0, A1 = 156.3, 23.7           # the upper arc runs from A0 down to A1 degrees
STEPS = 14                     # bars in the meter


def on_loop(q):
    """Point on the loop: q from 0 to 0.5 crosses the top arc to the code, 0.5 to 1 comes back."""
    if q < 0.5:
        a = math.radians(mix(A0, A1, q / 0.5))
        return TOP_C[0] + R * math.cos(a), TOP_C[1] + R * math.sin(a)
    a = math.radians(mix(-A1, -A0, (q - 0.5) / 0.5))
    return BOT_C[0] + R * math.cos(a), BOT_C[1] + R * math.sin(a)


def arrowhead(name, parent, tip, angle, mat):
    pts = [(0.0, 0.0), (-0.42, 0.22), (-0.42, -0.22)]
    c, s = math.cos(angle), math.sin(angle)
    return kit.shape(name, [(x * c - y * s, x * s + y * c) for x, y in pts], mat, parent, tip)


def build(T):
    cues = []
    end = sec(kit.frames())
    t_idea = T.at(0, 0.2)
    t_write = T.at(0, 0.66)
    t_back = T.start(1)
    t_own = T.at(1, 0.62)
    t_title = T.start(4) + 0.1
    t_result = T.at(4, 0.6)

    kit.backdrop(seed=21)
    kit.motes(seed=22, colour=kit.AMBER)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the loop
    loop_mat = kit.material(kit.MIST, alpha=0.55)
    top = kit.shape('arc-top', kit.arc_pts(R, 0.09, A1 + 4, A0 - 4), loop_mat, stage, TOP_C)
    bot = kit.shape('arc-bottom', kit.arc_pts(R, 0.09, -A0 + 4, -A1 - 4), loop_mat, stage, BOT_C)
    # Both arcs run with falling angle, so each arrow points along angle - 90 degrees at the arc's end.
    a_top, a_bot = math.radians(A1 + 4), math.radians(-A0 + 4)
    tip_top = (TOP_C[0] + R * math.cos(a_top), TOP_C[1] + R * math.sin(a_top))
    tip_bot = (BOT_C[0] + R * math.cos(a_bot), BOT_C[1] + R * math.sin(a_bot))
    head_top = arrowhead('head-top', stage, tip_top, a_top - math.pi / 2, loop_mat)
    head_bot = arrowhead('head-bottom', stage, tip_bot, a_bot - math.pi / 2, loop_mat)
    hot = kit.shape('arc-bottom-hot', kit.arc_pts(R, 0.16, -A0 + 4, -A1 - 4), kit.material(kit.AMBER), stage, BOT_C)
    alpha(hot, 1, 0.0)
    for ob, t0 in ((top, t_write - 0.3), (head_top, t_write - 0.3), (bot, t_back - 0.3), (head_bot, t_back - 0.3)):
        kit.fade(ob, t0, None, 0.4)
    for f in every(1, fr(t_result - 0.2), fr(t_result + 2.6)):
        t = sec(f)
        alpha(hot, f, span(t, t_result, t_result + 0.3) * (1 - span(t, t_result + 2.0, t_result + 2.5)) * (0.7 + 0.3 * math.sin((t - t_result) * 8)))

    # ------------------------------------------------------------ Pip and Pip's code
    p = parts.pip('pip', stage, PIP_AT, 1.15)
    parts.pip_idle(p)
    parts.pip_blink(p, (2.6, 9.2, 14.2, 21.0, 24.5))
    parts.pip_look(p, 0.3, 0.1, 0.03)
    code_glow = kit.shape('code-glow', kit.rrect_pts(4.6, 5.2, 1.5), kit.glow_material(kit.AMBER, 0.7, power=1.2), stage, CODE_AT)
    alpha(code_glow, 1, 0.0)
    code = parts.program('code', stage, CODE_AT, rows=6, w=3.0, h=3.6, seed=14, tab_icon=True, scale=0.85)

    # ------------------------------------------------------------ the meter under Pip
    lit = []
    for i in range(STEPS):
        h = 0.18 + 0.075 * i
        x = PIP_AT[0] - 1.75 + i * 0.25
        pts = [(px, py + h / 2) for px, py in kit.rrect_pts(0.17, h, 0.06)]
        kit.shape(f'step{i}', pts, kit.material(kit.INK600), stage, (x, -2.75))
        on = kit.shape(f'step{i}-on', pts, kit.material(kit.AMBER, kit.AMBER_DEEP), stage, (x, -2.75))
        lit.append(on)

    # ------------------------------------------------------------ the laps
    # Each lap: an idea goes from Pip to the code (first half) and comes back (second half).
    laps = [(t_write, t_write + 0.9, t_back, t_back + 0.9)]      # the first lap is told slowly
    t = T.start(2)
    for dur in (1.7, 1.3):
        laps.append((t, t + dur / 2, t + dur / 2, t + dur))
        t += dur + 0.6
    t = max(t, T.start(3))
    for dur in (1.0, 0.8, 0.65, 0.55):
        laps.append((t, t + dur / 2, t + dur / 2, t + dur))
        t += dur + 0.12
    t = max(t, T.start(4) + 0.4)
    while t + 0.6 < end - 0.2:
        laps.append((t, t + 0.3, t + 0.3, t + 0.6))
        t += 0.75
    gains = [1, 2, 3, 4, 3]                                         # bars each lap lights
    level = [1]
    for g in gains:
        level.append(min(STEPS, level[-1] + g))
    while len(level) < len(laps) + 1:
        level.append(STEPS)

    def where(t):
        """Spark position and whether it shows, at time t."""
        for a0, a1, b0, b1 in laps:
            if a0 <= t <= a1:
                return on_loop(0.5 * (t - a0) / (a1 - a0)), 1.0
            if b0 <= t <= b1:
                return on_loop(0.5 + 0.5 * (t - b0) / (b1 - b0)), 1.0
            if a1 < t < b0:
                return on_loop(0.5), 0.0
        return on_loop(0.0), 0.0

    sparks = []
    for k, (size, lag) in enumerate(((1.0, 0.0), (0.7, 0.045), (0.5, 0.09), (0.35, 0.135))):
        s_ob = kit.shape(f'spark{k}', kit.star_pts(0.28 * size, 0.08 * size), kit.material('#fff3cf'), stage, lift=0.3)
        g_ob = kit.shape(f'spark{k}-glow', kit.circle_pts(0.8 * size), kit.glow_material(kit.AMBER, 0.8), stage, lift=0.29)
        sparks.append((s_ob, g_ob, lag))
    for f in every(1):
        t = sec(f)
        for s_ob, g_ob, lag in sparks:
            (x, y), on = where(t - lag)
            if lag == 0 and t_idea <= t < t_write:          # the idea first appears over Pip's head
                q = span(t, t_idea, t_idea + 0.35, kit.back_out)
                x, y, on = PIP_AT[0] + 0.1, PIP_AT[1] + 2.0 + 0.08 * math.sin(t * 4), q
            key(s_ob, 'location', f, (x, y, s_ob.location.z))
            key(g_ob, 'location', f, (x, y, g_ob.location.z))
            key(s_ob, 'rotation_euler', f, (0, 0, t * 3))
            alpha(s_ob, f, on)
            alpha(g_ob, f, on)
    cues.append({'t': t_idea, 'type': 'pop', 'pitch': 1.4})

    # arrivals: the code glows; returns: Pip pulses and the meter climbs
    z_root = p['root'].location.z
    grow = []
    for k, (a0, a1, b0, b1) in enumerate(laps):
        for f, a in ((fr(a1) - 2, 0.0), (fr(a1), 0.9), (fr(a1 + 0.5), 0.0)):
            alpha(code_glow, f, a)
        cues.append({'t': a1, 'type': 'tick', 'pitch': 1.0 + 0.05 * min(k, 8), 'gain': 0.7})
        cues.append({'t': b1, 'type': 'blip', 'pitch': 0.9 + 0.08 * min(k, 8), 'gain': 0.6})
        before, after = level[k], level[k + 1]
        for i in range(before, after):
            alpha(lit[i], fr(b1) - 1, 0.0)
            alpha(lit[i], fr(b1 + 0.05 * (i - before)) + 2, 1.0)
        grow.append(b1)
    for i in range(STEPS):
        if i < level[0]:
            alpha(lit[i], 1, 1.0)
        elif not lit[i].animation_data:
            alpha(lit[i], 1, 0.0)
    for f in every(1):
        t = sec(f)
        n = sum(1 for b in grow if b <= t)
        pulse = sum(0.12 * math.exp(-(t - b) * 7) for b in grow if b <= t)
        s = 1.15 * (1 + 0.03 * min(n, 6)) * (1 + pulse)
        key(p['root'], 'scale', f, (s, s, s))
    cues.append({'t': laps[0][3], 'type': 'chime', 'gain': 0.8})

    parts.pip_look(p, t_write - 0.2, 0.13, 0.05)
    parts.pip_look(p, t_back + 0.3, 0.0, 0.0)
    parts.pip_eyes(p, laps[0][3], 1.1, 0.6)                   # pleased
    parts.pip_eyes(p, laps[0][3] + 1.0, 1.0, 1.0)
    parts.pip_look(p, t_own - 0.2, 0.13, 0.03)
    icon = code['icon']
    for f in every(1, fr(t_own), fr(t_own + 1.0)):
        q = span(sec(f), t_own, t_own + 1.0, lambda v: v)
        s = 1 + 0.5 * math.sin(math.pi * q)
        key(icon, 'scale', f, (s, s, 1))
    cues.append({'t': t_own, 'type': 'pop', 'pitch': 1.2, 'gain': 0.6})
    parts.pip_look(p, T.start(2), 0.06, 0.06)

    # ------------------------------------------------------------ the name
    title = kit.text('title', 'recursive self-improvement', 0.62, kit.material(kit.PAPER), stage, (0, 3.75))
    kit.fade(title, t_title, None, 0.6)
    cues.append({'t': t_title, 'type': 'swoosh', 'gain': 0.5})

    # ------------------------------------------------------------ camera
    def path(t):
        q = kit.smooth(t / end)
        push = span(t, T.start(3), T.start(4))
        return (0.0, 0.1 * q, kit.H0 - 0.6 * q - 1.0 * push + 1.0 * span(t, T.start(4), T.start(4) + 1.5))

    kit.camera(path, focus_z=1.0)
    return cues
