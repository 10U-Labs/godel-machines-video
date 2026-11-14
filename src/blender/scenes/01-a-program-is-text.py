"""Scene 01: A program is text.

A blank page appears beside Pip and fills with numbered lines of plain
instructions, then folds into a file. A stream of files passes under Pip, who
reads each one; the stream stops at a file marked with Pip's face. Pip opens
it, and one instruction is crossed out and rewritten.
"""
import math

import kit
from kit import fr, sec, span, mix, key, alpha, every

LINES = ['read the program', 'run its tests', 'find the line that fails', 'write a fix', 'run the tests again']
NEW_LINE = 'write three fixes, keep the best'
CHANGED = 3

PAGE_AT = (1.3, 0.1)
PAGE_W, PAGE_H = 8.4, 5.0
PIP_SIDE = (-5.6, -0.3)
PIP_TOP = (0.0, 1.5)
STREAM_Y = -2.2
GAP = 1.75


def page(stage):
    """A page of numbered instructions. Each line hides under a cover that can wipe away."""
    root = kit.empty('page', stage, (PAGE_AT[0], PAGE_AT[1], kit.next_z(stage)))
    kit.shape('page-shadow', kit.rrect_pts(PAGE_W + 0.6, PAGE_H + 0.6, 0.6), kit.glow_material(kit.INK900, 0.7, power=0.8), root, (0.15, -0.2))
    kit.shape('page-paper', kit.rrect_pts(PAGE_W, PAGE_H, 0.24), kit.material(kit.INK700), root)
    kit.shape('page-bar', [(x, y + PAGE_H / 2 - 0.32) for x, y in kit.rrect_pts(PAGE_W, 0.64, 0.24)], kit.material(kit.INK600), root)
    kit.shape('page-bar-fill', [(x, y + PAGE_H / 2 - 0.48) for x, y in kit.rrect_pts(PAGE_W, 0.32, 0)], kit.material(kit.INK600), root)
    for i, c in enumerate((kit.CORAL, kit.AMBER, kit.MINT)):
        kit.shape(f'page-dot{i}', kit.circle_pts(0.09), kit.material(c), root, (-PAGE_W / 2 + 0.34 + i * 0.28, PAGE_H / 2 - 0.32))
    icon = kit.badge('page-badge', root, (PAGE_W / 2 - 0.5, PAGE_H / 2 - 0.32))
    left = -PAGE_W / 2 + 0.55
    rows = []
    for i, body in enumerate(LINES):
        y = PAGE_H / 2 - 1.25 - i * 0.78
        num = kit.text(f'num{i}', f'{i + 1}', 0.36, kit.material(kit.AMBER), root, (left, y), face='JetBrainsMono', align='LEFT')
        words = kit.text(f'line{i}', body, 0.36, kit.material(kit.PAPER), root, (left + 0.6, y), face='JetBrainsMono', align='LEFT')
        cover = kit.shape(f'cover{i}', [(x - (PAGE_W - 0.7) / 2, y2) for x, y2 in kit.rrect_pts(PAGE_W - 0.7, 0.6, 0)],
                          kit.material(kit.INK700), root, (PAGE_W / 2 - 0.25, y))
        rows.append({'num': num, 'words': words, 'cover': cover, 'y': y})
    new = kit.text('line-new', NEW_LINE, 0.36, kit.material(kit.MINT), root, (left + 0.6, rows[CHANGED]['y']), face='JetBrainsMono', align='LEFT')
    new_cover = kit.shape('cover-new', [(x - (PAGE_W - 1.3) / 2, y2) for x, y2 in kit.rrect_pts(PAGE_W - 1.3, 0.6, 0)],
                          kit.material(kit.INK700), root, (PAGE_W / 2 - 0.25, rows[CHANGED]['y']))
    strike = kit.shape('strike', kit.bar_pts(0.22 * len(LINES[CHANGED]) + 0.2, 0.07), kit.material(kit.CORAL), root,
                       (left + 0.5, rows[CHANGED]['y'] + 0.02))
    cursor = kit.shape('cursor', kit.rrect_pts(0.2, 0.42, 0.03), kit.material(kit.MINT), root, (left + 0.6, rows[CHANGED]['y']))
    return {'root': root, 'rows': rows, 'icon': icon, 'new': new, 'new_cover': new_cover, 'strike': strike, 'cursor': cursor, 'left': left}


def build(T):
    cues = []
    end = sec(kit.frames())
    t_blank = T.start(0) + 0.2
    t_text = T.start(1) + 0.2
    t_list = T.at(1, 0.5)
    t_file = T.at(1, 0.8)
    t_stream = T.start(2)
    t_own = T.at(2, 0.52)
    t_open = T.start(3)
    t_change = T.at(3, 0.58)

    kit.backdrop(seed=11)
    kit.motes(seed=12)
    stage = kit.layer('stage', 1.0)

    # ------------------------------------------------------------ Pip
    p = kit.pip('pip', stage, PIP_SIDE, 1.2)
    zp = p['root'].location.z
    for f in every(1):
        t = sec(f)
        q1 = span(t, t_stream - 0.3, t_stream + 0.5)
        q2 = span(t, t_open, t_open + 0.6)
        x = mix(mix(PIP_SIDE[0], PIP_TOP[0], q1), PIP_SIDE[0], q2)
        y = mix(mix(PIP_SIDE[1], PIP_TOP[1], q1), PIP_SIDE[1], q2)
        key(p['root'], 'location', f, (x, y, zp))
    kit.pip_idle(p)
    kit.pip_blink(p, (2.4, 7.0, t_stream + 2.0, t_open + 1.5))
    kit.pip_look(p, 0.4, 0.13, 0.02)

    # ------------------------------------------------------------ the page of instructions
    pg = page(stage)
    root = pg['root']
    zr = root.location.z
    for f in every(1):
        t = sec(f)
        grow = kit.back_out((t - t_blank) / 0.45)
        shrink = span(t, t_file, t_file + 0.45, lambda v: v * v)
        reopen = kit.back_out((t - t_open - 0.1) / 0.55)
        s = max(0.001, grow * (1 - shrink)) if t < t_open else max(0.001, reopen)
        x = mix(PAGE_AT[0], 0.0, shrink) if t < t_open else mix(0.0, PAGE_AT[0], span(t, t_open, t_open + 0.6))
        y = mix(PAGE_AT[1], STREAM_Y, shrink) if t < t_open else mix(STREAM_Y, PAGE_AT[1], span(t, t_open, t_open + 0.6))
        key(root, 'location', f, (x, y, zr))
        key(root, 'scale', f, (s, s, 1))
    cues.append({'t': t_blank, 'type': 'pop'})
    pg['icon'].scale = (0.001,) * 3
    pg['icon'].keyframe_insert('scale', frame=1)
    pg['icon'].keyframe_insert('scale', frame=fr(t_open))
    key(pg['icon'], 'scale', fr(t_open + 0.3), (1, 1, 1))

    for i, row in enumerate(pg['rows']):                    # the lines appear one by one
        t0 = t_text + 0.32 * i
        row['cover'].keyframe_insert('scale', frame=fr(t0))
        key(row['cover'], 'scale', fr(t0 + 0.3), (0.001, 1, 1))
        cues.append({'t': t0, 'type': 'tick', 'pitch': 0.9 + 0.05 * i})
        num = row['num']
        num.keyframe_insert('scale', frame=fr(t_list + 0.15 * i))
        key(num, 'scale', fr(t_list + 0.15 * i + 0.12), (1.45, 1.45, 1))
        key(num, 'scale', fr(t_list + 0.15 * i + 0.3), (1, 1, 1))
        cues.append({'t': t_list + 0.15 * i, 'type': 'blip', 'pitch': 1.0 + 0.08 * i, 'gain': 0.5})

    # crossed out and rewritten
    left = pg['left']
    strike = pg['strike']
    strike.scale = (0.001, 1, 1)
    strike.keyframe_insert('scale', frame=1)
    strike.keyframe_insert('scale', frame=fr(t_change))
    key(strike, 'scale', fr(t_change + 0.25), (1, 1, 1))
    old = pg['rows'][CHANGED]
    for ob in (old['words'], strike):
        alpha(ob, 1, 1.0)
        alpha(ob, fr(t_change + 0.45), 1.0)
        alpha(ob, fr(t_change + 0.6), 0.0)
    cover = pg['new_cover']
    alpha(cover, 1, 0.0)                      # the cover for the new line waits until the old line is gone
    alpha(cover, fr(t_change + 0.55), 0.0)
    alpha(cover, fr(t_change + 0.56) + 1, 1.0)
    alpha(pg['new'], 1, 0.0)
    alpha(pg['new'], fr(t_change + 0.55), 0.0)
    alpha(pg['new'], fr(t_change + 0.56) + 1, 1.0)
    t_type = t_change + 0.6
    t_typed = min(end - 0.3, t_type + 0.9)
    cover.keyframe_insert('scale', frame=fr(t_type))
    key(cover, 'scale', fr(t_typed), (0.001, 1, 1))
    cur = pg['cursor']
    zc = cur.location.z
    width = 0.216 * len(NEW_LINE)
    for f in every(1):
        t = sec(f)
        q = span(t, t_type, t_typed, lambda v: v)
        on = 1.0 if t_change + 0.5 <= t else 0.0
        blink = 1.0 if (t < t_type or t > t_typed) and int(t * 3) % 2 else 0.0
        key(cur, 'location', f, (left + 0.6 + width * q + 0.1, old['y'], zc))
        alpha(cur, f, on * (1.0 - blink))
    cues.append({'t': t_change, 'type': 'swoosh', 'dur': 0.4, 'gain': 0.6})
    for k in range(8):
        cues.append({'t': t_type + k * 0.11, 'type': 'tick', 'pitch': 1.1 + 0.03 * (k % 3), 'gain': 0.6})

    # ------------------------------------------------------------ files streaming past
    # The page becomes the first file. More files come in from the right, and
    # the stream slows so that Pip's own file stops right under Pip.
    mine = 4
    count = mine + 3
    x0 = [0.0] + [9.5 + (i - 1) * GAP for i in range(1, count)]
    t_go, t_slow, d_stop = t_stream, t_own - 0.6, 0.9
    v = x0[mine] / ((t_slow - t_go) + d_stop / 2)     # speed that ends with Pip's file at x = 0

    def travel(t):
        if t < t_go:
            return 0.0
        if t < t_slow:
            return v * (t - t_go)
        q = min(1.0, (t - t_slow) / d_stop)
        return v * (t_slow - t_go) + v * d_stop * (q - q * q / 2)

    files = [kit.file_icon(f'file{i}', stage, (x0[i], STREAM_Y), 1.25, mine=(i == mine), seed=i) for i in range(count)]
    first = files[0]['root']
    for i, fi in enumerate(files):
        ob = fi['root']
        z = ob.location.z
        t_pass = None
        for f in every(1):
            t = sec(f)
            x = x0[i] - travel(t)
            key(ob, 'location', f, (x, STREAM_Y, z))
            if t_pass is None and i not in (0, mine) and t >= t_go and x <= 0:
                t_pass = t
            if i == 0:
                s = 1.25 * max(0.001, kit.back_out((t - t_file - 0.3) / 0.4))
                key(ob, 'scale', f, (s, s, 1))
        if i == mine:
            for f in every(1, fr(t_own - 0.3), fr(t_open)):
                t = sec(f)
                alpha(fi['glow'], f, span(t, t_own - 0.2, t_own + 0.2) * (0.75 + 0.25 * math.sin((t - t_own) * 6)))
            alpha(fi['glow'], fr(t_open) + 6, 0.0)
        elif t_pass is not None:                    # a flash as each file passes under Pip
            alpha(fi['glow'], fr(t_pass - 0.15), 0.0)
            alpha(fi['glow'], fr(t_pass), 0.8)
            alpha(fi['glow'], fr(t_pass + 0.3), 0.0)
            cues.append({'t': t_pass, 'type': 'blip', 'pitch': 1.2, 'gain': 0.35})
        ob.keyframe_insert('scale', frame=fr(t_open))   # every file goes as the page reopens
        key(ob, 'scale', fr(t_open + 0.25), (0.001, 0.001, 1))
    cues.append({'t': t_file + 0.3, 'type': 'pop', 'pitch': 0.8})
    cues.append({'t': t_go, 'type': 'whoosh', 'dur': 1.4, 'gain': 0.6})
    cues.append({'t': t_own, 'type': 'chime', 'pitch': 0.9, 'gain': 0.7})

    # Pip follows the files with its eyes, then looks down at its own file
    kit.pip_look(p, t_text, 0.13, 0.0)
    kit.pip_look(p, t_stream + 0.2, 0.08, -0.08)
    for k in range(4):
        kit.pip_look(p, t_stream + 0.5 + 0.55 * k, -0.06, -0.08, 0.45)
        kit.pip_look(p, t_stream + 0.75 + 0.55 * k, 0.08, -0.08, 0.05)
    kit.pip_look(p, t_own - 0.3, 0.0, -0.1, 0.3)
    kit.pip_eyes(p, t_own, 1.2, 1.2, 0.2)
    kit.pip_eyes(p, t_open, 1.0, 1.0, 0.3)
    kit.pip_look(p, t_open + 0.3, 0.13, 0.02)
    kit.pip_arm(p, 'right', t_change - 0.35, 75, 0.25)
    kit.pip_arm(p, 'right', t_typed + 0.2, 18, 0.35)

    # ------------------------------------------------------------ camera
    def path(t):
        q = kit.smooth(t / end)
        return (-0.2 + 0.3 * q, 0.05 * q, kit.H0 - 1.0 * q)

    kit.camera(path, focus_z=1.0)
    return cues
