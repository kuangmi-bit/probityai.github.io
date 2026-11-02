"""F3 Missing is not clean: a record with one passage missing (verdict from probity-verify).

"Record" is probity-verify's own word for the stored report it checks against the source capture
(adapters/source_coverage.py: a selected span found in the source and not in the record returns
contradicted, selected_span_missing_from_record). The picture separates the two readers' vantages, one
panel each, parted by one rule across the whole card and joined only by a dashed tie between the two copies
of the record, which crosses that rule:

Top panel: what a reader that trusts the record has in front of it. The record alone, its six passages packed
in a plain frame with a tab on its top edge that prints report.txt. Nothing in it is marked: a reader of the
record alone has nothing to flag. The reader stands at its left in the text's ink (fg): a person, head and
shoulders in profile, a page tall, facing the record with nothing in hand and no sight line drawn; a thought
cloud in the same ink trails to the crown of its head and holds the one word it thinks: fine. No check, no pass
glyph: a belief, not a verdict.
Bottom panel: what probity-verify has in front of it. The same six passages, now standing over the source
passages they came from, so the fifth place in the record is empty; nothing is drawn in it. Under it the
source capture, all seven passages, with a tab hanging from its foot that prints source.html. One straight
accent rung pairs each source passage with its record passage; the fifth rung, in loss ink, starts at the
source's fifth passage like the others and stops halfway up the gap between the rows, its round end in open
air far below the empty place: the source has the passage, and the rung reaches nothing in the record. A
brace gathers both
rows into the lens, which prints a receipt with a cross in the same loss ink: contradicted, with the packet's
reason line under the panel.
The only words are what the readers print and the two file paths the packet binds.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import figkit as fk

HERE = Path(__file__).resolve().parent
NAME = "f3-missing-not-clean"
REV = 5
CASE = tomllib.loads((HERE / "data/source-coverage.toml").read_text())
N, HOLE = 7, 4
FINE = "fine"  # what a reader that trusts the record concludes
TITLE = "A passage missing from the record is not a clean record"
DESC = (
    "Top: a reader that trusts the record has only the record in front of it, six passages with nothing to flag, "
    "and thinks it fine. Bottom: the same record over the source capture it came from, seven passages. "
    "probity-verify pairs each source passage with its passage in the record, finds the fifth has none, and "
    f"returns {CASE['decision']}, reason {CASE['reason']}."
)


def _tab(f: fk.Fig, cx, edge, name, below) -> float:
    """A file-name tab centred on cx on a frame's edge at y=edge: standing on top of the frame, or hanging
    from its foot when below. It carries the path the packet binds (product text). Returns its far edge."""
    sz = f.text_size
    cap = fk.cap_height(sz, "mono", 500)
    w = fk.text_width(name, sz, "mono", 500) + 24
    h = cap + 16
    y = edge if below else edge - h
    f.rect(cx - w / 2, y, w, h, fill="tile", stroke="rule", rx=5, sw=2.5)
    f.text(cx, y + h / 2 + cap / 2, name, "fg", "mono", 500, anchor="middle")
    return y + h if below else y


def _frame(f: fk.Fig, xs, y, sw_, sh_, tab, below) -> float:
    """A plain framed row round the pages at xs, top y, with a file-name tab; returns the tab's far edge."""
    fw = xs[-1] + sw_ - xs[0] + 20
    f.rect(xs[0] - 10, y - 10, fw, sh_ + 20, stroke="rule", rx=8, sw=2.5)
    edge = y + sh_ + 10 if below else y - 10
    return _tab(f, xs[0] - 10 + fw / 2, edge, tab, below=below)


def _draw(f: fk.Fig, geo, sgap, top, gsize, reason_below, lr) -> float:
    """Draw both panels with the top panel's record at top; returns the bottom of the last thing drawn."""
    sz = f.text_size
    sw_, sh_ = fk.sheet_size(*geo)
    rw = round(gsize * 1.9 * 0.74, 1)  # the receipt's width
    word_w = max(fk.text_width(w, sz, "sans", 600) for w in (FINE, CASE["decision"]))
    col_w = lr * 2.5 + 30 + rw + 16 + word_w
    gx = f.width - fk.PAD - col_w + lr * 1.25  # the readers' glyph column, the same in both panels
    mx = gx + lr * 1.25 + 30  # the verdicts' left edge
    tx = mx + rw + 16
    cap = fk.cap_height(sz, "sans", 600)
    x0 = fk.PAD + 10
    xs = [x0 + i * (sw_ + sgap) for i in range(N)]
    # top panel: the trusting reader first, then the record alone it looks at, its six passages packed. The reader
    # stands at the left, out of the verdict column, so the panel reads "a looker, then the record" and nothing at the
    # top stands where the bottom panel's printed verdict stands (a reader there was read as a passing verdict)
    yr = top
    ey = yr + sh_ / 2
    # the trusting reader is a person in profile, a page tall, facing the record. An eye, however large and aimed,
    # was read as an inspection icon of the lens's class ("the viewer or the checker", "an observation tool", r31;
    # "an inspection step", r26), and two inspection icons fuse into one checker. A person is not a tool (r31).
    # The person and its cloud are in fg, the ink of the word they hold: a third hue (self, indigo) failed taste row 2,
    # one accent plus at most one semantic hue per frame, and no cold reader in r35 named the indigo at all (r36)
    er = sh_ / 2  # half the reader's slot, as the eye's radius was
    cw = max(rw + 30, fk.text_width(FINE, sz, "sans", 600) + 20)
    ch = gsize * 1.6
    # the cloud holds the one word the reader thinks, and nothing else: a check in here was read as "a check that
    # passed" by the simple seat in five rounds out of five
    ccx, ccy = x0 + cw / 2, ey - ch * 0.3
    ex = x0 + cw + 34 + er
    shift = ex + er + 8 + 10 - x0  # the record starts right in front of the reader's face
    xt = [x + shift for x in xs[: N - 1]]
    assert xt[-1] + sw_ + 10 <= f.width - fk.PAD, "the top record runs off the frame"
    _frame(f, xt, yr, sw_, sh_, CASE["record_path"], below=False)
    for x in xt:
        fk.sheet(f, x, yr, *geo)
    hx, hy, rh = fk.reader(f, ex, ey, sh_, ink="fg", facing="right")
    # the trail lands just off the crown's back, so the last bubble sits clear of the head's outline
    fk.thought(f, ccx, ccy, cw, ch, (hx - 0.5 * rh, hy - 1.35 * rh), ink="fg")
    f.text(ccx, ccy + cap / 2, FINE, "fg", "sans", 600, anchor="middle")
    rule_y = yr + sh_ + 10 + max(28, ch * 0.4)
    # the panel rule: one line in rule ink across the whole card, edge to edge, so the top panel is a closed scene
    # (a person, a cloud, the record, nothing else) and the bottom panel another. Without it three seats of four
    # read the top row as the first row of one diagram and never tied "fine" to having only the record; two
    # graders in one round and the r26 grader named this divider (r32). Paid for by the brace-to-lens arrowhead
    f.line(0, rule_y, f.width, rule_y, "rule", sw=2.5)
    # bottom panel: the same six passages over the source passages they came from; the fifth place is empty
    tab_h = cap + 16
    yb = rule_y + 44 + tab_h + 10
    # one dashed tie runs from the top record's foot straight down through the rule, jogs in the bottom panel's
    # band and lands on the bottom record's tab, so the two report.txt rows read as one file seen twice: the tie
    # says one file, the rule says two vantages. The jog sits 22 units below the rule, never on it (at the gap's
    # midpoint it lay one unit from the rule), so the top panel holds only a short stub of the tie
    t1 = (xt[0] - 10 + xt[-1] + sw_ + 10) / 2
    t2 = (xs[0] - 10 + xs[N - 1] + sw_ + 10) / 2
    y0, y2 = yr + sh_ + 10, yb - 10 - tab_h
    jy = (rule_y + y2) / 2
    f.path(f"M{t1:.1f} {y0:.1f} L{t1:.1f} {jy:.1f} L{t2:.1f} {jy:.1f} L{t2:.1f} {y2:.1f}", stroke="rule", sw=2.5, dash="8 6")
    _frame(f, xs, yb, sw_, sh_, CASE["record_path"], below=False)
    for i, x in enumerate(xs):
        # the fifth place stays empty. The dashed footprint (r27) was counted as a seventh piece ("6 pieces and the
        # checked one has 7") and as "an entry in the report with no counterpart in the source": a placeholder is
        # an occupant, so nothing is drawn here
        if i != HOLE:
            fk.sheet(f, x, yb, *geo)
    under = yb + sh_ + 10  # the record frame's foot
    ys = under + 2 * (lr + 30) + 10  # the source's top
    src_foot = _frame(f, xs, ys, sw_, sh_, CASE["source_path"], below=True)
    for x in xs:
        fk.sheet(f, x, ys, *geo)
    # probity-verify pairs each source passage with its record passage, one straight rung per pair; the fifth
    # rung, in loss ink, starts at the source's fifth passage like the others and stops at the midpoint of the
    # gap between the rows, 48 units (wide) and 50 (narrow) short of the record's foot: it starts at a passage
    # that exists and visibly reaches nothing. A rung end inside the empty place was read as a seventh page or a
    # marker (r19 to r22), a footprint there as a placeholder entry (r27), a rung reaching the frame's foot under
    # a bare gap was read three ways (r24 to r26), and a rung stopping 20 units short (12 px on the panel the
    # readers see) was read by the simple seat as a link that 'does not hold' and as 'linking the fifth icon of
    # the middle row to the fifth icon of the bottom row' (r34); two graders and the jury seat asked for half (r35)
    tip = (under + ys - 10) / 2
    for i, x in enumerate(xs):
        mx_ = x + sw_ / 2
        if i == HOLE:
            f.line(mx_, ys - 12, mx_, tip, "loss", sw=4)
        else:
            f.line(mx_, ys - 12, mx_, under + 2, "accent", sw=3)
    # a brace gathers both rows into the lens: it reads the two rows side by side
    rx1 = xs[-1] + sw_ + 10
    bx = rx1 + 18
    bt_, bb_ = yb - 10, ys + sh_ + 10
    bm = (bt_ + bb_) / 2
    f.path(
        f"M{bx:.1f} {bt_:.1f} Q{bx + 12:.1f} {bt_:.1f} {bx + 12:.1f} {bt_ + 14:.1f} L{bx + 12:.1f} {bm - 14:.1f} "
        f"Q{bx + 12:.1f} {bm:.1f} {bx + 24:.1f} {bm:.1f} Q{bx + 12:.1f} {bm:.1f} {bx + 12:.1f} {bm + 14:.1f} "
        f"L{bx + 12:.1f} {bb_ - 14:.1f} Q{bx + 12:.1f} {bb_:.1f} {bx:.1f} {bb_:.1f}",
        stroke="accent",
        sw=3,
    )
    assert bx + 40 <= gx - lr, "the rows run into the readers' column"
    yv = bm
    # the route from the brace runs into the lens's rim with no arrowhead: it paid for the panel rule (r32), r27
    # had already shown no seat misses it, and the lens-to-receipt arrowhead keeps the route's direction
    f.line(bx + 26, yv, gx - lr - 2, yv, "accent", sw=3)
    fk.lens(f, gx, yv, lr)
    f.line(gx + lr + 2, yv, mx - 12, yv, "accent", sw=3)
    fk.arrow(f, mx - 4, yv, size=7)
    fk.slip(f, mx, yv, gsize * 1.9, CASE["glyph"], "loss")
    f.text(tx, yv + cap / 2, CASE["decision"], "fg", "sans", 600)
    if reason_below:
        ry = src_foot + 14 + sz
        f.text(fk.PAD - 1.5, ry, CASE["reason"], "muted", "mono", 500)
        return ry + sz * 0.6
    ry = bb_ + 14 + sz  # under the brace's foot: beside the receipt it ran across the brace's stem
    rx = f.width - fk.PAD - fk.text_width(CASE["reason"], sz, "mono", 500)
    assert ry - cap >= bb_ + 10, "the reason runs into the brace"
    f.text(rx, ry, CASE["reason"], "muted", "mono", 500)
    return max(ry + sz * 0.4, src_foot)


def wide() -> fk.Fig:
    f = fk.Fig(NAME, "wide", 1280, 0, TITLE, DESC)
    f.height = round(_draw(f, (3, 3, 12, 5, 11), 34, 76, 34, False, 18) + 26)
    return f


def narrow() -> fk.Fig:
    f = fk.Fig(NAME, "narrow", 720, 0, TITLE, DESC)
    # one cell column per page: seven portrait pages leave room for the verdict column in 720 units
    f.height = round(_draw(f, (1, 3, 12, 4, 7), 10, 86, 40, True, 20) + 30)
    return f


FIGS = (wide, narrow)
