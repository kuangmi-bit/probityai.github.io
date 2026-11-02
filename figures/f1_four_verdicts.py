"""F1 Four verdicts: one sealed archive, checked four ways, and what the verifier prints each time.

Two panels, one above the other, divided by a thin rule. The picture reads in two places (storyboard rule 8, at
most two reading zones per frame): the stack of verdicts right of the upper rows, and the two verifier ids between
the lower panel's lenses.
Panel 1 (arms 1 to 3 of demo/four-arms.sh): the archive, a box of three files sealed by one closed padlock, fans
into three rows. Each row reads left to right: the archive as the verifier gets it, the verifier's lens (blue),
and from the lens the route curves, as the fan did, into a stack of three receipts, one per row and in the rows'
order, each with its verdict glyph and, beside it, the verdict word over the exit code the verifier prints. The
stack is tight enough to read as one printout. The padlock is the same in every row; what happened to the archive
is drawn on its files. Row 2: a pencil in loss ink rests its point on one byte of the middle file, that one byte in
the same ink: someone changed one byte. The receipt's cross takes the same ink. Row 3: where the middle file stood
there is only a dashed footprint: a required file is missing, so not-established never reads as failed.
Panel 2 (arm 4) uses the same grammar: the same archive fans into two readings, the upper by the version 1 lens,
the lower by the version 2 lens (the same instrument made stronger and larger, as the stricter verifier is).
The verifier id each reading's record carries sits against its own lens, in the band between the two lenses:
version 1's under its lens, version 2's over its lens, so the two ids read together. Both routes run level past
the ids and into one open file folder, where both receipts stand, whole, each with the check that row 1's receipt
carries: kept together. The verdict is printed once, on row 1; the second printing of it was dropped.
Words and exit codes come from data/four-arms.toml; the row captions are the alt text, not words on the picture.
"""

from __future__ import annotations

import math
import tomllib
from pathlib import Path

import figkit as fk

HERE = Path(__file__).resolve().parent
NAME = "f1-four-verdicts"
REV = 3
ARMS = tomllib.loads((HERE / "data/four-arms.toml").read_text())["arm"]
TITLE = "Four verdicts from one evidence archive"
# the alt text: each row's caption with what the verifier prints for it, from data/four-arms.toml
DESC = " ".join(
    ["One sealed archive of three files, checked four ways."]
    + [f"{a['caption']}: {a['verdict']}, exit {a['exit']}." for a in ARMS[:3]]
    + [
        f"Below: the same archive is read by verifier {ARMS[3]['verifier_ids'][0]} and by the changed verifier "
        f"{ARMS[3]['verifier_ids'][1]}. Both print {ARMS[3]['verdict']}, exit {ARMS[3]['exit']}, and both "
        "receipts are kept in one folder."
    ]
)
INK = {
    "check": "fg",
    "cross": "loss",
    "query": "fg",
}  # the cross takes the pencil's ink: that changed byte is why the verifier refused
STATE = (
    {},
    {"mark": (1, (1, 0))},
    {"missing": 1},
)
LR, SH = 20, 62  # lens radius, receipt height
ROUTE_W = 3  # the verifier's route, stroke width
LINE = 1.2  # the verdict word's baseline to the exit code's, in text sizes
ID_CLEAR = 28  # clear card between a verifier id and its lens: 18 px at the README's 830, 16 at a 420 column


def _rim(lr: float, version: int) -> float:
    """How far a lens's rim reaches from its centre, stroke included (fk.lens: r, stroke 4; fk.lens_version 2:
    1.4 r, stroke 6)."""
    return lr + 2 if version == 1 else lr * 1.4 + 3


def pencil_rise(geo) -> float:
    """How far the pencil on a marked top-row byte reaches above its box's top (fk.box, fk.pencil at -45 degrees):
    the least clearance the row above needs."""
    cols, _rows, cell, gap, pad = geo
    length, hw = 4 * (cell + gap) + 4, max(10.0, cell) / 2
    point_y = pad + fk.EAR / 2  # the byte's top edge, from the box's top
    return (length + hw) * math.sin(math.radians(45)) - point_y


def _verdict(f: fk.Fig, arm, x, cy) -> float:
    """The verdict word over the exit code, as the verifier prints them, from x, the pair centred on cy. Returns the
    right edge."""
    sz = f.text_size
    f.text(x, cy - sz * 0.2, arm["verdict"], "fg", "mono", 500)
    f.text(x, cy - sz * 0.2 + sz * LINE, f"exit {arm['exit']}", "muted", "mono", 500)
    return x + fk.text_width(arm["verdict"], sz, "mono", 500)


def verdict_block(sz: float) -> tuple[float, float]:
    """(rise, drop) of a verdict pair round its centre: from the word's ink top to the exit code's ink bottom."""
    rise, _ = fk.ink_bounds("verified", sz, "mono", 500)
    _, drop = fk.ink_bounds("exit 0", sz, "mono", 500)
    return sz * 0.2 + rise, sz * (LINE - 0.2) + drop


def _lens_in(f: fk.Fig, x, cy, lr=LR, version=1) -> tuple[float, float]:
    """The route from an archive's right edge x into a lens. Returns the lens centre x and the x its rim ends at."""
    lx = x + 30 + lr
    rim = _rim(lr, version)
    f.line(x + 6, cy, lx - rim - 2, cy, "accent", sw=ROUTE_W)
    fk.lens_version(f, lx, cy, lr, version)
    return lx, lx + rim + 2


def _route(f: fk.Fig, x0, y0, x1, y1, level_to=None) -> None:
    """The verifier's route out of its lens, from (x0, y0) to an arrow whose tip is at (x1 - 4, y1): straight when
    the two are level, else one path that bends as the fan does. With level_to it runs level that far first and
    bends only after it (past text that lies under or over it)."""
    xe = x1 - 12
    if abs(y1 - y0) < 0.5:
        f.line(x0, y0, xe, y0, "accent", sw=ROUTE_W)
    else:
        xb = x0 if level_to is None else level_to
        mid = (xb + xe) / 2
        head = f"M{x0:.1f} {y0:.1f} " + (f"L{xb:.1f} {y0:.1f} " if level_to is not None else "")
        f.path(head + f"C{mid:.1f} {y0:.1f} {mid:.1f} {y1:.1f} {xe:.1f} {y1:.1f}", stroke="accent", sw=ROUTE_W)
    fk.arrow(f, x1 - 4, y1, size=7)


def _row(f: fk.Fig, k, bx, cy, qy, geo, sgap, run, lr=LR, sh=SH) -> float:
    """Panel 1: one archive at bx centred on cy, read by the verifier, whose route runs on into its receipt and
    verdict centred on qy (the row's place in the stack; cy itself where the rows need no stack). Returns the
    right edge."""
    arm = ARMS[k]
    bw, bh = fk.box_size(3, geo, sgap)
    fk.box(f, bx, cy - bh / 2 + 6, geo=geo, sgap=sgap, lock_r=lr * 0.8, **STATE[k])
    _lx, out = _lens_in(f, bx + bw, cy, lr, 1)
    sx = out + run + 12
    _route(f, out, cy, sx, qy)
    fk.slip(f, sx, qy, sh, arm["glyph"], INK[arm["glyph"]])
    return _verdict(f, arm, sx + round(sh * 0.74, 1) + 26, qy)


def facing_ids(f: fk.Fig, lr, gap) -> tuple[float, float, float]:
    """Panel 2's two verifier ids in the band between the lenses, each against its own lens: version 1's ink
    starts under the lens's handle, version 2's ends over the stronger rim, `gap` of clear card between them.
    Returns (the lens pitch this needs, id 1's baseline below route 1, id 2's baseline above route 2)."""
    sz = f.text_size
    v1, v2 = ARMS[3]["verifier_ids"]
    rise1, drop1 = fk.ink_bounds(v1, sz, "mono", 500)
    rise2, drop2 = fk.ink_bounds(v2, sz, "mono", 500)
    down1 = _rim(lr, 1) * 1.5 + ID_CLEAR + rise1  # the handle reaches 1.5 rims down and right
    up2 = _rim(lr, 2) + ID_CLEAR + drop2
    return down1 + drop1 + gap + rise2 + up2, down1, up2


def _pair(f: fk.Fig, x0, cy, geo, sgap, pitch, lr=LR, fan=96, bend=110, narrow=False) -> float:
    """Panel 2: one archive at x0 centred on cy fans, as in panel 1, into two readings: the version 1 lens on
    the upper route, the version 2 lens (the same instrument made stronger) on the lower. The verifier id each
    reading's record carries (product text from data/four-arms.toml) stands against its own lens: in the wide
    layout both face each other in the band between the lenses (pitch from facing_ids); in the narrow layout,
    where the longer id spans the column, version 1's sits over its lens and version 2's under its lens. Both
    routes run level past the ids and bend into one open file folder, where both receipts stand, whole. Returns
    the lowest y drawn."""
    arm = ARMS[3]
    bw, bh = fk.box_size(3, geo, sgap)
    # the same archive the upper panel fans from, drawn the same: three byte-grid files in the tray. Lined pages
    # here were read as "a second locked bundle" (round 29); the grid tray reads as files in every upper row.
    fk.box(f, x0, cy - bh / 2 + 6, geo=geo, sgap=sgap, lock_r=lr * 0.8)
    rows = (cy - pitch / 2, cy + pitch / 2)
    rx = x0 + bw + fan
    fx = x0 + bw + 10
    for ry in rows:
        f.path(
            f"M{fx:.1f} {cy:.1f} C{fx + 50:.1f} {cy:.1f} {rx - 70:.1f} {ry:.1f} {rx - 16:.1f} {ry:.1f}",
            stroke="rule",
            sw=2.5,
        )
        fk.arrow(f, rx - 6, ry, "rule", size=7)
    outs = []
    for k, ry in enumerate(rows):
        f.line(rx - 4, ry, rx + 6, ry, "accent", sw=ROUTE_W)
        outs.append(_lens_in(f, rx, ry, lr, k + 1))
    lx = outs[0][0]
    sz = f.text_size
    v1, v2 = arm["verifier_ids"]
    _, down1, up2 = facing_ids(f, lr, 0)  # the ids' offsets from their routes
    w1, w2 = (fk.text_width(v, sz, "mono", 500) for v in (v1, v2))
    if narrow:
        # over lens 1, ending at its right rim; under lens 2, ending at the frame's margin where the column is too
        # narrow for it to start at the rim
        x1 = lx + lr - w1
        y1 = rows[0] - _rim(lr, 1) - ID_CLEAR - fk.ink_bounds(v1, sz, "mono", 500)[1]
        x2 = min(lx - lr, f.width - fk.PAD - w2)
        y2 = rows[1] + _rim(lr, 2) * 1.5 + ID_CLEAR + fk.ink_bounds(v2, sz, "mono", 500)[0]
    else:
        x1, y1 = lx - lr, rows[0] + down1
        x2, y2 = lx - lr, rows[1] - up2
        assert y2 - y1 >= 0, "the ids must face each other with clear card between"
    f.text(x1, y1, v1, "fg", "mono", 500)
    f.text(x2, y2, v2, "fg", "mono", 500)
    ids_right = max(x1 + w1, x2 + w2)
    low_text = y2 + fk.ink_bounds(v2, sz, "mono", 500)[1]
    # the receipts' place: one open folder right of the ids; both routes run level past the ids and bend into it
    sh2 = SH + 10
    rw = round(sh2 * 0.74, 1)
    g = 14
    fw = 2 * rw + 3 * g
    if narrow:
        px = f.width - fk.PAD - fw - 6
        level_to = None
    else:
        level_to = ids_right + 16
        px = level_to + bend + 12
    top = cy - sh2 / 2 - 14
    fh = sh2 + 34
    for (_lx, out), ry, ty in zip(outs, rows, (cy - 20, cy + 20)):
        _route(f, out, ry, px, ty, level_to)
    fk.folder_back(f, px, top, fw, fh)
    for k in range(2):
        fk.slip(f, px + g + k * (rw + g), cy - 10, sh2, "check", "fg")
    # the folder's slanted front pocket, the back's own width, over the receipts' torn feet only
    fk.folder_front(f, px, top, fw, fh, 30)
    assert px + fw <= f.width - fk.PAD, px + fw
    handle = rows[1] + _rim(lr, 2) * 1.5  # the stronger lens's handle, the lowest mark of the panel
    return max(low_text, top + fh, handle) + 20


def wide() -> fk.Fig:
    W, pad = 1280, fk.PAD
    geo, sgap = (3, 3, 11, 4, 10), 10
    bw, bh = fk.box_size(3, geo, sgap)
    f = fk.Fig(NAME, "wide", W, 0, TITLE, DESC)
    pitch = bh + 40
    c0 = 30 + bh / 2
    centres = [c0, c0 + pitch, c0 + 2 * pitch]
    sy = centres[1]
    fk.box(f, pad, sy - bh / 2 + 6, geo=geo, sgap=sgap, lock_r=16)
    rx = pad + bw + 96
    fx = pad + bw + 10
    for cy in centres:
        f.path(
            f"M{fx:.1f} {sy:.1f} C{fx + 50:.1f} {sy:.1f} {rx - 70:.1f} {cy:.1f} {rx - 16:.1f} {cy:.1f}",
            stroke="rule",
            sw=2.5,
        )
        fk.arrow(f, rx - 6, cy, "rule", size=7)
    # the receipts stand in one stack, the rows' order, close enough to read as one printout: the verdict pairs
    # are 26 units of card apart, under the reading-zone gate's 0.06 of the frame height
    rise, drop = verdict_block(f.text_size)
    stack = rise + drop + 26
    assert stack >= SH + 12, stack  # the receipts stay apart
    for k, cy in enumerate(centres):
        right = _row(f, k, rx, cy, sy + (k - 1) * stack, geo, sgap, 90)
        assert right <= W - pad, (k, right)
    rule_y = centres[-1] + bh / 2 + 30
    f.line(pad, rule_y, W - pad, rule_y, "rule", sw=1.5)
    pitch2, _, _ = facing_ids(f, LR, 26)
    c2 = rule_y + 30 + _rim(LR, 1) + pitch2 / 2
    low = _pair(f, pad, c2, geo, sgap, pitch2, fan=96)
    f.height = round(low + 24)
    return f


def narrow() -> fk.Fig:
    W, pad = 720, fk.PAD
    geo, sgap = (3, 3, 9, 4, 8), 8
    bw, bh = fk.box_size(3, geo, sgap)
    f = fk.Fig(NAME, "narrow", W, 0, TITLE, DESC)
    # the rows as close as the pencil on row 2 allows, so the three verdict pairs read as one column
    pitch = bh + pencil_rise(geo) + 6
    rise, drop = verdict_block(f.text_size)
    assert pitch >= rise + drop + 8, pitch
    c0 = 30 + bh / 2
    centres = [c0, c0 + pitch, c0 + 2 * pitch]
    for k, cy in enumerate(centres):
        right = _row(f, k, pad, cy, cy, geo, sgap, 19, 18, 58)
        assert right <= W - pad, (k, right)
    rule_y = centres[-1] + bh / 2 + 30
    f.line(pad, rule_y, W - pad, rule_y, "rule", sw=1.5)
    # panel 2: the same archive fans into the version 1 and version 2 readings, one folder keeps both
    pitch2 = bh + 2 * f.text_size + 40
    # version 1's id stands over its lens: 24 of card under the rule, the id's ink, ID_CLEAR, then the rim
    v1_ink = sum(fk.ink_bounds(ARMS[3]["verifier_ids"][0], f.text_size, "mono", 500))
    c2 = rule_y + 24 + v1_ink + ID_CLEAR + _rim(18, 1) + pitch2 / 2
    low = _pair(f, pad, c2, geo, sgap, pitch2, 18, fan=70, narrow=True)
    f.height = round(low + 24)
    return f


FIGS = (wide, narrow)
