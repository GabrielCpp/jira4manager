const I = {
  refresh: '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 8a5 5 0 1 1-1.5-3.6"/><path d="M13 2.5v2.5h-2.5"/></svg>',
  ext: '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 3h4v4M13 3L7.5 8.5M11 9.5V13H3V5h3.5"/></svg>',
  close: '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 4l8 8M12 4l-8 8"/></svg>',
  lock: '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2"/></svg>',
  warn: '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 2l6.5 11.5h-13z"/><path d="M8 6.5v3.2M8 11.6v.1"/></svg>',
  eye: '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M1.5 8S4 3.5 8 3.5 14.5 8 14.5 8 12 12.5 8 12.5 1.5 8 1.5 8z"/><circle cx="8" cy="8" r="2"/></svg>',
  plus: '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M8 3v10M3 8h10"/></svg>',
  list: '<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M5.5 4.5h8M5.5 8h8M5.5 11.5h8"/><circle cx="2.8" cy="4.5" r=".8" fill="currentColor"/><circle cx="2.8" cy="8" r=".8" fill="currentColor"/><circle cx="2.8" cy="11.5" r=".8" fill="currentColor"/></svg>',
  epics: '<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M8.8 1.8L3.5 9h4l-.8 5.2L12.5 7h-4z"/></svg>',
  board: '<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2" y="2.5" width="3.4" height="11" rx="1"/><rect x="6.3" y="2.5" width="3.4" height="7" rx="1"/><rect x="10.6" y="2.5" width="3.4" height="9" rx="1"/></svg>',
  chev: (c) => `<svg class="chev" width="10" height="10" viewBox="0 0 10 10" style="${c ? 'transform:rotate(-90deg)' : ''}"><path d="M2 3.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>`,
  person: '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="8" cy="5.5" r="2.6"/><path d="M3 13.5c.6-2.6 2.6-4 5-4s4.4 1.4 5 4"/></svg>',
  search: '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5L14 14"/></svg>',
  check: '<svg width="9" height="9" viewBox="0 0 10 10"><path d="M2 5.2l2 2 4-4.4" fill="none" stroke="#fff" stroke-width="1.6"/></svg>',
  caret: '<svg width="9" height="9" viewBox="0 0 10 10"><path d="M2 3.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>',
};

const SHELL = `
<div class="app" id="app">
  <aside class="sidebar">
    <div class="ws"><div class="ws-logo">A</div><div class="ws-name" id="ws-name"></div></div>
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
      <div class="tabs" id="tabs"></div>
      <span class="spacer"></span>
      <span class="sync hide-sm" id="sync-text"></span>
      <button class="icon-btn" id="refresh" title="Refresh" data-act="refresh">${I.refresh}</button>
      <button class="btn-primary sm" data-act="new" title="New issue (C)">${I.plus}<span class="hide-sm" id="new-label">New issue</span></button>
    </header>
    <div class="toolbar" id="toolbar"></div>
    <div class="content" id="content"></div>
    <section class="detail" id="detail">
      <div class="detail-top">
        <span id="d-crumb" class="d-crumb"></span>
        <span class="spacer"></span>
        <span class="saving" id="d-saving"></span>
        <span class="ext" data-act="browser">${I.ext}<span class="hide-sm">Open in browser</span></span>
        <button class="icon-btn" data-act="close-detail" title="Close (Esc)">${I.close}</button>
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
    <p class="lede">Manage issues, epics and boards in a fast desktop client.</p>
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
      <span class="hint"><a class="lnk" data-act="token-help">Create an API token</a> in your account settings. Tokens expire after at most a year.</span>
    </div>
    <div class="form-error" id="form-error"></div>
    <button class="btn-primary" id="signin-btn" type="submit">Sign in</button>
    <div class="foot">${I.lock}The token goes to your system keychain. Only the site and email are saved to disk.</div>
  </form>
</div>

<div class="modal-back" id="modal"></div>
<div class="menu" id="menu"></div>
<div class="toast" id="toast"></div>

<div class="knobs" id="knobs">
  <div class="knobs-panel">
    <form id="knobs-form">
      <fieldset>
        <legend>Screen</legend>
        <label><input type="radio" name="screen" value="signin">Sign-in</label>
        <label><input type="radio" name="screen" value="app" checked>App</label>
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
        <legend>View data</legend>
        <label><input type="radio" name="data" value="loaded" checked>Loaded</label>
        <label><input type="radio" name="data" value="loading">First load</label>
        <label><input type="radio" name="data" value="empty">Empty</label>
        <label><input type="radio" name="data" value="error">Error</label>
      </fieldset>
      <fieldset>
        <legend>Next write to Jira</legend>
        <label><input type="radio" name="write" value="ok" checked>Succeeds</label>
        <label><input type="radio" name="write" value="fail">Fails (500)</label>
        <label><input type="radio" name="write" value="screen">Status change needs a Jira screen</label>
      </fieldset>
      <fieldset>
        <legend>Theme</legend>
        <label><input type="radio" name="theme" value="dark" checked>Dark</label>
        <label><input type="radio" name="theme" value="light">Light</label>
      </fieldset>
      <div class="note">These knobs drive the mockup state. They are not part of the app.</div>
    </form>
  </div>
  <div class="knobs-btn" data-act="knobs">
    <svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 5h10M3 11h10"/><circle cx="6" cy="5" r="1.6" fill="var(--raised)"/><circle cx="10" cy="11" r="1.6" fill="var(--raised)"/></svg>
    Mockup knobs
  </div>
</div>`;
document.body.insertAdjacentHTML('afterbegin', SHELL);

const SITE = 'acme-labs.atlassian.net';
const ME = { name: 'Sam Rivera', color: '#7c6cf0' };
const PEOPLE = {
  me: ME,
  ada: { name: 'Ada Okafor', color: '#d9467a' },
  milo: { name: 'Milo Tran', color: '#2f9e8f' },
  rin: { name: 'Rin Sato', color: '#c27c0e' },
  lee: { name: 'Lee Brandt', color: '#4a72d9' },
};
const STATUS = {
  'In Progress': { cat: 'indeterminate', icon: 'progress' },
  'In Review': { cat: 'indeterminate', icon: 'review' },
  'To Do': { cat: 'new', icon: 'todo' },
  'Backlog': { cat: 'new', icon: 'backlog' },
  'Done': { cat: 'done', icon: 'done' },
};
const PROJECTS = [
  {
    key: 'CASE', name: 'Case Platform', team: 'Intake team', color: '#7c6cf0', style: 'Company-managed',
    statuses: ['In Progress', 'In Review', 'To Do', 'Done'], initial: 'To Do',
    noTransition: [['In Review', 'To Do']],
    board: { name: 'CASE board', type: 'scrum', sprint: 'Sprint 14', ends: 'ends Nov 28', sprints: [
      { id: 14, name: 'Sprint 14', state: 'active', dates: 'Nov 17 to Nov 28', goal: 'Intake v2 on staging' },
      { id: 15, name: 'Sprint 15', state: 'future', dates: 'Dec 1 to Dec 12', goal: 'Audit trail, first slice' },
      { id: 16, name: 'Sprint 16', state: 'future', dates: 'No dates yet', goal: '' },
    ], columns: [['To Do', ['To Do']], ['In Progress', ['In Progress']], ['In Review', ['In Review']], ['Done', ['Done']]] },
  },
  {
    key: 'CASE1', name: 'Case Portal', team: 'Portal team', color: '#3fb68b', style: 'Team-managed',
    statuses: ['In Progress', 'To Do', 'Backlog', 'Done'], initial: 'Backlog', noTransition: [],
    board: { name: 'CASE1 board', type: 'kanban', backlogStatus: 'Backlog', columns: [['To Do', ['To Do']], ['In Progress', ['In Progress']], ['Done', ['Done']]] },
  },
  {
    key: 'OPS', name: 'Operations', team: 'Platform ops', color: '#4ea7fc', style: 'Company-managed',
    statuses: ['In Progress', 'To Do', 'Done'], initial: 'To Do', noTransition: [],
    board: { name: 'OPS board', type: 'kanban', columns: [['To Do', ['To Do']], ['In Progress', ['In Progress']], ['Done', ['Done']]] },
  },
];
const PRIORITIES = ['Highest', 'High', 'Medium', 'Low', 'Lowest'];
const TYPES = { Bug: '#eb5757', Story: '#3fb68b', Task: '#4ea7fc', Epic: '#a78bfa' };
const STANDARD = ['Bug', 'Story', 'Task'];

const RICH = [
  { t: 'h2', c: 'What happens' },
  { t: 'p', c: [['text', 'A draft saved on step 3 is gone after the session times out. '], ['mention', 'ada'], ['text', ' saw it on staging after '], ['key', 'CASE-128'], ['text', ' shipped.']] },
  { t: 'ol', c: ['Fill the intake form to step 3.', 'Wait 30 minutes.', 'Press Next.'] },
  { t: 'panel', kind: 'Info panel' },
  { t: 'pre', lang: 'rust', c: 'let draft = store.draft(case_id).await?;\nassert!(draft.is_some());' },
  { t: 'table', kind: 'Table with merged cells' },
  { t: 'tasks', c: [[true, 'Reproduced on staging'], [false, 'Draft survives a timeout']] },
];
const SHORT = [
  { t: 'p', c: [['text', 'The reviewer picks a new owner from the queue without opening the case. Keep the current sort order.']] },
  { t: 'ul', c: ['Only reviewers see the action.', 'The old owner gets no notification.'] },
];
const EPIC_DOC = [
  { t: 'p', c: [['text', 'Replace the single intake page with a five-step form that saves a draft at every step.']] },
  { t: 'h3', c: 'Done when' },
  { t: 'tasks', c: [[false, 'Every step saves a draft'], [false, 'The rollout checklist is signed off']] },
];
const AUDIT_DOC = [{ t: 'p', c: [['text', 'Keep a record of every status and owner change on a case, for the yearly audit.']] }];
const PORTAL_DOC = [{ t: 'p', c: [['text', 'Claimants check the status of their case without calling support.']] }];

let ISSUES = [
  ['CASE-100', 'Epic', 'Intake form v2', 'In Progress', 1, 'me', null, '1d', EPIC_DOC, true],
  ['CASE-120', 'Epic', 'Audit trail for case changes', 'To Do', 2, 'ada', null, '4d', AUDIT_DOC, true],
  ['CASE-90', 'Epic', 'Move attachments to object storage', 'Done', 2, 'milo', null, '21d', null, true],
  ['CASE-131', 'Bug', 'Intake form loses the draft after a session timeout', 'In Progress', 1, 'me', 'CASE-100', '2h', RICH, true],
  ['CASE-139', 'Bug', 'Double-clicking Submit creates two cases', 'To Do', 0, 'milo', 'CASE-100', '3h', SHORT, true],
  ['CASE-128', 'Story', 'Postcode lookup on the address step', 'In Review', 2, 'ada', 'CASE-100', '5h', SHORT, true],
  ['CASE-136', 'Task', 'Write the intake v2 rollout checklist', 'To Do', 3, 'rin', 'CASE-100', '1d', null, true],
  ['CASE-135', 'Story', 'Reassign a case from the review queue', 'To Do', 2, 'me', null, '1d', SHORT, true],
  ['CASE-117', 'Bug', 'Case list sorts Updated as text', 'Done', 3, 'ada', null, '2d', SHORT, true],
  ['CASE-122', 'Story', 'Record who changed a case status and when', 'To Do', 2, null, 'CASE-120', '4d', SHORT, false],
  ['CASE-123', 'Task', 'Retention policy for audit records', 'To Do', 3, null, 'CASE-120', '4d', null, false],
  ['CASE-141', 'Task', 'Upgrade the PDF renderer', 'To Do', 4, null, null, '6d', null, false],
  ['CASE-96', 'Task', 'Copy legacy attachments', 'Done', 2, 'milo', 'CASE-90', '22d', null, true],
  ['CASE-97', 'Story', 'Serve attachments from signed URLs', 'Done', 2, 'milo', 'CASE-90', '21d', SHORT, true],
  ['CASE1-20', 'Epic', 'Self-service status page', 'In Progress', 1, 'lee', null, '2d', PORTAL_DOC, true],
  ['CASE1-30', 'Epic', 'Accessible forms', 'To Do', 2, 'rin', null, '5d', null, true],
  ['CASE1-41', 'Story', 'Show case status to the claimant without login', 'In Progress', 1, 'lee', 'CASE1-20', '4h', SHORT, true],
  ['CASE1-44', 'Bug', 'Status page shows times in UTC', 'To Do', 2, 'me', 'CASE1-20', '1d', SHORT, true],
  ['CASE1-45', 'Task', 'Add the status page to the sitemap', 'Done', 3, 'lee', 'CASE1-20', '3d', null, true],
  ['CASE1-38', 'Bug', 'Focus lost after closing the upload dialog', 'In Progress', 2, 'rin', 'CASE1-30', '6h', SHORT, true],
  ['CASE1-47', 'Story', 'Label every form field for screen readers', 'Backlog', 2, null, 'CASE1-30', '5d', null, true],
  ['CASE1-49', 'Task', 'Check colour contrast on buttons', 'Backlog', 3, null, null, '8d', null, true],
  ['CASE1-36', 'Story', 'Email the claimant when the status changes', 'Done', 2, 'me', null, '9d', SHORT, true],
  ['OPS-12', 'Task', 'Rotate the staging database credentials', 'To Do', 1, 'me', null, '2d', SHORT, true],
  ['OPS-14', 'Task', 'Alert when the backup runs over an hour', 'In Progress', 1, 'ada', null, '6h', SHORT, true],
  ['OPS-9', 'Bug', 'Support inbox forwards to the old address', 'Done', 3, 'rin', null, '15d', null, true],
  ['CASE-143', 'Story', 'Export the audit trail as CSV', 'To Do', 3, null, 'CASE-120', '2d', null, 15],
].map(([key, type, summary, status, priority, assignee, parent, updated, desc, sprint]) =>
  ({ key, proj: key.split('-')[0], type, summary, status, priority, assignee, parent, updated, desc, sprint: key.startsWith('CASE-') ? (sprint === true ? 14 : sprint || null) : null }));
issueByKey('CASE-122').sprint = 15;
function issueByKey(k) { return ISSUES.find((i) => i.key === k); }

const M = window.MOCK || {};
const state = {
  screen: M.screen || 'app',
  signin: 'idle',
  outcome: 'idle',
  data: 'loaded',
  write: 'ok',
  proj: M.proj || 'CASE',
  view: M.view || 'issues',
  boardTab: M.boardTab || 'board',
  type: 'all',
  epic: 'any',
  assignee: 'any',
  prio: 'any',
  status: 'any',
  q: '',
  picked: new Set(),
  lastPicked: null,
  showDone: false,
  sel: 0,
  card: null,
  openId: M.openId || null,
  expanded: { CASE: true, CASE1: true },
  collapsed: {},
  editing: null,
  descTab: 'write',
  modal: null,
  pending: {},
  refreshing: false,
};

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const project = (k = state.proj) => PROJECTS.find((p) => p.key === k);
const issue = (k) => ISSUES.find((i) => i.key === k);
const cat = (s) => STATUS[s].cat;
const CAT_ORDER = { indeterminate: 0, new: 1, done: 2 };
const isEpic = (i) => i.type === 'Epic';

function statusIcon(name, size = 14) {
  const key = STATUS[name].icon;
  const ring = (stroke, dash = '') => `<circle cx="7" cy="7" r="5.5" fill="none" stroke="${stroke}" stroke-width="1.5" ${dash}/>`;
  let inner = '';
  if (key === 'backlog') inner = ring('var(--muted)', 'stroke-dasharray="2 2"');
  else if (key === 'todo') inner = ring('var(--text-2)');
  else if (key === 'progress') inner = ring('var(--amber)') + '<path d="M7 7V3.5A3.5 3.5 0 0 1 7 10.5Z" fill="var(--amber)"/>';
  else if (key === 'review') inner = ring('var(--green)') + '<path d="M7 7V3.5A3.5 3.5 0 1 1 3.5 7Z" fill="var(--green)"/>';
  else if (key === 'done') inner = '<circle cx="7" cy="7" r="6.25" fill="var(--accent)"/><path d="M4.4 7.2l1.8 1.8 3.4-3.6" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>';
  return `<svg width="${size}" height="${size}" viewBox="0 0 14 14" role="img" aria-label="${esc(name)}"><title>${esc(name)}</title>${inner}</svg>`;
}
function priorityIcon(p) {
  const title = `<title>${PRIORITIES[p]} priority</title>`;
  if (p === 0) return `<svg width="14" height="14" viewBox="0 0 14 14" role="img">${title}<rect x="1" y="1" width="12" height="12" rx="3" fill="#f2994a"/><path d="M7 3.8v4" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/><circle cx="7" cy="10.2" r=".9" fill="#fff"/></svg>`;
  const filled = { 1: 3, 2: 2, 3: 1, 4: 0 }[p];
  const bars = [[2, 8, 3], [6, 5, 6], [10, 2, 9]].map(([x, y, h], i) =>
    `<rect x="${x}" y="${y}" width="2.4" height="${h}" rx=".6" fill="${i < filled ? 'var(--text-2)' : 'var(--border-strong)'}"/>`).join('');
  return `<svg width="14" height="14" viewBox="0 0 14 14" role="img">${title}${bars}</svg>`;
}
function typeIcon(t, size = 14) {
  const mark = {
    Bug: '<circle cx="7" cy="7" r="2.2" fill="#fff"/>',
    Story: '<path d="M4.8 3.8h4.4v6.6L7 8.8l-2.2 1.6z" fill="#fff"/>',
    Task: '<path d="M4.3 7.2l1.9 1.9 3.6-3.8" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
    Epic: '<path d="M7.6 3L4.6 7.4h2.2l-.4 3.6 3-4.6H7.2z" fill="#fff"/>',
  }[t];
  return `<svg width="${size}" height="${size}" viewBox="0 0 14 14" role="img" aria-label="${t}"><title>${t}</title><rect x="1" y="1" width="12" height="12" rx="3" fill="${TYPES[t]}"/>${mark}</svg>`;
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
function epicChip(key) {
  if (!key) return '';
  const e = issue(key);
  return `<span class="chip" data-open="${key}" title="Epic ${key}">${typeIcon('Epic', 12)}<span>${esc(e.summary)}</span></span>`;
}

function blocked(p, from, to) {
  return p.noTransition.some(([a, b]) => a === from && b === to);
}
function transitionsFor(i) {
  const p = project(i.proj);
  return p.statuses.filter((s) => s !== i.status && !blocked(p, i.status, s));
}
function epicsOf(p = state.proj) {
  return ISSUES.filter((i) => i.proj === p && isEpic(i));
}
function childrenOf(key) {
  return ISSUES.filter((i) => i.parent === key);
}
function progress(key) {
  const c = childrenOf(key);
  const n = (k) => c.filter((i) => cat(i.status) === k).length;
  return { total: c.length, done: n('done'), doing: n('indeterminate'), todo: n('new') };
}
function progressBar(key) {
  const g = progress(key);
  if (!g.total) return '<span class="bar empty" title="No child issues"></span><span class="pct">No issues</span>';
  const w = (n) => `${(100 * n / g.total).toFixed(1)}%`;
  return `<span class="bar" title="${g.done} done, ${g.doing} in progress, ${g.todo} to do"><i class="d" style="width:${w(g.done)}"></i><i class="p" style="width:${w(g.doing)}"></i></span><span class="pct">${g.done} of ${g.total}</span>`;
}

function filtered(list) {
  const q = state.q.trim().toLowerCase();
  return list
    .filter((i) => state.type === 'all' || i.type === state.type)
    .filter((i) => state.epic === 'any' || (state.epic === 'none' ? !i.parent : i.parent === state.epic))
    .filter((i) => state.assignee === 'any' || (state.assignee === 'none' ? !i.assignee : i.assignee === state.assignee))
    .filter((i) => state.prio === 'any' || i.priority === state.prio)
    .filter((i) => state.status === 'any' || i.status === state.status)
    .filter((i) => !q || i.key.toLowerCase().includes(q) || i.summary.toLowerCase().includes(q));
}
const filtersOn = () => state.type !== 'all' || state.epic !== 'any' || state.assignee !== 'any' || state.prio !== 'any' || state.status !== 'any' || !!state.q.trim();
const inBacklog = () => state.view === 'board' && state.boardTab === 'backlog' && hasBacklog();
const pickable = (i) => cat(i.status) !== 'done';
function clearFilters() {
  Object.assign(state, { type: 'all', epic: 'any', assignee: 'any', prio: 'any', status: 'any', q: '', sel: 0 });
}
function listIssues() {
  if (state.data === 'empty') return [];
  return filtered(ISSUES.filter((i) => i.proj === state.proj && !isEpic(i)))
    .filter((i) => state.showDone || cat(i.status) !== 'done');
}
function listEpics() {
  if (state.data === 'empty') return [];
  return epicsOf().filter((i) => state.showDone || cat(i.status) !== 'done');
}
function groupsOf(items) {
  const p = project();
  return [...p.statuses].sort((a, b) => CAT_ORDER[cat(a)] - CAT_ORDER[cat(b)])
    .map((s) => ({ s, items: items.filter((i) => i.status === s).sort((a, b) => a.priority - b.priority) }))
    .filter((g) => g.items.length);
}
function ordered() {
  if (state.view === 'board' && state.boardTab === 'backlog') return backlogSections().flatMap((g) => state.collapsed[g.key] ? [] : g.items);
  const items = state.view === 'epics' ? listEpics() : listIssues();
  return groupsOf(items).flatMap((g) => state.collapsed[g.s] ? [] : g.items);
}
function boardIssues() {
  if (state.data === 'empty') return [];
  const p = project();
  return filtered(ISSUES.filter((i) => i.proj === p.key && !isEpic(i)))
    .filter((i) => p.board.type === 'scrum' ? i.sprint === activeSprint(p)?.id : i.status !== p.board.backlogStatus);
}
function backlogIssues() {
  if (state.data === 'empty') return [];
  const p = project();
  return filtered(ISSUES.filter((i) => i.proj === p.key && !isEpic(i)))
    .filter((i) => p.board.type === 'scrum' ? !i.sprint && cat(i.status) !== 'done' : i.status === p.board.backlogStatus);
}
const activeSprint = (p = project()) => (p.board.sprints || []).find((x) => x.state === 'active');
function backlogSections() {
  const p = project();
  if (p.board.type !== 'scrum') return [{ key: 'backlog', items: backlogIssues() }];
  if (state.data === 'empty') return [];
  const mine = filtered(ISSUES.filter((i) => i.proj === p.key && !isEpic(i)));
  const all = ISSUES.filter((i) => i.proj === p.key && !isEpic(i));
  return p.board.sprints.map((sp) => ({ key: `sprint:${sp.id}`, sprint: sp, items: mine.filter((i) => i.sprint === sp.id), all: all.filter((i) => i.sprint === sp.id).length }))
    .concat([{ key: 'backlog', items: backlogIssues(), all: all.filter((i) => !i.sprint && pickable(i)).length }]);
}
const hasBacklog = (p = project()) => p.board.type === 'scrum' || !!p.board.backlogStatus;

function renderSidebar() {
  $('#ws-name').textContent = SITE;
  $('#nav').innerHTML = `<div class="nav-section">Projects</div>` + PROJECTS.map((p) => {
    const open = state.expanded[p.key];
    const item = (view, icon, label) => `<div class="nav-item sub ${state.proj === p.key && state.view === view ? 'active' : ''}" data-nav="${p.key}:${view}">${icon}<span class="t">${label}</span></div>`;
    return `<div class="nav-item proj" data-toggle="${p.key}">${projDot(p.key)}<span class="t">${esc(p.name)}</span><span class="pkey">${p.key}</span>${I.chev(!open)}</div>` +
      (open ? item('issues', I.list, 'Issues') + item('epics', I.epics, 'Epics') + item('board', I.board, 'Board') : '');
  }).join('');
  $('#me-avatar').outerHTML = avatar('me', 'lg').replace('class="avatar', 'id="me-avatar" class="avatar');
  $('#me-name').textContent = ME.name;
}

function renderTop() {
  const p = project();
  const label = { issues: 'Issues', epics: 'Epics', board: p.board.name }[state.view];
  $('#crumb').innerHTML = `${projDot(p.key)}<span>${esc(p.name)}</span><span class="sep">›</span><span>${esc(label)}</span>`;
  $('#tabs').innerHTML = state.view === 'board' && hasBacklog(p)
    ? ['board', 'backlog'].map((t) => `<div class="tab ${state.boardTab === t ? 'active' : ''}" data-btab="${t}">${t === 'board' ? 'Board' : `Backlog <span class="n">${backlogIssues().length}</span>`}</div>`).join('')
    : '';
  const busy = state.refreshing || state.data === 'loading';
  $('#sync-text').textContent = busy ? 'Refreshing…' : state.data === 'error' ? 'Refresh failed' : 'Updated just now';
  $('#refresh').classList.toggle('spin', busy);
  $('#new-label').textContent = state.view === 'epics' ? 'New epic' : 'New issue';
}

function typeChips() {
  return `<div class="seg">${['all', ...STANDARD].map((t) => `<span class="seg-i ${state.type === t ? 'on' : ''}" data-type="${t}">${t === 'all' ? 'All types' : typeIcon(t, 12) + t}</span>`).join('')}</div>`;
}
function epicFilter() {
  const label = state.epic === 'any' ? 'Any epic' : state.epic === 'none' ? 'No epic' : issue(state.epic).summary;
  return `<span class="filter ${state.epic !== 'any' ? 'on' : ''}" data-pick="epic-filter">${typeIcon('Epic', 12)}<span class="t">${esc(label)}</span>${I.caret}</span>`;
}
function pillFilter(kind, icon, label, on) {
  return `<span class="filter ${on ? 'on' : ''}" data-pick="${kind}">${icon}<span class="t">${esc(label)}</span>${I.caret}</span>`;
}
function moreFilters() {
  const who = state.assignee === 'any' ? 'Any assignee' : state.assignee === 'none' ? 'Unassigned' : PEOPLE[state.assignee].name;
  const pr = state.prio === 'any' ? 'Any priority' : PRIORITIES[state.prio];
  const st = state.status === 'any' ? 'Any status' : state.status;
  return pillFilter('assignee-filter', state.assignee === 'any' || state.assignee === 'none' ? I.person : avatar(state.assignee, 'xs'), who, state.assignee !== 'any') +
    pillFilter('priority-filter', priorityIcon(state.prio === 'any' ? 2 : state.prio), pr, state.prio !== 'any') +
    pillFilter('status-filter', statusIcon(state.status === 'any' ? 'To Do' : state.status, 12), st, state.status !== 'any');
}
function searchBox() {
  return `<label class="search">${I.search}<input id="q" value="${esc(state.q)}" placeholder="Key or text" autocomplete="off" spellcheck="false"><span class="kbd">/</span></label>`;
}
function clearLink() {
  return filtersOn() ? '<span class="clear" data-act="clear-filters">Clear filters</span>' : '';
}
function doneToggle(what) {
  return `<span class="filter ${state.showDone ? 'on' : ''}" data-act="toggle-done">${statusIcon('Done', 12)}${state.showDone ? `Showing done ${what}` : `Show done ${what}`}</span>`;
}
function jqlFor() {
  const p = state.proj;
  const done = state.showDone ? '' : ' AND statusCategory != Done';
  if (state.view === 'epics') return `project = ${p} AND issuetype = Epic${done} ORDER BY Rank`;
  if (state.view === 'board') return `Board "${project().board.name}" (${project().board.type})`;
  const type = state.type === 'all' ? ' AND issuetype in standardIssueTypes()' : ` AND issuetype = ${state.type}`;
  const epic = state.epic === 'any' ? '' : state.epic === 'none' ? ' AND parent is EMPTY' : ` AND parent = ${state.epic}`;
  const who = state.assignee === 'any' ? '' : state.assignee === 'none' ? ' AND assignee is EMPTY' : ` AND assignee = "${PEOPLE[state.assignee].name}"`;
  const pr = state.prio === 'any' ? '' : ` AND priority = ${PRIORITIES[state.prio]}`;
  const st = state.status === 'any' ? '' : ` AND status = "${state.status}"`;
  const q = state.q.trim() ? ` AND text ~ "${state.q.trim()}"` : '';
  return `project = ${p}${type}${epic}${who}${pr}${st}${q}${done} ORDER BY Rank`;
}
function renderToolbar() {
  const p = project();
  let left = '', right = '';
  if (state.view === 'issues') {
    const n = listIssues().length;
    left = typeChips() + epicFilter() + moreFilters() + searchBox() + doneToggle('issues') + clearLink();
    right = `<span class="total" title="${esc(jqlFor())}">${n} issue${n === 1 ? '' : 's'}</span>`;
  } else if (state.view === 'epics') {
    const n = listEpics().length;
    left = doneToggle('epics');
    right = `<span class="total" title="${esc(jqlFor())}">${n} epic${n === 1 ? '' : 's'}</span>`;
  } else {
    left = typeChips() + epicFilter() + moreFilters() + searchBox() + clearLink();
    right = inBacklog() ? ''
      : p.board.type === 'scrum'
        ? `<span class="pill" title="Scrum board">${statusIcon('In Progress', 12)}${p.board.sprint} · ${p.board.ends}</span>`
        : '<span class="total">Kanban board</span>';
  }
  const had = document.activeElement?.id === 'q';
  const pos = had ? document.activeElement.selectionStart : 0;
  $('#toolbar').innerHTML = `<div class="tb-left">${left}</div><span class="spacer"></span>${right}`;
  if (had && $('#q')) { $('#q').focus(); $('#q').setSelectionRange(pos, pos); }
}

function skeleton() {
  return Array.from({ length: 9 }, (_, i) => `<div class="skel"><i style="width:14px"></i><i style="width:52px"></i><i style="width:14px"></i><i style="width:${38 + (i * 13) % 34}%"></i><span class="spacer"></span><i style="width:20px;height:20px;border-radius:50%"></i></div>`).join('');
}
function errorBox(what) {
  return `<div class="empty">${I.warn.replace('width="14" height="14"', 'width="28" height="28"')}<h3>Couldn't load ${what}</h3><p>Jira answered with 503 Service Unavailable. Your last changes were saved before this.</p><button class="btn" data-act="retry">${I.refresh}Try again</button></div>`;
}
function emptyBox(title, body, btn = '') {
  return `<div class="empty"><svg width="28" height="28" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="8" cy="8" r="5.5"/><path d="M5.5 8.2l1.7 1.7 3.3-3.4"/></svg><h3>${title}</h3><p>${body}</p>${btn}</div>`;
}

function issueRow(i, flat, o = {}) {
  const on = state.picked.has(i.key);
  const box = o.pick === undefined ? '' : o.pick
    ? `<span class="pick-box ${on ? 'on' : ''}" data-pickrow="${i.key}" title="Select (X)">${on ? I.check : ''}</span>`
    : '<span class="pick-box gap"></span>';
  return `<div class="row ${flat.indexOf(i) === state.sel ? 'sel' : ''} ${state.pending[i.key] ? 'pending' : ''} ${on ? 'picked' : ''}" data-id="${i.key}" ${o.drag ? 'draggable="true"' : ''}>
    ${box}
    ${priorityIcon(i.priority)}
    <span class="id">${i.key}</span>
    ${statusIcon(i.status)}
    ${typeIcon(i.type)}
    <span class="title">${esc(i.summary)}</span>
    <span class="meta">${epicChip(i.parent)}</span>
    ${avatar(i.assignee)}
    ${o.act || ''}
    <span class="date" title="Updated">${i.updated}</span>
  </div>`;
}
function epicRow(e, flat) {
  return `<div class="row epic-row ${flat.indexOf(e) === state.sel ? 'sel' : ''} ${state.pending[e.key] ? 'pending' : ''}" data-id="${e.key}">
    ${typeIcon('Epic')}
    <span class="id">${e.key}</span>
    ${statusIcon(e.status)}
    <span class="title">${esc(e.summary)}</span>
    <span class="prog">${progressBar(e.key)}</span>
    ${avatar(e.assignee)}
    <span class="date" title="Updated">${e.updated}</span>
  </div>`;
}
function grouped(items, rowFn) {
  const flat = ordered();
  return groupsOf(items).map(({ s, items }) => {
    const c = state.collapsed[s];
    return `<div class="group-head" data-group="${esc(s)}">${I.chev(c)}${statusIcon(s)}<span>${esc(s)}</span><span class="n">${items.length}</span></div>` +
      (c ? '' : items.map((i) => rowFn(i, flat)).join(''));
  }).join('');
}

function renderIssues() {
  const p = project();
  const items = listIssues();
  if (!items.length) {
    const filteredOut = state.type !== 'all' || state.epic !== 'any';
    return filteredOut
      ? emptyBox('No issues match these filters', 'Clear the type or epic filter to see the rest of the project.', '<button class="btn" data-act="clear-filters">Clear filters</button>')
      : emptyBox(`No open issues in ${esc(p.name)}`, 'Create the first Bug, Story or Task for this project.', `<button class="btn" data-act="new">${I.plus}New issue</button>`);
  }
  return grouped(items, issueRow);
}
function renderEpics() {
  const p = project();
  const items = listEpics();
  if (!items.length) {
    return emptyBox(`No ${state.showDone ? '' : 'open '}epics in ${esc(p.name)}`, 'An epic groups the Bugs, Stories and Tasks that deliver one larger piece of work.', `<button class="btn" data-act="new">${I.plus}New epic</button>`);
  }
  return grouped(items, epicRow);
}
function card(i) {
  return `<div class="card ${state.card === i.key ? 'sel' : ''} ${state.pending[i.key] ? 'pending' : ''}" draggable="true" data-card="${i.key}">
    <div class="c-top">${typeIcon(i.type)}<span class="id">${i.key}</span><span class="spacer"></span>${avatar(i.assignee)}</div>
    <div class="c-title">${esc(i.summary)}</div>
    <div class="c-foot">${priorityIcon(i.priority)}${epicChip(i.parent)}</div>
  </div>`;
}
function renderBoard() {
  const p = project();
  const items = boardIssues();
  if (!items.length && state.data === 'empty') {
    return emptyBox(`Nothing on ${esc(p.board.name)}`, p.board.type === 'scrum' ? `${p.board.sprint} has no issues. Move issues in from the backlog.` : 'No issue is in a board column yet.');
  }
  return `<div class="board">${p.board.columns.map(([name, sts], ci) => {
    const cards = items.filter((i) => sts.includes(i.status)).sort((a, b) => a.priority - b.priority);
    return `<div class="col">
      <div class="col-head">${statusIcon(sts[0])}<span>${esc(name)}</span><span class="n">${cards.length}</span></div>
      <div class="col-body" data-drop="${ci}">${cards.map(card).join('') || '<div class="col-empty">Drop issues here</div>'}</div>
    </div>`;
  }).join('')}</div>`;
}
function catCounts(items) {
  const n = (k) => items.filter((i) => cat(i.status) === k).length;
  return `<span class="cc" title="To do"><i class="c-new"></i>${n('new')}</span><span class="cc" title="In progress"><i class="c-ip"></i>${n('indeterminate')}</span><span class="cc" title="Done"><i class="c-done"></i>${n('done')}</span>`;
}
function moveBtn(i) {
  if (cat(i.status) === 'done') return '<span class="row-act-gap"></span>';
  return `<button class="btn sm row-act" data-pick="move-sprint" data-key="${i.key}">Move to ${I.caret}</button>`;
}
function renderSprintBacklog() {
  const p = project();
  const flat = ordered();
  const row = (i) => issueRow(i, flat, { pick: pickable(i), drag: pickable(i), act: moveBtn(i) });
  const of = (g) => filtersOn() ? `${g.items.length} of ${g.all}` : `${g.items.length} issue${g.items.length === 1 ? '' : 's'}`;
  return backlogSections().map((g) => {
    const c = state.collapsed[g.key];
    const sp = g.sprint;
    const head = sp
      ? `<div class="sprint-head" data-group="${g.key}">${I.chev(c)}<b>${esc(sp.name)}</b><span class="state ${sp.state}">${sp.state === 'active' ? 'Active' : 'Future'}</span><span class="muted">${esc(sp.dates)}</span>${sp.goal ? `<span class="goal">${esc(sp.goal)}</span>` : ''}<span class="spacer"></span>${catCounts(g.items)}<span class="n">${of(g)}</span></div>`
      : `<div class="sprint-head backlog" data-group="backlog">${I.chev(c)}<b>Backlog</b><span class="muted">Open issues in no sprint</span><span class="spacer"></span>${catCounts(g.items)}<span class="n">${of(g)}</span></div>`;
    const empty = filtersOn() && g.all ? 'No issue here matches the filters.' : sp ? `No issues in ${esc(sp.name)} yet. Drag issues here or use Move to.` : 'Every open issue is in a sprint.';
    return `<div class="sprint-sec" data-dropsprint="${sp ? sp.id : 'backlog'}">` + head + (c ? '' : g.items.map(row).join('') || `<div class="sprint-empty">${empty}</div>`) + '</div>';
  }).join('') + selBar() + `<div class="backlog-note">Sprints are created, started and completed in Jira. <a class="lnk" data-act="browser-backlog">Open the backlog in the browser</a></div>`;
}
function selBar() {
  const n = state.picked.size;
  if (!n) return '';
  const scrum = project().board.type === 'scrum';
  return `<div class="sel-bar"><b>${n} selected</b>${scrum
    ? `<button class="btn-primary sm" data-pick="move-picked">Move to ${I.caret}</button><span class="hint">or drag them onto a sprint · <span class="kbd">M</span></span>`
    : '<button class="btn-primary sm" data-act="picked-to-board">Move to board</button>'}<span class="spacer"></span><span class="clear" data-act="clear-picked">Clear <span class="kbd">Esc</span></span></div>`;
}
function togglePick(key, range) {
  const flat = ordered().filter(pickable);
  if (range && state.lastPicked) {
    const a = flat.findIndex((i) => i.key === state.lastPicked);
    const b = flat.findIndex((i) => i.key === key);
    if (a >= 0 && b >= 0) flat.slice(Math.min(a, b), Math.max(a, b) + 1).forEach((i) => state.picked.add(i.key));
  } else if (state.picked.has(key)) state.picked.delete(key);
  else if (pickable(issue(key))) state.picked.add(key);
  state.lastPicked = key;
}
function moveMany(keys, to) {
  const p = project();
  const xs = keys.map(issue).filter((x) => x && pickable(x) && x.sprint !== to);
  if (!xs.length) return;
  const before = xs.map((x) => [x, x.sprint]);
  xs.forEach((x) => { x.sprint = to; state.pending[x.key] = true; });
  state.picked.clear();
  render();
  setTimeout(() => {
    xs.forEach((x) => delete state.pending[x.key]);
    const name = to ? p.board.sprints.find((sp) => sp.id === to).name : 'the backlog';
    if (state.write === 'fail') {
      before.forEach(([x, sp]) => { x.sprint = sp; });
      toast(`${I.warn}<span>Couldn't move ${xs.length === 1 ? xs[0].key : `${xs.length} issues`}. Jira answered 500. Nothing moved.</span>`, 4000);
    } else {
      xs.forEach((x) => { x.updated = 'now'; });
      toast(xs.length === 1 ? `${xs[0].key} moved to ${name}` : `Moved ${xs.length} issues to ${name}`);
    }
    render();
  }, 650);
}
function sprintMenuItems(exclude, allowBacklog) {
  const p = project();
  return p.board.sprints.filter((sp) => sp.id !== exclude)
    .map((sp) => ({ value: sp.id, html: `<span>${esc(sp.name)}</span><span class="muted sm">${sp.state === 'active' ? 'active, on the board' : sp.dates}</span>` }))
    .concat(allowBacklog ? [{ value: null, html: '<span>Backlog</span><span class="muted sm">no sprint</span>' }] : []);
}
function renderBacklog() {
  const p = project();
  if (p.board.type === 'scrum') return renderSprintBacklog();
  const items = backlogIssues();
  if (!items.length) return emptyBox('The backlog is empty', p.board.type === 'scrum' ? `Every open issue is in ${p.board.sprint}.` : 'Every open issue is on the board.');
  const flat = ordered();
  const act = p.board.type === 'scrum' ? `Move to ${p.board.sprint}` : 'Move to board';
  return `<div class="backlog-note">${p.board.type === 'scrum' ? `Issues not in ${p.board.sprint}, in the order Jira ranks them.` : `Issues in the ${p.board.backlogStatus} status, in the order Jira ranks them.`}</div>` +
    items.map((i) => issueRow(i, flat, { pick: true, act: `<button class="btn sm row-act" data-act="to-board" data-key="${i.key}">${act}</button>` })).join('') + selBar();
}
function renderContent() {
  if (state.data === 'loading') return skeleton();
  if (state.data === 'error') return errorBox({ issues: 'issues', epics: 'epics', board: 'the board' }[state.view]);
  if (state.view === 'issues') return renderIssues();
  if (state.view === 'epics') return renderEpics();
  return state.boardTab === 'backlog' && hasBacklog() ? renderBacklog() : renderBoard();
}

function inline(parts) {
  return parts.map(([k, v]) => {
    if (k === 'text') return esc(v);
    if (k === 'code') return `<code>${esc(v)}</code>`;
    if (k === 'strong') return `<strong>${esc(v)}</strong>`;
    if (k === 'mention') return `<span class="mention">@${esc(PEOPLE[v].name)}</span>`;
    if (k === 'key') return `<span class="key" data-open="${v}">${v}</span>`;
    return '';
  }).join('');
}
function renderMd(doc, key) {
  if (!doc || !doc.length) return '<p class="no-desc">No description.</p>';
  return doc.map((b) => {
    if (b.t === 'h2') return `<h2>${esc(b.c)}</h2>`;
    if (b.t === 'h3') return `<h3>${esc(b.c)}</h3>`;
    if (b.t === 'p') return `<p>${inline(b.c)}</p>`;
    if (b.t === 'ul') return `<ul>${b.c.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>`;
    if (b.t === 'ol') return `<ol>${b.c.map((x) => `<li>${esc(x)}</li>`).join('')}</ol>`;
    if (b.t === 'tasks') return `<ul class="tasks">${b.c.map(([on, x]) => `<li><span class="box ${on ? 'on' : ''}">${on ? '<svg width="9" height="9" viewBox="0 0 10 10"><path d="M2 5.2l2 2 4-4.4" fill="none" stroke="#fff" stroke-width="1.6"/></svg>' : ''}</span><span>${esc(x)}</span></li>`).join('')}</ul>`;
    if (b.t === 'pre') return `<pre><span class="lang">${esc(b.lang)}</span><code>${esc(b.c)}</code></pre>`;
    if (b.t === 'quote') return `<blockquote>${esc(b.c)}</blockquote>`;
    return `<div class="unsupported">${I.eye}<span><b>${esc(b.kind)}</b> is not shown here.</span><span class="open" data-act="browser" data-key="${key}">Open in browser</span></div>`;
  }).join('');
}
const unsupportedIn = (doc) => (doc || []).filter((b) => b.kind).map((b) => b.kind.toLowerCase());
function toMd(doc) {
  const inl = (parts) => parts.map(([k, v]) => k === 'code' ? `\`${v}\`` : k === 'strong' ? `**${v}**` : k === 'mention' ? `@[${PEOPLE[v].name}](accountId:5b10ac8d82e05b22cc7d4ef5)` : v).join('');
  return (doc || []).map((b) => {
    if (b.t === 'h2') return `## ${b.c}`;
    if (b.t === 'h3') return `### ${b.c}`;
    if (b.t === 'p') return inl(b.c);
    if (b.t === 'ul') return b.c.map((x) => `- ${x}`).join('\n');
    if (b.t === 'ol') return b.c.map((x, n) => `${n + 1}. ${x}`).join('\n');
    if (b.t === 'tasks') return b.c.map(([on, x]) => `- [${on ? 'x' : ' '}] ${x}`).join('\n');
    if (b.t === 'pre') return `\`\`\`${b.lang}\n${b.c}\n\`\`\``;
    if (b.t === 'quote') return `> ${b.c}`;
    return '';
  }).join('\n\n');
}
function fromMd(md) {
  const out = [];
  const lines = md.replace(/\r/g, '').split('\n');
  const inl = (s) => s.split(/(`[^`]+`|\*\*[^*]+\*\*|\b[A-Z][A-Z0-9]+-\d+\b)/).filter(Boolean).map((x) =>
    x.startsWith('`') ? ['code', x.slice(1, -1)] : x.startsWith('**') ? ['strong', x.slice(2, -2)] : /^[A-Z][A-Z0-9]+-\d+$/.test(x) ? ['key', x] : ['text', x]);
  const take = (re, map) => { const c = []; while (i < lines.length && re.test(lines[i])) c.push(map(lines[i++])); return c; };
  let i = 0;
  while (i < lines.length) {
    const l = lines[i];
    if (!l.trim()) { i++; continue; }
    if (l.startsWith('```')) {
      const lang = l.slice(3).trim() || 'text';
      const body = [];
      i++;
      while (i < lines.length && !lines[i].startsWith('```')) body.push(lines[i++]);
      i++;
      out.push({ t: 'pre', lang, c: body.join('\n') });
    } else if (l.startsWith('### ')) { out.push({ t: 'h3', c: l.slice(4) }); i++; }
    else if (/^##? /.test(l)) { out.push({ t: 'h2', c: l.replace(/^#+ /, '') }); i++; }
    else if (l.startsWith('> ')) { out.push({ t: 'quote', c: l.slice(2) }); i++; }
    else if (/^- \[[ x]\] /.test(l)) out.push({ t: 'tasks', c: take(/^- \[[ x]\] /, (x) => [x[3] === 'x', x.slice(6)]) });
    else if (/^[-*] /.test(l)) out.push({ t: 'ul', c: take(/^[-*] /, (x) => x.slice(2)) });
    else if (/^\d+\. /.test(l)) out.push({ t: 'ol', c: take(/^\d+\. /, (x) => x.replace(/^\d+\. /, '')) });
    else {
      const para = [];
      while (i < lines.length && lines[i].trim() && !/^(#|>|```|[-*] |\d+\. )/.test(lines[i])) para.push(lines[i++]);
      out.push({ t: 'p', c: inl(para.join(' ')) });
    }
  }
  return out;
}

function prop(k, v, pick) {
  return `<div class="prop"><span class="k">${k}</span><span class="v ${pick ? 'edit' : ''}" ${pick ? `data-pick="${pick}" title="Change ${k.toLowerCase()}"` : ''}>${v}</span></div>`;
}
function renderDetail() {
  const d = $('#detail');
  const i = issue(state.openId);
  d.classList.toggle('open', !!i);
  if (!i) return;
  const p = project(i.proj);
  $('#d-crumb').innerHTML = `${projDot(p.key)}<span class="hide-sm">${esc(p.name)}</span><span class="sep">›</span>${typeIcon(i.type)}<span>${i.key}</span>`;
  $('#d-saving').innerHTML = state.pending[i.key] ? `<span class="icon-btn spin" style="width:auto;height:auto">${I.refresh}</span>Saving to Jira…` : '';
  const title = state.editing === 'summary'
    ? `<input class="title-input" id="t-in" value="${esc(i.summary)}" aria-label="Summary">`
    : `<h1 class="editable" data-act="edit-summary" title="Click to edit">${esc(i.summary)}</h1>`;
  const locked = unsupportedIn(i.desc);
  let desc;
  if (state.editing === 'desc') {
    const src = $('#d-src')?.value ?? toMd(i.desc);
    desc = `<div class="editor">
      <div class="ed-tabs"><span class="ed-tab ${state.descTab === 'write' ? 'on' : ''}" data-dtab="write">Write</span><span class="ed-tab ${state.descTab === 'preview' ? 'on' : ''}" data-dtab="preview">Preview</span><span class="spacer"></span><span class="hint">Markdown</span></div>
      ${state.descTab === 'write' ? `<textarea id="d-src" spellcheck="true">${esc(src)}</textarea>` : `<textarea id="d-src" hidden>${esc(src)}</textarea><div class="md preview">${renderMd(fromMd(src), i.key)}</div>`}
      <div class="ed-foot"><span class="hint">Saved to Jira as rich text.</span><span class="spacer"></span><button class="btn" data-act="cancel-desc">Cancel</button><button class="btn-primary sm" data-act="save-desc">Save <kbd>Ctrl Enter</kbd></button></div>
    </div>`;
  } else {
    const head = `<div class="sub-head">Description<span class="spacer"></span>${locked.length
      ? `<span class="lock-note" title="Editing here would drop them">${I.lock}Holds ${locked.join(' and ')}. Edit in the browser.</span>`
      : `<button class="btn sm" data-act="edit-desc">Edit</button>`}</div>`;
    desc = head + `<div class="md">${renderMd(i.desc, i.key)}</div>`;
  }
  let children = '';
  if (isEpic(i)) {
    const kids = childrenOf(i.key).sort((a, b) => CAT_ORDER[cat(a.status)] - CAT_ORDER[cat(b.status)]);
    const g = progress(i.key);
    children = `<div class="sub-head">Child issues <span class="n">${g.total ? `${g.done} of ${g.total} done` : ''}</span><span class="spacer"></span>
        <button class="btn sm" data-pick="add-child">${I.plus}Add existing</button><button class="btn sm" data-act="new-child">${I.plus}New child issue</button></div>
      ${g.total ? `<div class="epic-prog">${progressBar(i.key)}</div>` : ''}
      ${kids.map((k) => `<div class="child-row ${state.pending[k.key] ? 'pending' : ''}" data-open="${k.key}">${typeIcon(k.type)}<span class="id">${k.key}</span>${statusIcon(k.status)}<span class="title">${esc(k.summary)}</span>${avatar(k.assignee)}<button class="icon-btn x" data-act="unlink" data-key="${k.key}" title="Remove from this epic">${I.close}</button></div>`).join('')
      || '<p class="no-desc">No issues in this epic yet. Add an existing Bug, Story or Task, or create one.</p>'}`;
  }
  $('#d-main').innerHTML = title + desc + children;
  const name = (k) => k ? `${avatar(k)}${esc(PEOPLE[k].name)}` : `${avatar(null)}<span class="muted">Unassigned</span>`;
  $('#d-props').innerHTML =
    prop('Status', `${statusIcon(i.status)}${esc(i.status)}`, 'status') +
    prop('Assignee', name(i.assignee), 'assignee') +
    prop('Priority', `${priorityIcon(i.priority)}${PRIORITIES[i.priority]}`, 'priority') +
    (isEpic(i) ? '' : prop('Epic', i.parent ? `${typeIcon('Epic')}<span class="ell">${esc(issue(i.parent).summary)}</span>` : '<span class="muted">None</span>', 'epic')) +
    '<hr>' +
    prop('Type', `${typeIcon(i.type)}${i.type}`) +
    prop('Reporter', name('ada')) +
    prop('Project', `${projDot(p.key)}<span class="ell">${esc(p.name)}</span>`) +
    '<hr>' +
    prop('Created', '<span class="muted">Nov 2</span>') +
    prop('Updated', `<span class="muted">${i.updated === 'now' ? 'just now' : i.updated + ' ago'}</span>`) +
    '<div class="keys"><span class="kbd">S</span> status <span class="kbd">A</span> assignee <span class="kbd">P</span> priority' + (isEpic(i) ? '' : ' <span class="kbd">E</span> epic') + '</div>';
  if (state.editing === 'summary') { const t = $('#t-in'); t.focus(); t.setSelectionRange(t.value.length, t.value.length); }
  if (state.editing === 'desc' && state.descTab === 'write') $('#d-src').focus();
}

function renderModal() {
  const m = $('#modal');
  m.classList.toggle('open', !!state.modal);
  if (!state.modal) { m.innerHTML = ''; return; }
  if (m.innerHTML) return;
  const p = project();
  const md = state.modal;
  const types = md.fromEpic ? STANDARD : [...STANDARD, 'Epic'];
  const opt = (v, label, cur) => `<option value="${v}" ${cur ? 'selected' : ''}>${esc(label)}</option>`;
  const lands = p.board.type === 'scrum' ? 'It lands in the backlog.' : `It starts in ${p.initial}.`;
  m.innerHTML = `<form class="modal" id="create-form" novalidate>
    <div class="modal-head">${projDot(p.key)}<span>${esc(p.name)}</span><span class="sep">›</span><span id="m-kind">New ${md.type === 'Epic' ? 'epic' : 'issue'}</span><span class="spacer"></span><button type="button" class="icon-btn" data-act="close-modal" title="Close (Esc)">${I.close}</button></div>
    <div class="seg type-seg">${types.map((t) => `<label class="seg-i ${md.type === t ? 'on' : ''}"><input type="radio" name="type" value="${t}" ${md.type === t ? 'checked' : ''}>${typeIcon(t, 12)}${t}</label>`).join('')}</div>
    <input class="m-title" id="c-summary" name="summary" placeholder="Summary" autocomplete="off">
    <textarea class="m-desc" name="desc" placeholder="Description, in Markdown"></textarea>
    <div class="m-props">
      <label>Priority<select name="priority">${PRIORITIES.map((x, n) => opt(n, x, n === 2)).join('')}</select></label>
      <label>Assignee<select name="assignee">${opt('', 'Unassigned', true)}${Object.entries(PEOPLE).map(([k, v]) => opt(k, v.name)).join('')}</select></label>
      <label class="epic-field" ${md.type === 'Epic' ? 'hidden' : ''}>Epic<select name="parent">${opt('', 'None', !md.parent)}${epicsOf().filter((e) => cat(e.status) !== 'done').map((e) => opt(e.key, `${e.key} ${e.summary}`, e.key === md.parent)).join('')}</select></label>
    </div>
    <div class="form-error" id="m-error"></div>
    <div class="m-foot"><span class="hint">Created in ${p.key}. ${lands}</span><span class="spacer"></span><button type="button" class="btn" data-act="close-modal">Cancel</button><button type="submit" class="btn-primary" id="m-submit">Create <kbd>Ctrl Enter</kbd></button></div>
  </form>`;
  $('#c-summary').focus();
}

function renderSignin() {
  $('#signin').classList.toggle('open', state.screen === 'signin');
  const err = $('#form-error');
  const msgs = {
    rejected: 'Jira rejected this email and API token. Check that the token belongs to this email and has not expired.',
    notfound: `No Jira Cloud site answers at <b>${esc(siteValue() || 'that address')}</b>. Check the site name.`,
    offline: 'Can\'t reach the site. Check your connection and try again.',
    expired: 'Your API token stopped working. Sign in again with a new token. Your site and email are kept.',
  };
  err.classList.toggle('show', !!msgs[state.signin]);
  err.innerHTML = msgs[state.signin] ? `${I.warn}<span>${msgs[state.signin]}</span>` : '';
  $('#f-site').closest('.input').classList.toggle('bad', state.signin === 'notfound');
  $('#f-token').closest('.input').classList.toggle('bad', state.signin === 'rejected' || state.signin === 'expired');
  const btn = $('#signin-btn');
  btn.disabled = state.signin === 'checking';
  btn.innerHTML = state.signin === 'checking' ? `<span class="icon-btn spin" style="width:auto;height:auto;color:#fff">${I.refresh}</span>Checking…` : 'Sign in';
}
function siteValue() {
  return $('#f-site').value.trim().replace(/^https?:\/\//, '').replace(/\/.*$/, '').replace(/\.atlassian\.net$/, '');
}

function render() {
  document.title = state.screen === 'signin' ? 'jira4manager · Sign in' : 'jira4manager';
  renderSignin();
  renderSidebar();
  renderTop();
  renderToolbar();
  $('#content').innerHTML = renderContent();
  $('#content').classList.toggle('board-mode', state.view === 'board' && state.boardTab === 'board');
  renderDetail();
  renderModal();
}

let toastTimer;
function toast(html, ms = 2600) {
  const t = $('#toast');
  t.innerHTML = html;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), ms);
}

function write(i, change, opts = {}) {
  const before = { ...i };
  Object.assign(i, change);
  state.pending[i.key] = true;
  render();
  setTimeout(() => {
    delete state.pending[i.key];
    const mode = state.write;
    if (mode === 'fail' || (mode === 'screen' && opts.transition)) {
      Object.assign(i, before);
      toast(mode === 'fail'
        ? `${I.warn}<span>Couldn't save ${i.key}. Jira answered 500. Your change was undone.</span>`
        : `${I.warn}<span>Jira asks for <b>Resolution</b> to move ${i.key} to ${esc(change.status)}. <a class="lnk" data-act="browser" data-key="${i.key}">Finish in the browser</a></span>`, 4200);
    } else {
      i.updated = 'now';
      if (opts.done) toast(opts.done);
    }
    render();
  }, 650);
}
function setStatus(i, to) {
  const p = project(i.proj);
  if (i.status === to) return;
  if (blocked(p, i.status, to)) {
    toast(`${I.warn}<span>The ${p.key} workflow has no transition from ${esc(i.status)} to ${esc(to)}.</span>`, 3600);
    return;
  }
  write(i, { status: to }, { transition: true });
}

let menuPick = null;
function openMenu(anchor, title, items, onPick) {
  const m = $('#menu');
  m.innerHTML = `<div class="m-title-sm">${title}</div>` + (items.length
    ? items.map((it, n) => `<div class="mi ${it.current ? 'cur' : ''}" data-mi="${n}">${it.html}</div>`).join('')
    : '<div class="mi none">Nothing to choose</div>');
  m.classList.add('open');
  const r = anchor.getBoundingClientRect();
  const h = m.offsetHeight;
  m.style.left = `${Math.max(8, Math.min(r.left, innerWidth - m.offsetWidth - 8))}px`;
  m.style.top = `${r.bottom + 4 + h > innerHeight ? Math.max(8, r.top - h - 4) : r.bottom + 4}px`;
  menuPick = (n) => onPick(items[n].value);
}
function closeMenu() {
  $('#menu').classList.remove('open');
  menuPick = null;
}
function pick(kind, anchor) {
  const i = issue(state.openId);
  if (kind === 'epic-filter') {
    const items = [{ value: 'any', html: 'Any epic', current: state.epic === 'any' }, { value: 'none', html: '<span class="muted">No epic</span>', current: state.epic === 'none' }]
      .concat(epicsOf().map((e) => ({ value: e.key, html: `${typeIcon('Epic')}<span class="id">${e.key}</span><span class="ell">${esc(e.summary)}</span>`, current: state.epic === e.key })));
    return openMenu(anchor, 'Filter by epic', items, (v) => { state.epic = v; state.sel = 0; render(); });
  }
  if (kind === 'move-sprint') {
    const x = issue(anchor.dataset.key);
    const p = project(x.proj);
    if (state.picked.has(x.key) && state.picked.size > 1) return pick('move-picked', anchor);
    return openMenu(anchor, `Move ${x.key} to`, sprintMenuItems(x.sprint, !!x.sprint), (v) => moveMany([x.key], v));
  }
  if (kind === 'move-picked') {
    return openMenu(anchor, `Move ${state.picked.size} issue${state.picked.size === 1 ? '' : 's'} to`, sprintMenuItems(null, true), (v) => moveMany([...state.picked], v));
  }
  const setF = (k) => (v) => { state[k] = v; state.sel = 0; render(); };
  if (kind === 'assignee-filter') {
    const items = [{ value: 'any', html: 'Any assignee', current: state.assignee === 'any' }, { value: 'none', html: `${avatar(null)}<span class="muted">Unassigned</span>`, current: state.assignee === 'none' }]
      .concat(Object.entries(PEOPLE).map(([k, v]) => ({ value: k, html: `${avatar(k)}<span>${esc(v.name)}</span>`, current: state.assignee === k })));
    return openMenu(anchor, 'Filter by assignee', items, setF('assignee'));
  }
  if (kind === 'priority-filter') {
    return openMenu(anchor, 'Filter by priority', [{ value: 'any', html: 'Any priority', current: state.prio === 'any' }]
      .concat(PRIORITIES.map((x, n) => ({ value: n, html: `${priorityIcon(n)}<span>${x}</span>`, current: state.prio === n }))), setF('prio'));
  }
  if (kind === 'status-filter') {
    return openMenu(anchor, `Filter by ${state.proj} status`, [{ value: 'any', html: 'Any status', current: state.status === 'any' }]
      .concat(project().statuses.map((x) => ({ value: x, html: `${statusIcon(x)}<span>${esc(x)}</span>`, current: state.status === x }))), setF('status'));
  }
  if (!i) return;
  if (kind === 'status') {
    const p = project(i.proj);
    const items = p.statuses.filter((s) => s !== i.status).map((s) => ({ value: s, html: `${statusIcon(s)}<span>${esc(s)}</span>${blocked(p, i.status, s) ? '<span class="muted sm">no transition</span>' : ''}`, disabled: blocked(p, i.status, s) }))
      .filter((x) => !x.disabled);
    return openMenu(anchor, `Move ${i.key} to`, items, (v) => setStatus(i, v));
  }
  if (kind === 'assignee') {
    const items = [{ value: null, html: `${avatar(null)}<span class="muted">Unassigned</span>`, current: !i.assignee }]
      .concat(Object.entries(PEOPLE).map(([k, v]) => ({ value: k, html: `${avatar(k)}<span>${esc(v.name)}</span>`, current: i.assignee === k })));
    return openMenu(anchor, 'Assign to someone who can be assigned in this project', items, (v) => write(i, { assignee: v }));
  }
  if (kind === 'priority') {
    return openMenu(anchor, 'Priority', PRIORITIES.map((x, n) => ({ value: n, html: `${priorityIcon(n)}<span>${x}</span>`, current: i.priority === n })), (v) => write(i, { priority: v }));
  }
  if (kind === 'epic' && !isEpic(i)) {
    const items = [{ value: null, html: '<span class="muted">No epic</span>', current: !i.parent }]
      .concat(epicsOf(i.proj).filter((e) => cat(e.status) !== 'done').map((e) => ({ value: e.key, html: `${typeIcon('Epic')}<span class="id">${e.key}</span><span class="ell">${esc(e.summary)}</span>`, current: i.parent === e.key })));
    return openMenu(anchor, `Epics in ${i.proj}`, items, (v) => write(i, { parent: v }, { done: v ? `${i.key} is now in ${v}` : `${i.key} left its epic` }));
  }
  if (kind === 'add-child' && isEpic(i)) {
    const items = ISSUES.filter((x) => x.proj === i.proj && !isEpic(x) && x.parent !== i.key && cat(x.status) !== 'done')
      .map((x) => ({ value: x.key, html: `${typeIcon(x.type)}<span class="id">${x.key}</span><span class="ell">${esc(x.summary)}</span>${x.parent ? `<span class="muted sm">from ${x.parent}</span>` : ''}` }));
    return openMenu(anchor, `Add an open ${i.proj} issue to this epic`, items, (v) => write(issue(v), { parent: i.key }, { done: `${v} added to ${i.key}` }));
  }
}

function selectRow(delta) {
  const flat = ordered();
  if (!flat.length) return;
  state.sel = Math.max(0, Math.min(flat.length - 1, state.sel + delta));
  if (state.openId) state.openId = flat[state.sel].key;
  render();
  document.querySelector('.row.sel')?.scrollIntoView({ block: 'nearest' });
}
function columnsNow() {
  const items = boardIssues();
  return project().board.columns.map(([, sts]) => items.filter((i) => sts.includes(i.status)).sort((a, b) => a.priority - b.priority));
}
function moveCardSel(dx, dy) {
  const cols = columnsNow();
  let ci = cols.findIndex((c) => c.some((i) => i.key === state.card));
  if (ci < 0) { const first = cols.findIndex((c) => c.length); if (first < 0) return; state.card = cols[first][0].key; return render(); }
  let ri = cols[ci].findIndex((i) => i.key === state.card);
  if (dy) ri = Math.max(0, Math.min(cols[ci].length - 1, ri + dy));
  if (dx) {
    let n = ci + dx;
    while (n >= 0 && n < cols.length && !cols[n].length) n += dx;
    if (n < 0 || n >= cols.length) return;
    ci = n;
    ri = Math.min(ri, cols[ci].length - 1);
  }
  state.card = cols[ci][ri].key;
  render();
}
function moveToColumn(key, ci) {
  const i = issue(key);
  const sts = project(i.proj).board.columns[ci]?.[1];
  if (!sts || sts.includes(i.status)) return;
  setStatus(i, sts[0]);
}
function openIssue(key) {
  state.openId = key;
  state.editing = null;
  const idx = ordered().findIndex((i) => i.key === key);
  if (idx >= 0) state.sel = idx;
  if (state.view === 'board') state.card = key;
  render();
}
function nav(projKey, view) {
  Object.assign(state, { proj: projKey, view, card: null, openId: null, editing: null, boardTab: 'board' });
  clearFilters();
  state.picked.clear();
  state.expanded[projKey] = true;
  $('#app').classList.remove('mobile-nav');
  if (state.data !== 'loaded') return render();
  state.refreshing = true;
  render();
  setTimeout(() => { state.refreshing = false; render(); }, 600);
}
function refresh() {
  if (state.data === 'error') {
    state.data = 'loading';
    syncKnobs();
    render();
    setTimeout(() => { state.data = 'loaded'; syncKnobs(); render(); }, 900);
    return;
  }
  state.refreshing = true;
  render();
  setTimeout(() => { state.refreshing = false; render(); }, 700);
}
function newIssue(parent = null) {
  closeMenu();
  const filterEpic = state.view !== 'epics' && !['any', 'none'].includes(state.epic) ? state.epic : null;
  state.modal = { type: state.view === 'epics' && !parent ? 'Epic' : 'Story', parent: parent || filterEpic, fromEpic: !!parent };
  $('#modal').innerHTML = '';
  render();
}
function closeModal() {
  state.modal = null;
  render();
}
function submitCreate(e) {
  e?.preventDefault();
  const f = new FormData($('#create-form'));
  const summary = String(f.get('summary')).trim();
  const err = $('#m-error');
  if (!summary) {
    $('#c-summary').classList.add('bad');
    err.innerHTML = `${I.warn}<span>A summary is required.</span>`;
    err.classList.add('show');
    return;
  }
  const btn = $('#m-submit');
  btn.disabled = true;
  btn.innerHTML = `<span class="icon-btn spin" style="width:auto;height:auto;color:#fff">${I.refresh}</span>Creating…`;
  setTimeout(() => {
    if (state.write === 'fail') {
      btn.disabled = false;
      btn.innerHTML = 'Create <kbd>Ctrl Enter</kbd>';
      err.innerHTML = `${I.warn}<span>Jira answered 500. Nothing was created. Your text is still here.</span>`;
      err.classList.add('show');
      return;
    }
    const p = project();
    const n = Math.max(...ISSUES.filter((i) => i.proj === p.key).map((i) => +i.key.split('-')[1])) + 1;
    const type = f.get('type');
    const md = String(f.get('desc')).trim();
    const created = {
      key: `${p.key}-${n}`, proj: p.key, type, summary, status: p.initial, priority: +f.get('priority'),
      assignee: f.get('assignee') || null, parent: type === 'Epic' ? null : f.get('parent') || null,
      updated: 'now', desc: md ? fromMd(md) : null, sprint: null,
    };
    ISSUES.push(created);
    state.modal = null;
    render();
    toast(`Created <b>${created.key}</b><a class="lnk" data-open="${created.key}">Open</a>`, 4000);
  }, 700);
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
  Object.assign(state, { screen: 'signin', signin: 'idle', openId: null, modal: null });
  $('#f-token').value = '';
  syncKnobs();
  render();
  toast('Signed out. The API token was removed from the keychain.');
}

function syncKnobs() {
  const f = $('#knobs-form');
  f.querySelector(`input[name=screen][value=${state.screen}]`).checked = true;
  f.querySelector(`input[name=data][value=${state.data}]`).checked = true;
  f.querySelector(`input[name=signin][value=${state.outcome}]`).checked = true;
}

document.addEventListener('click', (e) => {
  if (!e.target.closest('#menu')) closeMenu();
  const mi = e.target.closest('[data-mi]');
  if (mi && menuPick) { const f = menuPick; closeMenu(); f(+mi.dataset.mi); return; }
  if (e.target.id === 'modal') return closeModal();
  const act = e.target.closest('[data-act]');
  if (act) {
    const a = act.dataset.act;
    const i = issue(state.openId);
    if (a === 'retry' || a === 'refresh') refresh();
    if (a === 'close-detail') { state.openId = null; state.editing = null; render(); }
    if (a === 'browser') toast(`Opens ${SITE}/browse/${act.dataset.key || state.openId} in your browser`);
    if (a === 'browser-backlog') toast(`Opens the ${state.proj} backlog on ${SITE} in your browser`);
    if (a === 'theme') setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
    if (a === 'signout') signOut();
    if (a === 'mobile-nav') $('#app').classList.toggle('mobile-nav');
    if (a === 'knobs') $('#knobs').classList.toggle('open');
    if (a === 'token-help') toast('Opens the API token page of your Atlassian account in your browser');
    if (a === 'new') newIssue();
    if (a === 'new-child' && i) newIssue(i.key);
    if (a === 'close-modal') closeModal();
    if (a === 'toggle-done') { state.showDone = !state.showDone; state.sel = 0; render(); }
    if (a === 'clear-filters') { clearFilters(); render(); }
    if (a === 'clear-picked') { state.picked.clear(); render(); }
    if (a === 'picked-to-board') { const p = project(); [...state.picked].forEach((k) => setStatus(issue(k), p.board.columns[0][1][0])); state.picked.clear(); render(); }
    if (a === 'edit-summary') { state.editing = 'summary'; render(); }
    if (a === 'edit-desc') { state.editing = 'desc'; state.descTab = 'write'; render(); }
    if (a === 'cancel-desc') { state.editing = null; render(); }
    if (a === 'save-desc' && i) { const md = $('#d-src').value; state.editing = null; write(i, { desc: md.trim() ? fromMd(md) : null }); }
    if (a === 'unlink') { e.stopPropagation(); write(issue(act.dataset.key), { parent: null }, { done: `${act.dataset.key} left ${state.openId}` }); }
    if (a === 'to-board') {
      const x = issue(act.dataset.key);
      const p = project(x.proj);
      if (p.board.type === 'scrum') moveMany([x.key], activeSprint(p).id);
      else setStatus(x, p.board.columns[0][1][0]);
    }
    return;
  }
  const pk = e.target.closest('[data-pick]');
  if (pk) return pick(pk.dataset.pick, pk);
  const dt = e.target.closest('[data-dtab]');
  if (dt) { state.descTab = dt.dataset.dtab; return render(); }
  const open = e.target.closest('[data-open]');
  if (open) { $('#toast').classList.remove('show'); return issue(open.dataset.open) ? openIssue(open.dataset.open) : toast(`${open.dataset.open} is not in this mockup`); }
  const tg = e.target.closest('[data-toggle]');
  if (tg) { state.expanded[tg.dataset.toggle] = !state.expanded[tg.dataset.toggle]; return render(); }
  const nv = e.target.closest('[data-nav]');
  if (nv) { const [p, v] = nv.dataset.nav.split(':'); return nav(p, v); }
  const g = e.target.closest('[data-group]');
  if (g) { state.collapsed[g.dataset.group] = !state.collapsed[g.dataset.group]; return render(); }
  const pr = e.target.closest('[data-pickrow]');
  if (pr) { togglePick(pr.dataset.pickrow, e.shiftKey); return render(); }
  const row = e.target.closest('[data-id]');
  if (row && inBacklog() && (e.ctrlKey || e.metaKey || e.shiftKey)) { togglePick(row.dataset.id, e.shiftKey); return render(); }
  if (row) return openIssue(row.dataset.id);
  const c = e.target.closest('[data-card]');
  if (c) return openIssue(c.dataset.card);
  const ty = e.target.closest('[data-type]');
  if (ty) { state.type = ty.dataset.type; state.sel = 0; return render(); }
  const bt = e.target.closest('[data-btab]');
  if (bt) { state.boardTab = bt.dataset.btab; state.sel = 0; state.picked.clear(); return render(); }
});

document.addEventListener('input', (e) => {
  if (e.target.id !== 'q') return;
  state.q = e.target.value;
  state.sel = 0;
  render();
});
document.addEventListener('change', (e) => {
  if (e.target.name === 'type' && e.target.closest('#create-form')) {
    const t = e.target.value;
    state.modal.type = t;
    document.querySelectorAll('.type-seg .seg-i').forEach((l) => l.classList.toggle('on', l.querySelector('input').value === t));
    $('.epic-field').hidden = t === 'Epic';
    $('#m-kind').textContent = t === 'Epic' ? 'New epic' : 'New issue';
  }
});

document.addEventListener('dragstart', (e) => {
  const r = e.target.closest?.('.row[draggable]');
  if (r) {
    const key = r.dataset.id;
    const keys = state.picked.has(key) ? [...state.picked] : [key];
    e.dataTransfer.setData('text/x-keys', JSON.stringify(keys));
    e.dataTransfer.effectAllowed = 'move';
    const ghost = document.createElement('div');
    ghost.className = 'drag-ghost';
    ghost.textContent = keys.length > 1 ? `${keys.length} issues` : key;
    document.body.appendChild(ghost);
    e.dataTransfer.setDragImage(ghost, 12, 12);
    setTimeout(() => ghost.remove());
    keys.forEach((k) => document.querySelector(`.row[data-id="${k}"]`)?.classList.add('dragging'));
    return;
  }
  const c = e.target.closest('[data-card]');
  if (!c) return;
  e.dataTransfer.setData('text/plain', c.dataset.card);
  c.classList.add('dragging');
});
document.addEventListener('dragend', () => document.querySelectorAll('.dragging, .over').forEach((x) => x.classList.remove('dragging', 'over')));
document.addEventListener('dragover', (e) => {
  const z = e.target.closest('[data-drop], [data-dropsprint]');
  if (!z) return;
  e.preventDefault();
  document.querySelectorAll('.over').forEach((x) => x !== z && x.classList.remove('over'));
  z.classList.add('over');
});
document.addEventListener('drop', (e) => {
  const sz = e.target.closest('[data-dropsprint]');
  if (sz) {
    e.preventDefault();
    const keys = JSON.parse(e.dataTransfer.getData('text/x-keys') || '[]');
    const v = sz.dataset.dropsprint;
    sz.classList.remove('over');
    return moveMany(keys, v === 'backlog' ? null : +v);
  }
  const z = e.target.closest('[data-drop]');
  if (!z) return;
  e.preventDefault();
  moveToColumn(e.dataTransfer.getData('text/plain'), +z.dataset.drop);
});

document.addEventListener('keydown', (e) => {
  if (state.screen !== 'app') return;
  if (e.key === 'Escape') {
    if ($('#menu').classList.contains('open')) return closeMenu();
    if (e.target.id === 'q') { e.target.blur(); return; }
    if (state.modal) return closeModal();
    if (state.editing) { state.editing = null; return render(); }
    if (state.openId) { state.openId = null; return render(); }
    if (state.picked.size) { state.picked.clear(); return render(); }
    $('#knobs').classList.remove('open');
    return;
  }
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
    if (state.modal) { e.preventDefault(); return submitCreate(); }
    if (state.editing === 'desc') { e.preventDefault(); return document.querySelector('[data-act=save-desc]').click(); }
  }
  if (e.target.id === 't-in' && e.key === 'Enter') {
    const v = e.target.value.trim();
    const i = issue(state.openId);
    state.editing = null;
    if (v && v !== i.summary) write(i, { summary: v }); else render();
    return;
  }
  if (e.target.matches('input, textarea, select') || e.ctrlKey || e.metaKey || e.altKey || state.modal) return;
  const k = e.key.toLowerCase();
  if (k === 'c') { e.preventDefault(); return newIssue(); }
  if (e.key === '/' && $('#q')) { e.preventDefault(); return $('#q').focus(); }
  if (inBacklog() && !state.openId && (k === 'x' || k === 'm')) {
    e.preventDefault();
    const cur = ordered()[state.sel];
    if (k === 'x' && cur) { togglePick(cur.key, e.shiftKey); return render(); }
    if (k === 'm') {
      if (project().board.type !== 'scrum') return;
      if (!state.picked.size && cur && pickable(cur)) state.picked.add(cur.key);
      render();
      const anchor = document.querySelector('[data-pick=move-picked]');
      if (anchor) pick('move-picked', anchor);
    }
    return;
  }
  if (state.openId && ['s', 'a', 'p', 'e'].includes(k)) {
    const kind = { s: 'status', a: 'assignee', p: 'priority', e: 'epic' }[k];
    const anchor = document.querySelector(`#d-props [data-pick=${kind}]`);
    if (anchor) { e.preventDefault(); pick(kind, anchor); }
    return;
  }
  if (state.view === 'board' && state.boardTab === 'board') {
    const dir = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1], h: [-1, 0], l: [1, 0], k: [0, -1], j: [0, 1] }[e.key.length === 1 ? k : e.key];
    if (dir) {
      e.preventDefault();
      if (e.shiftKey && dir[0] && state.card) {
        const ci = columnsNow().findIndex((c) => c.some((i) => i.key === state.card));
        return moveToColumn(state.card, ci + dir[0]);
      }
      return moveCardSel(dir[0], dir[1]);
    }
    if (e.key === 'Enter' && state.card) return openIssue(state.card);
    return;
  }
  if (k === 'j' || e.key === 'ArrowDown') { e.preventDefault(); selectRow(1); }
  else if (k === 'k' || e.key === 'ArrowUp') { e.preventDefault(); selectRow(-1); }
  else if (e.key === 'Enter') { const i = ordered()[state.sel]; if (i) openIssue(i.key); }
});

function setTheme(t) {
  document.documentElement.dataset.theme = t;
  const r = document.querySelector(`#knobs-form input[name=theme][value=${t}]`);
  if (r) r.checked = true;
}

$('#signin-form').addEventListener('submit', signIn);
document.addEventListener('submit', (e) => { if (e.target.id === 'create-form') submitCreate(e); });
$('#knobs-form').addEventListener('change', (e) => {
  const f = new FormData($('#knobs-form'));
  document.documentElement.dataset.theme = f.get('theme');
  if (e.target.name === 'screen') state.screen = f.get('screen');
  if (e.target.name === 'data') state.data = f.get('data');
  if (e.target.name === 'write') state.write = f.get('write');
  if (e.target.name === 'signin') {
    state.outcome = f.get('signin');
    if (state.outcome === 'expired') { state.screen = 'signin'; prefill(); }
    state.signin = state.outcome === 'expired' ? 'expired' : 'idle';
  }
  syncKnobs();
  render();
});

function prefill() {
  $('#f-site').value = SITE;
  $('#f-email').value = 'sam@acme-labs.example';
}
if (state.openId) state.sel = Math.max(0, ordered().findIndex((i) => i.key === state.openId));
if (state.view === 'board') state.card = state.openId || null;
syncKnobs();
render();
