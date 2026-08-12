/* Imaginary Origin — newsletter sign-up.
 * MIT · (c) 2026 Pablo Nogueira Grossi / G6 LLC
 *
 * ONE endpoint constant, shared by every page with a sign-up form. Do not copy
 * this logic inline into a page: AXLE/index.html and the journal issues would
 * then drift, which is how the placeholder form below got shipped in the first
 * place.
 *
 * Set NL_ENDPOINT to the Apps Script /exec URL — see newsletter-appsscript.gs.
 * While it is empty, the form does NOT pretend to work. It hides itself and
 * offers a mailto link instead. The previous form on AXLE/index.html posted to
 * "formspree.io/f/YOUR_FORM_ID", so every address typed into it was lost with
 * no error shown to the reader. Never let this fail silently.
 *
 * Markup contract — a page needs:
 *   <form id="nl-form">
 *     <input type="email" id="nl-email" name="email" required>
 *     <input type="text"  id="nl-hp" name="company" tabindex="-1">   (honeypot)
 *     <button id="nl-btn" type="submit">
 *   </form>
 *   <div id="nl-msg"></div>
 * and: <script src="newsletter.js" data-source="Imaginary Origin No. 4"></script>
 */
(function () {
  var NL_ENDPOINT = "";   // <-- paste the Apps Script /exec URL here

  var FALLBACK = "mailto:g6llc@proton.me" +
    "?subject=Imaginary%20Origin%20newsletter" +
    "&body=Please%20add%20this%20address%20to%20the%20newsletter.";
  var LINK = ' style="color:#16161a;"';

  function init() {
    var form = document.getElementById("nl-form");
    if (!form) return;
    var msg = document.getElementById("nl-msg"),
        email = document.getElementById("nl-email"),
        hp = document.getElementById("nl-hp"),
        btn = document.getElementById("nl-btn"),
        tag = document.currentScript && document.currentScript.dataset.source;

    if (!NL_ENDPOINT) {
      form.style.display = "none";
      if (msg) {
        msg.innerHTML = 'Sign-up by email for now: <a href="' + FALLBACK + '"' + LINK +
                        ">g6llc@proton.me</a> &mdash; one line is enough.";
      }
      return;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (hp && hp.value) return;              // honeypot: bots only
      if (btn) btn.disabled = true;
      if (msg) msg.textContent = "Sending…";

      var body = new FormData();
      body.append("email", email.value);
      body.append("source", tag || document.title || "");

      fetch(NL_ENDPOINT, { method: "POST", mode: "no-cors", body: body })
        .then(function () {
          form.style.display = "none";
          if (msg) msg.textContent =
            "Thank you — added. You will hear from the journal a few times a year.";
        })
        .catch(function () {
          if (btn) btn.disabled = false;
          if (msg) msg.innerHTML =
            'That did not go through. Please email <a href="' + FALLBACK + '"' + LINK +
            ">g6llc@proton.me</a> instead.";
        });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
