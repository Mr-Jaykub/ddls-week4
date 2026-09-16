from pathlib import Path
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results/results.json"
CIF = ROOT / "data/p53_alphafold_model.cif"
app = FastAPI(title="p53 confidence screen")


def load_results():
    try:
        return json.loads(RESULTS.read_text())
    except Exception as exc:
        raise HTTPException(500, f"Could not read results/results.json: {exc}")


@app.get("/api/results")
def api_results():
    return load_results()


@app.get("/structure.cif")
def structure():
    if not CIF.exists():
        raise HTTPException(404, "Structure file not found")
    return FileResponse(CIF, media_type="chemical/x-mmcif")


@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(INDEX)


INDEX = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>p53 confidence screen</title><script src="https://cdn.tailwindcss.com"></script>
<script src="https://3Dmol.csb.pitt.edu/build/3Dmol-min.js"></script>
<style>body{background:#f8fafc}.mono{font-variant-numeric:tabular-nums}.viewer{height:560px}.chart{height:330px}</style></head>
<body class="text-slate-900"><main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
<header class="mb-6"><p class="text-sm font-semibold uppercase tracking-widest text-indigo-700">p53 model confidence screen</p><h1 class="mt-2 text-3xl font-bold tracking-tight">A readable, bounded answer for the chemist</h1></header>
<section id="summary" class="relative z-10 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200"></section>
<div class="mt-6 grid gap-6 lg:grid-cols-2"><section class="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200"><div class="mb-3 flex items-center justify-between"><h2 class="text-lg font-semibold">Structure</h2><span class="text-xs text-slate-500">mmCIF · pLDDT from B-factor</span></div><div id="viewer" class="viewer relative z-0 overflow-hidden rounded-xl bg-slate-950"></div><div id="legend" class="mt-3 flex flex-wrap gap-3 text-xs"></div><p class="mt-3 text-sm text-slate-600"><strong>Scope:</strong> residues 18–28 are marked separately and excluded from the shortlist. Residues 293–312 and 183/185 are highlighted as distinct flagged regions.</p></section>
<section class="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200"><h2 class="text-lg font-semibold">Confidence matching the claim</h2><p class="mt-1 text-sm text-slate-600">Per-residue local pLDDT across residues 94–312; lower values are weaker assignments.</p><div id="chart" class="chart mt-3"></div><div id="regional" class="mt-4 grid grid-cols-2 gap-3"></div><div id="pae" class="mt-4 rounded-xl bg-amber-50 p-3 text-sm text-amber-900"></div></section></div>
<section class="mt-6 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200"><div class="flex items-center justify-between"><h2 class="text-lg font-semibold">Ranked caution / triage list</h2><span id="count" class="text-sm text-slate-500"></span></div><div class="mt-4 overflow-x-auto"><table class="min-w-full text-left text-sm"><thead class="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-500"><tr><th class="px-3 py-2">Rank</th><th class="px-3 py-2">Residue</th><th class="px-3 py-2">AA</th><th class="px-3 py-2">pLDDT</th><th class="px-3 py-2">Tier</th><th class="px-3 py-2">Region</th></tr></thead><tbody id="table"></tbody></table></div></section>
<section id="caveat" class="mt-6 rounded-2xl border-l-4 border-amber-500 bg-amber-50 p-5 text-amber-950"></section>
<footer class="mt-8 text-xs text-slate-500">Rendered from <code>results/results.json</code> at request time. Structure served from <code>data/p53_alphafold_model.cif</code>.</footer></main>
<script>
const iconInfo='<svg aria-hidden="true" class="mr-2 inline h-5 w-5 align-text-bottom" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 10v6m0-9h.01"/></svg>';
const iconAlert='<svg aria-hidden="true" class="mr-2 inline h-5 w-5 align-text-bottom" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3 2.5 20h19L12 3Z"/><path d="M12 9v5m0 3h.01"/></svg>';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function band(v,b){return v<50?b[0]:v<70?b[1]:v<90?b[2]:b[3]}
function region(n){return n>=293?'293–312 edge/linker':(n===183||n===185?'DBD isolated hit':'DBD 94–292')}
function renderChart(d){const el=document.getElementById('chart'), W=760,H=300,p={l:48,r:16,t:18,b:34};let vals=d.ranked_flagged_residues;let all=d.per_residue_plddt_94_312.map(x=>({x:x.residue,y:x.plddt}));let min=Math.min(...all.map(x=>x.y)), max=100;let X=x=>p.l+(x-94)/(312-94)*(W-p.l-p.r),Y=y=>p.t+(max-y)/(max-min)*(H-p.t-p.b);let path=all.map((q,i)=>(i?'L':'M')+X(q.x).toFixed(1)+' '+Y(q.y).toFixed(1)).join(' ');let dots=vals.map(q=>`<circle cx="${X(q.residue)}" cy="${Y(q.plddt)}" r="4" fill="#dc2626"/>`).join('');el.innerHTML=`<svg viewBox="0 0 ${W} ${H}" class="h-full w-full" role="img" aria-label="pLDDT across residues 94 to 312"><line x1="${p.l}" x2="${W-p.r}" y1="${Y(70)}" y2="${Y(70)}" stroke="#dc2626" stroke-dasharray="6 4"/><path d="${path}" fill="none" stroke="#334155" stroke-width="2"/>${dots}<text x="${p.l+5}" y="${Y(70)-6}" font-size="12" fill="#b91c1c">70 cutoff</text><text x="${p.l}" y="${H-8}" font-size="12">94</text><text x="${W-p.r-20}" y="${H-8}" font-size="12">312</text><text x="6" y="${p.t+8}" font-size="12">100</text><text x="12" y="${Y(70)+4}" font-size="12">70</text></svg>`}
function renderViewer(d){let v=$3Dmol.createViewer('viewer',{backgroundColor:'#020617'});fetch('/structure.cif').then(r=>r.text()).then(cif=>{v.addModel(cif,'cif');v.setStyle({}, {cartoon:{colorscheme:{prop:'b',gradient:'rwb',min:0,max:100}}});v.setStyle({resi:'293-312'},{cartoon:{color:'#ef4444'},stick:{color:'#ef4444'}});v.setStyle({resi:'183,185'},{cartoon:{color:'#f59e0b'},stick:{color:'#f59e0b'}});v.setStyle({resi:'18-28'},{cartoon:{color:'#a855f7'},stick:{color:'#a855f7'}});v.zoomTo();v.render();});let b=d.field&&d.field.confidence_bands||['<50 very low','50–<70 low','70–<90 confident','≥90 very high'];document.getElementById('legend').innerHTML=b.map((x,i)=>`<span><i class="mr-1 inline-block h-3 w-3 rounded-full ${['bg-red-500','bg-orange-400','bg-yellow-300','bg-blue-500'][i]}"></i>${esc(x)}</span>`).join('')}
async function main(){let d=await fetch('/api/results').then(r=>r.json());let res=d.regional_comparison;let flagged=d.ranked_flagged_residues;document.getElementById('summary').innerHTML=`<div class="flex gap-3">${iconInfo}<div><h2 class="text-lg font-semibold">Headline answer</h2><p class="mt-2 leading-7">The screen found that the folded p53 core is uniformly well modelled. The flagged set is dominated by the tail of the owner’s requested 94–312 range, rather than by problems spread through the fold, so this is a caution/triage list—not a clean target set.</p><p class="mt-3 text-sm font-medium text-slate-700">Structure check: the model sequence matches canonical P04637 residue-for-residue, 393 aa; the file is a monomer, while p53 functions as a tetramer.</p></div></div>`;document.getElementById('regional').innerHTML=['94-292','293-312'].map(k=>`<div class="rounded-xl bg-slate-50 p-3"><div class="text-xs font-semibold text-slate-500">${k}</div><div class="mt-1 text-xl font-bold">min ${k==='94-292'?Math.min(...d.per_residue_plddt_94_312.filter(x=>x.residue<=292).map(x=>x.plddt)).toFixed(2):Math.min(...d.per_residue_plddt_94_312.filter(x=>x.residue>=293).map(x=>x.plddt)).toFixed(2)}</div><div class="text-sm text-slate-600">mean ${res[k].mean_plddt} · ${res[k].below_70_percent}% below 70</div></div>`).join('');document.getElementById('pae').innerHTML=`${iconAlert}<strong>PAE not used for this claim.</strong> The inspected file is pairwise relative-placement confidence, ${esc(d.pae?.matrix_dimensions||'393x393')}, in ${esc(d.pae?.units||'angstroms')}; it is not per-residue pLDDT.`;document.getElementById('count').textContent=`${d.summary.passing_count} flagged of ${d.summary.core_residues_screened}`;document.getElementById('table').innerHTML=flagged.map(x=>`<tr class="border-b border-slate-100"><td class="px-3 py-2 mono">${x.rank}</td><td class="px-3 py-2 mono">${x.residue}</td><td class="px-3 py-2">${x.amino_acid}</td><td class="px-3 py-2 mono">${x.plddt.toFixed(2)}</td><td class="px-3 py-2"><span class="rounded-full px-2 py-1 text-xs ${x.tier==='very low'?'bg-red-100 text-red-800':'bg-orange-100 text-orange-800'}">${x.tier}</span></td><td class="px-3 py-2">${region(x.residue)}</td></tr>`).join('');document.getElementById('caveat').innerHTML=`${iconAlert}<strong>Read this before using the list:</strong> the shortlist is dominated by the 293–312 range boundary rather than problems inside the fold, and the two core hits disappear entirely at a cutoff of 65.`;renderChart(d);renderViewer(d)}main();
</script></body></html>'''

