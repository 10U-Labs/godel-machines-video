"""Write closed captions for a production from its narration timings.

    python src/render/captions.py godel-machines

Reads out/<name>/voice/timings.json, which holds every narration line with
its start and end inside its scene. Scenes play one after another, so a
line's time in the video is the length of the scenes before it plus its start
(the same rule src/audio/mix.py uses to place the voice). Long lines are
broken into captions of at most two short rows, and each caption gets a share
of the line's time in proportion to its length. The length of a row and the
blank between captions are the production's [captions] settings (see
src/production.py). Writes out/<name>/<name>.srt.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import production  # noqa: E402


def split_rows(text, row):
    """The best way to break text into two rows of at most row characters, or None."""
    words = text.split()
    best = None
    for i in range(1, len(words)):
        top, bottom = " ".join(words[:i]), " ".join(words[i:])
        if len(top) > row or len(bottom) > row:
            continue
        # rows of about equal length, and a break after punctuation if one is close
        score = abs(len(top) - len(bottom)) - (10 if top[-1] in ".,;:?!" else 0)
        if best is None or score < best[0]:
            best = (score, top, bottom)
    return None if best is None else best[1:]


def fits(text, row):
    return len(text) <= row or split_rows(text, row) is not None


def pieces(text, row):
    """Split text into captions that each fit on two rows, at the most natural breaks.

    Whole sentences are kept together where they fit. A sentence too long for
    one caption is cut in two near its middle, after a comma if one is close,
    so no caption is left with only a word or two.
    """
    if fits(text, row):
        return [text]
    sentences = re.split(r"(?<=[.?!])\s+", text)
    if len(sentences) > 1:
        out = [sentences[0]]
        for p in sentences[1:]:
            if fits(out[-1] + " " + p, row):
                out[-1] += " " + p
            else:
                out.append(p)
        if len(out) > 1:
            return [q for part in out for q in pieces(part, row)]
    words = text.split()
    best = None
    for i in range(1, len(words)):
        head = " ".join(words[:i])
        score = abs(len(head) - len(text) / 2) - (12 if head[-1] in ",;:" else 0)
        if best is None or score < best[0]:
            best = (score, i)
    i = best[1]
    return pieces(" ".join(words[:i]), row) + pieces(" ".join(words[i:]), row)


def rows(text, row):
    """Break one caption into one or two rows of about equal length."""
    if len(text) <= row:
        return text
    top, bottom = split_rows(text, row)
    return f"{top}\n{bottom}"


def stamp(seconds):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def captions(timings, row, gap):
    out = []
    offset = 0.0
    for scene in timings["scenes"]:
        for line in scene["lines"]:
            parts = pieces(line["text"], row)
            start, end = offset + line["start"], offset + line["end"]
            total = sum(len(p) for p in parts)
            t = start
            for k, p in enumerate(parts):
                t_end = end if k == len(parts) - 1 else t + (end - start) * len(p) / total
                out.append((t, t_end - (0 if k == len(parts) - 1 else gap), rows(p, row)))
                t = t_end
        offset += scene["duration"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("production")
    args = ap.parse_args()
    out = production.out(args.production)
    srt = out / f"{args.production}.srt"

    timings = json.loads((out / "voice/timings.json").read_text(encoding="utf-8"))
    settings = production.settings(args.production)["captions"]
    cues = captions(timings, settings["row"], settings["gap"])
    srt.write_text(
        "\n".join(f"{i}\n{stamp(a)} --> {stamp(b)}\n{text}\n" for i, (a, b, text) in enumerate(cues, 1)),
        encoding="utf-8",
    )
    print(f"{len(cues)} captions -> {srt}")


if __name__ == "__main__":
    main()
