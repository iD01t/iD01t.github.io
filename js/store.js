/* iD01t Productions — id01t.store shared behaviors */
(function () {
  "use strict";

  var header = document.querySelector("header.site");
  var toggle = document.querySelector(".nav-toggle");
  var mobile = document.getElementById("mobileNav");

  if (header) {
    window.addEventListener("scroll", function () {
      header.classList.toggle("scrolled", window.scrollY > 10);
    }, { passive: true });
  }

  if (toggle && mobile) {
    toggle.addEventListener("click", function () {
      var open = mobile.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "✕" : "☰";
    });
    mobile.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        mobile.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.textContent = "☰";
      });
    });
  }

  /* highlight current page in nav */
  var here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("nav.primary a").forEach(function (a) {
    var target = (a.getAttribute("href") || "").split("/").pop();
    if (target === here) a.classList.add("active");
  });

  /* reveal on scroll */
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if ("IntersectionObserver" in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  /* copy-to-clipboard buttons (press kit) */
  document.querySelectorAll(".copy-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var el = document.getElementById(btn.getAttribute("data-copy"));
      if (!el) return;
      var done = function () {
        btn.textContent = "Copied ✓";
        setTimeout(function () { btn.textContent = "Copy"; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(el.textContent).then(done);
      } else {
        var r = document.createRange(); r.selectNodeContents(el);
        var s = getSelection(); s.removeAllRanges(); s.addRange(r);
        document.execCommand("copy"); s.removeAllRanges(); done();
      }
    });
  });

  /* dynamic year */
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
