"""RETIRED — generated the FIRST version of slides.html. Do not run.

slides.html is now hand-maintained: Jakub edits its phrasing directly, and this
script would silently overwrite those edits and revert them to generated text.

Use ../check_slides.py instead. It verifies, non-destructively, that every figure
in the deck still agrees with results/results.json — which is the guarantee this
generator existed to provide, without the overwrite risk.

Kept only as the record of how the deck and its embedded structure were first built.

--- original docstring ---
Generate slides.html from results/results.json and the mmCIF.

Self-contained: the structure and every figure are embedded, so the deck needs no
local files at presentation time. Only 3Dmol.js is fetched from a CDN, and the deck
degrades to a static message if that fails.

Numbers are pulled from results.json at build time — nothing is retyped.
"""
import json
from pathlib import Path

R = json.loads(Path("results/results.json").read_text())
CIF = Path("data/p53_alphafold_model.cif").read_text()

series = R["per_residue_plddt_94_312"]
flagged = R["ranked_flagged_residues"]
reg = R["regional_comparison"]
cut = R["scope"]["cutoff"]["value"]
alt = R["alternative_cutoff_counts"]

D = {
    "cut": cut,
    "n_scope": R["summary"]["core_residues_screened"],
    "n_flag": R["summary"]["passing_count"],
    "n_verylow": R["summary"]["very_low_count"],
    "n_low": R["summary"]["low_count"],
    "core_mean": reg["94-292"]["mean_plddt"],
    "core_pct": reg["94-292"]["below_70_percent"],
    "core_n": reg["94-292"]["count"],
    "core_below65": reg["94-292"]["below_65_count"],
    "core_below80": reg["94-292"]["below_80_count"],
    "tail_mean": reg["293-312"]["mean_plddt"],
    "tail_pct": reg["293-312"]["below_70_percent"],
    "tail_n": reg["293-312"]["count"],
    "n_tail_flagged": sum(1 for f in flagged if f["residue"] >= 293),
    "n_core_flagged": sum(1 for f in flagged if f["residue"] <= 292),
    "core_hits": [f["residue"] for f in flagged if f["residue"] <= 292],
    "core_hit_vals": [f["plddt"] for f in flagged if f["residue"] <= 292],
    "series": [[s["residue"], s["plddt"]] for s in series],
    "flagged": [[f["residue"], f["plddt"]] for f in flagged],
    "alt65": alt["below_65"], "alt80": alt["below_80"],
}

HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trusting a predicted structure — p53</title>
<script src="https://3Dmol.csb.pitt.edu/build/3Dmol-min.js"></script>
<style>
:root{
  --ink:#0a0e1a; --ink2:#121829; --paper:#f2efe6; --dim:#8d97b0;
  --trust:#4d7cfe; --amber:#f0a828; --danger:#e3564a; --rule:#242c44;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{background:var(--ink);color:var(--paper);
  font:400 16px/1.6 "Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  overflow:hidden;-webkit-font-smoothing:antialiased}
.deck{position:relative;height:100vh;width:100vw}
.slide{position:absolute;inset:0;display:none;flex-direction:column;
  padding:6vh 7vw 9vh;opacity:0;transition:opacity .28s ease}
.slide.on{display:flex;opacity:1}
.kicker{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;
  color:var(--trust);font-weight:600;margin-bottom:1.1rem}
h1{font-size:clamp(2.4rem,5.4vw,4.2rem);line-height:1.02;letter-spacing:-.035em;
  font-weight:800;margin-bottom:2rem}
h1 em{font-style:normal;color:var(--amber)}
.lead{font-size:clamp(1.05rem,1.7vw,1.4rem);line-height:1.62;max-width:46ch;color:#ded9cc}
ul{list-style:none;margin-top:1.6rem;max-width:52ch}
li{position:relative;padding-left:1.5rem;margin-bottom:1rem;
  font-size:clamp(1rem,1.45vw,1.2rem);line-height:1.55;color:#ded9cc}
li::before{content:"";position:absolute;left:0;top:.62em;width:.5rem;height:.5rem;
  background:var(--trust);border-radius:50%}
li.warn::before{background:var(--amber)}
li.bad::before{background:var(--danger)}
strong{color:#fff;font-weight:650}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:3.5vw;align-items:center;flex:1;min-height:0}
.cols.wide{grid-template-columns:1.15fr .85fr}
.stat{display:flex;gap:2.5rem;margin-top:2rem;flex-wrap:wrap}
.stat div{min-width:0}
.num{font-size:clamp(2.1rem,4.4vw,3.4rem);font-weight:800;letter-spacing:-.04em;line-height:1}
.num.blue{color:var(--trust)} .num.amber{color:var(--amber)} .num.red{color:var(--danger)}
.cap{font-size:.82rem;color:var(--dim);margin-top:.45rem;letter-spacing:.02em}
.panel{background:var(--ink2);border:1px solid var(--rule);border-radius:14px;padding:1.4rem}
#viewer{width:100%;height:46vh;border-radius:14px;overflow:hidden;background:#05070f;
  border:1px solid var(--rule);position:relative}
.chartbox{width:100%}
.pill{display:inline-flex;align-items:center;gap:.45rem;font-size:.78rem;color:var(--dim);
  margin-right:1.1rem}
.pill i{width:.62rem;height:.62rem;border-radius:50%;display:inline-block}
.quote{border-left:3px solid var(--amber);padding-left:1.3rem;font-size:clamp(1.05rem,1.6vw,1.3rem);
  line-height:1.55;color:#ded9cc;max-width:48ch;margin-top:.5rem}
.two{display:grid;grid-template-columns:1fr 1fr;gap:2.4rem;margin-top:1.6rem}
.two h3{font-size:.76rem;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);
  font-weight:600;margin-bottom:.9rem}
.two p{font-size:1rem;line-height:1.6;color:#ded9cc}
.two h3.term{text-transform:none;letter-spacing:0;font-size:1rem;color:var(--paper);
  font-weight:700;margin-bottom:.75rem}
.two h3.term span{color:var(--dim);font-weight:400}
.ask{color:var(--trust);font-size:1.05rem;margin-bottom:.7rem}
.askbox{margin-top:1.8rem;max-width:56ch;border-left:3px solid var(--trust);
  padding:.2rem 0 .2rem 1.4rem}
.askbox-h{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--trust);
  font-weight:600;margin-bottom:.8rem}
.askbox p{font-size:1.05rem;line-height:1.6;color:#ded9cc}
.two li,.two p{font-size:.98rem}
.bar{position:fixed;left:0;bottom:0;height:3px;background:var(--trust);transition:width .28s ease;z-index:10}
.count{position:fixed;right:2.2vw;bottom:2.4vh;font-size:.78rem;color:var(--dim);
  font-variant-numeric:tabular-nums;z-index:10}
.hint{position:fixed;left:2.2vw;bottom:2.4vh;font-size:.72rem;color:#4a5068;z-index:10}
@media(max-width:900px){.cols,.cols.wide,.two{grid-template-columns:1fr}#viewer{height:34vh}}
</style></head><body>
<div class="deck" id="deck">

<section class="slide">
  <div class="kicker">Module 4 &middot; Jakub Palacka</div>
  <h1>Can you trust<br>a <em>predicted</em> shape?</h1>
  <p class="lead" style="max-width:58ch">A cancer researcher has an AI-predicted 3D model of p53
  &mdash; a protein that goes wrong in roughly half of all human tumours. A chemist is about to
  design a drug against specific positions on it. Her job is to warn him off the ones the model
  is not sure about.</p>
  <div class="askbox">
    <div class="askbox-h">What she asked me for</div>
    <p>Go through positions <strong>94&ndash;312</strong> &mdash; the folded core. Flag every one
    the model is <strong>not confident</strong> about. Rank them worst first, using one rule fixed
    in advance.</p>
    <p style="margin-top:.7rem">Explicitly <em>not</em> a shortlist of good targets &mdash; a
    <strong>caution list</strong>: &ldquo;check these before you build on them.&rdquo;</p>
  </div>
</section>

<section class="slide">
  <div class="kicker">Two kinds of confidence</div>
  <h1>Which number<br>answers it?</h1>
  <p class="lead" style="max-width:64ch;margin-bottom:0">The AI marks its own work &mdash; and
  hands back two different confidence scores.</p>
  <div class="two" style="margin-top:1.4rem">
    <div>
      <h3 class="term">pLDDT <span>&mdash; predicted Local Distance Difference Test</span></h3>
      <p class="ask">&ldquo;Is <em>this</em> bit in the right place?&rdquo;</p>
      <p>One score per position. Scored <strong>0&ndash;100</strong>, higher is better. Below
      about <strong>70</strong> the model is telling you not to rely on it.</p>
    </div>
    <div>
      <h3 class="term">PAE <span>&mdash; Predicted Aligned Error</span></h3>
      <p class="ask">&ldquo;Are <em>these two</em> bits right relative to each other?&rdquo;</p>
      <p>One score per pair of positions. An expected error in &aring;ngstr&ouml;m &mdash; a
      distance, so <strong>smaller is better</strong>.</p>
    </div>
  </div>
  <ul style="margin-top:1.5rem">
    <li>Her question is about single positions, so <strong>pLDDT</strong> answers it.</li>
    <li class="warn">The file she pointed me to held <strong>only PAE</strong>. The per-position
    scores were inside the model file all along.</li>
    <li>It is her protein: sequence matches exactly, <strong>393 positions</strong>, no mutations.</li>
  </ul>
</section>

<section class="slide">
  <div class="kicker">What the scores show</div>
  <h1>Solid, then<br>a cliff</h1>
  <div class="cols wide">
    <div class="chartbox">
      <div id="chart"></div>
      <div style="margin-top:.9rem">
        <span class="pill"><i style="background:var(--trust)"></i>confidence per position</span>
        <span class="pill"><i style="background:var(--danger)"></i>below the line</span>
      </div>
    </div>
    <div>
      <div class="stat" style="margin-top:0">
        <div><div class="num blue">__CORE_MEAN__</div>
          <div class="cap">average, positions 94&ndash;292</div></div>
        <div><div class="num red">__TAIL_MEAN__</div>
          <div class="cap">average, positions 293&ndash;312</div></div>
      </div>
      <ul style="margin-top:2rem">
        <li><strong>__N_FLAG__</strong> positions fell below the cut-off of __CUT__.</li>
        <li class="bad"><strong>__N_TAIL__ of them</strong> sit in the last 20 positions of her range.</li>
        <li>Only <strong>__CORE_PCT__%</strong> of the folded part was flagged at all.</li>
      </ul>
    </div>
  </div>
</section>

<section class="slide">
  <div class="kicker">The catch</div>
  <h1>The list found<br>her <em>own edge</em></h1>
  <div class="cols">
    <div>
      <ul style="margin-top:0">
        <li class="warn">Her range runs about <strong>20 positions past</strong> where the protein
        stops being folded. Those positions are floppy, not faulty.</li>
        <li class="bad">So the shortlist is mostly a map of <strong>where she drew the boundary</strong>,
        not of problems inside the fold.</li>
        <li>The only __N_CORE__ hits inside the fold sit <strong>right on the line</strong> &mdash;
        move the cut-off from __CUT__ to 65 and both disappear.</li>
      </ul>
      <p class="quote" style="margin-top:2rem">What I refused to do: hand over __N_FLAG__ positions
      as a clean target list.</p>
    </div>
    <div><div id="viewer"></div>
      <div style="margin-top:.8rem">
        <span class="pill"><i style="background:var(--trust)"></i>trustworthy</span>
        <span class="pill"><i style="background:var(--danger)"></i>the floppy tail</span>
        <span class="pill"><i style="background:var(--amber)"></i>the two borderline</span>
      </div>
    </div>
  </div>
</section>

<section class="slide">
  <div class="kicker">The delivery</div>
  <h1>What I<br>sent back</h1>
  <div class="two" style="margin-top:0">
    <div>
      <h3 class="term">The list she asked for</h3>
      <p><strong>__N_FLAG__ positions</strong> ranked worst first, each labelled
      <span style="color:var(--danger)">don&rsquo;t rely on it</span> or
      <span style="color:var(--amber)">treat with caution</span>, with the rule printed on it so
      the chemist can re-apply it without asking us.</p>
    </div>
    <div>
      <h3 class="term">Two things she didn&rsquo;t ask for</h3>
      <p>Her range runs <strong>20 positions past</strong> the fold &mdash; so most of the list is
      her boundary, not a defect. And the file she pointed me at <strong>cannot</strong> answer her
      question.</p>
    </div>
  </div>
  <ul style="margin-top:1.6rem;max-width:62ch">
    <li>Inside the real fold, only <strong>__CORE_PCT__%</strong> of positions were flagged
    &mdash; and both of those sit on the line. She asked which parts the model is unsure of, and
    the answer is <strong>almost none of them</strong>.</li>
    <li class="warn">That is <em>not</em> the same as saying those positions are good targets. A
    high score means the model is confident <strong>where it put the atoms</strong> &mdash;
    nothing about whether a drug could bind there. She asked me not to pick targets, and I
    didn&rsquo;t.</li>
  </ul>
</section>

<section class="slide">
  <div class="kicker">AI use</div>
  <h1>Who did what</h1>
  <div class="two">
    <div><h3>Pi &mdash; the analyst</h3>
      <p>Wrote the spec, the analysis script, the results file and the viewer. On its own it
      found that position 183 is known to carry a <strong>chemical tag</strong> the cell adds
      after the protein is built &mdash; and correctly refused to claim that explained the dip
      in confidence there.</p></div>
    <div><h3>Claude &mdash; independent review</h3>
      <p>Found that the companion file had no per-position scores at all. Suggested areas to probe
      and drafted possible questions for my second interview round. Recomputed the screen
      separately as a cross-check.</p></div>
  </div>
  <ul style="margin-top:2rem">
    <li><strong>Me:</strong> ran the interview, chose which questions to ask, set the cut-off, and
    decided what to refuse.</li>
    <li class="warn">The cut-off was chosen <strong>after</strong> I had looked at the files &mdash;
    reproducible, but not blind. I say so in the report.</li>
  </ul>
</section>

<section class="slide">
  <div class="kicker">Limits &amp; next step</div>
  <h1>What this<br>cannot tell you</h1>
  <ul style="margin-top:0">
    <li class="warn">A confidence score only says <em>where the model put an atom</em>. It says
    nothing about the <strong>chemical tags</strong> the cell adds, the <strong>other molecules</strong>
    p53 grips onto, or the fact that real p53 works as a <strong>group of four</strong> &mdash;
    this model is a single copy on its own.</li>
    <li>I also never checked her 94&ndash;312 range against a source &mdash; and the whole finding
    is about <strong>where that range ends</strong>.</li>
  </ul>
  <p class="quote" style="margin-top:2.4rem"><strong>Next experiment:</strong> compare positions
  183 and 185 against a real, measured structure of the folded core &mdash; that is the one result
  a cut-off cannot settle.</p>
</section>

</div>
<div class="bar" id="bar"></div>
<div class="count" id="count"></div>
<div class="hint">&larr; &rarr; to move</div>
<script>
const DATA = __DATA__;
const CIF = `__CIF__`;

/* ---------- slide engine ---------- */
const slides=[...document.querySelectorAll('.slide')];
let i=0, drawn={};
function show(n){
  i=Math.max(0,Math.min(slides.length-1,n));
  slides.forEach((s,k)=>s.classList.toggle('on',k===i));
  document.getElementById('bar').style.width=((i+1)/slides.length*100)+'%';
  document.getElementById('count').textContent=(i+1)+' / '+slides.length;
  if(i===2&&!drawn.chart){drawn.chart=1;chart();}
  if(i===3&&!drawn.viewer){drawn.viewer=1;viewer();}
}
addEventListener('keydown',e=>{
  if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(i+1);}
  if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(i-1);}
  if(e.key==='Home')show(0); if(e.key==='End')show(slides.length-1);
});
addEventListener('click',e=>{if(!e.target.closest('#viewer'))show(i+1);});

/* ---------- confidence chart ---------- */
function chart(){
  const W=660,H=360,p={l:46,r:14,t:20,b:34};
  const S=DATA.series, lo=94, hi=312, ymin=30, ymax=100;
  const X=r=>p.l+(r-lo)/(hi-lo)*(W-p.l-p.r);
  const Y=v=>p.t+(ymax-v)/(ymax-ymin)*(H-p.t-p.b);
  const path=S.map((d,k)=>(k?'L':'M')+X(d[0]).toFixed(1)+' '+Y(d[1]).toFixed(1)).join(' ');
  const dots=DATA.flagged.map(d=>`<circle cx="${X(d[0]).toFixed(1)}" cy="${Y(d[1]).toFixed(1)}" r="3.4" fill="#e3564a"/>`).join('');
  document.getElementById('chart').innerHTML=`
  <svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto" role="img"
    aria-label="Confidence per position across the requested range, high until position 293 then falling sharply">
    <line x1="${p.l}" x2="${W-p.r}" y1="${Y(DATA.cut)}" y2="${Y(DATA.cut)}"
      stroke="#f0a828" stroke-width="1.5" stroke-dasharray="7 5"/>
    <text x="${W-p.r}" y="${Y(DATA.cut)-9}" font-size="12.5" fill="#f0a828" text-anchor="end">cut-off ${DATA.cut}</text>
    <path d="${path}" fill="none" stroke="#4d7cfe" stroke-width="2.1" stroke-linejoin="round"/>
    ${dots}
    <line x1="${p.l}" x2="${p.l}" y1="${p.t}" y2="${H-p.b}" stroke="#242c44"/>
    <line x1="${p.l}" x2="${W-p.r}" y1="${H-p.b}" y2="${H-p.b}" stroke="#242c44"/>
    <text x="${p.l}" y="${H-12}" font-size="12.5" fill="#8d97b0">94</text>
    <text x="${X(293).toFixed(1)}" y="${H-12}" font-size="12.5" fill="#e3564a" text-anchor="middle">293</text>
    <text x="${W-p.r}" y="${H-12}" font-size="12.5" fill="#8d97b0" text-anchor="end">312</text>
    <text x="8" y="${p.t+6}" font-size="12.5" fill="#8d97b0">100</text>
    <text x="8" y="${H-p.b}" font-size="12.5" fill="#8d97b0">30</text>
  </svg>`;
}

/* ---------- live structure ---------- */
function viewer(){
  const box=document.getElementById('viewer');
  if(typeof $3Dmol==='undefined'){
    box.innerHTML='<div style="padding:1.2rem;color:#8d97b0;font-size:.9rem">'+
      '3D viewer needs a network connection. The shape: one compact folded block, '+
      'with a long loose tail at the end of the requested range.</div>';
    return;
  }
  const v=$3Dmol.createViewer(box,{backgroundColor:'#05070f'});
  v.addModel(CIF,'cif');
  // show only the range under discussion — the out-of-scope tails just add sprawl
  v.setStyle({},{});
  v.setStyle({resi:'94-292'},{cartoon:{color:'#4d7cfe',thickness:.9}});
  v.setStyle({resi:'293-312'},{cartoon:{color:'#e3564a',thickness:.9},stick:{color:'#e3564a',radius:.2}});
  v.setStyle({resi:'183,185'},{cartoon:{color:'#f0a828',thickness:.9},stick:{color:'#f0a828',radius:.28}});
  v.zoomTo({resi:'94-312'});
  v.zoom(1.25);
  v.render();
  v.spin('y',.45);
}
show(0);
</script></body></html>"""

subs = {
    "__CORE_MEAN__": str(D["core_mean"]), "__TAIL_MEAN__": str(D["tail_mean"]),
    "__N_FLAG__": str(D["n_flag"]), "__N_TAIL__": str(D["n_tail_flagged"]),
    "__CORE_PCT__": str(D["core_pct"]), "__N_CORE__": str(D["n_core_flagged"]),
    "__CUT__": str(int(D["cut"])),
    "__DATA__": json.dumps(D, separators=(",", ":")),
    "__CIF__": CIF,
}
out = HTML
for k, v in subs.items():
    out = out.replace(k, v)

Path("slides.html").write_text(out)
print(f"wrote slides.html  ({len(out)/1024:.0f} KB)")
print(f"  cut-off {D['cut']} | {D['n_flag']} flagged | {D['n_tail_flagged']} in tail | "
      f"{D['n_core_flagged']} in core ({D['core_hits']})")
print(f"  core mean {D['core_mean']} / tail mean {D['tail_mean']}")
print(f"  unsubstituted placeholders: {[t for t in subs if t in out]}")
