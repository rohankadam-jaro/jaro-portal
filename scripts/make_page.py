"""One-off: derive portal/public/feedback.html from DPU/public/testimonials.html."""
import pathlib
root = pathlib.Path(__file__).resolve().parents[2]
h = open(root/"DPU/public/testimonials.html", encoding="utf-8").read()
def sub(a, b, n=1):
    global h
    assert h.count(a) >= 1, a
    h = h.replace(a, b) if n == 0 else h.replace(a, b, n)

sub("Student Testimonials — DPU × Jaro Education", "Student Feedback — All Universities · Jaro Education")
sub("DPU · Student Voices", "All Universities · Student Voices")
sub("← Back to Dashboard", "← Back to Portal")
sub("Verified Student Feedback · DPU × Jaro Education", "Verified Student Feedback · All Universities")
sub("Real experiences from Dr. D. Y. Patil Vidyapeeth students across MBA, MCA, and other programs.",
    "Real experiences from Jaro students across DPU, BVDU, Symbiosis, Amrita, Amity, CU, DSU, LIBA, Parul, MUJ and Dr. MGR.")
sub('<div class="footer-badge">DPU Testimonials</div>', '<div class="footer-badge">All Student Feedback</div>')

css = """
    .uni-wrap { padding:16px 48px 0; display:flex; align-items:flex-start; gap:14px; flex-wrap:wrap; background:var(--white); }
    .video-sec { padding:28px 48px 8px; display:none; }
    .video-sec h2 { font-family:'Libre Baskerville',serif; font-size:1.2rem; color:var(--navy); margin-bottom:14px; }
    .video-sec h2 small { font-family:'Nunito Sans',sans-serif; font-size:.72rem; color:var(--muted); font-weight:700; margin-left:8px; }
    .v-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:18px; }
    .v-card { background:var(--white); border:1px solid var(--border); border-radius:14px; overflow:hidden; box-shadow:var(--shadow-sm); }
    .v-card video { width:100%; aspect-ratio:16/9; background:#000; display:block; }
    .v-info { padding:12px 14px; display:flex; align-items:center; gap:10px; }
    .v-t { font-size:.85rem; font-weight:700; color:var(--navy); }
    .v-s { font-size:.7rem; color:var(--muted); margin-top:2px; }
    .v-yt { margin-left:auto; font-size:.68rem; font-weight:700; color:var(--red); text-decoration:none; white-space:nowrap; }
    .t-uni { background:var(--navy); color:#fff; }
    @media(max-width:820px) { .uni-wrap,.video-sec { padding-left:20px; padding-right:20px; } }
  </style>"""
sub("  </style>", css)

# university chips first, video section after the controls
sub('  <div class="stats-strip">', '  <div class="uni-wrap"><span class="co-chips-label">University:</span><div class="co-chips" id="uni-chips"></div></div>\n\n  <div class="stats-strip">')
sub('  <main class="main">', '  <section class="video-sec" id="video-sec"><h2>Student Videos<small id="v-count"></small></h2><div class="v-grid" id="v-grid"></div></section>\n\n  <main class="main">')

# tag + data
sub('<span class="t-tag">${t.p}</span>', '<span class="t-tag t-uni">${t.u}</span>\n      <span class="t-tag">${t.p}</span>')
sub("let activeRating = 'all', activeDomain = 'all', activeCompany = 'all';" if False else "activeRating = 'all', activeDomain = 'all', activeCompany = 'all';",
    "activeRating = 'all', activeDomain = 'all', activeCompany = 'all', activeUni = 'all', VIDEOS = [];")
sub("filtered=ALL.filter(t=>{", "filtered=ALL.filter(t=>{\n    if(activeUni!=='all' && t.u!==activeUni) return false;")
# don't jump to page top on every filter change
sub("window.scrollTo({top:0,behavior:'smooth'});", "if(window._pg){document.querySelector('.results-bar').scrollIntoView({behavior:'smooth',block:'start'});window._pg=false;}")
sub("currentPage=p; render();", "currentPage=p; window._pg=true; render();")

# replace the fetch block with a university-aware loader
i = h.index("fetch('/td.json')")
j = h.index("</script>", i)
loader = r"""const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');

function refreshScope(){
  const pool = activeUni==='all' ? ALL : ALL.filter(t=>t.u===activeUni);
  const avg=pool.length?(pool.reduce((s,t)=>s+t.r,0)/pool.length).toFixed(1):'—';
  document.getElementById('s-total').textContent=pool.length.toLocaleString()+'+';
  document.getElementById('s-avg').textContent=avg+'★';
  document.getElementById('s-best').textContent=pool.filter(t=>t.r===5).length.toLocaleString()+'+';
  document.getElementById('s-domains').textContent=new Set(pool.map(t=>t.d)).size+'+';
  const cc={};pool.forEach(t=>{cc[t.c]=(cc[t.c]||0)+1;});
  const top10=Object.entries(cc).sort((a,b)=>b[1]-a[1]).slice(0,10).map(e=>e[0]);
  document.getElementById('co-chips').innerHTML='<button class="chip active" data-co="all" onclick="setCompany(this)">All</button>'+top10.map(c=>`<button class="chip" data-co="${esc(c)}" onclick="setCompany(this)">${esc(c)}</button>`).join('');
  document.getElementById('co-list').innerHTML=Object.keys(cc).sort().map(c=>`<option value="${esc(c)}">`).join('');
  activeCompany='all'; document.getElementById('co-search').value='';
  const vids=VIDEOS.filter(v=>activeUni==='all'||v.u===activeUni);
  document.getElementById('video-sec').style.display=vids.length?'block':'none';
  document.getElementById('v-count').textContent=vids.length+' video'+(vids.length!==1?'s':'');
  document.getElementById('v-grid').innerHTML=vids.map(v=>`<div class="v-card"><video controls preload="none" title="${esc(v.t)}"><source src="${esc(v.src)}" type="video/mp4"></video><div class="v-info"><div><div class="v-t">${esc(v.t)}</div><div class="v-s">${esc(v.u)}${v.s?' · '+esc(v.s):''}</div></div>${v.yt?`<a class="v-yt" href="${esc(v.yt)}" target="_blank" rel="noreferrer">▶ YouTube</a>`:''}</div></div>`).join('');
  applyFilters();
}

function setUni(btn){
  document.querySelectorAll('#uni-chips .chip').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active'); activeUni=btn.dataset.u; refreshScope();
}

Promise.all([fetch('/feedback.json').then(r=>r.json()), fetch('/videos.json').then(r=>r.json()).catch(()=>[])])
  .then(([data,vids])=>{
    ALL=data; VIDEOS=vids;
    const uc={};ALL.forEach(t=>{uc[t.u]=(uc[t.u]||0)+1;});
    document.getElementById('uni-chips').innerHTML='<button class="chip active" data-u="all" onclick="setUni(this)">All</button>'+Object.entries(uc).sort((a,b)=>b[1]-a[1]).map(([u,n])=>`<button class="chip" data-u="${esc(u)}" onclick="setUni(this)">${esc(u)} (${n})</button>`).join('');
    refreshScope();
  })
  .catch(()=>{
    document.getElementById('grid').innerHTML='<div class="empty"><div class="empty-icon">⚠️</div><p>Failed to load feedback.</p></div>';
  });
"""
h = h[:i] + loader + h[j:]
open(root/"portal/public/feedback.html","w",encoding="utf-8").write(h)
