(function () {
  "use strict";

  /* ---------------- utils ---------------- */
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  };
  var esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  };
  var inPosts = /\/posts\//.test(location.pathname);

  /* ---------------- header shadow ---------------- */
  var header = $(".site-header");
  if (header) {
    var onScrollHeader = function () {
      header.classList.toggle("scrolled", window.scrollY > 8);
    };
    window.addEventListener("scroll", onScrollHeader, { passive: true });
    onScrollHeader();
  }

  /* ---------------- reading progress ---------------- */
  var bar = $(".progress-bar");
  if (bar) {
    var updateBar = function () {
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      var pct = max > 0 ? (window.scrollY / max) * 100 : 0;
      bar.style.width = Math.min(100, Math.max(0, pct)) + "%";
    };
    window.addEventListener("scroll", updateBar, { passive: true });
    window.addEventListener("resize", updateBar);
    updateBar();
  }

  /* ---------------- favorites storage ---------------- */
  var FAV_KEY = "ggbond_favs";
  var storageOk = (function () {
    try {
      var t = "__ggbond_probe__";
      localStorage.setItem(t, "1");
      localStorage.removeItem(t);
      return true;
    } catch (e) { return false; }
  })();
  var memFavs = [];
  var getFavs = function () {
    if (storageOk) {
      try {
        var v = JSON.parse(localStorage.getItem(FAV_KEY));
        return Array.isArray(v) ? v : [];
      } catch (e) { return []; }
    }
    return memFavs.slice();
  };
  var setFavs = function (list) {
    memFavs = list.slice();
    if (storageOk) {
      try { localStorage.setItem(FAV_KEY, JSON.stringify(list)); }
      catch (e) { /* blocked or quota exceeded: fall back to in-memory */ }
    }
  };
  var toggleFav = function (slug) {
    var list = getFavs();
    var i = list.indexOf(slug);
    if (i === -1) list.push(slug); else list.splice(i, 1);
    setFavs(list);
    return i === -1;
  };

  /* ---------------- shared index (lazy) ---------------- */
  var indexPromise = null;
  var loadIndex = function () {
    if (!indexPromise) {
      var url = (inPosts ? "../" : "") + "assets/posts-index.json";
      indexPromise = fetch(url).then(function (r) { return r.json(); }).catch(function () { return []; });
    }
    return indexPromise;
  };
  var postUrl = function (slug) { return (inPosts ? "" : "posts/") + slug + ".html"; };

  /* ---------------- theme ---------------- */
  var THEME_KEY = "ggbond_theme";
  var applyTheme = function (t) {
    document.documentElement.setAttribute("data-theme", t);
  };
  var storedTheme = null;
  try { storedTheme = localStorage.getItem(THEME_KEY); } catch (e) {}
  applyTheme(storedTheme === "light" ? "light" : "dark");

  /* ---------------- floating toolbar ---------------- */
  var toolbar = document.createElement("div");
  toolbar.className = "float-bar";
  var tocBtn = null;
  if ($(".article-body")) {
    tocBtn = document.createElement("button");
    tocBtn.type = "button";
    tocBtn.className = "float-btn";
    tocBtn.title = "目录";
    tocBtn.textContent = "☰";
    toolbar.appendChild(tocBtn);
  }
  var themeBtn = document.createElement("button");
  themeBtn.type = "button";
  themeBtn.className = "float-btn";
  themeBtn.title = "切换深浅色";
  var paintThemeBtn = function () {
    themeBtn.textContent = document.documentElement.getAttribute("data-theme") === "light" ? "☾" : "☀";
  };
  paintThemeBtn();
  themeBtn.addEventListener("click", function () {
    var next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
    applyTheme(next);
    try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
    paintThemeBtn();
  });
  toolbar.appendChild(themeBtn);
  var topBtn = document.createElement("button");
  topBtn.type = "button";
  topBtn.className = "float-btn";
  topBtn.title = "回到顶部";
  topBtn.textContent = "↑";
  topBtn.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
  toolbar.appendChild(topBtn);
  document.body.appendChild(toolbar);

  /* ---------------- recent reads ---------------- */
  var RECENT_KEY = "ggbond_recent";
  var getRecent = function () {
    try {
      var v = JSON.parse(localStorage.getItem(RECENT_KEY));
      return Array.isArray(v) ? v : [];
    } catch (e) { return []; }
  };
  var pushRecent = function (slug, title) {
    try {
      var list = getRecent().filter(function (x) { return x.slug !== slug; });
      list.unshift({ slug: slug, title: title, t: Date.now() });
      localStorage.setItem(RECENT_KEY, JSON.stringify(list.slice(0, 5)));
    } catch (e) {}
  };

  /* ---------------- article page ---------------- */
  var body = $(".article-body");
  if (body) {
    /* record this read */
    var favBtnEl = document.getElementById("fav-btn");
    if (favBtnEl) {
      var h1El = $("h1");
      pushRecent(favBtnEl.getAttribute("data-slug") || "", h1El ? h1El.textContent.trim() : document.title);
    }

    /* tag chips -> links */
    $$(".article-foot .tag-row .tag").forEach(function (sp) {
      var raw = sp.textContent.trim().replace(/^#/, "");
      if (!raw) return;
      var a = document.createElement("a");
      a.className = "tag";
      a.href = "../tags.html#tag-" + encodeURIComponent(raw);
      a.textContent = "#" + raw;
      sp.parentNode.replaceChild(a, sp);
    });

    /* 1. heading anchors + ids */
    var h2s = $$("h2", body);
    h2s.forEach(function (h, i) {
      if (!h.id) h.id = "sec-" + (i + 1);
      var a = document.createElement("a");
      a.className = "h2-anchor";
      a.href = "#" + h.id;
      a.setAttribute("aria-label", "本节链接");
      a.textContent = "#";
      h.appendChild(a);
    });

    /* 2. table of contents */
    if (h2s.length > 1) {
      var toc = document.createElement("nav");
      toc.className = "toc";
      toc.id = "toc";
      var list = h2s.map(function (h) {
        return '<li><a href="#' + h.id + '">' + esc(h.textContent.replace(/#$/, "").trim()) + "</a></li>";
      }).join("");
      toc.innerHTML =
        '<details open><summary>本文目录 <span class="toc-count">' + h2s.length + " 节</span></summary>" +
        '<ol class="toc-list">' + list + "</ol></details>";
      var head = $(".article-head");
      if (head && head.parentNode) head.parentNode.insertBefore(toc, head.nextSibling);
      else body.parentNode.insertBefore(toc, body);

      if (tocBtn) {
        tocBtn.addEventListener("click", function () {
          var d = $("details", toc);
          if (toc.getBoundingClientRect().top < 0) toc.scrollIntoView({ behavior: "smooth", block: "start" });
          if (d) d.open = true;
        });
      }

      /* scroll spy */
      var tocLinks = $$(".toc-list a", toc);
      var spy = function () {
        var best = 0;
        h2s.forEach(function (h, i) {
          if (h.getBoundingClientRect().top <= 120) best = i;
        });
        tocLinks.forEach(function (a, i) { a.classList.toggle("on", i === best); });
      };
      window.addEventListener("scroll", spy, { passive: true });
      spy();
    }

    /* 3. favorite button */
    var favBtn = document.getElementById("fav-btn");
    if (favBtn) {
      var favSlug = favBtn.getAttribute("data-slug");
      var renderFav = function (on) {
        favBtn.classList.toggle("on", on);
        favBtn.textContent = on ? "★ 已收藏" : "☆ 收藏";
      };
      renderFav(getFavs().indexOf(favSlug) !== -1);
      favBtn.addEventListener("click", function () { renderFav(toggleFav(favSlug)); });
      window.addEventListener("storage", function (e) {
        if (e.key === FAV_KEY || e.key === null) renderFav(getFavs().indexOf(favSlug) !== -1);
      });
    }

    /* 4. checklist download (generated on the fly) */
    var foot = $(".article-foot");
    if (foot) {
      var h1 = $("h1");
      var pageTitle = h1 ? h1.textContent.trim() : document.title;
      var dl = document.createElement("button");
      dl.type = "button";
      dl.className = "checklist-btn";
      dl.textContent = "⤓ 下载本文检查清单";
      dl.addEventListener("click", function () {
        var md = ["# " + pageTitle + " · 检查清单", "", "> 来源：" + location.href, "", "## 覆盖章节", ""];
        h2s.forEach(function (h, i) { md.push((i + 1) + ". " + h.textContent.replace(/#$/, "").trim()); });
        md.push("", "## 上线前自查", "");
        ["关键路径已覆盖，且断言写在结果而非动作上",
          "失败时的证据可复现：截图 / 日志 / trace 至少留存一项",
          "测试数据可重复运行，不依赖上一次的残留状态",
          "异常路径已覆盖：超时、空数据、权限不足、重复提交",
          "已知限制与未覆盖项已写进报告，没有默默跳过"
        ].forEach(function (x) { md.push("- [ ] " + x); });
        md.push("", "## 备注", "", "- ", "");
        var blob = new Blob([md.join("\n")], { type: "text/markdown;charset=utf-8" });
        var a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = (favBtn ? favBtn.getAttribute("data-slug") : "checklist") + "-checklist.md";
        document.body.appendChild(a);
        a.click();
        setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
      });
      var back = $(".back-link", foot);
      if (back) foot.insertBefore(dl, back); else foot.appendChild(dl);
    }

    /* 5. prev / next / related */
    loadIndex().then(function (items) {
      if (!items.length) return;
      var slug = favBtn ? favBtn.getAttribute("data-slug") : "";
      var cur = null;
      items.forEach(function (it) { if (it.slug === slug) cur = it; });
      if (!cur) return;
      var bySlug = {};
      items.forEach(function (it) { bySlug[it.slug] = it; });
      /* 难度标识 + 最后更新 */
      var metaEl = $(".post-meta");
      if (metaEl && !metaEl.querySelector(".post-level")) {
        var lvEl = document.createElement("span");
        lvEl.className = "post-level " + (cur.level === "入门" ? "lv-basic" : cur.level === "深入" ? "lv-deep" : "lv-mid");
        lvEl.textContent = cur.level || "进阶";
        metaEl.appendChild(lvEl);
      }
      if (cur.updated) {
        var footEl = $(".article-foot");
        var backEl = footEl ? footEl.querySelector(".back-link") : null;
        if (footEl && !footEl.querySelector(".updated")) {
          var upEl = document.createElement("span");
          upEl.className = "updated";
          upEl.textContent = "最后更新 " + cur.updated;
          if (backEl) footEl.insertBefore(upEl, backEl); else footEl.appendChild(upEl);
        }
      }

      var wrapEl = document.createElement("section");
      wrapEl.className = "article-more";
      var navHtml = '<div class="pn-row">' +
        (cur.prev && bySlug[cur.prev] ? '<a class="pn prev" href="' + postUrl(cur.prev) + '"><span>← 上一篇</span><strong>' + esc(bySlug[cur.prev].title) + "</strong></a>" : "<span></span>") +
        (cur.next && bySlug[cur.next] ? '<a class="pn next" href="' + postUrl(cur.next) + '"><span>下一篇 →</span><strong>' + esc(bySlug[cur.next].title) + "</strong></a>" : "<span></span>") +
        "</div>";
      var relHtml = "";
      if (cur.related && cur.related.length) {
        relHtml = '<h3 class="more-title">相关阅读</h3><div class="rel-grid">' +
          cur.related.filter(function (s) { return bySlug[s]; }).map(function (s) {
            var it = bySlug[s];
            return '<a class="rel-card" href="' + postUrl(it.slug) + '"><span class="rel-cat">' + esc(it.cat) +
              "</span><strong>" + esc(it.title) + "</strong></a>";
          }).join("") + "</div>";
      }
      wrapEl.innerHTML = navHtml + relHtml;
      var article = $(".article") || body.parentNode;
      article.appendChild(wrapEl);
    });
  }

  /* ---------------- home page: search ---------------- */
  var searchInput = document.getElementById("post-search");
  var cards = $$(".post-card");
  var countEl = document.getElementById("search-count");
  var favFilter = document.getElementById("fav-filter");
  if (cards.length && searchInput) {
    var baseHtml = cards.map(function (card) {
      var t = card.querySelector("h3");
      var p = card.querySelector("p");
      return { title: t ? t.innerHTML : "", desc: p ? p.innerHTML : "" };
    });
    var baseHay = cards.map(function (card) {
      return (card.textContent || "").replace(/\s+/g, " ").toLowerCase();
    });
    var hay = baseHay.slice();
    var pyArr = cards.map(function () { return ""; });
    var indexLoaded = false;
    var slugPos = {};
    cards.forEach(function (c, i) { slugPos[c.getAttribute("data-slug")] = i; });

    var hydrate = function () {
      if (indexLoaded) return;
      indexLoaded = true;
      loadIndex().then(function (items) {
        items.forEach(function (it) {
          var i = slugPos[it.slug];
          if (i == null) return;
          hay[i] = (it.title + " " + it.cat + " " + it.fw + " " + (it.tags || []).join(" ") + " " +
            (it.headings || []).join(" ") + " " + it.desc + " " + it.text + " " +
            (it.py || "") + " " + it.slug.replace(/-/g, " ")).toLowerCase();
          pyArr[i] = it.py || "";
        });
        runFilter();
      });
    };

    var fuzzyMatch = function (text, terms) {
      return terms.every(function (term) { return text.indexOf(term) !== -1; });
    };
    var markBodyHit = function (card, idx, terms) {
      var foot = card.querySelector(".post-foot");
      if (!foot) return;
      var old = foot.querySelector(".body-hit");
      if (old) old.remove();
      if (!terms.length) return;
      var own = (baseHtml[idx].title + " " + baseHtml[idx].desc).toLowerCase();
      var inOwn = terms.some(function (t) { return own.indexOf(t) !== -1; });
      if (!inOwn) {
        var tag = document.createElement("span");
        tag.className = "body-hit";
        tag.textContent = "正文命中";
        foot.appendChild(tag);
      }
    };
    var favOnly = false;
    var highlight = function (card, idx, terms) {
      var t = card.querySelector("h3");
      var p = card.querySelector("p");
      var paint = function (el, original) {
        if (!el) return;
        if (!terms.length) { el.innerHTML = original; return; }
        var out = original;
        terms.forEach(function (term) {
          var re = new RegExp("(" + term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi");
          out = out.replace(re, '<mark class="hit">$1</mark>');
        });
        el.innerHTML = out;
      };
      paint(t, baseHtml[idx].title);
      paint(p, baseHtml[idx].desc);
    };
    var runFilter = function () {
      var q = searchInput.value.trim();
      var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
      var favs = getFavs();
      var shown = 0;
      cards.forEach(function (card, i) {
        var slug = card.getAttribute("data-slug") || "";
        var bySearch = !terms.length || fuzzyMatch(hay[i], terms);
        var byFav = !favOnly || favs.indexOf(slug) !== -1;
        var show = bySearch && byFav;
        card.classList.toggle("hidden", !show);
        if (!card.classList.contains("hidden")) {
          highlight(card, i, terms);
          markBodyHit(card, i, terms);
        }
        if (show) shown++;
      });
      if (countEl) {
        countEl.textContent = (terms.length || favOnly) ? "匹配 " + shown + " 篇" : "共 " + cards.length + " 篇";
      }
      var empty = document.getElementById("search-empty");
      if (empty) {
        empty.classList.toggle("show", shown === 0);
        empty.style.display = shown === 0 ? "block" : "none";
      }
    };
    /* a11y: 结果数量播报 + 收藏筛选状态 */
    if (countEl) { countEl.setAttribute("role", "status"); countEl.setAttribute("aria-live", "polite"); }
    if (favFilter) favFilter.setAttribute("aria-pressed", "false");

    /* search suggestions */
    var suggEl = document.createElement("div");
    suggEl.className = "search-suggest";
    suggEl.id = "search-suggest";
    suggEl.setAttribute("role", "listbox");
    searchInput.setAttribute("role", "combobox");
    searchInput.setAttribute("aria-autocomplete", "list");
    searchInput.setAttribute("aria-controls", "search-suggest");
    searchInput.setAttribute("aria-expanded", "false");
    searchInput.parentNode.appendChild(suggEl);
    var suggActive = -1;
    var suggHits = [];
    var hideSugg = function () {
      suggEl.classList.remove("show");
      suggEl.innerHTML = "";
      suggHits = [];
      suggActive = -1;
      searchInput.setAttribute("aria-expanded", "false");
      searchInput.removeAttribute("aria-activedescendant");
    };
    var setActive = function (k) {
      var items = $$(".search-suggest-item", suggEl);
      items.forEach(function (a, i) { a.classList.toggle("active", i === k); });
      suggActive = k;
      if (k >= 0 && items[k]) searchInput.setAttribute("aria-activedescendant", items[k].id);
    };
    var renderSugg = function (terms) {
      if (!terms.length) { hideSugg(); return; }
      var q = terms.join(" ");
      var hits = [];
      cards.forEach(function (card, i) {
        if (hits.length >= 6) return;
        var title = (baseHtml[i].title || "").toLowerCase();
        var pyv = pyArr[i] || "";
        if (title.indexOf(q) !== -1 || (pyv && pyv.indexOf(q) !== -1)) hits.push(i);
      });
      if (!hits.length) { hideSugg(); return; }
      suggHits = hits;
      suggEl.innerHTML = hits.map(function (i, k) {
        var card = cards[i];
        var catEl = card.querySelector(".post-cat");
        return '<a class="search-suggest-item" role="option" id="sugg-' + k + '" href="' +
          card.getAttribute("href") + '"><span class="sugg-title">' + baseHtml[i].title +
          '</span><span class="sugg-cat">' + esc(catEl ? catEl.textContent : "") + "</span></a>";
      }).join("");
      suggEl.classList.add("show");
      searchInput.setAttribute("aria-expanded", "true");
      setActive(-1);
      suggActive = -1;
      suggEl.querySelectorAll(".search-suggest-item").forEach(function (a, i) {
        a.addEventListener("mouseenter", function () { setActive(i); });
      });
    };
    searchInput.addEventListener("keydown", function (e) {
      if (!suggHits.length) return;
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setActive((suggActive + 1) % suggHits.length);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setActive(suggActive <= 0 ? suggHits.length - 1 : suggActive - 1);
      } else if (e.key === "Enter" && suggActive >= 0) {
        e.preventDefault();
        location.href = cards[suggHits[suggActive]].getAttribute("href");
      } else if (e.key === "Escape") {
        hideSugg();
      }
    });
    searchInput.addEventListener("blur", function () { setTimeout(hideSugg, 120); });

    searchInput.addEventListener("focus", hydrate);
    searchInput.addEventListener("input", function () {
      hydrate();
      runFilter();
      renderSugg(searchInput.value.trim().toLowerCase().split(/\s+/).filter(Boolean));
    });
    if (favFilter) {
      favFilter.addEventListener("click", function () {
        favOnly = !favOnly;
        favFilter.classList.toggle("on", favOnly);
        favFilter.setAttribute("aria-pressed", favOnly ? "true" : "false");
        favFilter.textContent = favOnly ? "★ 显示全部" : "☆ 只看收藏";
        runFilter();
      });
    }
    window.addEventListener("storage", function (e) {
      if (e.key === FAV_KEY || e.key === null) runFilter();
    });
    runFilter();

    /* keyboard shortcut */
    document.addEventListener("keydown", function (e) {
      if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      } else if (e.key === "Escape" && document.activeElement === searchInput) {
        searchInput.value = "";
        runFilter();
        searchInput.blur();
      }
    });

    /* last query hint */
    var LASTQ_KEY = "ggbond_lastq";
    var RECENTQ_KEY = "ggbond_recentq";
    var getRecentQ = function () {
      try {
        var v = JSON.parse(localStorage.getItem(RECENTQ_KEY));
        return Array.isArray(v) ? v.filter(function (x) { return typeof x === "string"; }) : [];
      } catch (e) { return []; }
    };
    var pushRecentQ = function (q) {
      if (!q) return;
      try {
        var list = getRecentQ().filter(function (x) { return x !== q; });
        list.unshift(q);
        localStorage.setItem(RECENTQ_KEY, JSON.stringify(list.slice(0, 6)));
      } catch (e) {}
    };

    try {
      var lastQ = localStorage.getItem(LASTQ_KEY);
      if (lastQ) searchInput.setAttribute("placeholder", "上次搜索：" + lastQ);
    } catch (e) {}

    /* recent query chips */
    var chipsEl = document.createElement("div");
    chipsEl.className = "recent-q";
    chipsEl.id = "recent-q";
    chipsEl.setAttribute("aria-label", "最近搜索");
    searchInput.parentNode.parentNode.insertBefore(chipsEl, searchInput.parentNode.nextSibling);
    var renderChips = function () {
      var list = getRecentQ();
      if (!list.length) { chipsEl.innerHTML = ""; chipsEl.classList.remove("show"); return; }
      chipsEl.classList.add("show");
      chipsEl.innerHTML = '<span class="recent-q-label">最近搜索</span>' +
        list.map(function (q) {
          return '<button type="button" class="recent-q-chip" data-q="' + esc(q) + '">' + esc(q) + "</button>";
        }).join("");
    };
    chipsEl.addEventListener("click", function (e) {
      var btn = e.target.closest(".recent-q-chip");
      if (!btn) return;
      searchInput.value = btn.getAttribute("data-q") || "";
      hydrate();
      runFilter();
      searchInput.focus();
    });
    renderChips();

    searchInput.addEventListener("blur", function () {
      try {
        var v = searchInput.value.trim();
        if (v) { localStorage.setItem(LASTQ_KEY, v); pushRecentQ(v); renderChips(); }
      } catch (e) {}
    });

    /* recent reads bar */
    var recents = getRecent();
    if (recents.length && !document.getElementById("recent-bar")) {
      var barEl = document.createElement("div");
      barEl.className = "recent-bar";
      barEl.id = "recent-bar";
      var links = recents.slice(0, 3).map(function (r) {
        return '<a href="posts/' + r.slug + '.html">' + esc(r.title) + "</a>";
      });
      barEl.innerHTML = '<span class="rb-label">继续阅读</span>' + links.join('<span class="rb-sep">·</span>') +
        '<span class="rb-more">按 Ctrl/⌘ + K 搜索</span>';
      var anchor = searchInput.closest(".search-bar") || searchInput;
      anchor.parentNode.insertBefore(barEl, anchor);
    }
  }

  /* ---------------- favorites page ---------------- */
  var favWrap = document.getElementById("fav-list");
  if (favWrap) {
    var renderFavList = function () {
      var favs = getFavs();
      var emptyEl = document.getElementById("fav-empty");
      loadIndex().then(function (items) {
        var bySlug = {};
        items.forEach(function (it) { bySlug[it.slug] = it; });
        var list = favs.map(function (s) { return bySlug[s]; }).filter(Boolean);
        if (emptyEl) emptyEl.style.display = list.length ? "none" : "block";
        favWrap.innerHTML = list.map(function (it) {
          return '<a class="post-card" href="' + postUrl(it.slug) + '">' +
            '<div class="post-meta"><span class="post-cat">' + esc(it.cat) + '</span><span class="post-fw">' +
            esc(it.fw) + "</span></div><h3>" + esc(it.title) + "</h3><p>" + esc(it.desc) +
            '</p><div class="post-foot"><span>' + esc((it.tags || []).join(" ")) +
            '</span><span class="read">阅读全文 →</span></div></a>';
        }).join("");
        var n = document.getElementById("fav-count");
        if (n) n.textContent = list.length;
      });
    };
    renderFavList();

    var expBtn = document.getElementById("fav-export");
    if (expBtn) expBtn.addEventListener("click", function () {
      var blob = new Blob([JSON.stringify(getFavs(), null, 2)], { type: "application/json" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "favorites.json";
      document.body.appendChild(a);
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
    });

    var impInput = document.getElementById("fav-import");
    if (impInput) impInput.addEventListener("change", function () {
      var f = impInput.files && impInput.files[0];
      if (!f) return;
      var reader = new FileReader();
      reader.onload = function () {
        try {
          var arr = JSON.parse(reader.result);
          if (Array.isArray(arr)) {
            var merged = getFavs();
            arr.forEach(function (s) { if (typeof s === "string" && merged.indexOf(s) === -1) merged.push(s); });
            setFavs(merged);
            renderFavList();
          }
        } catch (e) {}
        impInput.value = "";
      };
      reader.readAsText(f);
    });

    var clearBtn = document.getElementById("fav-clear");
    if (clearBtn) clearBtn.addEventListener("click", function () {
      if (confirm("确定清空全部收藏？此操作不可撤销。")) { setFavs([]); renderFavList(); }
    });
    window.addEventListener("storage", function (e) {
      if (e.key === FAV_KEY || e.key === null) renderFavList();
    });
  }

  /* ---------------- tags page ---------------- */
  var tagCloud = document.getElementById("tag-cloud");
  if (tagCloud) {
    loadIndex().then(function (items) {
      var map = {};
      items.forEach(function (it) {
        (it.tags || []).forEach(function (t) { (map[t] = map[t] || []).push(it); });
      });
      var names = Object.keys(map).sort(function (a, b) { return map[b].length - map[a].length || a.localeCompare(b); });
      tagCloud.innerHTML = names.map(function (t) {
        return '<a class="tag-chip" href="#tag-' + encodeURIComponent(t) + '"><span>' + esc(t) +
          '</span><em>' + map[t].length + "</em></a>";
      }).join("");
      var groups = document.getElementById("tag-groups");
      if (groups) {
        groups.innerHTML = names.map(function (t) {
          return '<section class="tag-group" id="tag-' + encodeURIComponent(t) + '"><h2>' + esc(t) +
            ' <span class="tag-num">' + map[t].length + " 篇</span></h2><ul>" +
            map[t].map(function (it) {
              return '<li><a href="' + postUrl(it.slug) + '">' + esc(it.title) + '</a><span>' + esc(it.cat) + "</span></li>";
            }).join("") + "</ul></section>";
        }).join("");
      }
    });
  }

  /* ---------------- paths page: reading progress ---------------- */
  var pathCards = $$(".path-card");
  if (pathCards.length) {
    var readSet = {};
    getRecent().forEach(function (r) { readSet[r.slug] = 1; });
    pathCards.forEach(function (card) {
      var steps = $$(".path-steps li", card);
      if (!steps.length) return;
      var done = 0;
      steps.forEach(function (li) {
        var a = li.querySelector("a");
        if (!a) return;
        var slug = (a.getAttribute("href") || "").replace(/^.*\//, "").replace(/\.html$/, "");
        if (readSet[slug]) { li.classList.add("done"); done++; }
      });
      var bar = document.createElement("div");
      bar.className = "path-progress";
      bar.innerHTML = '<span class="path-progress-num">已读 ' + done + " / " + steps.length +
        '</span><span class="path-progress-track"><span class="path-progress-fill"></span></span>';
      var head = card.querySelector("h2");
      if (head && head.nextSibling) card.insertBefore(bar, head.nextSibling);
      else card.appendChild(bar);
      var fill = bar.querySelector(".path-progress-fill");
      if (fill) fill.style.width = Math.round((done / steps.length) * 100) + "%";
    });
  }

  /* ---------------- paths page: series collections ---------------- */
  var seriesList = document.getElementById("series-list");
  if (seriesList) {
    loadIndex().then(function (items) {
      if (!items.length) return;
      var readSet2 = {};
      getRecent().forEach(function (r) { readSet2[r.slug] = 1; });
      var groups = {};
      items.forEach(function (it) { (groups[it.cat] = groups[it.cat] || []).push(it); });
      var cats = Object.keys(groups)
        .filter(function (c) { return groups[c].length >= 4; })
        .sort(function (a, b) { return groups[b].length - groups[a].length || a.localeCompare(b); });
      seriesList.innerHTML = cats.map(function (c) {
        var list = groups[c];
        var done = list.filter(function (it) { return readSet2[it.slug]; }).length;
        var pct = Math.round((done / list.length) * 100);
        return '<section class="series-item"><h3>' + esc(c) +
          ' <span class="series-count">' + list.length + " 篇 · 已读 " + done +
          '</span></h3><div class="path-progress"><span class="path-progress-track">' +
          '<span class="path-progress-fill" style="width:' + pct + '%"></span></span></div><ol class="series-steps">' +
          list.map(function (it, i) {
            return '<li' + (readSet2[it.slug] ? ' class="done"' : "") + '><span class="series-num">' + (i + 1) +
              '</span><a href="' + postUrl(it.slug) + '">' + esc(it.title) + '</a>' +
              '<small>' + it.mins + " 分钟 · " + it.level + "</small></li>";
          }).join("") + "</ol></section>";
      }).join("");
    });
  }

  /* ---------------- service worker (offline reading) ---------------- */
  if ("serviceWorker" in navigator && location.protocol === "https:") {
    var swSrc = document.currentScript ? document.currentScript.src : "";
    var swRoot = swSrc ? new URL("../", swSrc).pathname : location.pathname.replace(/[^/]*$/, "");
    window.addEventListener("load", function () {
      navigator.serviceWorker.register(swRoot + "sw.js", { scope: swRoot }).catch(function () {});
    });
  }

  /* ---------------- copy buttons ---------------- */
  $$(".copy-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var head = btn.closest(".code-head");
      var pre = head ? head.nextElementSibling : null;
      var code = pre ? pre.querySelector("code") : null;
      if (!code) return;
      var text = code.innerText;
      var done = function () {
        btn.textContent = "已复制 ✓";
        btn.classList.add("ok");
        setTimeout(function () {
          btn.textContent = "复制";
          btn.classList.remove("ok");
        }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, done);
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta);
        done();
      }
    });
  });

  /* ---------------- terminal typing effect ---------------- */
  var typed = $("[data-typed]");
  if (typed) {
    var lines = (typed.getAttribute("data-typed") || "").split("|");
    var k = 0;
    var renderTyped = function () {
      typed.textContent = lines[k];
      k = (k + 1) % lines.length;
    };
    renderTyped();
    setInterval(renderTyped, 2600);
  }
})();
