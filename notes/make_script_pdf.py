"""Typeset notes/speaking-script.md as a podium-ready PDF.

Run: uv run python notes/make_script_pdf.py
Writes: notes/speaking-script.pdf

Uses Chromium's print engine rather than a PDF library, so the cue chips,
the running clock and the page breaks come out of ordinary CSS. Re-run this
after editing the script; the PDF is a build product, not the source.
"""
import html as H
import re
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "notes/speaking-script.md"
OUT = ROOT / "notes/speaking-script.pdf"
md = SRC.read_text()


def inline(s):
    s = H.escape(s)
    s = re.sub(r"\*\*\[→\]\*\*", '<span class="cue adv">&#8594;&nbsp; advance</span>', s)
    s = re.sub(r"\*\*\[(beat[^\]]*)\]\*\*", lambda m: f'<span class="cue beat">{m.group(1)}</span>', s)
    s = re.sub(r"\*\*\[(end[^\]]*)\]\*\*", lambda m: f'<span class="cue end">{m.group(1)}</span>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


body, lead = [], []
in_slides = False
open_tag = None


def close():
    global open_tag
    if open_tag:
        body.append("</section>")
        open_tag = None


for block in re.split(r"\n\s*\n", md.strip()):
    b = block.strip()
    if not b or b == "---":
        continue
    if b.startswith("# "):
        continue
    if b.startswith("## "):
        head = b[3:].strip()
        m = re.match(r"(\d+)\s*\u00b7\s*(.+?)\s*\u2014\s*(\d+:\d\d)$", head)
        close()
        if m:
            in_slides = True
            body.append('<section class="slide"><h2><span class="n">' + m.group(1) + '</span>'
                        '<span class="t">' + H.escape(m.group(2)) + '</span>'
                        '<span class="clock">' + m.group(3) + '</span></h2>')
        else:
            body.append('<section class="tail"><h3>' + inline(head) + "</h3>")
        open_tag = True
        continue
    if re.match(r"^\d\.\s", b):
        parts = []
        for item in re.split(r"\n(?=\d\.\s)", b):
            txt = re.sub(r"^\d+\.\s*", "", item).replace("\n", " ")
            parts.append("<li>" + inline(txt) + "</li>")
        body.append("<ol>" + "".join(parts) + "</ol>")
        continue
    para = "<p>" + inline(b.replace("\n", " ")) + "</p>"
    (body if in_slides else lead).append(para)

close()

doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 16mm 15mm 18mm; }}
* {{ box-sizing: border-box; }}
body {{ font: 12.6pt/1.62 "DejaVu Serif", Georgia, serif; color: #14181f; margin: 0; }}
h1 {{ font: 700 22pt/1.15 "DejaVu Sans", sans-serif; margin: 0 0 2mm; letter-spacing: -.01em; }}
.sub {{ font: 10.5pt/1.5 "DejaVu Sans", sans-serif; color: #55606f; margin: 0 0 3mm; }}
.lead {{ border-left: 2.5pt solid #c8ccd4; padding: 0 0 0 4mm; margin: 0 0 7mm; }}
.lead p {{ font-size: 10.6pt; line-height: 1.55; color: #414b59; margin: 0 0 2mm; }}
.slide {{ margin: 0 0 6mm; }}
h2 {{ break-after: avoid; }}
p:has(> .cue:only-child) {{ break-before: avoid; margin-top: 1mm; }}
.slide p:last-child {{ margin-bottom: 0; }}
h2 {{ display: flex; align-items: baseline; gap: 3mm; margin: 0 0 2.5mm;
      padding: 0 0 1.5mm; border-bottom: 1.2pt solid #d7dbe2;
      font: 700 13.2pt/1.25 "DejaVu Sans", sans-serif; }}
h2 .n {{ flex: none; width: 7mm; height: 7mm; border-radius: 50%; background: #1f3a8a; color: #fff;
        font-size: 9.5pt; display: inline-flex; align-items: center; justify-content: center; }}
h2 .t {{ flex: 1; }}
h2 .clock {{ flex: none; font: 700 12pt/1 "DejaVu Sans", sans-serif; color: #1f3a8a;
             font-variant-numeric: tabular-nums; }}
p {{ margin: 0 0 3.2mm; }}
.slide p {{ padding-left: 10mm; }}
strong {{ font-weight: 700; }}
.cue {{ display: inline-block; font: 700 8.6pt/1 "DejaVu Sans", sans-serif;
        letter-spacing: .06em; text-transform: uppercase; padding: 1.5mm 2.5mm;
        border-radius: 2pt; vertical-align: 1pt; }}
.adv {{ background: #1f3a8a; color: #fff; }}
.beat {{ background: #fdf0d5; color: #8a5a00; border: .8pt solid #e8c887; }}
.end {{ background: #14181f; color: #fff; }}
.tail {{ break-inside: avoid; margin: 0 0 5mm; }}
.tail h3 {{ font: 700 11.4pt/1.3 "DejaVu Sans", sans-serif; margin: 0 0 2mm; color: #14181f; }}
.tail p, .tail li {{ font-size: 11.2pt; line-height: 1.55; }}
ol {{ margin: 0 0 3mm; padding-left: 6mm; }}
li {{ margin: 0 0 2mm; }}
.rule {{ border: 0; border-top: 1.2pt solid #d7dbe2; margin: 6mm 0 5mm; }}
</style></head><body>
<h1>Speaking script &mdash; Week 4 seminar</h1>
<div class="sub">Jakub Palacka &middot; 8 slides &middot; runs 6:38 of a 7:00 slot</div>
<div class="lead">{''.join(lead)}</div>
{''.join(body)}
</body></html>"""

tmp = Path(tempfile.gettempdir()) / "speaking-script.html"
tmp.write_text(doc)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg = b.new_page()
    pg.goto(tmp.as_uri()); pg.wait_for_timeout(600)
    pg.pdf(path=str(OUT), format="A4", print_background=True,
           display_header_footer=True,
           header_template='<div></div>',
           footer_template='<div style="width:100%;font:8pt DejaVu Sans,sans-serif;color:#8a929e;'
                           'padding:0 15mm;display:flex;justify-content:space-between">'
                           '<span>Week 4 seminar &mdash; speaking script</span>'
                           '<span class="pageNumber"></span></div>',
           margin={"top": "14mm", "bottom": "16mm", "left": "15mm", "right": "15mm"})
    b.close()
print("wrote", OUT)
