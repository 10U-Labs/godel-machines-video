"""Scene 01: What it means.

The question mark over Ultron's three forms turns into a tick: yes. Then the
computer scientist's study. On the right a program shows above a computer: a
sheet of its code, with eyes. The scientist writes at his desk. The program
rewrites two lines of its code, and then the computer under it grows a pair
of arms: the two ways it can change itself. Small programs with a mistake in
them are brought to it to fix. After one change it sends a mistake back
unfixed; after another it fixes them faster than before.
"""
import kit
import parts
from kit import mix, sec, span


def build(T):
    cues = []
    end = sec(kit.frames())
    t_yes = T.at(0, 0.05)
    t_study = T.at(0, 0.45)
    t_program = T.start(1) - 0.1
    t_machine = T.at(1, 0.55)
    t_write0, t_write1 = T.at(2, 0.04), T.at(2, 0.44)
    t_code = T.at(2, 0.53)
    t_body = T.at(2, 0.76)
    t_job = T.start(3) - 0.75
    t_worse = T.at(3, 0.1)
    t_better = T.at(3, 0.42)
    t_named = T.at(3, 0.74)

    parts.backdrop(seed=21)
    kit.motes(n=12, seed=22, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ the answer, over his three forms
    hall = parts.room('hall', far, stage, lamps=(-5.4, -1.9, 2.4), glow=0.05)
    parts.cut(hall, None, t_study)
    near = hall[1]
    forms = parts.three_forms(near)
    for k, (x, _) in enumerate(parts.FORMS):
        pool = parts.spot(f'pool{k}', forms['root'], (x, parts.FLOOR + 2.2), 2.8, parts.RED, 0.2)
        parts.visible([pool], [(-1.0, None)], 0.3)
    parts.hover(forms['first'], 0.0, t_study)
    parts.sway(forms['second'], 0.0, t_study, phase=0.6, amount=1.6)
    parts.sway(forms['third'], 0.0, t_study, phase=1.9, amount=0.6)
    onlooker = parts.scientist('onlooker', near, (7.0, parts.FLOOR), facing=-1)
    parts.nod(onlooker, 0.0, t_study, 0.4)
    mark = kit.text('mark', '?', 1.5, kit.material(parts.BONE), near, (0.6, 3.0))
    parts.resize(mark, t_yes, 1.0, 0.001, 0.2)
    yes = parts.seal('yes', near, (0.6, 3.0), 1.2, parts.RED, parts.HOT)
    kit.pop(yes, t_yes + 0.15, 1.2)
    parts.pulse('yes-pulse', near, (0.6, 3.0), t_yes + 0.25, 1.0, parts.RED, 0.9, 0.06)
    cues.append({'t': t_yes + 0.15, 'type': 'chime', 'gain': 0.6})
    parts.dip([t_study])
    cues.append({'t': t_study - 0.2, 'type': 'whoosh', 'gain': 0.5})

    # ------------------------------------------------------------ the study: a program, and the machine it runs on
    st = parts.study(far, stage)
    parts.cut(st['roots'], t_study, None)
    front, who, ai = st['front'], st['who'], st['ai']
    pg, box = ai['program'], ai['computer']
    bx, by = ai['at']
    kit.pop(pg['root'], t_program, ai['size'])
    parts.open_eyes(pg['eyes'], t_program + 0.5)
    parts.drift(pg['root'], t_program + 0.6, end)
    parts.blink(pg['eyes'], (t_machine + 1.2, t_code + 2.6, t_body + 2.2, t_better + 2.0))
    cues.append({'t': t_program, 'type': 'pop', 'pitch': 1.2})
    parts.visible([box['beam']], [(t_machine, None)], 0.4)
    parts.pulse('machine', front, (bx, by + 1.3), t_machine + 0.1, 1.7, parts.ICE, 0.9, 0.05)
    cues.append({'t': t_machine, 'type': 'blip', 'pitch': 0.8, 'gain': 0.6})

    # the scientist writes
    parts.nod(who, t_study, end, 0.4)
    parts.write(who, t_write0, t_write1)
    for k in range(6):
        cues.append({'t': mix(t_write0, t_write1, k / 6), 'type': 'tick', 'pitch': 0.9 + 0.05 * (k % 3), 'gain': 0.3})

    # one way: it changes its own program
    quill = parts.pen('pen', pg['root'], (-pg['w'] / 2 - 0.35, pg['ys'][2]))
    kit.pop(quill, t_code - 0.3, 1.0, 0.3, t_body - 0.3)
    for k, r in enumerate((2, 4)):
        when = t_code + 0.2 + 0.7 * k
        bar = parts.band(pg, r, parts.FROST, 0.3)
        parts.lit(bar, [(0.0, 0.0), (when - 0.1, 0.0), (when + 0.1, 1.0), (when + 0.8, 0.0)])
        parts.rewrite(pg, r, when)
        cues.append({'t': when, 'type': 'tick', 'pitch': 1.3 + 0.1 * k, 'gain': 0.6})

    # the other way: it changes the machine
    for k, when in enumerate(parts.arms('new-arm', box, ai['at'], front, t_body)):
        cues.append({'t': when, 'type': 'pop', 'pitch': 0.7 + 0.15 * k})

    # ------------------------------------------------------------ worse, and better
    turns = [(t_job, True, 1.0), (t_worse + 0.5, False, 1.0)]
    when = t_better + 0.4
    while when < end - 1.0:
        turns.append((when, True, 1.8))
        when += 0.95
    for k, (t0, fixed, pace) in enumerate(turns):
        t_fix = parts.errand(f'task{k}', front, t0, ai['bench'], fixed, pace, seed=k)
        if fixed:
            parts.pulse(f'fixed{k}', front, ai['bench'], t_fix, 0.6, parts.FROST, 0.5, 0.05)
            cues.append({'t': t_fix, 'type': 'blip', 'pitch': 1.0 + 0.04 * k, 'gain': 0.45})
        else:
            cues.append({'t': t_fix, 'type': 'tick', 'pitch': 0.45, 'gain': 0.8})
    parts.rewrite(pg, 1, t_worse, colours=(parts.ASH, parts.RUST))
    parts.look(pg['eyes'], t_worse + 0.3, 0.0, -0.05)
    cues.append({'t': t_worse, 'type': 'tick', 'pitch': 0.6, 'gain': 0.6})
    parts.rewrite(pg, 1, t_better)
    parts.rewrite(pg, 3, t_better + 0.25)
    parts.look(pg['eyes'], t_better, 0.06, 0.0)
    cues.append({'t': t_better, 'type': 'tick', 'pitch': 1.5, 'gain': 0.6})
    parts.pulse('named', front, (bx, by + 3.4), t_named, 3.0, parts.FROST, 1.1, 0.06)
    cues.append({'t': t_named, 'type': 'chime', 'gain': 0.5})

    # ------------------------------------------------------------ camera
    def path(t):
        if t < t_study:
            return (0.6, 0.5, 19.8)
        pos = mix((-1.6, 0.3, 19.8), (0.8, 0.5, 17.4), span(t, t_study, t_machine + 1.0))
        pos = mix(pos, (-3.2, 0.2, 17.2), span(t, T.start(2) - 0.4, T.start(2) + 1.0))
        pos = mix(pos, (2.0, 0.4, 16.8), span(t, t_code - 1.2, t_code))
        pos = mix(pos, (2.6, 0.4, 17.4), span(t, t_job - 0.2, t_job + 1.0))
        return mix(pos, (-0.4, 0.4, 19.9), span(t, t_named - 0.5, end))

    kit.camera(path, focus_z=1.0)
    return cues
