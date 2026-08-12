/**
 * Imaginary Origin — newsletter sign-up endpoint
 * Receives POSTs from the sign-up form in vol4.html and appends a row to a Google Sheet.
 * The Sheet is then the source for Autocrat, which does the sending.
 *
 * Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC — MIT
 *
 * ── SET UP (once, about three minutes) ─────────────────────────────────────
 * 1. Create a Google Sheet. Name the first tab: Subscribers
 * 2. Extensions → Apps Script. Delete the stub, paste this file, Save.
 * 3. Run → onOpen once, and approve the permission prompt. This creates the
 *    header row and lets the script write to the Sheet.
 * 4. Deploy → New deployment → type "Web app".
 *       Execute as:      Me
 *       Who has access:  Anyone            ← required; the form posts anonymously
 *    Deploy, then copy the /exec URL.
 * 5. Paste that URL into NL_ENDPOINT in vol4.html's sign-up script.
 *
 * Redeploy (Deploy → Manage deployments → edit → Version: New) after any edit
 * here, or the live endpoint keeps running the old code.
 *
 * ── AUTOCRAT ───────────────────────────────────────────────────────────────
 * Autocrat merges one email per row. Point it at the Subscribers tab and:
 *   - set the merge condition to  Unsubscribed = FALSE
 *   - map <<Email>> to the recipient field
 *   - let it write its result into the "Merge status" column (last column),
 *     which is why that column is left empty here
 * Sending to a large list in one run can hit Gmail's daily quota
 * (~100/day consumer, ~1500/day Workspace). Batch if the list outgrows it.
 *
 * ── NOTE ON CONSENT ────────────────────────────────────────────────────────
 * This records a single opt-in: someone typed their address and pressed a
 * button. It is not double opt-in. If you later mail readers in the EU or UK,
 * a confirmation step is the defensible standard. The Confirmed column exists
 * so that can be added without reshaping the Sheet.
 */

var SHEET_NAME = 'Subscribers';
var HEADERS = ['Timestamp', 'Email', 'Source', 'Confirmed', 'Unsubscribed', 'Merge status'];

function onOpen() {
  var sh = _sheet();
  if (sh.getLastRow() === 0) {
    sh.appendRow(HEADERS);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    sh.setFrozenRows(1);
  }
}

function _sheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  return ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
}

function _isEmail(s) {
  return typeof s === 'string' && /^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(s.trim());
}

function doPost(e) {
  try {
    var p = (e && e.parameter) || {};

    // Honeypot: the form's hidden "company" field is only ever filled by bots.
    if (p.company) return _ok('ignored');

    var email = String(p.email || '').trim().toLowerCase();
    if (!_isEmail(email)) return _ok('invalid');

    var sh = _sheet();
    if (sh.getLastRow() === 0) onOpen();

    // Do not add the same address twice — Autocrat would mail it twice.
    var existing = sh.getLastRow() > 1
      ? sh.getRange(2, 2, sh.getLastRow() - 1, 1).getValues().map(function (r) {
          return String(r[0]).trim().toLowerCase();
        })
      : [];
    if (existing.indexOf(email) !== -1) return _ok('duplicate');

    sh.appendRow([
      new Date(),
      email,
      String(p.source || '').slice(0, 120),
      false,   // Confirmed     — set true if you add a confirmation step
      false,   // Unsubscribed  — Autocrat's merge condition reads this
      ''       // Merge status  — Autocrat writes here; leave empty
    ]);
    return _ok('added');
  } catch (err) {
    console.error(err);
    return _ok('error');
  }
}

/**
 * The form posts with mode:'no-cors', so it never reads this response — it
 * only needs the request to succeed. Returning text keeps the endpoint
 * debuggable from curl.
 */
function _ok(status) {
  return ContentService.createTextOutput(status).setMimeType(ContentService.MimeType.TEXT);
}

/** Visiting the /exec URL in a browser should not look like an error page. */
function doGet() {
  return ContentService
    .createTextOutput('Imaginary Origin newsletter endpoint. POST an email field to subscribe.')
    .setMimeType(ContentService.MimeType.TEXT);
}
