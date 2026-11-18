const SHELL = `
<div class="app" id="app">
  <aside class="sidebar">
    <div class="ws">
      <div class="ws-logo">A</div>
      <div class="ws-name" id="ws-name"></div>
    </div>
    <nav class="nav" id="nav"></nav>
    <div class="side-foot">
      <div id="me-avatar"></div>
      <span class="who" id="me-name"></span>
      <span class="spacer"></span>
      <button class="icon-btn" title="Toggle theme" data-act="theme"><svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M13.5 9.5A5.5 5.5 0 1 1 6.5 2.5a4.5 4.5 0 0 0 7 7z"/></svg></button>
      <button class="icon-btn" title="Sign out" data-act="signout"><svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M6.5 13.5h-3v-11h3M10.5 11l3-3-3-3M13.5 8H6.5"/></svg></button>
    </div>
  </aside>
  <main class="main">
    <header class="topbar">
      <button class="icon-btn hamb" data-act="mobile-nav"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2.5 4.5h11M2.5 8h11M2.5 11.5h11"/></svg></button>
      <div class="crumb" id="crumb"></div>
      <div class="tabs">
        <div class="tab active" data-tab="open">Open</div>
        <div class="tab" data-tab="all">All</div>
      </div>
      <span class="spacer"></span>
      <span class="sync hide-sm" id="sync-text"></span>
      <button class="icon-btn" id="refresh" title="Refresh" data-act="refresh"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 8a5 5 0 1 1-1.5-3.6"/><path d="M13 2.5v2.5h-2.5"/></svg></button>
    </header>
    <div class="toolbar"><span class="jql mono" id="jql" title="The JQL this view runs"></span><span class="total" id="total"></span></div>
    <div class="banner" id="banner" style="display:none"></div>
    <div class="content" id="content"></div>
    <section class="detail" id="detail">
      <div class="detail-top">
        <span id="d-crumb" style="min-width:0;overflow:hidden"></span>
        <span class="spacer"></span>
        <span class="kbd hide-sm">J</span><span class="kbd hide-sm">K</span>
        <span class="ext" data-act="browser"><svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 3h4v4M13 3L7.5 8.5M11 9.5V13H3V5h3.5"/></svg><span class="hide-sm">Open in browser</span></span>
        <button class="icon-btn" data-act="close-detail" title="Close (Esc)"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 4l8 8M12 4l-8 8"/></svg></button>
      </div>
      <div class="detail-body">
        <div class="detail-main" id="d-main"></div>
        <aside class="props" id="d-props"></aside>
      </div>
    </section>
  </main>
</div>

<div class="signin" id="signin">
  <form class="signin-card" id="signin-form" novalidate>
    <div class="signin-brand"><div class="ws-logo">j4</div>jira4manager</div>
    <h1>Connect your Jira site</h1>
    <p class="lede">Read your issues in a fast desktop client. Nothing on your site changes.</p>
    <div class="field">
      <label for="f-site">Site</label>
      <div class="input"><input id="f-site" placeholder="your-site" autocomplete="off" spellcheck="false"><span class="suffix">.atlassian.net</span></div>
      <span class="hint">A full URL works too.</span>
    </div>
    <div class="field">
      <label for="f-email">Email</label>
      <div class="input"><input id="f-email" type="email" placeholder="you@company.com" autocomplete="off" spellcheck="false"></div>
    </div>
    <div class="field">
      <label for="f-token">API token</label>
      <div class="input"><input id="f-token" type="password" placeholder="Paste your API token" autocomplete="off"></div>
      <span class="hint"><a style="color:var(--blue);cursor:pointer" data-act="token-help">Create an API token</a> in your account settings. Tokens expire after at most a year.</span>
    </div>
    <div class="form-error" id="form-error"></div>
    <button class="btn-primary" id="signin-btn" type="submit">Sign in</button>
    <div class="foot"><svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2"/></svg>The token goes to your system keychain. Only the site and email are saved to disk.</div>
  </form>
</div>

<div class="toast" id="toast"></div>

<div class="knobs" id="knobs">
  <div class="knobs-panel">
    <form id="knobs-form" data-lavish-question="design-knobs">
      <fieldset>
        <legend>Screen</legend>
        <label><input type="radio" name="screen" value="signin">Sign-in</label>
        <label><input type="radio" name="screen" value="app" checked>Issues</label>
      </fieldset>
      <fieldset>
        <legend>Sign-in outcome on submit</legend>
        <label><input type="radio" name="signin" value="idle" checked>Success</label>
        <label><input type="radio" name="signin" value="rejected">Token rejected</label>
        <label><input type="radio" name="signin" value="notfound">Unknown site</label>
        <label><input type="radio" name="signin" value="offline">Offline</label>
        <label><input type="radio" name="signin" value="expired">Token expired later</label>
      </fieldset>
      <fieldset>
        <legend>Issue list state</legend>
        <label><input type="radio" name="data" value="loaded" checked>Loaded</label>
        <label><input type="radio" name="data" value="loading">First load</label>
        <label><input type="radio" name="data" value="empty">Empty</label>
        <label><input type="radio" name="data" value="error">Error</label>
        <label><input type="radio" name="data" value="ratelimited">Rate limited</label>
        <label><input type="radio" name="data" value="offline">Offline</label>
      </fieldset>
      <fieldset>
        <legend>Accent</legend>
        <label><input type="radio" name="accent" value="#7c6cf0" checked><span class="swatch" style="background:#7c6cf0"></span>Violet</label>
        <label><input type="radio" name="accent" value="#3fb68b"><span class="swatch" style="background:#3fb68b"></span>Green</label>
        <label><input type="radio" name="accent" value="#4ea7fc"><span class="swatch" style="background:#4ea7fc"></span>Blue</label>
        <label><input type="radio" name="accent" value="#f2994a"><span class="swatch" style="background:#f2994a"></span>Orange</label>
      </fieldset>
      <fieldset>
        <legend>Density</legend>
        <label><input type="radio" name="density" value="compact" checked>Compact</label>
        <label><input type="radio" name="density" value="comfortable">Comfortable</label>
      </fieldset>
      <fieldset>
        <legend>Theme</legend>
        <label><input type="radio" name="theme" value="dark" checked>Dark</label>
        <label><input type="radio" name="theme" value="light">Light</label>
      </fieldset>
      <fieldset>
        <legend>Sidebar</legend>
        <label><input type="radio" name="sidebar" value="shown" checked>Shown</label>
        <label><input type="radio" name="sidebar" value="hidden">Hidden</label>
      </fieldset>
      <div class="note">State knobs drive the mockup. Queue the look knobs to keep them in the next revision.</div>
      <button type="submit" class="btn-primary">Queue these choices</button>
    </form>
  </div>
  <div class="knobs-btn" data-act="knobs">
    <svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 5h10M3 11h10"/><circle cx="6" cy="5" r="1.6" fill="var(--raised)"/><circle cx="10" cy="11" r="1.6" fill="var(--raised)"/></svg>
    Mockup knobs
  </div>
</div>`;
document.body.insertAdjacentHTML('afterbegin', SHELL);

const SITE = 'acme-labs.atlassian.net';
const ME = { id: 'me', name: 'Sam Rivera', color: '#7c6cf0' };
const PEOPLE = {
  me: ME,
  ada: { name: 'Ada Okafor', color: '#d9467a' },
  milo: { name: 'Milo Tran', color: '#2f9e8f' },
  rin: { name: 'Rin Sato', color: '#c27c0e' },
  lee: { name: 'Lee Brandt', color: '#4a72d9' },
};
const PROJECTS = [
  { key: 'API', name: 'Platform API', color: '#7c6cf0' },
  { key: 'WEB', name: 'Web Console', color: '#3fb68b' },
  { key: 'OPS', name: 'Operations', color: '#4ea7fc' },
  { key: 'MOB', name: 'Mobile', color: '#f2994a' },
];
const STATUSES = [
  { name: 'In Progress', cat: 'indeterminate', icon: 'progress' },
  { name: 'In Review', cat: 'indeterminate', icon: 'review' },
  { name: 'Blocked', cat: 'indeterminate', icon: 'blocked' },
  { name: 'To Do', cat: 'new', icon: 'todo' },
  { name: 'Backlog', cat: 'new', icon: 'backlog' },
  { name: 'Done', cat: 'done', icon: 'done' },
];
const PRIORITIES = ['Highest', 'High', 'Medium', 'Low', 'Lowest'];
const TYPES = { Bug: '#eb5757', Story: '#3fb68b', Task: '#4ea7fc', Epic: '#a78bfa' };

const RICH = [
  { t: 'h2', c: 'Context' },
  { t: 'p', c: [['text', 'Tokens are refreshed every 15 minutes, but '], ['code', 'POST /v2/session'], ['text', ' keeps the old one alive until it expires. '], ['mention', 'ada'], ['text', ' saw this on staging after '], ['key', 'API-412'], ['text', ' shipped.']] },
  { t: 'h3', c: 'Steps to reproduce' },
  { t: 'ol', c: ['Sign in on two devices.', 'Rotate the token on the first one.', 'Call any endpoint from the second device.'] },
  { t: 'panel', kind: 'Info panel' },
  { t: 'pre', lang: 'rust', c: 'let session = store.session(&token).await?;\nassert!(session.expires_at > now);' },
  { t: 'h3', c: 'Done when' },
  { t: 'tasks', c: [[true, 'Old token is rejected with 401'], [false, 'Audit log records the revocation'], [false, 'Docs updated']] },
  { t: 'table', kind: 'Table with merged cells' },
  { t: 'quote', c: 'Security asked for this before the November release.' },
  { t: 'p', c: [['strong', 'Links: '], ['link', 'Runbook'], ['text', ' · '], ['link', 'Grafana board']] },
];
const SHORT = [
  { t: 'p', c: [['text', 'The settings page loads every project before it renders. Load the first page and fetch the rest on scroll.']] },
  { t: 'ul', c: ['Keep the current sort order.', 'Show a skeleton row while a page loads.'] },
];
const MEDIA = [
  { t: 'p', c: [['text', 'Screenshot from the customer is below. The spinner never stops after the second retry.']] },
  { t: 'media', kind: 'Image (customer-report.png)' },
  { t: 'p', c: [['text', 'Reported by support in '], ['key', 'OPS-77'], ['text', '.']] },
];

let ISSUES = [
  ['API-431', 'Token rotation leaves the previous session alive', 'In Progress', 1, 'Bug', ['security', 'auth'], 'me', '2h', RICH, 3],
  ['API-428', 'Rate-limit headers missing on 429 responses', 'In Review', 2, 'Bug', ['api'], 'ada', '5h', SHORT, 1],
  ['API-433', 'Paginate the audit log endpoint', 'To Do', 2, 'Story', ['api'], 'me', '1d', SHORT, 0],
  ['API-419', 'Remove the v1 session endpoints', 'Backlog', 3, 'Task', ['cleanup'], null, '6d', null, 0],
  ['API-402', 'Scoped tokens for service accounts', 'Done', 1, 'Epic', ['auth'], 'me', '9d', SHORT, 2],
  ['WEB-212', 'Settings page fetches every project up front', 'In Progress', 2, 'Story', ['perf'], 'me', '3h', SHORT, 2],
  ['WEB-208', 'Dark theme contrast on disabled buttons', 'Blocked', 3, 'Bug', ['a11y', 'design'], 'rin', '1d', null, 1],
  ['WEB-215', 'Spinner never stops after the second retry', 'To Do', 0, 'Bug', ['support'], 'me', '4h', MEDIA, 4],
  ['WEB-201', 'Keyboard focus lost after closing a dialog', 'In Review', 2, 'Bug', ['a11y'], 'milo', '2d', SHORT, 0],
  ['WEB-190', 'Empty state for the reports page', 'Backlog', 4, 'Task', [], null, '12d', null, 0],
  ['WEB-198', 'Export issues to CSV', 'Done', 2, 'Story', ['reports'], 'lee', '8d', SHORT, 1],
  ['OPS-88', 'Alert when the backup job runs longer than an hour', 'In Progress', 1, 'Task', ['backups'], 'ada', '6h', SHORT, 0],
  ['OPS-91', 'Rotate the staging database credentials', 'To Do', 1, 'Task', ['security'], 'me', '2d', SHORT, 1],
  ['OPS-77', 'Support inbox forwards to the old address', 'Done', 3, 'Bug', ['support'], 'rin', '15d', null, 0],
  ['MOB-41', 'Offline banner hides the first list row', 'In Progress', 2, 'Bug', ['offline'], 'lee', '1d', SHORT, 0],
  ['MOB-43', 'Push notification opens the wrong issue', 'To Do', 1, 'Bug', ['notifications'], 'me', '3d', SHORT, 2],
].map(([id, title, status, priority, type, labels, assignee, updated, desc, comments]) => ({ id, title, status, priority, type, labels, assignee, updated, desc, comments }));

const COMMENT_BODIES = [
  [['text', 'I can reproduce this on '], ['code', 'staging-2'], ['text', '. The old session row is never deleted.']],
  [['mention', 'me'], ['text', ' I think the cleanup job skips rows created before the migration. See '], ['key', 'API-402'], ['text', '.']],
  [['text', 'Moved to review after the hotfix. Tests pass locally.']],
  [['text', 'Customer confirmed the workaround works for now.']],
];
const COMMENTERS = ['ada', 'milo', 'me', 'rin'];

const M = window.MOCK || {};
const state = {
  screen: M.screen || 'app',
  signin: M.signin || 'idle',
  outcome: M.signin || 'idle',
  data: M.data || 'loaded',
  view: 'mine',
  tab: 'open',
  sel: 0,
  openId: M.openId || null,
  collapsed: {},
  refreshing: false,
  synced: 'just now',
};

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const status = (name) => STATUSES.find((s) => s.name === name);
const project = (key) => PROJECTS.find((p) => p.key === key);
const ICON = {
  refresh: '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 8a5 5 0 1 1-1.5-3.6"/><path d="M13 2.5v2.5h-2.5"/></svg>',
  ext: '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 3h4v4M13 3L7.5 8.5M11 9.5V13H3V5h3.5"/></svg>',
  close: '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 4l8 8M12 4l-8 8"/></svg>',
  lock: '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2"/></svg>',
  warn: '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 2l6.5 11.5h-13z"/><path d="M8 6.5v3.2M8 11.6v.1"/></svg>',
  eye: '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M1.5 8S4 3.5 8 3.5 14.5 8 14.5 8 12 12.5 8 12.5 1.5 8 1.5 8z"/><circle cx="8" cy="8" r="2"/></svg>',
  chev: (collapsed) => `<svg class="chev" width="10" height="10" viewBox="0 0 10 10" style="${collapsed ? 'transform:rotate(-90deg)' : ''}"><path d="M2 3.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>`,
};

function statusIcon(name, size = 14) {
  const key = status(name).icon;
  const ring = (stroke, dash = '') => `<circle cx="7" cy="7" r="5.5" fill="none" stroke="${stroke}" stroke-width="1.5" ${dash}/>`;
  let inner = '';
  if (key === 'backlog') inner = ring('var(--muted)', 'stroke-dasharray="2 2"');
  else if (key === 'todo') inner = ring('var(--text-2)');
  else if (key === 'progress') inner = ring('var(--amber)') + '<path d="M7 7V3.5A3.5 3.5 0 0 1 7 10.5Z" fill="var(--amber)"/>';
  else if (key === 'review') inner = ring('var(--green)') + '<path d="M7 7V3.5A3.5 3.5 0 1 1 3.5 7Z" fill="var(--green)"/>';
  else if (key === 'blocked') inner = ring('var(--red)') + '<path d="M4.5 9.5l5-5" stroke="var(--red)" stroke-width="1.5"/>';
  else if (key === 'done') inner = '<circle cx="7" cy="7" r="6.25" fill="var(--accent)"/><path d="M4.4 7.2l1.8 1.8 3.4-3.6" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>';
  return `<svg width="${size}" height="${size}" viewBox="0 0 14 14" aria-label="${esc(name)}">${inner}</svg>`;
}
function priorityIcon(p) {
  const title = `title="${PRIORITIES[p]}"`;
  if (p === 0) return `<svg ${title} width="14" height="14" viewBox="0 0 14 14"><rect x="1" y="1" width="12" height="12" rx="3" fill="#f2994a"/><path d="M7 3.8v4" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/><circle cx="7" cy="10.2" r=".9" fill="#fff"/></svg>`;
  const filled = { 1: 3, 2: 2, 3: 1, 4: 0 }[p];
  const bars = [[2, 8, 3], [6, 5, 6], [10, 2, 9]].map(([x, y, h], i) =>
    `<rect x="${x}" y="${y}" width="2.4" height="${h}" rx=".6" fill="${i < filled ? 'var(--text-2)' : 'var(--border-strong)'}"/>`).join('');
  return `<svg ${title} width="14" height="14" viewBox="0 0 14 14">${bars}</svg>`;
}
function typeIcon(t) {
  return `<svg width="14" height="14" viewBox="0 0 14 14" aria-label="${t}"><rect x="1.5" y="1.5" width="11" height="11" rx="3" fill="${TYPES[t]}"/><circle cx="7" cy="7" r="2" fill="#fff"/></svg>`;
}
function avatar(key, cls = '') {
  if (!key) return `<div class="avatar none ${cls}" title="Unassigned"></div>`;
  const p = PEOPLE[key];
  return `<div class="avatar ${cls}" style="background:${p.color}" title="${esc(p.name)}">${p.name[0]}</div>`;
}
function projDot(key) {
  const p = project(key);
  return `<span class="proj-dot" style="background:${p.color}">${p.key[0]}</span>`;
}

function jql() {
  const open = state.tab === 'open' ? ' AND statusCategory != Done' : '';
  return state.view === 'mine'
    ? `assignee = currentUser()${open} ORDER BY updated DESC`
    : `project = ${state.view}${open} ORDER BY updated DESC`;
}
function visible() {
  if (state.data === 'empty') return [];
  return ISSUES
    .filter((i) => state.view === 'mine' ? i.assignee === 'me' : i.id.startsWith(state.view + '-'))
    .filter((i) => state.tab === 'all' || status(i.status).cat !== 'done');
}
function groups() {
  const v = visible();
  return STATUSES.map((s) => ({ s, items: v.filter((i) => i.status === s.name).sort((a, b) => a.priority - b.priority) }))
    .filter((g) => g.items.length);
}
function ordered() {
  return groups().flatMap((g) => state.collapsed[g.s.name] ? [] : g.items);
}

function renderSidebar() {
  $('#ws-name').textContent = SITE;
  const mine = ISSUES.filter((i) => i.assignee === 'me' && status(i.status).cat !== 'done').length;
  $('#nav').innerHTML = `
    <div class="nav-item ${state.view === 'mine' ? 'active' : ''}" data-view="mine">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="8" cy="8" r="5.5"/><circle cx="8" cy="8" r="2"/></svg>
      <span class="t">My issues</span><span class="count">${state.data === 'loaded' ? mine : ''}</span>
    </div>
    <div class="nav-section">Projects</div>
    ${PROJECTS.map((p) => `<div class="nav-item ${state.view === p.key ? 'active' : ''}" data-view="${p.key}">${projDot(p.key)}<span class="t">${esc(p.name)}</span></div>`).join('')}`;
  $('#me-avatar').outerHTML = avatar('me', 'lg').replace('class="avatar', 'id="me-avatar" class="avatar');
  $('#me-name').textContent = ME.name;
}

function renderTop() {
  const p = state.view === 'mine' ? null : project(state.view);
  $('#crumb').innerHTML = p
    ? `${projDot(p.key)}<span>${esc(p.name)}</span><span class="sep">›</span><span>Issues</span>`
    : `<span>My issues</span>`;
  document.querySelectorAll('[data-tab]').forEach((x) => x.classList.toggle('active', x.dataset.tab === state.tab));
  const busy = state.refreshing || state.data === 'loading';
  $('#sync-text').textContent = busy ? 'Refreshing…' : state.data === 'error' ? 'Refresh failed' : state.data === 'offline' ? 'Updated 4 min ago' : `Updated ${state.synced}`;
  $('#refresh').classList.toggle('spin', busy);
  $('#jql').textContent = jql();
  const n = visible().length;
  $('#total').textContent = ['loaded', 'ratelimited', 'offline', 'empty'].includes(state.data) ? `${n} issue${n === 1 ? '' : 's'}` : '';
}

function renderBanner() {
  const b = $('#banner');
  const msg = {
    ratelimited: ['warn', `${ICON.warn}<span>Jira is limiting requests from this account. Retrying in 12 s. The list below is from the last refresh.</span>`],
    offline: ['warn', `${ICON.warn}<span>Can't reach ${SITE}. Showing what loaded 4 min ago.</span><span class="act" data-act="retry">Try again</span>`],
  }[state.data];
  b.style.display = msg ? 'flex' : 'none';
  if (msg) { b.className = `banner ${msg[0]}`; b.innerHTML = msg[1]; }
}

function renderList() {
  if (state.data === 'loading') {
    return Array.from({ length: 9 }, (_, i) => `<div class="skel"><i style="width:14px"></i><i style="width:52px"></i><i style="width:14px"></i><i style="width:${38 + (i * 13) % 34}%"></i><span class="spacer"></span><i style="width:20px;height:20px;border-radius:50%"></i></div>`).join('');
  }
  if (state.data === 'error') {
    return `<div class="empty">${ICON.warn.replace('width="14" height="14"', 'width="28" height="28"')}<h3>Couldn't load issues</h3><p>Jira answered with 503 Service Unavailable. Nothing on your site changed.</p><button class="btn" data-act="retry">${ICON.refresh}Try again</button></div>`;
  }
  const gs = groups();
  if (!gs.length) {
    const p = state.view === 'mine' ? null : project(state.view);
    return `<div class="empty"><svg width="28" height="28" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="8" cy="8" r="5.5"/><path d="M5.5 8.2l1.7 1.7 3.3-3.4"/></svg><h3>${p ? `No ${state.tab === 'open' ? 'open ' : ''}issues in ${esc(p.name)}` : 'Nothing assigned to you'}</h3><p>${state.tab === 'open' ? 'Issues in a Done status are hidden. Switch to All to see them.' : 'This view matches no issues on your site.'}</p>${state.tab === 'open' ? '<button class="btn" data-tab="all">Show all issues</button>' : ''}</div>`;
  }
  const flat = ordered();
  const body = gs.map(({ s, items }) => {
    const collapsed = state.collapsed[s.name];
    return `<div class="group-head" data-group="${esc(s.name)}">${ICON.chev(collapsed)}${statusIcon(s.name)}<span>${esc(s.name)}</span><span class="n">${items.length}</span></div>` +
      (collapsed ? '' : items.map((i) => `
        <div class="row ${flat.indexOf(i) === state.sel ? 'sel' : ''}" data-id="${i.id}">
          ${priorityIcon(i.priority)}
          <span class="id">${i.id}</span>
          ${statusIcon(i.status)}
          <span class="title">${esc(i.title)}</span>
          <span class="meta">${i.labels.map((l) => `<span class="label">${esc(l)}</span>`).join('')}</span>
          ${avatar(i.assignee)}
          <span class="date" title="Updated">${i.updated}</span>
        </div>`).join(''));
  }).join('');
  const cap = state.view === 'OPS' && state.tab === 'all' ? `<div class="cap-note">Showing the 1,000 most recently updated issues. Narrow the view to see older ones.</div>` : '';
  return body + cap;
}

function inline(parts) {
  return parts.map(([k, v]) => {
    if (k === 'text') return esc(v);
    if (k === 'code') return `<code>${esc(v)}</code>`;
    if (k === 'strong') return `<strong>${esc(v)}</strong>`;
    if (k === 'mention') return `<span class="mention">@${esc(PEOPLE[v].name)}</span>`;
    if (k === 'key') return `<span class="key" data-open="${v}">${v}</span>`;
    if (k === 'link') return `<a data-act="link">${esc(v)}</a>`;
    return '';
  }).join('');
}
function unsupported(kind, key) {
  return `<div class="unsupported">${ICON.eye}<span><b>${esc(kind)}</b> is not shown here.</span><span class="open" data-act="browser" data-key="${key}">Open in browser</span></div>`;
}
function markdown(doc, key) {
  if (!doc) return '<p class="no-desc">No description.</p>';
  return doc.map((b) => {
    if (b.t === 'h2') return `<h2>${esc(b.c)}</h2>`;
    if (b.t === 'h3') return `<h3>${esc(b.c)}</h3>`;
    if (b.t === 'p') return `<p>${inline(b.c)}</p>`;
    if (b.t === 'ul') return `<ul>${b.c.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>`;
    if (b.t === 'ol') return `<ol>${b.c.map((x) => `<li>${esc(x)}</li>`).join('')}</ol>`;
    if (b.t === 'tasks') return `<ul class="tasks">${b.c.map(([on, x]) => `<li><span class="box ${on ? 'on' : ''}">${on ? '<svg width="9" height="9" viewBox="0 0 10 10"><path d="M2 5.2l2 2 4-4.4" fill="none" stroke="#fff" stroke-width="1.6"/></svg>' : ''}</span><span>${esc(x)}</span></li>`).join('')}</ul>`;
    if (b.t === 'pre') return `<pre><span class="lang">${esc(b.lang)}</span><code>${esc(b.c)}</code></pre>`;
    if (b.t === 'quote') return `<blockquote>${esc(b.c)}</blockquote>`;
    return unsupported(b.kind, key);
  }).join('');
}

function renderDetail() {
  const d = $('#detail');
  const i = ISSUES.find((x) => x.id === state.openId);
  d.classList.toggle('open', !!i);
  if (!i) return;
  const p = project(i.id.split('-')[0]);
  $('#d-crumb').innerHTML = `<span style="display:inline-flex;align-items:center;gap:8px;white-space:nowrap">${projDot(p.key)}${esc(p.name)} › ${typeIcon(i.type)}${i.id}</span>`;
  const comments = Array.from({ length: i.comments }, (_, n) => `
    <div class="comment">${avatar(COMMENTERS[n % 4], 'lg')}<div><div class="who"><b>${esc(PEOPLE[COMMENTERS[n % 4]].name)}</b><span>${n + 1}d ago</span></div><div class="md"><p>${inline(COMMENT_BODIES[n % 4])}</p></div></div></div>`).join('');
  $('#d-main').innerHTML = `
    <h1>${esc(i.title)}</h1>
    <div class="md">${markdown(i.desc, i.id)}</div>
    <div class="sub-head">Comments <span class="n">${i.comments || ''}</span></div>
    ${comments || '<p style="color:var(--muted);margin:0">No comments yet.</p>'}
    <div class="read-only-note">${ICON.lock}<span>Read-only. Editing and commenting arrive in a later release.</span></div>`;
  const st = status(i.status);
  $('#d-props').innerHTML = `
    <div class="prop"><span class="k">Status</span><span class="v">${statusIcon(i.status)}${esc(st.name)}</span></div>
    <div class="prop"><span class="k">Priority</span><span class="v">${priorityIcon(i.priority)}${PRIORITIES[i.priority]}</span></div>
    <div class="prop"><span class="k">Assignee</span><span class="v">${avatar(i.assignee)}${i.assignee ? esc(PEOPLE[i.assignee].name) : '<span style="color:var(--muted)">Unassigned</span>'}</span></div>
    <div class="prop"><span class="k">Reporter</span><span class="v">${avatar('ada')}${esc(PEOPLE.ada.name)}</span></div>
    <hr>
    <div class="prop"><span class="k">Type</span><span class="v">${typeIcon(i.type)}${i.type}</span></div>
    <div class="prop"><span class="k">Labels</span><span class="v wrap">${i.labels.map((l) => `<span class="label">${esc(l)}</span>`).join('') || '<span style="color:var(--muted)">None</span>'}</span></div>
    <hr>
    <div class="prop"><span class="k">Created</span><span class="v" style="color:var(--text-2)">Nov 2</span></div>
    <div class="prop"><span class="k">Updated</span><span class="v" style="color:var(--text-2)">${i.updated} ago</span></div>`;
}

function renderSignin() {
  const s = $('#signin');
  s.classList.toggle('open', state.screen === 'signin');
  const err = $('#form-error');
  const msgs = {
    rejected: 'Jira rejected this email and API token. Check that the token belongs to this email and has not expired.',
    notfound: `No Jira Cloud site answers at <b>${esc(siteValue() || 'that address')}</b>. Check the site name.`,
    offline: 'Can\'t reach the site. Check your connection and try again.',
    expired: 'Your API token stopped working. Sign in again with a new token. Your site and email are kept.',
  };
  err.classList.toggle('show', !!msgs[state.signin]);
  err.innerHTML = msgs[state.signin] ? `${ICON.warn}<span>${msgs[state.signin]}</span>` : '';
  $('#f-site').closest('.input').classList.toggle('bad', state.signin === 'notfound');
  $('#f-token').closest('.input').classList.toggle('bad', state.signin === 'rejected' || state.signin === 'expired');
  const btn = $('#signin-btn');
  btn.disabled = state.signin === 'checking';
  btn.innerHTML = state.signin === 'checking' ? `<span class="icon-btn spin" style="width:auto;height:auto;color:#fff">${ICON.refresh}</span>Checking…` : 'Sign in';
}
function siteValue() {
  return $('#f-site').value.trim().replace(/^https?:\/\//, '').replace(/\/.*$/, '').replace(/\.atlassian\.net$/, '');
}

function render() {
  document.title = state.screen === 'signin' ? 'jira4manager — Sign in' : 'jira4manager';
  renderSignin();
  renderSidebar();
  renderTop();
  renderBanner();
  $('#content').innerHTML = renderList();
  renderDetail();
}

let toastTimer;
function toast(html) {
  const t = $('#toast');
  t.innerHTML = html;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2400);
}

function select(delta) {
  const flat = ordered();
  if (!flat.length) return;
  state.sel = Math.max(0, Math.min(flat.length - 1, state.sel + delta));
  if (state.openId) state.openId = flat[state.sel].id;
  render();
  document.querySelector('.row.sel')?.scrollIntoView({ block: 'nearest' });
}
function openIssue(id) {
  state.openId = id;
  const idx = ordered().findIndex((i) => i.id === id);
  if (idx >= 0) state.sel = idx;
  render();
}
function setView(view) {
  state.view = view;
  state.sel = 0;
  state.openId = null;
  $('#app').classList.remove('mobile-nav');
  if (state.data !== 'loaded') return render();
  state.refreshing = true;
  render();
  setTimeout(() => { state.refreshing = false; state.synced = 'just now'; render(); }, 700);
}
function refresh() {
  if (state.data === 'error' || state.data === 'offline') {
    state.data = 'loading';
    syncKnobs();
    render();
    setTimeout(() => { state.data = 'loaded'; syncKnobs(); render(); }, 900);
    return;
  }
  state.refreshing = true;
  render();
  setTimeout(() => { state.refreshing = false; state.synced = 'just now'; render(); }, 700);
}
function signIn(e) {
  e.preventDefault();
  if (!siteValue() || !$('#f-email').value.trim() || !$('#f-token').value.trim()) {
    toast('Fill in the site, email and API token.');
    return;
  }
  const want = state.outcome === 'idle' || state.outcome === 'expired' ? 'ok' : state.outcome;
  state.signin = 'checking';
  render();
  setTimeout(() => {
    if (want !== 'ok') { state.signin = want; return render(); }
    state.signin = 'idle';
    state.screen = 'app';
    state.data = 'loading';
    syncKnobs();
    render();
    toast(`Signed in to <b>${esc(SITE)}</b> as ${esc(ME.name)}`);
    setTimeout(() => { state.data = 'loaded'; syncKnobs(); render(); }, 900);
  }, 900);
}
function signOut() {
  state.screen = 'signin';
  state.signin = 'idle';
  state.openId = null;
  $('#f-token').value = '';
  syncKnobs();
  render();
  toast('Signed out. The API token was removed from the keychain.');
}

function syncKnobs() {
  const f = $('#knobs-form');
  if (!f) return;
  f.querySelector(`input[name=screen][value=${state.screen}]`).checked = true;
  f.querySelector(`input[name=data][value=${state.data}]`).checked = true;
  f.querySelector(`input[name=signin][value=${state.outcome}]`).checked = true;
}

document.addEventListener('click', (e) => {
  const act = e.target.closest('[data-act]');
  if (act) {
    const a = act.dataset.act;
    if (a === 'retry' || a === 'refresh') refresh();
    if (a === 'close-detail') { state.openId = null; render(); }
    if (a === 'browser') toast(`Opens ${SITE}/browse/${act.dataset.key || state.openId} in your browser`);
    if (a === 'link') toast('Opens the link in your browser');
    if (a === 'theme') setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
    if (a === 'signout') signOut();
    if (a === 'mobile-nav') $('#app').classList.toggle('mobile-nav');
    if (a === 'knobs') $('#knobs').classList.toggle('open');
    if (a === 'token-help') toast('Opens the API token page of your Atlassian account in your browser');
    return;
  }
  const open = e.target.closest('[data-open]');
  if (open) {
    const target = ISSUES.find((i) => i.id === open.dataset.open);
    return target ? openIssue(target.id) : toast(`${open.dataset.open} is not in this mockup`);
  }
  const g = e.target.closest('[data-group]');
  if (g) { state.collapsed[g.dataset.group] = !state.collapsed[g.dataset.group]; return render(); }
  const row = e.target.closest('[data-id]');
  if (row) return openIssue(row.dataset.id);
  const tab = e.target.closest('[data-tab]');
  if (tab) { state.tab = tab.dataset.tab; state.sel = 0; return render(); }
  const nav = e.target.closest('[data-view]');
  if (nav) return setView(nav.dataset.view);
});

document.addEventListener('keydown', (e) => {
  if (state.screen !== 'app') return;
  if (e.target.matches('input, textarea, select') || e.ctrlKey || e.metaKey || e.altKey) return;
  const k = e.key.toLowerCase();
  if (k === 'j' || e.key === 'ArrowDown') { e.preventDefault(); select(1); }
  else if (k === 'k' || e.key === 'ArrowUp') { e.preventDefault(); select(-1); }
  else if (e.key === 'Enter') { const i = ordered()[state.sel]; if (i) openIssue(i.id); }
  else if (e.key === 'Escape') { if (state.openId) { state.openId = null; render(); } $('#knobs').classList.remove('open'); }
});

function setTheme(t) {
  document.documentElement.dataset.theme = t;
  const r = document.querySelector(`#knobs-form input[name=theme][value=${t}]`);
  if (r) r.checked = true;
}

$('#signin-form').addEventListener('submit', signIn);
$('#knobs-form').addEventListener('change', (e) => {
  const f = new FormData($('#knobs-form'));
  document.documentElement.style.setProperty('--accent', f.get('accent'));
  document.documentElement.dataset.density = f.get('density');
  document.documentElement.dataset.theme = f.get('theme');
  $('#app').classList.toggle('no-sidebar', f.get('sidebar') === 'hidden');
  if (e.target.name === 'screen') state.screen = f.get('screen');
  if (e.target.name === 'data') state.data = f.get('data');
  if (e.target.name === 'signin') {
    state.outcome = f.get('signin');
    if (state.outcome === 'expired') { state.screen = 'signin'; prefill(); }
    state.signin = state.outcome === 'expired' ? 'expired' : 'idle';
  }
  syncKnobs();
  render();
});
$('#knobs-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const f = Object.fromEntries(new FormData(e.currentTarget));
  const text = `Accent ${f.accent}, ${f.density} density, ${f.theme} theme, sidebar ${f.sidebar}`;
  if (window.lavish?.queuePrompt) {
    window.lavish.queuePrompt(`Make these the mockup defaults: ${text}.`, { tag: 'choice', text: 'Design knobs: ' + text, element: e.currentTarget, queueKey: 'design-knobs', data: { question: 'design-knobs', answer: f } });
    toast('Queued. Press Send to Agent when ready.');
  } else {
    toast('Open this in Lavish to send choices back.');
  }
});

function prefill() {
  $('#f-site').value = SITE;
  $('#f-email').value = 'sam@acme-labs.example';
}
if (state.signin === 'expired') prefill();
if (state.openId) state.sel = Math.max(0, ordered().findIndex((i) => i.id === state.openId));
syncKnobs();
render();
