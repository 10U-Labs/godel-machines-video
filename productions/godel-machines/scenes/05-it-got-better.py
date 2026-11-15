"""Scene 05: It got better.

The first program stands over a board of a hundred problems, and twenty of
them light up. A trail of eighty steps climbs to its best descendant, which
stands over its own board, where fifty light up.
"""
import math

import kit
import parts
from kit import fr, sec, span, mix, key, alpha, every

FIRST_AT = (-4.6, 1.3)
BEST_AT = (4.6, 1.6)
CELL, GAP = 0.24, 0.06


def board(name, stage, centre, solved, t0, dur, colour):
    """A ten-by-ten board of problems; the first `solved` cells light up one by one from t0."""
    pitch = CELL + GAP
    lit = []
    for i in range(100):
        r, c = divmod(i, 10)
        at = (centre[0] + (c - 4.5) * pitch, centre[1] + (4.5 - r) * pitch)
        kit.shape(f'{name}-cell{i}', kit.rrect_pts(CELL, CELL, 0.05), kit.material(kit.INK600), stage, at)
        if i < solved:
            on = kit.shape(f'{name}-on{i}', kit.rrect_pts(CELL, CELL, 0.05), kit.material(*colour), stage, at)
            t = t0 + dur * i / max(1, solved - 1)
            alpha(on, 1, 0.0)
            alpha(on, fr(t), 0.0)
            alpha(on, fr(t) + 2, 1.0)
            lit.append(on)
    return lit


def build(T):
    kit.state['zstep'] = 0.0005
    cues = []
    end = sec(kit.frames())
    t_first = T.start(0)
    t_solve = T.at(0, 0.55)
    t_rounds0, t_rounds1 = T.start(1), T.at(1, 0.45)
    t_best = T.at(1, 0.5)
    t_fifty = T.at(1, 0.68)

    kit.backdrop(seed=51, glow=kit.MINT_DEEP)
    kit.motes(seed=52, colour=kit.AMBER)
    stage = kit.layer('stage', 1.0)

    first = parts.pip('first', stage, FIRST_AT, 1.0, *parts.score_colour(20))
    kit.pop(first['root'], t_first - 0.4, 1.0)
    parts.pip_idle(first, step=2)
    parts.pip_blink(first, (2.0, 5.5, 8.0))
    parts.pip_look(first, t_solve - 0.3, 0.0, -0.1)
    parts.pip_look(first, t_best + 0.2, 0.13, 0.05)
    cues.append({'t': max(0.05, t_first - 0.4), 'type': 'pop'})

    board('first', stage, (FIRST_AT[0], -2.0), 20, t_solve, 0.9, (kit.MINT, kit.MINT_DEEP))
    for k in range(5):
        cues.append({'t': t_solve + 0.2 * k, 'type': 'tick', 'pitch': 1.0 + 0.05 * k, 'gain': 0.4})
    n20 = kit.text('first-count', '20', 0.5, kit.material(kit.MINT), stage, (FIRST_AT[0] - 2.3, -2.0), face='JetBrainsMono')
    kit.appear(n20, t_solve + 0.9, None, 0.3)

    # eighty rounds: a trail of steps climbing from the first program to the best one
    steps = []
    for k in range(80):
        q = k / 79
        x = mix(FIRST_AT[0] + 1.3, BEST_AT[0] - 1.5, q)
        y = mix(FIRST_AT[1] + 0.6, BEST_AT[1] + 0.4, q) + 1.6 * math.sin(math.pi * q)
        dot = kit.shape(f'step{k}', kit.circle_pts(0.05 + 0.03 * q, n=12), kit.material(kit.AMBER if k % 10 == 9 else kit.MIST), stage, (x, y))
        t = mix(t_rounds0, t_rounds1, q ** 0.8)
        alpha(dot, 1, 0.0)
        alpha(dot, fr(t), 0.0)
        alpha(dot, fr(t) + 2, 1.0)
        steps.append(dot)
    cues.append({'t': t_rounds0, 'type': 'rise', 'dur': t_rounds1 - t_rounds0, 'pitch': 1.0, 'gain': 0.5})

    best = parts.pip('best', stage, BEST_AT, 1.25, *parts.score_colour(50))
    kit.pop(best['root'], t_best, 1.25)
    parts.pip_idle(best, phase=1.1, step=2)
    parts.pip_blink(best, (t_best + 1.2,))
    alpha(best['halo'], 1, 1.0)
    cues.append({'t': t_best, 'type': 'pop', 'pitch': 1.3})
    parts.pip_look(best, t_fifty - 0.3, 0.0, -0.1)
    parts.pip_arm(best, 'right', t_fifty + 1.0, 140, 0.3)
    parts.pip_arm(best, 'left', t_fifty + 1.0, 140, 0.3)

    board('best', stage, (BEST_AT[0], -2.0), 50, t_fifty, 1.1, (kit.AMBER, kit.AMBER_DEEP))
    for k in range(6):
        cues.append({'t': t_fifty + 0.2 * k, 'type': 'tick', 'pitch': 1.2 + 0.05 * k, 'gain': 0.4})
    n50 = kit.text('best-count', '50', 0.5, kit.material(kit.AMBER), stage, (BEST_AT[0] + 2.3, -2.0), face='JetBrainsMono')
    kit.appear(n50, t_fifty + 1.1, None, 0.3)
    cues.append({'t': t_fifty + 1.1, 'type': 'chime', 'gain': 0.6})

    def path(t):
        q = kit.smooth(t / end)
        return (mix(-1.2, 1.0, q), 0.1, kit.H0 + 0.6 - 0.8 * q)

    kit.camera(path, focus_z=1.0)
    return cues
