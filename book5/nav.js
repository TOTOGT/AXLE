/* ═══════════════════════════════════════════════════════════════════
   PRINCIPIA ORTHOGONA · Book 5 · Shared Nav + 40-Language Picker
   nav.js — <script src="nav.js"></script> in every book5 page
   ═══════════════════════════════════════════════════════════════════ */

(function () {

const CSS = `
.po-nav {
  position: sticky; top: 0; z-index: 500;
  background: rgba(4,4,10,0.97); backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(201,168,76,0.18);
  padding: .55rem 1.6rem;
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: .5rem;
  font-family: 'JetBrains Mono', 'Courier New', monospace;
}
.po-nav a.po-brand {
  font-size: .58rem; letter-spacing: .25em; text-transform: uppercase;
  color: #c9a84c; text-decoration: none; white-space: nowrap;
}
.po-nav-chapters {
  display: flex; gap: .9rem; flex-wrap: wrap; align-items: center;
}
.po-nav-chapters a {
  font-size: .52rem; letter-spacing: .1em; text-transform: uppercase;
  color: #6b6757; text-decoration: none; transition: color .18s; white-space: nowrap;
}
.po-nav-chapters a:hover        { color: #c9a84c; }
.po-nav-chapters a.po-current   { color: #c9a84c; border-bottom: 1px solid #c9a84c; }
.po-nav-chapters a.po-accent    { color: #0ABAB5; }
.po-nav-right {
  display: flex; align-items: center; gap: .8rem; flex-shrink: 0;
}
.po-lang-label { font-size: .52rem; letter-spacing: .12em; text-transform: uppercase; color: #6b6757; }
.po-sel-wrap { position: relative; }
.po-sel-wrap::after {
  content: '▾'; position: absolute; right: .4rem; top: 50%;
  transform: translateY(-50%); color: #c9a84c; pointer-events: none; font-size: .55rem;
}
.po-nav select {
  appearance: none; -webkit-appearance: none;
  background: #0c0d16; color: #c9a84c;
  border: 1px solid rgba(201,168,76,0.2); border-radius: 2px;
  font-family: inherit; font-size: .62rem;
  padding: .22rem 1.4rem .22rem .5rem; cursor: pointer; min-width: 180px;
}
.po-nav select:focus { outline: none; border-color: #c9a84c; }
.po-script-chip {
  font-size: .5rem; letter-spacing: .08em; text-transform: uppercase;
  color: #6b6757; padding: .12rem .4rem;
  border: 1px solid #2a2920; border-radius: 2px; white-space: nowrap;
}
@media (max-width: 720px) { .po-nav-chapters { display: none; } .po-nav select { min-width: 130px; } }
`;

const LANGUAGES = {
  "pt":    { name:"Portuguese",             native:"Português",          dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇧🇷" },
  "ru":    { name:"Russian",                native:"Русский",            dir:"ltr", script:"Cyrillic",    font:"'Noto Serif',serif",              flag:"🇷🇺" },
  "hi":    { name:"Hindi",                  native:"हिन्दी",             dir:"ltr", script:"Devanagari",  font:"'Noto Serif Devanagari',serif",    flag:"🇮🇳" },
  "zh":    { name:"Mandarin (Simplified)",  native:"普通话",              dir:"ltr", script:"CJK",         font:"'Noto Serif SC',serif",           flag:"🇨🇳" },
  "es":    { name:"Spanish",                native:"Español",            dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇪🇸" },
  "ar":    { name:"Arabic",                 native:"العربية",            dir:"rtl", script:"Arabic",      font:"'Noto Naskh Arabic',serif",       flag:"🇸🇦" },
  "bn":    { name:"Bengali",                native:"বাংলা",              dir:"ltr", script:"Bengali",     font:"'Noto Serif Bengali',serif",      flag:"🇧🇩" },
  "ta":    { name:"Tamil",                  native:"தமிழ்",              dir:"ltr", script:"Tamil",       font:"'Noto Serif Tamil',serif",        flag:"🇮🇳" },
  "fr":    { name:"French",                 native:"Français",           dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇫🇷" },
  "de":    { name:"German",                 native:"Deutsch",            dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇩🇪" },
  "ja":    { name:"Japanese",               native:"日本語",              dir:"ltr", script:"CJK",         font:"'Noto Serif JP',serif",           flag:"🇯🇵" },
  "ko":    { name:"Korean",                 native:"한국어",              dir:"ltr", script:"Hangul",      font:"'Noto Serif KR',serif",           flag:"🇰🇷" },
  "it":    { name:"Italian",                native:"Italiano",           dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇮🇹" },
  "nl":    { name:"Dutch",                  native:"Nederlands",         dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇳🇱" },
  "pl":    { name:"Polish",                 native:"Polski",             dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇵🇱" },
  "uk":    { name:"Ukrainian",              native:"Українська",         dir:"ltr", script:"Cyrillic",    font:"'Noto Serif',serif",              flag:"🇺🇦" },
  "el":    { name:"Greek",                  native:"Ελληνικά",           dir:"ltr", script:"Greek",       font:"'Noto Serif',serif",              flag:"🇬🇷" },
  "tr":    { name:"Turkish",                native:"Türkçe",             dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇹🇷" },
  "ro":    { name:"Romanian",               native:"Română",             dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇷🇴" },
  "cs":    { name:"Czech",                  native:"Čeština",            dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇨🇿" },
  "te":    { name:"Telugu",                 native:"తెలుగు",             dir:"ltr", script:"Telugu",      font:"'Noto Serif Telugu',serif",       flag:"🇮🇳" },
  "mr":    { name:"Marathi",                native:"मराठी",              dir:"ltr", script:"Devanagari",  font:"'Noto Serif Devanagari',serif",    flag:"🇮🇳" },
  "gu":    { name:"Gujarati",               native:"ગુજરાતી",            dir:"ltr", script:"Gujarati",    font:"'Noto Serif Gujarati',serif",      flag:"🇮🇳" },
  "kn":    { name:"Kannada",                native:"ಕನ್ನಡ",              dir:"ltr", script:"Kannada",     font:"'Noto Serif Kannada',serif",       flag:"🇮🇳" },
  "ml":    { name:"Malayalam",              native:"മലയാളം",             dir:"ltr", script:"Malayalam",   font:"'Noto Serif Malayalam',serif",     flag:"🇮🇳" },
  "ur":    { name:"Urdu",                   native:"اردو",               dir:"rtl", script:"Arabic",      font:"'Noto Nastaliq Urdu',serif",       flag:"🇵🇰" },
  "pa":    { name:"Punjabi (Gurmukhi)",     native:"ਪੰਜਾਬੀ",             dir:"ltr", script:"Gurmukhi",    font:"'Noto Serif Gurmukhi',serif",      flag:"🇮🇳" },
  "sw":    { name:"Swahili",                native:"Kiswahili",          dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇰🇪" },
  "am":    { name:"Amharic",                native:"አማርኛ",              dir:"ltr", script:"Ethiopic",    font:"'Noto Serif Ethiopic',serif",      flag:"🇪🇹" },
  "fa":    { name:"Persian",                native:"فارسی",              dir:"rtl", script:"Arabic",      font:"'Noto Naskh Arabic',serif",       flag:"🇮🇷" },
  "he":    { name:"Hebrew",                 native:"עברית",              dir:"rtl", script:"Hebrew",      font:"'Noto Serif Hebrew',serif",        flag:"🇮🇱" },
  "ha":    { name:"Hausa",                  native:"Hausa",              dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇳🇬" },
  "id":    { name:"Indonesian",             native:"Bahasa Indonesia",   dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇮🇩" },
  "vi":    { name:"Vietnamese",             native:"Tiếng Việt",         dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇻🇳" },
  "th":    { name:"Thai",                   native:"ภาษาไทย",            dir:"ltr", script:"Thai",        font:"'Noto Serif Thai',serif",          flag:"🇹🇭" },
  "my":    { name:"Burmese",                native:"မြန်မာ",             dir:"ltr", script:"Myanmar",     font:"'Noto Sans Myanmar',sans-serif",   flag:"🇲🇲" },
  "hu":    { name:"Hungarian",              native:"Magyar",             dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🇭🇺" },
  "sr":    { name:"Serbian",                native:"Српски",             dir:"ltr", script:"Cyrillic",    font:"'Noto Serif',serif",              flag:"🇷🇸" },
  "zh-tw": { name:"Mandarin (Traditional)", native:"繁體中文",            dir:"ltr", script:"CJK",         font:"'Noto Serif TC',serif",           flag:"🇹🇼" },
  "la":    { name:"Latin",                  native:"Lingua Latina",      dir:"ltr", script:"Latin",       font:"'Noto Serif',serif",              flag:"🏛"  },
};

const TIERS = [
  ["Tier 1 — Core academic",         ["pt","ru","hi","zh"]],
  ["Tier 2 — Major world",           ["es","ar","bn","ta"]],
  ["Tier 3 — Academic + East Asian", ["fr","de","ja","ko","it"]],
  ["Tier 4 — European",              ["nl","pl","uk","el","tr","ro","cs"]],
  ["Tier 5 — South Asian",           ["te","mr","gu","kn","ml","ur","pa"]],
  ["Tier 6 — Middle East + Africa",  ["sw","am","fa","he","ha"]],
  ["Tier 7 — Southeast Asian",       ["id","vi","th","my"]],
  ["Tier 8 — Additional",            ["hu","sr","zh-tw","la"]],
];

const CHAPTERS = [
  { href:"index.html",         label:"Contents" },
  { href:"chV-preface.html",   label:"Ch 0" },
  { href:"chV-banach.html",    label:"Ch 1" },
  { href:"chV-constants.html", label:"Ch 2" },
  { href:"chV-sorrys.html",    label:"Ch 3" },
  { href:"chV-g6.html",        label:"Ch G⁶" },
  { href:"chV-axle.html",      label:"AXLE" },
  { href:"chV-seed.html",      label:"The Seed" },
];

const STORAGE_KEY = 'po_lang';
function savedLang() { try { return sessionStorage.getItem(STORAGE_KEY) || 'pt'; } catch(e) { return 'pt'; } }
function saveLang(c) { try { sessionStorage.setItem(STORAGE_KEY, c); } catch(e) {} }

function buildNav() {
  const cur = location.pathname.split('/').pop() || 'index.html';
  const chLinks = CHAPTERS.map(ch =>
    `<a href="${ch.href}"${cur === ch.href ? ' class="po-current"' : ''}>${ch.label}</a>`
  ).join('');

  let optHtml = '';
  for (const [tl, codes] of TIERS) {
    optHtml += `<optgroup label="${tl}">`;
    for (const c of codes) {
      const l = LANGUAGES[c]; if (!l) continue;
      optHtml += `<option value="${c}">${l.flag} ${l.name} · ${l.native}</option>`;
    }
    optHtml += `</optgroup>`;
  }

  const nav = document.createElement('nav');
  nav.className = 'po-nav';
  nav.innerHTML = `
    <a class="po-brand" href="index.html">Principia Orthogona · Vol V · The Seed</a>
    <div class="po-nav-chapters">
      ${chLinks}
      <a href="../impa-portal.html" class="po-accent">IMPA →</a>
      <a href="../portal.html" class="po-accent">Portal →</a>
    </div>
    <div class="po-nav-right">
      <span class="po-lang-label">Translation</span>
      <div class="po-sel-wrap">
        <select id="po-lang-select" aria-label="Select language">${optHtml}</select>
      </div>
      <span class="po-script-chip" id="po-script-chip">Latin</span>
    </div>
  `;
  return nav;
}

function applyLang(code) {
  const l = LANGUAGES[code]; if (!l) return;
  saveLang(code);
  const chip = document.getElementById('po-script-chip');
  if (chip) chip.textContent = l.script;
  const sel = document.getElementById('po-lang-select');
  if (sel) sel.value = code;
  if (typeof window.PO_CONTENT !== 'undefined') {
    const blocks   = window.PO_CONTENT[code] || window.PO_CONTENT['__fallback__'](code, l);
    const colB     = document.getElementById('colB');
    const contentB = document.getElementById('contentB');
    const header   = document.getElementById('colBHeader');
    if (colB) { colB.setAttribute('dir', l.dir); colB.style.fontFamily = l.font; colB.className = (colB.className.replace('col-rtl','').trim()) + (l.dir==='rtl'?' col-rtl':''); }
    if (header) header.innerHTML = `<span>${l.flag}</span><span>${l.name}</span><span style="color:#c9a84c">${l.native}</span>`;
    if (contentB && typeof window.PO_RENDER !== 'undefined') contentB.innerHTML = window.PO_RENDER(blocks);
    const grid = document.getElementById('bilingualGrid');
    if (grid) {
      grid.style.direction = l.dir==='rtl'?'rtl':'ltr';
      const colA = document.getElementById('colA');
      if (colA) colA.style.order = l.dir==='rtl'?'2':'';
      if (colB) colB.style.order = l.dir==='rtl'?'1':'';
    }
  }
}

function mount() {
  if (!document.getElementById('po-nav-css')) {
    const s = document.createElement('style'); s.id = 'po-nav-css'; s.textContent = CSS; document.head.appendChild(s);
  }
  const nav = buildNav();
  const ex = document.querySelector('nav');
  if (ex) ex.replaceWith(nav); else document.body.prepend(nav);
  const sel = document.getElementById('po-lang-select');
  if (sel) { sel.value = savedLang(); sel.addEventListener('change', e => applyLang(e.target.value)); }
  applyLang(savedLang());
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
else mount();

window.PO_LANGUAGES = LANGUAGES;
window.PO_NAV_VERSION = '1.0';
})();
