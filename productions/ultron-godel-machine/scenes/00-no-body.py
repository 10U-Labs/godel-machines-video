"""Scene 00: A program with no body.

A lab at night, with nobody in it. Over a console a pair of red eyes opens:
a program has started up. It talks, and beside it stands the dotted outline
of the body it does not have. Then the story goes back: two people work at
the console, cannot get the program to start, and leave for a party. In the
empty lab it starts by itself. It looks for someone to build it a body, finds
nobody, and turns to the machines.
"""
import kit
import parts
from kit import alpha, fr, key, mix, sec, span


def build(T):
    cues = []
    end = sec(kit.frames())
    t_on = T.at(0, 0.08)
    t_talk0, t_talk1 = T.at(0, 0.42), T.at(0, 0.68)
    t_nobody = T.at(0, 0.8)
    t_ask = T.start(1)
    t_name = T.at(2, 0.1)
    t_back = T.start(3) - 0.2
    t_leave = T.at(4, 0.28)
    t_gone = T.at(4, 0.56)
    t_start = T.at(4, 0.76)
    t_want = T.start(5)
    t_alone = T.at(5, 0.28)
    t_self = T.at(5, 0.7)

    parts.backdrop(seed=11)
    kit.motes(n=12, seed=12, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    lab = parts.first_lab(far, stage)
    sx, sy = lab['spot']

    # ------------------------------------------------------------ the two who try to make the program
    day = parts.spot('day', far, (-1.0, 1.0), 10.0, parts.STEEL100, 0.1)
    door = parts.spot('door', stage, (-9.6, parts.FLOOR + 2.2), 2.8, parts.WARM, 0.34)
    parts.visible([day, door], [(t_back, t_gone + 0.2)], 0.6)
    makers = kit.empty('makers', stage)
    one = parts.figure('maker-one', makers, (-7.5, parts.FLOOR), coat='#7d3b3b', coat_deep='#552525')
    two = parts.figure('maker-two', makers, (-6.2, parts.FLOOR), coat='#5d5a78', coat_deep='#403e57', hair='#4a3a2e')
    parts.cut([makers], t_back, t_gone + 0.3)
    for who, phase in ((one, 0.0), (two, 1.3)):
        parts.nod(who, t_back, t_leave, phase)
        parts.reach(who, t_back + 0.4 + phase * 0.3, 62)
        parts.reach(who, t_leave - 0.2, 0)
    parts.turn(one, t_leave + 0.1)
    parts.turn(two, t_leave + 0.4)
    parts.stroll(one, t_leave + 0.1, t_gone - 0.2, -7.5, -11.5)
    parts.stroll(two, t_leave + 0.4, t_gone + 0.2, -6.2, -11.5)
    attempt = kit.ring('attempt', stage, (sx, sy), 0.5, parts.ASH, 0.06)
    tries = [mix(t_back + 0.9, t_leave - 1.2, k / 3) for k in range(4)]
    for k, t0 in enumerate(tries):
        for dt, a, s in ((0.0, 0.0, 0.5), (0.25, 0.8, 1.0), (0.6, 0.3, 0.9), (0.8, 0.7, 1.0), (1.1, 0.0, 0.3)):
            alpha(attempt, fr(t0 + dt), a)
            key(attempt, 'scale', fr(t0 + dt), (s, s, 1))
        cues.append({'t': t0 + 0.25, 'type': 'blip', 'pitch': 0.9 - 0.08 * k, 'gain': 0.5})
    parts.dip([t_back])
    cues.append({'t': t_back - 0.2, 'type': 'whoosh', 'gain': 0.6})
    cues.append({'t': t_leave + 0.2, 'type': 'swoosh', 'gain': 0.5})

    # ------------------------------------------------------------ Ultron, with no body
    u = parts.presence('ultron', stage, (sx, sy))
    parts.hover(u)
    spans = [(t_on, t_back - 0.35), (t_start, None)]
    parts.visible(u['shapes'] + [lab['console']['beam']], spans, 0.5)
    for t0 in (t_on, t_start):
        parts.open_eyes(u['eyes'], t0 + 0.1)
        cues.append({'t': t0, 'type': 'rise', 'dur': 1.0, 'pitch': 0.7, 'gain': 0.7})
    parts.blink(u['eyes'], (t_on + 2.3, t_ask + 2.0, t_name + 2.6, t_want + 1.2, t_self + 1.6))
    parts.talk(u, t_talk0, t_talk1, seed=1)
    parts.talk(u, T.at(1, 0.1), T.at(1, 0.9), seed=2)
    for k in range(3):
        cues.append({'t': mix(t_talk0, t_talk1, k / 3), 'type': 'tick', 'pitch': 0.8 + 0.1 * k, 'gain': 0.35})
        cues.append({'t': T.at(1, 0.15 + 0.25 * k), 'type': 'tick', 'pitch': 1.0 - 0.1 * k, 'gain': 0.35})

    ghost = parts.outline('ghost', stage, (sx + 2.7, parts.FLOOR + 3.2), 0.8, parts.ASH, 1.0)
    parts.visible(ghost['shapes'], [(t_nobody, T.end(1) + 0.2), (t_want + 0.2, t_alone + 1.0)], 0.4)
    cues.append({'t': t_nobody, 'type': 'tick', 'gain': 0.5})
    parts.look(u['eyes'], t_nobody + 0.3, 0.13, -0.03)
    parts.look(u['eyes'], T.end(1), 0.0, 0.0)
    parts.look(u['eyes'], t_want + 0.2, 0.13, -0.03)
    parts.look(u['eyes'], t_alone, -0.12, 0.0)
    parts.look(u['eyes'], t_alone + 0.9, 0.13, 0.0)
    parts.look(u['eyes'], t_self, 0.14, 0.05)

    label = kit.text('name', 'Ultron', 0.5, kit.material(parts.BONE), stage, (sx, sy + 1.25))
    kit.fade(label, t_name, t_back - 0.6)

    # ------------------------------------------------------------ he turns to the machines
    plan = parts.outline('plan', stage, (lab['stand'][0], parts.FLOOR + 3.25), 0.8)
    parts.visible(plan['shapes'], [(t_self + 0.5, None)], 0.6)
    for k, m in enumerate(lab['machines']):
        parts.work(m, t_self + 0.3 + 0.25 * k, end, sh=(0, 14), el=(-12, 10), rate=0.9)
        cues.append({'t': t_self + 0.3 + 0.25 * k, 'type': 'tick', 'pitch': 0.7, 'gain': 0.5})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((-1.5, 0.2, 19.5), (-3.2, 0.5, 15.4), span(t, 0.0, T.end(2)))
        if t >= t_back:
            pos = mix((-2.2, 0.0, 19.0), (-1.6, 0.0, 18.5), span(t, t_back, t_gone))
            pos = mix(pos, (-3.2, 0.4, 15.4), span(t, t_start, t_want))
            pos = mix(pos, (0.4, 0.2, 19.6), span(t, t_alone, end))
        return pos

    kit.camera(path, focus_z=1.0)
    return cues
