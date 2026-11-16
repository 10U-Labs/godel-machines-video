"""Scene 07: Nobody told him to.

The study. The scientist writes at his desk, far from the AI on the right,
which fixes the small programs brought to it. A dotted outline shows around
its program, bigger than it is: the better version of itself. Nobody goes
near it. It rewrites its own lines and grows to fill the outline, its
computer grows arms, and it fixes the small programs faster. The scientist
writes that down. Then the lab from the start of the film, with nobody in
it. Ultron talks, the dotted outline of a body shows beside him, and the
machines' lamps turn red. At the last word every light goes out. After a
moment of dark, his two red eyes open in it.
"""
import kit
import parts
from kit import alpha, mix, sec, span


def build(T):
    cues = []
    end = sec(kit.frames())
    t_write0, t_write1 = T.at(0, 0.02), T.at(0, 0.4)
    t_job = T.at(0, 0.52)
    t_better = T.at(1, 0.26)
    t_become = T.at(1, 0.57)
    t_grown = t_become + 1.6
    t_wrote = T.start(2)
    t_lab = T.start(3) - 0.2
    t_ask = T.at(3, 0.52)
    t_stir = T.at(3, 0.86)
    t_black = T.end(3) + 0.3
    t_eyes = t_black + 1.9

    # No motes drift in front of this scene: its last seconds are dark.
    parts.backdrop(seed=81)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the study: an AI, and nobody telling it what to do
    st = parts.study(far, stage)
    parts.cut(st['roots'], None, t_lab)
    front, who, ai = st['front'], st['who'], st['ai']
    pg, box = ai['program'], ai['computer']
    bx, by = ai['at']
    alpha(box['beam'], 1, 1.0)
    parts.drift(pg['root'])
    parts.blink(pg['eyes'], (t_job + 0.4, t_better + 1.7, t_grown + 1.0))
    parts.nod(who, 0.0, t_lab, 0.4)
    parts.write(who, t_write0, t_write1)
    for k in range(4):
        cues.append({'t': mix(t_write0, t_write1, k / 4), 'type': 'tick', 'pitch': 0.9 + 0.05 * (k % 3), 'gain': 0.3})

    # what it is trying to do
    turns = [(t_job + 1.8 * k, 1.0) for k in range(4)]
    when = t_grown + 0.2
    while when < t_lab - 1.3:
        turns.append((when, 1.8))
        when += 0.95
    for k, (t0, pace) in enumerate(turns):
        t_fix = parts.errand(f'task{k}', front, t0, ai['bench'], True, pace, seed=k)
        parts.pulse(f'fixed{k}', front, ai['bench'], t_fix, 0.6, parts.FROST, 0.5, 0.05)
        cues.append({'t': t_fix, 'type': 'blip', 'pitch': 1.0 + 0.04 * k, 'gain': 0.45})

    # a better version of it
    grown = 0.94
    ahead = parts.dotted_sheet('better', front, (bx, by + 4.3), scale=grown)
    parts.drift(ahead['root'])
    parts.visible(ahead['shapes'], [(t_better, t_grown - 0.2)], 0.4)
    parts.look(pg['eyes'], t_better + 0.3, 0.0, 0.06)
    parts.look(pg['eyes'], t_become, 0.0, 0.0)
    cues.append({'t': t_better, 'type': 'rise', 'dur': 0.8, 'pitch': 1.1, 'gain': 0.5})

    # it becomes that version, and nobody told it to
    for k, r in enumerate((1, 3, 4)):
        t0 = t_become + 0.25 * k
        parts.rewrite(pg, r, t0)
        cues.append({'t': t0, 'type': 'tick', 'pitch': 1.3 + 0.1 * k, 'gain': 0.6})
    parts.resize(pg['root'], t_become + 0.3, ai['size'], grown, 1.0)
    for k, t0 in enumerate(parts.arms('new-arm', box, ai['at'], front, t_become + 0.8, gap=0.4, t1=t_lab)):
        cues.append({'t': t0, 'type': 'pop', 'pitch': 0.7 + 0.15 * k})
    parts.pulse('became', front, (bx, by + 4.3), t_grown - 0.2, 2.3, parts.FROST, 1.0, 0.06)
    cues.append({'t': t_grown - 0.2, 'type': 'chime', 'gain': 0.5})

    # he wrote that down
    parts.write(who, t_wrote - 0.6, T.end(2) - 0.4)
    for k in range(4):
        cues.append({'t': mix(t_wrote - 0.6, T.end(2) - 0.4, k / 4), 'type': 'tick', 'pitch': 0.9 + 0.05 * (k % 3), 'gain': 0.3})

    # ------------------------------------------------------------ the lab: nobody told Ultron to build a body
    lab = parts.first_lab(far, stage)
    parts.cut(lab['roots'], t_lab, None)
    parts.dip([t_lab])
    cues.append({'t': t_lab - 0.2, 'type': 'whoosh', 'gain': 0.6})
    room = lab['front']
    sx, sy = lab['spot']
    alpha(lab['console']['beam'], 1, 1.0)
    u = parts.presence('ultron', room, (sx, sy))
    parts.hover(u, t_lab, t_black + 0.5)
    parts.blink(u['eyes'], (t_lab + 1.5,))
    parts.talk(u, t_ask, T.at(3, 0.76), seed=3)
    for k in range(3):
        cues.append({'t': mix(t_ask, T.at(3, 0.76), k / 3), 'type': 'tick', 'pitch': 0.8 + 0.1 * k, 'gain': 0.35})
    ghost = parts.outline('ghost', room, (sx + 2.7, parts.FLOOR + 3.2), 0.8, parts.ASH, 1.0)
    parts.visible(ghost['shapes'], [(t_ask + 0.15, None)], 0.4)
    parts.look(u['eyes'], t_ask + 0.3, 0.13, -0.03)
    for k, m in enumerate(lab['machines']):
        t0 = t_stir + 0.3 * k
        parts.light(m, t0)
        parts.work(m, t0, t_black + 0.5, sh=(0, 16), el=(-14, 10), rate=0.8)
        cues.append({'t': t0, 'type': 'pop', 'pitch': 0.7 + 0.1 * k})

    # ------------------------------------------------------------ dark, and then his eyes
    cam_lab = (-2.2, 0.4, 17.4)
    night = parts.dark(stage, t_black)
    cues.append({'t': t_black, 'type': 'pop', 'pitch': 0.3, 'gain': 0.7})
    last = parts.presence('last', night, (cam_lab[0], cam_lab[1] + 0.15), 2.2)
    for bar in last['bars']:
        alpha(bar, 1, 0.0)
    parts.lit(last['halo'], [(0.0, 0.0), (t_eyes, 0.0), (t_eyes + 1.6, 0.35)])
    parts.visible(last['eyes']['shapes'], [(t_eyes, None)], 0.3)
    parts.open_eyes(last['eyes'], t_eyes + 0.05, 0.6)
    parts.hover(last, t_eyes, end)
    cues.append({'t': t_eyes, 'type': 'rise', 'dur': 1.4, 'pitch': 0.5, 'gain': 0.8})

    # ------------------------------------------------------------ camera
    def path(t):
        if t < t_lab:
            pos = mix((-1.0, 0.3, 19.9), (2.2, 0.4, 17.2), span(t, t_job - 0.6, t_job + 0.9))
            return mix(pos, (-3.6, 0.2, 17.0), span(t, t_wrote - 0.6, t_wrote + 0.6))
        pos = mix((-0.6, 0.3, 20.2), cam_lab, span(t, t_lab, T.end(3)))
        return mix(pos, (cam_lab[0], cam_lab[1], 15.4), span(t, t_eyes, end))

    kit.camera(path, focus_z=1.0)
    return cues
