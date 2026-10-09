/* ============================================================
   منصة إجتـاز التعليمية — سلوك الواجهة
   Egtaz Educational Platform — app logic
   ============================================================ */
(function () {
  "use strict";

  const $  = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => Array.from((c || document).querySelectorAll(s));
  const store = {
    get(k, d) { try { return JSON.parse(localStorage.getItem("egtaz_" + k)) ?? d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem("egtaz_" + k, JSON.stringify(v)); } catch {} },
    del(k) { try { localStorage.removeItem("egtaz_" + k); } catch {} }
  };

  /* ---------------- Toast ---------------- */
  const toastWrap = $("#toast-wrap");
  function toast(msg) {
    const t = document.createElement("div");
    t.className = "toast";
    t.textContent = msg;
    toastWrap.appendChild(t);
    setTimeout(() => t.remove(), 3200);
  }

  /* ---------------- Loader ---------------- */
  window.addEventListener("load", () => {
    setTimeout(() => {
      $("#loader").classList.add("done");
      if (!store.get("update_seen", false)) openModal("modal-update");
      else if (!store.get("welcome_seen", false)) {
        store.set("welcome_seen", true);
        toast("أهلًا بك في منصة إجتـاز 👋");
      }
    }, 900);
  });

  /* ---------------- Modals ---------------- */
  function openModal(id) {
    const m = document.getElementById(id);
    if (!m) return;
    m.classList.add("open");
    m.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }
  function closeModal(m) {
    m.classList.remove("open");
    m.setAttribute("aria-hidden", "true");
    if (!document.querySelector(".modal.open")) document.body.style.overflow = "";
  }
  document.addEventListener("click", (e) => {
    if (e.target.matches("[data-close]")) {
      const m = e.target.closest(".modal");
      if (m) closeModal(m);
    }
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") $$(".modal.open").forEach(closeModal);
  });

  const openers = {
    "btn-review-open": "modal-review",
    "btn-leader-name": "modal-leader-name",
    "btn-search-open": "modal-search",
    "btn-search-open-2": "modal-search",
    "btn-report-open": "modal-report"
  };
  Object.entries(openers).forEach(([btn, modal]) => {
    const el = document.getElementById(btn);
    if (el) el.addEventListener("click", (e) => { e.preventDefault(); openModal(modal); });
  });

  $("#modal-update").addEventListener("click", (e) => {
    if (e.target.closest("[data-close]")) store.set("update_seen", true);
  });

  /* ---------------- SVG cover generator (as in original) ---------------- */
  function coverSVG(badge, lines) {
    const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
    const tspans = lines.map((ln, i) =>
      `<tspan x="300" y="${137 + (i - (lines.length - 1) / 2) * 45}">${esc(ln)}</tspan>`).join("");
    return `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="300" viewBox="0 0 600 300" dir="rtl">
      <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#1e293b"/>
        </linearGradient>
        <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#10b981"/><stop offset="100%" stop-color="#059669"/>
        </linearGradient>
      </defs>
      <rect width="600" height="300" fill="url(#bg)"/>
      <circle cx="600" cy="0" r="150" fill="#ffffff" opacity="0.03"/>
      <circle cx="0" cy="300" r="200" fill="#ffffff" opacity="0.03"/>
      <rect x="20" y="20" width="560" height="260" fill="none" stroke="#334155" stroke-width="2" rx="10" stroke-dasharray="10 5" opacity="0.5"/>
      <rect x="200" y="35" width="200" height="40" fill="url(#accent)" rx="20"/>
      <text x="300" y="62" font-family="Cairo, sans-serif, Arial" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">${esc(badge)}</text>
      <text font-family="Cairo, sans-serif, Arial" font-size="36" font-weight="900" fill="#f8fafc" text-anchor="middle">${tspans}</text>
      <rect x="180" y="255" width="240" height="1" fill="#334155"/>
      <text x="300" y="275" font-family="Cairo, sans-serif, Arial" font-size="16" font-weight="bold" fill="#94a3b8" text-anchor="middle">منصة إجتـاز التعليمية - Egtaz</text>
    </svg>`;
  }

  /* ---------------- Carousel ---------------- */
  const track = $("#carousel-track");
  const carousel = $("#carousel");
  const dotsWrap = $("#carousel-dots");
  const counter = $("#carousel-counter");
  let slide = 0, autoTimer = null, dragging = false, startX = 0, startOffset = 0;

  EGTAZ.featured.forEach((item, i) => {
    const card = document.createElement("article");
    card.className = "test-card";
    card.innerHTML = `
      <div class="test-cover">
        ${coverSVG(item.coverBadge, item.coverTitle)}
        <span class="cover-type">${item.type}</span>
      </div>
      <div class="test-body">
        <div class="test-meta"><b>${item.category}</b><span>${item.meta}</span></div>
        <div class="test-title">${item.title}</div>
        <button class="btn btn-primary" data-quiz="${i}">${item.cta}</button>
      </div>`;
    track.appendChild(card);

    const dot = document.createElement("button");
    dot.setAttribute("aria-label", "شريحة " + (i + 1));
    dot.addEventListener("click", () => goTo(i, true));
    dotsWrap.appendChild(dot);
  });

  function slideWidth() {
    const card = track.children[0];
    if (!card) return 0;
    return card.getBoundingClientRect().width + 20;
  }
  function maxSlide() {
    const visible = Math.max(1, Math.round(carousel.clientWidth / slideWidth()));
    return Math.max(0, EGTAZ.featured.length - visible);
  }
  function goTo(i, user) {
    slide = Math.max(0, Math.min(i, maxSlide()));
    track.style.transform = `translateX(${slide * slideWidth()}px)`;
    counter.textContent = `${slide + 1} / ${EGTAZ.featured.length}`;
    $$("#carousel-dots button").forEach((d, k) => d.classList.toggle("active", k === slide));
    if (user) restartAuto();
  }
  function restartAuto() {
    clearInterval(autoTimer);
    autoTimer = setInterval(() => goTo(slide >= maxSlide() ? 0 : slide + 1), 4500);
  }
  $("#carousel-next").addEventListener("click", () => goTo(slide >= maxSlide() ? 0 : slide + 1, true));
  $("#carousel-prev").addEventListener("click", () => goTo(slide <= 0 ? maxSlide() : slide - 1, true));

  /* drag / swipe */
  function dragStart(x) {
    dragging = true; startX = x;
    startOffset = -slide * slideWidth();
    track.style.transition = "none";
    carousel.classList.add("dragging");
    clearInterval(autoTimer);
  }
  function dragMove(x) {
    if (!dragging) return;
    const dx = x - startX;
    track.style.transform = `translateX(${startOffset + dx}px)`;
  }
  function dragEnd(x) {
    if (!dragging) return;
    dragging = false;
    carousel.classList.remove("dragging");
    track.style.transition = "";
    const dx = x - startX;
    if (Math.abs(dx) > 50) goTo(slide + (dx > 0 ? -1 : 1), true);
    else goTo(slide, true);
    restartAuto();
  }
  carousel.addEventListener("mousedown", (e) => { e.preventDefault(); dragStart(e.clientX); });
  window.addEventListener("mousemove", (e) => dragMove(e.clientX));
  window.addEventListener("mouseup", (e) => dragEnd(e.clientX));
  carousel.addEventListener("touchstart", (e) => dragStart(e.touches[0].clientX), { passive: true });
  carousel.addEventListener("touchmove", (e) => dragMove(e.touches[0].clientX), { passive: true });
  carousel.addEventListener("touchend", (e) => dragEnd(e.changedTouches[0].clientX));
  window.addEventListener("resize", () => goTo(slide));
  goTo(0); restartAuto();

  /* ---------------- Render: sections ---------------- */
  const sectionsGrid = $("#sections-grid");
  EGTAZ.sections.forEach((s, idx) => {
    const el = document.createElement("div");
    el.className = "section-card reveal";
    el.innerHTML = `<div class="ico">${s.icon}</div><h4>${s.name}</h4><p>${s.desc}</p>`;
    el.addEventListener("click", () => {
      if (idx >= 9) openModal("modal-locked");       // الأقسام المميزة
      else toast(`سيتم فتح قسم: ${s.name}`);
    });
    sectionsGrid.appendChild(el);
  });

  /* ---------------- Render: axes + history ---------------- */
  function renderAxes() {
    const wrap = $("#axes-list");
    wrap.innerHTML = "";
    EGTAZ.axes.forEach((a) => {
      const row = document.createElement("div");
      row.className = "axis-row";
      row.innerHTML = `<span>${a.name}</span><div class="axis-bar"><i style="width:0%"></i></div><b>${a.value}%</b>`;
      wrap.appendChild(row);
      requestAnimationFrame(() => setTimeout(() => { row.querySelector("i").style.width = a.value + "%"; }, 60));
    });
  }
  function renderHistory() {
    const wrap = $("#history-list");
    wrap.innerHTML = "";
    EGTAZ.history.forEach((h) => {
      const pct = Math.round((h.score / h.total) * 100);
      const el = document.createElement("div");
      el.className = "history-item";
      el.innerHTML = `
        <div><b>${h.title}</b><div class="date">${h.kind} · ${h.date}</div></div>
        <div class="score">${h.score} / ${h.total} · ${pct}%</div>`;
      wrap.appendChild(el);
    });
  }
  renderAxes(); renderHistory();
  $("#btn-panel-refresh").addEventListener("click", () => { renderAxes(); renderHistory(); toast("تم تحديث لوحة التقدم 🔄"); });
  $("#btn-history-refresh").addEventListener("click", () => { renderHistory(); toast("تم تحديث سجل المحاولات"); });

  /* ---------------- Render: tiles ---------------- */
  const tilesGrid = $("#tiles-grid");
  EGTAZ.quickTiles.forEach((t) => {
    const el = document.createElement("div");
    el.className = "tile reveal";
    el.innerHTML = `<div class="ico">${t.icon}</div><div><h4>${t.title}</h4><p>${t.desc}</p></div>`;
    el.addEventListener("click", () => {
      if (t.target === "search") return openModal("modal-search");
      const target = document.getElementById(t.target);
      if (target) target.scrollIntoView({ behavior: "smooth" });
    });
    tilesGrid.appendChild(el);
  });

  /* ---------------- Render: lessons ---------------- */
  const lessonsGrid = $("#lessons-grid");
  EGTAZ.lessons.forEach((l) => {
    const el = document.createElement("article");
    el.className = "lesson-card reveal";
    el.innerHTML = `
      <span class="lesson-tag">${l.tag}</span>
      <h4>${l.title}</h4>
      <a class="btn btn-outline btn-sm" href="${l.url}" target="_blank" rel="noopener">اقرأ الشرح</a>`;
    lessonsGrid.appendChild(el);
  });

  /* ---------------- Render: leaderboard ---------------- */
  function renderLeaders() {
    const wrap = $("#leader-list");
    wrap.innerHTML = "";
    EGTAZ.leaderboard.forEach((p) => {
      const row = document.createElement("div");
      row.className = "leader-row reveal top-" + p.rank;
      row.innerHTML = `
        <div class="leader-medal">${p.medal}</div>
        <div class="leader-name"><b>${p.name}</b><span>${p.attempts} محاولة مكتملة</span></div>
        <div class="leader-attempts">${p.attempts} محاولة</div>
        <div class="leader-points">⭐ ${p.points.toLocaleString("ar-EG")} نقطة</div>`;
      wrap.appendChild(row);
    });
  }
  renderLeaders();

  /* ---------------- Render: reviews ---------------- */
  const reviewsGrid = $("#reviews-grid");
  let reviewsShown = 3;
  const extraReviews = [
    { initial: "س", name: "سارة محمود", role: "زائرة", stars: 5, text: "المحاكيات قريبة جدًا من أسئلة المسابقة الحقيقية، والشروحات مرتبة وسهلة." },
    { initial: "أ", name: "أحمد سمير", role: "مشترك", stars: 5, text: "خريطة المذاكرة ساعدتني أخلص المنهج في وقت قياسي. تجربة ممتازة." },
    { initial: "ن", name: "نجلاء حسن", role: "زائرة", stars: 4, text: "محتوى رائع، وأتمنى مزيدًا من الاختبارات في اللغة الإنجليزية." }
  ];
  const allReviews = () => EGTAZ.reviews.concat(extraReviews);
  function renderReviews() {
    reviewsGrid.innerHTML = "";
    allReviews().slice(0, reviewsShown).forEach((r) => {
      const el = document.createElement("article");
      el.className = "review-card reveal show";
      el.innerHTML = `
        <div class="review-head">
          <div class="avatar">${r.initial || "·"}</div>
          <div><b>${r.name}</b><span>${r.role}</span></div>
        </div>
        <div class="stars">${"★".repeat(r.stars)}${"☆".repeat(5 - r.stars)}</div>
        <p>${r.text}</p>`;
      reviewsGrid.appendChild(el);
    });
  }
  renderReviews();
  $("#btn-more-reviews").addEventListener("click", () => {
    const total = allReviews().length;
    if (reviewsShown >= total) { toast("لا مزيد من الآراء حاليًا"); return; }
    reviewsShown = Math.min(total, reviewsShown + 3);
    renderReviews();
    if (reviewsShown >= total) $("#btn-more-reviews").classList.add("hidden");
  });

  /* ---------------- Study map ---------------- */
  const mapSectionSel = $("#map-section");
  EGTAZ.sections.forEach((s) => {
    const o = document.createElement("option");
    o.value = s.id; o.textContent = s.name;
    mapSectionSel.appendChild(o);
  });

  function renderMap() {
    const plan = store.get("map", null);
    const pctEl = $("#map-percent");
    const ring = $("#progress-ring");
    if (!plan) {
      pctEl.textContent = "0%";
      ring.style.setProperty("--p", 0);
      $("#map-done").textContent = "0";
      $("#map-left").textContent = "0";
      $("#map-days-left").textContent = "0";
      $("#map-status").textContent = "لم تتم المزامنة بعد — أنشئ خطتك أولًا.";
      $("#map-days-track .days-chips")?.remove();
      return;
    }
    const done = plan.days.filter((d) => d.done).length;
    const pct = Math.round((done / plan.days.length) * 100);
    pctEl.textContent = pct + "%";
    ring.style.setProperty("--p", pct);
    $("#map-done").textContent = done;
    $("#map-left").textContent = plan.days.length - done;
    $("#map-days-left").textContent = plan.days.length;
    $("#map-status").textContent = plan.synced
      ? "تمت المزامنة مع حسابك ✓ — أكمل من حيث توقفت كل محتوى التخصص."
      : "لم تتم المزامنة بعد — أكمل من حيث توقفت كل محتوى التخصص.";

    const trackWrap = $("#map-days-track");
    trackWrap.querySelector(".days-chips")?.remove();
    const chips = document.createElement("div");
    chips.className = "days-chips";
    const current = plan.days.findIndex((d) => !d.done);
    plan.days.forEach((d, i) => {
      const c = document.createElement("span");
      c.className = "day-chip" + (d.done ? " done" : i === current ? " current" : "");
      c.textContent = (i === current ? "اليوم الحالي · " : "") + "يوم " + (i + 1);
      c.style.cursor = "pointer";
      c.addEventListener("click", () => {
        plan.days[i].done = !plan.days[i].done;
        store.set("map", plan);
        renderMap();
      });
      chips.appendChild(c);
    });
    trackWrap.appendChild(chips);
  }
  renderMap();

  $("#map-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const days = Math.max(3, Math.min(120, parseInt($("#map-days").value, 10) || 14));
    const sectionId = $("#map-section").value;
    const section = EGTAZ.sections.find((s) => s.id === sectionId);
    store.set("map", {
      sectionId, sectionName: section ? section.name : "",
      days: Array.from({ length: days }, () => ({ done: false })),
      synced: false
    });
    renderMap();
    toast("تم إنشاء خريطتك وحفظها 🗺️");
  });
  $("#map-sync").addEventListener("click", () => {
    const plan = store.get("map", null);
    if (!plan) return toast("لا توجد خطة للمزامنة");
    plan.synced = true;
    store.set("map", plan);
    renderMap();
    toast("تمت المزامنة الآن ✓");
  });
  $("#map-edit").addEventListener("click", () => {
    $("#map-days").focus();
    toast("عدّل المدة ثم اضغط «إنشاء خريطتي»");
  });
  $("#map-clear").addEventListener("click", () => {
    store.del("map");
    renderMap();
    toast("تم مسح الخطة");
  });

  /* ---------------- Search ---------------- */
  const searchInput = $("#search-input");
  const searchResults = $("#search-results");
  function renderSearch(q) {
    const list = q
      ? EGTAZ.searchIndex.filter((it) => (it.title + " " + it.type + " " + it.meta).includes(q))
      : EGTAZ.searchIndex;
    searchResults.innerHTML = "";
    if (!list.length) {
      searchResults.innerHTML = `<p class="muted center">لا توجد نتائج مطابقة لـ «${q}»</p>`;
      return;
    }
    list.forEach((it) => {
      const el = document.createElement("div");
      el.className = "search-item";
      el.innerHTML = `<div><b>${it.title}</b><br><small>${it.meta}</small></div><span class="type">${it.type}</span>`;
      el.addEventListener("click", () => toast("فتح: " + it.title));
      searchResults.appendChild(el);
    });
  }
  searchInput.addEventListener("input", () => renderSearch(searchInput.value.trim()));
  $("#fake-search-open").addEventListener("click", () => {
    openModal("modal-search");
    renderSearch("");
    searchInput.focus();
  });
  $("#modal-search").addEventListener("click", (e) => {
    if (e.target.closest("#modal-search .modal-card") && $("#modal-search").classList.contains("open")) {
      if (!searchResults.children.length) renderSearch("");
    }
  });

  /* ---------------- Login / user menu ---------------- */
  const userMenu = $("#user-menu");
  const loginBtn = $("#btn-login-open");
  function setLoggedIn(on, points) {
    store.set("logged_in", on);
    if (on) {
      loginBtn.textContent = "حسابي ▾";
      if (points != null) {
        store.set("points", points);
        $("#header-points").textContent = points;
        $("#menu-points").textContent = points;
      } else {
        const p = store.get("points", 0);
        $("#header-points").textContent = p;
        $("#menu-points").textContent = p;
      }
    } else {
      loginBtn.textContent = "تسجيل الدخول";
      userMenu.classList.remove("open");
    }
  }
  setLoggedIn(store.get("logged_in", false));

  function loginGate() {
    if (store.get("logged_in", false)) userMenu.classList.toggle("open");
    else openModal("modal-login");
  }
  ["btn-login-open", "btn-login-open-2", "btn-login-open-3", "btn-login-open-4", "btn-login-open-5"]
    .forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.addEventListener("click", (e) => { e.preventDefault(); loginGate(); });
    });
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".user-menu-wrap")) userMenu.classList.remove("open");
  });
  $("#menu-logout").addEventListener("click", () => {
    setLoggedIn(false);
    toast("تم تسجيل الخروج ✓");
  });
  $("#menu-speed").addEventListener("click", () => {
    userMenu.classList.remove("open");
    openModal("modal-speed");
  });
  $("#menu-session").addEventListener("click", () => {
    userMenu.classList.remove("open");
    openModal("modal-session");
  });

  $("#login-form").addEventListener("submit", (e) => {
    e.preventDefault();
    closeModal($("#modal-login"));
    setLoggedIn(true, 120);
    toast("تم تسجيل الدخول بنجاح ✓ (عرض تجريبي)");
    e.target.reset();
  });

  let reviewStars = 5;
  $$("#star-picker span").forEach((st) => {
    st.addEventListener("click", () => {
      reviewStars = parseInt(st.dataset.v, 10);
      $$("#star-picker span").forEach((s) => s.classList.toggle("on", parseInt(s.dataset.v, 10) <= reviewStars));
    });
    st.addEventListener("mouseenter", () => {
      const v = parseInt(st.dataset.v, 10);
      $$("#star-picker span").forEach((s) => s.classList.toggle("on", parseInt(s.dataset.v, 10) <= v));
    });
  });
  $("#star-picker").addEventListener("mouseleave", () => {
    $$("#star-picker span").forEach((s) => s.classList.toggle("on", parseInt(s.dataset.v, 10) <= reviewStars));
  });
  $$("#star-picker span").forEach((s) => s.classList.add("on"));

  $("#review-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const name = $("#review-name").value.trim() || "زائر";
    const text = $("#review-text").value.trim();
    EGTAZ.reviews.unshift({ initial: name.charAt(0), name, role: "زائر", stars: reviewStars, text });
    reviewsShown = Math.max(reviewsShown, 3);
    renderReviews();
    closeModal($("#modal-review"));
    e.target.reset();
    toast("شكرًا لك! تم إرسال تقييمك ⭐");
    document.getElementById("reviews").scrollIntoView({ behavior: "smooth" });
  });

  $("#leader-name-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const name = $("#leader-name-input").value.trim();
    if (!name) return;
    store.set("leader_name", name);
    closeModal($("#modal-leader-name"));
    toast(`تم حفظ اسمك: ${name} ✓`);
    e.target.reset();
  });

  $("#report-form").addEventListener("submit", (e) => {
    e.preventDefault();
    closeModal($("#modal-report"));
    e.target.reset();
    toast("تم إرسال بلاغك للإدارة ✓");
  });

  $("#btn-notice-dismiss").addEventListener("click", () => {
    $("#notice-card").style.display = "none";
  });

  /* ---------------- Quiz engine ---------------- */
  const quiz = {
    items: [], idx: 0, answers: [], title: "", kind: "", timer: null, seconds: 0, startedAt: 0
  };

  function startQuiz(title, kind, count) {
    const bank = EGTAZ.questionBank.slice().sort(() => Math.random() - 0.5);
    quiz.items = bank.slice(0, Math.min(count || 8, bank.length));
    quiz.idx = 0;
    quiz.answers = new Array(quiz.items.length).fill(null);
    quiz.title = title;
    quiz.kind = kind;
    quiz.seconds = 0;
    $("#quiz-title").textContent = title;
    $("#quiz-kind").textContent = kind;
    $("#quiz-result").classList.add("hidden");
    $("#quiz-body").classList.remove("hidden");
    $("#review-list").classList.add("hidden");
    clearInterval(quiz.timer);
    quiz.timer = setInterval(() => {
      quiz.seconds++;
      const m = String(Math.floor(quiz.seconds / 60)).padStart(2, "0");
      const s = String(quiz.seconds % 60).padStart(2, "0");
      $("#quiz-timer").textContent = `${m}:${s}`;
    }, 1000);
    $("#quiz-timer").textContent = "00:00";
    openModal("modal-quiz");
    renderQuestion();
  }

  function renderQuestion() {
    const q = quiz.items[quiz.idx];
    $("#quiz-index").textContent = `السؤال ${quiz.idx + 1} من ${quiz.items.length}`;
    $("#quiz-progress-bar").style.width = ((quiz.idx + 1) / quiz.items.length * 100) + "%";
    $("#quiz-question").textContent = q.q;
    const opts = $("#quiz-options");
    opts.innerHTML = "";
    q.options.forEach((opt, i) => {
      const b = document.createElement("button");
      b.className = "option" + (quiz.answers[quiz.idx] === i ? " selected" : "");
      b.textContent = opt;
      b.addEventListener("click", () => {
        quiz.answers[quiz.idx] = i;
        $$(".option", opts).forEach((o, k) => o.classList.toggle("selected", k === i));
      });
      opts.appendChild(b);
    });
    $("#quiz-prev").disabled = quiz.idx === 0;
    $("#quiz-next").textContent = quiz.idx === quiz.items.length - 1 ? "إنهاء الاختبار" : "التالي";
  }

  $("#quiz-prev").addEventListener("click", () => {
    if (quiz.idx > 0) { quiz.idx--; renderQuestion(); }
  });
  $("#quiz-next").addEventListener("click", () => {
    if (quiz.idx < quiz.items.length - 1) { quiz.idx++; renderQuestion(); }
    else finishQuiz();
  });
  $("#quiz-quit").addEventListener("click", () => {
    if (confirm("هل تريد الانسحاب من الاختبار؟")) {
      clearInterval(quiz.timer);
      closeModal($("#modal-quiz"));
    }
  });

  function finishQuiz() {
    clearInterval(quiz.timer);
    const correct = quiz.items.reduce((acc, q, i) => acc + (quiz.answers[i] === q.correct ? 1 : 0), 0);
    const pct = Math.round((correct / quiz.items.length) * 100);
    $("#quiz-body").classList.add("hidden");
    $("#quiz-result").classList.remove("hidden");
    $("#result-percent").textContent = pct + "%";
    $("#result-ring").style.setProperty("--p", pct);
    $("#result-score").textContent = `${correct} إجابة صحيحة من ${quiz.items.length} · الزمن ${$("#quiz-timer").textContent}`;

    const pts = store.get("points", 0) + correct;
    store.set("points", pts);
    $("#header-points").textContent = pts;

    EGTAZ.history.unshift({
      title: quiz.title, date: new Date().toISOString().slice(0, 10),
      score: correct, total: quiz.items.length, kind: quiz.kind
    });
    renderHistory();

    // إخفاء خطأ محتمل: الأسئلة التي أخطأ فيها المستخدم تذهب لنقاط الضعف
    const missed = quiz.items.filter((q, i) => quiz.answers[i] !== q.correct).length;
    const weak = store.get("weak", 12) + missed;
    store.set("weak", weak);
    $("#weak-count").textContent = weak;
  }

  $("#btn-result-review").addEventListener("click", () => {
    const list = $("#review-list");
    list.classList.toggle("hidden");
    if (!list.classList.contains("hidden")) {
      list.innerHTML = "<h4>مراجعة أسئلة الاختبار</h4>";
      quiz.items.forEach((q, i) => {
        const user = quiz.answers[i];
        const ok = user === q.correct;
        const el = document.createElement("div");
        el.className = "review-item";
        el.innerHTML = `
          <b>${i + 1}. ${q.q}</b>
          <div class="${ok ? "ok" : "no"}">إجابتك: ${user !== null ? q.options[user] : "لم تُجب"} ${ok ? "✓" : "✗"}</div>
          ${ok ? "" : `<div class="ok">الإجابة الصحيحة: ${q.options[q.correct]}</div>`}
          <div class="muted small">المحور: ${q.axis}</div>`;
        list.appendChild(el);
      });
      const pdfBtn = document.createElement("button");
      pdfBtn.className = "btn btn-outline btn-sm";
      pdfBtn.textContent = "📥 تحميل مراجعة الاختبار (PDF / صور)";
      pdfBtn.addEventListener("click", () => openModal("modal-pdf"));
      list.appendChild(pdfBtn);
    }
  });
  $("#btn-result-retry").addEventListener("click", () => startQuiz(quiz.title, quiz.kind, quiz.items.length));

  /* بدء الاختبار من بطاقات الكاروسيل */
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-quiz]");
    if (!btn) return;
    const item = EGTAZ.featured[parseInt(btn.dataset.quiz, 10)];
    if (!item) return;
    startQuiz(item.title, item.kind === "sim" ? "محاكي شامل" : "اختبار", item.kind === "sim" ? 10 : 8);
  });

  $("#btn-weakness").addEventListener("click", () => startQuiz("اختبار نقاط الضعف", "تدريب مخصص", 6));
  $("#btn-weakness-2").addEventListener("click", () => startQuiz("اختبار نقاط الضعف", "تدريب مخصص", 6));
  $("#btn-free-section").addEventListener("click", () => {
    document.getElementById("featured").scrollIntoView({ behavior: "smooth" });
    toast("هذا هو القسم المجاني — استمتع بالتدريب 🎉");
  });
  $("#btn-free-section-2").addEventListener("click", () => {
    document.getElementById("featured").scrollIntoView({ behavior: "smooth" });
    toast("هذا هو القسم المجاني — استمتع بالتدريب 🎉");
  });

  /* ---------------- PDF modal ---------------- */
  $("#modal-pdf").addEventListener("click", (e) => {
    if (e.target.closest(".modal-backdrop") || e.target.closest(".modal-close")) return;
    if ($("#modal-pdf").classList.contains("open")) {
      setTimeout(() => { $("#pdf-pages").textContent = "12 صفحة"; }, 800);
    }
  });
  $("#btn-pdf-download").addEventListener("click", () => {
    toast("جارٍ تجهيز الملف للتحميل… (عرض تجريبي)");
    closeModal($("#modal-pdf"));
  });

  /* ---------------- App download ---------------- */
  function appDownload() {
    toast("سيتم تحويلك لصفحة تحميل التطبيق قريبًا 📲");
  }
  $("#btn-app-download").addEventListener("click", appDownload);
  $("#btn-app-download-2").addEventListener("click", appDownload);

  /* ---------------- Speed test V3 ---------------- */
  let speedReadyAt = 0, speedArmed = false;
  $("#btn-speed-start").addEventListener("click", () => {
    const box = $("#speed-box");
    box.classList.remove("hot");
    box.textContent = "استعد...";
    $("#speed-result").textContent = "";
    speedArmed = true;
    setTimeout(() => {
      box.classList.add("hot");
      box.textContent = "اضغط الآن!";
      speedReadyAt = performance.now();
    }, 1200 + Math.random() * 2500);
  });
  $("#speed-box").addEventListener("click", () => {
    const box = $("#speed-box");
    if (!speedArmed) return;
    if (!box.classList.contains("hot")) {
      $("#speed-result").textContent = "مبكرًا جدًا! حاول مرة أخرى.";
      speedArmed = false;
      return;
    }
    const ms = Math.round(performance.now() - speedReadyAt);
    $("#speed-result").textContent = `زمن رد فعلك: ${ms} ms ${ms < 250 ? "— ممتاز! ⚡" : ms < 400 ? "— جيد جدًا" : "— يمكنك الأفضل"}`;
    box.classList.remove("hot");
    box.textContent = "اضغط «ابدأ»";
    speedArmed = false;
  });

  /* ---------------- About more ---------------- */
  $("#btn-about-more").addEventListener("click", () => {
    $$(".about-item").forEach((d) => (d.open = true));
    toast("تم عرض كل التفاصيل");
  });

  /* ---------------- YouTube timer (زياراتك) ---------------- */
  let ytSeconds = 0;
  setInterval(() => {
    ytSeconds++;
    const m = String(Math.floor(ytSeconds / 60)).padStart(2, "0");
    const s = String(ytSeconds % 60).padStart(2, "0");
    const el = $("#yt-timer");
    if (el) el.textContent = `${m}:${s}`;
  }, 1000);

  /* ---------------- Header / nav ---------------- */
  $("#nav-toggle").addEventListener("click", () => $("#nav").classList.toggle("open"));
  $$("#nav a").forEach((a) => a.addEventListener("click", () => $("#nav").classList.remove("open")));

  const sectionsForNav = ["home", "featured", "sections", "lessons", "leaders", "about"];
  window.addEventListener("scroll", () => {
    let current = "home";
    sectionsForNav.forEach((id) => {
      const el = document.getElementById(id);
      if (el && el.getBoundingClientRect().top <= 120) current = id;
    });
    $$("#nav a").forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + current));
    $$("#bottom-nav a").forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + current));
  }, { passive: true });

  /* ---------------- Reveal on scroll ---------------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        en.target.classList.add("show");
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.12 });
  $$(".reveal").forEach((el) => io.observe(el));

  /* ---------------- Misc ---------------- */
  $("#year").textContent = new Date().getFullYear();

  // نقاط المستخدم المحفوظة
  const savedPoints = store.get("points", 0);
  $("#header-points").textContent = savedPoints;
  $("#menu-points").textContent = savedPoints;
  $("#weak-count").textContent = store.get("weak", 12);
})();
