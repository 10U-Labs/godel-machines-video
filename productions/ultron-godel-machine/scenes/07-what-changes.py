"""Scene 07: What changes.

The same hall. On the left stand Ultron's two bodies: the feeble one, with
his eyes lit in it, and the powerful one, still dark. His program comes out
of the feeble body as a small red sheet of code. Not one of its lines
changes. It goes into the powerful body, whose eyes light, and the feeble
body sags. On the right the Gödel Machine rewrites its code, line after
line. At the end Ultron has a new body around the same code, and the Gödel
Machine has new code.
"""
import kit
import parts
from kit import alpha, every, fr, key, mix, sec, span

SCALE = 0.82
OLD = (-6.3, parts.FLOOR)
NEW = (-3.0, parts.FLOOR)
ABOVE = (-4.7, 2.75)
PAGE = (3.8, 0.9)


def build(T):
    cues = []
    t_body = T.start(1)
    t_out = T.at(1, 0.24)
    t_in = T.at(1, 0.68)
    t_code = T.start(2)
    t_ultron = T.at(3, 0.05)
    t_machine = T.at(3, 0.55)

    parts.backdrop(seed=81)
    kit.motes(n=16, seed=82, colour=parts.ASH)
    far = kit.layer('far', -3.0)
    stage = kit.layer('stage', 1.0)
    front = parts.room('hall', far, stage, lamps=(-4.6, 3.8), glow=0.05)[1]
    for ob in (parts.spot('red-pool', front, (-4.6, parts.FLOOR + 2.4), 3.8, parts.RED, 0.13),
               parts.spot('blue-pool', front, PAGE, 3.4, parts.ICE, 0.12)):
        alpha(ob, 1, 1.0)

    # ------------------------------------------------------------ Ultron: the same program, a better body
    weak = parts.feeble('feeble', front, OLD, SCALE)
    strong = parts.powerful('powerful', front, NEW, SCALE)
    old_head = (OLD[0] + 0.04 * SCALE, parts.FLOOR + 3.52 * SCALE)
    new_head = (NEW[0], parts.FLOOR + 4.98 * SCALE)
    parts.blink(weak['eyes'], (T.at(0, 0.5), t_body + 1.0))
    parts.hide(weak['eyes']['shapes'], t_out, 0.3)
    parts.visible(strong['eyes']['shapes'] + [strong['core'][0], strong['core'][2]], [(t_in + 0.6, None)], 0.3)
    parts.blink(strong['eyes'], (t_code + 1.8, t_ultron + 2.2))
    for k, at in enumerate((OLD, NEW)):
        parts.pulse(f'body{k}', front, (at[0], parts.FLOOR + 2.0 + 0.5 * k), t_body + 0.15 + 0.5 * k, 1.5 + 0.4 * k, parts.BONE, 0.9, 0.05)
        cues.append({'t': t_body + 0.15 + 0.5 * k, 'type': 'pop', 'pitch': 0.8 - 0.2 * k, 'gain': 0.7})
    for when, lean, drop in ((t_out + 0.2, 0.0, 0.0), (t_out + 0.9, -0.1, -0.1)):
        key(weak['rig'], 'rotation_euler', fr(when), (0, 0, lean))
        key(weak['rig'], 'location', fr(when), (0, drop, 0))
    for when, turn in ((t_out + 0.2, 0.0), (t_out + 1.0, 0.3)):
        key(weak['head'], 'rotation_euler', fr(when), (0, 0, turn))

    own = parts.own_program('own', front, ABOVE, 0.5)
    z = own['root'].location.z
    key(own['root'], 'scale', 1, parts.TINY)
    key(own['root'], 'scale', max(1, fr(t_out) - 1), parts.TINY)
    for f in every(1, fr(t_out), fr(t_out + 0.8)):
        q = span(sec(f), t_out, t_out + 0.75)
        s = mix(0.04, 0.5, q)
        x, y = mix(old_head, ABOVE, q)
        key(own['root'], 'location', f, (x, y, z))
        key(own['root'], 'scale', f, (s, s, s))
    for f in every(1, fr(t_in), fr(t_in + 0.8)):
        q = span(sec(f), t_in, t_in + 0.75)
        s = mix(0.5, 0.04, q)
        x, y = mix(ABOVE, new_head, q)
        key(own['root'], 'location', f, (x, y, z))
        key(own['root'], 'scale', f, (s, s, s))
    key(own['root'], 'scale', fr(t_in + 0.8) + 1, parts.TINY)
    parts.blink(own['eyes'], (t_out + 1.5, t_out + 2.9))
    cues.append({'t': t_out, 'type': 'whoosh', 'gain': 0.6})
    cues.append({'t': t_in, 'type': 'swoosh', 'gain': 0.7})
    cues.append({'t': t_in + 0.7, 'type': 'pop', 'pitch': 0.5, 'gain': 0.9})

    # ------------------------------------------------------------ the Gödel Machine: better code
    pg = parts.page('machine', front, PAGE, rows=8, seed=5)
    parts.drift(pg['root'])
    parts.pen('pen', pg['root'], (-pg['w'] / 2 - 0.35, pg['ys'][7]))
    parts.blink(pg['eyes'], (T.at(0, 0.7), t_code + 2.4, t_machine + 1.3))
    for k in range(7):
        when = mix(t_code + 0.4, T.end(2) - 0.5, k / 6)
        parts.rewrite(pg, k, when)
        cues.append({'t': when, 'type': 'tick', 'pitch': 1.0 + 0.08 * k, 'gain': 0.55})
    who = parts.figure('scientist', front, (7.3, parts.FLOOR), coat='#56707e', coat_deep='#3b505c', hair='#c9c2b8', facing=-1)
    parts.nod(who, phase=0.4)

    # ------------------------------------------------------------ what each ends up with
    parts.pulse('new-body', front, (NEW[0], parts.FLOOR + 2.4), t_ultron, 2.3, parts.RED, 1.0, 0.06)
    cues.append({'t': t_ultron, 'type': 'pop', 'pitch': 0.5})
    parts.pulse('new-code', front, PAGE, t_machine, 2.4, parts.FROST, 1.0, 0.06)
    parts.rewrite(pg, 7, t_machine)
    cues.append({'t': t_machine, 'type': 'chime', 'gain': 0.5})
    cues.append({'t': T.at(0, 0.1), 'type': 'whoosh', 'gain': 0.4})

    # ------------------------------------------------------------ camera
    def path(t):
        pos = mix((0.4, 0.3, 20.6), (0.4, 0.3, 20.2), span(t, 0.0, T.end(0)))
        pos = mix(pos, (-3.7, 0.7, 15.6), span(t, t_body - 0.3, t_body + 1.2))
        pos = mix(pos, (3.3, 0.5, 15.6), span(t, t_code - 0.4, t_code + 1.0))
        return mix(pos, (0.4, 0.3, 20.4), span(t, t_ultron - 0.4, t_ultron + 1.0))

    kit.camera(path, focus_z=1.0)
    return cues
