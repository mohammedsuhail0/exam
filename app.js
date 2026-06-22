(() => {
  const CONFIG = {
    minKeystrokeIntervalMs: 15,
    fpsDropThreshold: 18,
    rAFWindowSize: 60,
    maxEventsBuffer: 300,
    zeroTolerance: true,
    auditEndpoint: "/api/audit"
  };

  const state = {
    sessionId: "",
    sessionToken: "",
    started: false,
    terminated: false,
    lastKeyTs: 0,
    frameSamples: [],
    eventBuffer: [],
    questions: []
  };

  const el = {
    consent: document.getElementById("consent"),
    startBtn: document.getElementById("start-btn"),
    startScreen: document.getElementById("start-screen"),
    examScreen: document.getElementById("exam-screen"),
    terminatedScreen: document.getElementById("terminated-screen"),
    resultScreen: document.getElementById("result-screen"),
    terminateReason: document.getElementById("terminate-reason"),
    terminateCode: document.getElementById("terminate-code"),
    restartBtn: document.getElementById("restart-btn"),
    resultRestartBtn: document.getElementById("result-restart-btn"),
    resultSummary: document.getElementById("result-summary"),
    resultBreakdown: document.getElementById("result-breakdown"),
    sessionId: document.getElementById("session-id"),
    mcqContainer: document.getElementById("mcq-container"),
    fibContainer: document.getElementById("fib-container"),
    submitBtn: document.getElementById("submit-btn"),
    statusPill: document.getElementById("status-pill")
  };

  function nowIso() {
    return new Date().toISOString();
  }

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function renderQuestions(questions) {
    const mcqs = questions.filter(q => q.type === "mcq");
    const fibs = questions.filter(q => q.type === "fib");

    el.mcqContainer.innerHTML = mcqs.map((q, idx) => `
      <article class="card">
        <h2>Question ${idx + 1} (MCQ)</h2>
        <p>${escapeHtml(q.text)}</p>
        ${q.options.map((opt) => `<label><input type="radio" name="${q.id}" value="${opt}"> ${escapeHtml(opt)}</label>`).join("")}
      </article>
    `).join("");

    el.fibContainer.innerHTML = fibs.map((q, idx) => `
      <article class="card">
        <h2>Question ${mcqs.length + idx + 1} (Fill in the blank)</h2>
        <p>${escapeHtml(q.text)}</p>
        <input class="fib-input" data-qid="${q.id}" type="text" autocomplete="off" placeholder="Type answer here">
      </article>
    `).join("");
  }

  function logEvent(type, confidence, details = {}) {
    const evt = {
      type,
      confidence,
      ts: nowIso(),
      sessionId: state.sessionId,
      details
    };
    state.eventBuffer.push(evt);
    if (state.eventBuffer.length > CONFIG.maxEventsBuffer) {
      state.eventBuffer.shift();
    }

    try {
      const existing = JSON.parse(localStorage.getItem("secure_exam_audit") || "[]");
      existing.push(evt);
      localStorage.setItem("secure_exam_audit", JSON.stringify(existing.slice(-1000)));
    } catch (_) {
      // Best effort local fallback.
    }

    if (CONFIG.auditEndpoint && state.sessionToken) {
      fetch(CONFIG.auditEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${state.sessionToken}`
        },
        body: JSON.stringify(evt),
        keepalive: true
      }).catch(() => {});
    }
  }

  function terminateSession(reasonCode, reasonText, confidence = "critical", details = {}) {
    if (state.terminated) return;
    state.terminated = true;
    logEvent("session_terminated", confidence, { reasonCode, reasonText, ...details });

    el.examScreen.classList.add("hidden");
    el.startScreen.classList.add("hidden");
    el.terminatedScreen.classList.remove("hidden");
    el.terminateReason.textContent = reasonText;
    el.terminateCode.textContent = reasonCode;
    el.statusPill.className = "pill warn";
    el.statusPill.textContent = "Terminated";

    if (document.fullscreenElement) {
      document.exitFullscreen().catch(() => {});
    }
  }

  function enforceZeroStrike(type, reasonCode, reasonText, details = {}) {
    logEvent(type, "critical", details);
    if (CONFIG.zeroTolerance) {
      terminateSession(reasonCode, reasonText, "critical", details);
    }
  }

  async function enterSecureMode() {
    if (!el.consent.checked) return;

    try {
      const startResp = await fetch("/api/session/start", { method: "POST" });
      const startData = await startResp.json();
      if (!startResp.ok || !startData?.token || !startData?.sessionId || !startData?.questions) {
        terminateSession("SESSION_START_FAILED", "Server session initialization failed.");
        return;
      }
      state.sessionId = startData.sessionId;
      state.sessionToken = startData.token;
      state.questions = startData.questions;
    } catch (_) {
      terminateSession("SESSION_START_FAILED", "Unable to reach session service.");
      return;
    }

    try {
      await document.documentElement.requestFullscreen();
    } catch (_) {
      terminateSession("FULLSCREEN_REQUIRED", "Fullscreen permission failed.");
      return;
    }

    state.started = true;
    el.startScreen.classList.add("hidden");
    el.examScreen.classList.remove("hidden");
    el.sessionId.textContent = state.sessionId;

    // Render questions dynamically before binding monitors
    renderQuestions(state.questions);

    logEvent("session_started", "info", {
      userAgent: navigator.userAgent,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
    });

    bindSecurityMonitors();
    startPerformanceMonitor();
  }

  function bindSecurityMonitors() {
    window.addEventListener("blur", () => {
      enforceZeroStrike("focus_lost", "FOCUS_LOST", "Window focus left secure exam.");
    });

    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        enforceZeroStrike("visibility_hidden", "TAB_HIDDEN", "Tab visibility changed to hidden.");
      }
    });

    document.addEventListener("fullscreenchange", () => {
      if (state.started && !document.fullscreenElement && !state.terminated) {
        enforceZeroStrike("fullscreen_exit", "FULLSCREEN_EXIT", "Fullscreen exited during secure session.");
      }
    });

    document.addEventListener("mouseleave", () => {
      enforceZeroStrike("pointer_left_window", "POINTER_EXIT", "Pointer left exam window bounds.");
    });

    document.addEventListener("contextmenu", (e) => {
      e.preventDefault();
      enforceZeroStrike("contextmenu_blocked", "CONTEXT_MENU", "Context menu invocation detected.");
    });

    document.addEventListener("selectstart", (e) => {
      e.preventDefault();
      logEvent("selection_blocked", "medium");
    });

    document.addEventListener("paste", (e) => {
      e.preventDefault();
      enforceZeroStrike("paste_detected", "PASTE_DETECTED", "Clipboard paste is disabled.");
    });

    document.addEventListener("keydown", (e) => {
      const key = (e.key || "").toLowerCase();
      const ctrlOrMeta = e.ctrlKey || e.metaKey;
      const blocked =
        e.altKey ||
        key === "f12" ||
        key === "printscreen" ||
        (ctrlOrMeta && ["c", "v", "x", "u", "s", "a", "p"].includes(key)) ||
        (ctrlOrMeta && e.shiftKey && ["i", "j", "c"].includes(key));
      if (blocked) {
        e.preventDefault();
        enforceZeroStrike("shortcut_blocked", "SHORTCUT_BLOCKED", "Disallowed keyboard shortcut detected.", {
          key: e.key,
          ctrlKey: e.ctrlKey,
          altKey: e.altKey,
          shiftKey: e.shiftKey,
          metaKey: e.metaKey
        });
        return;
      }

      const isFibInput = document.activeElement && document.activeElement.classList && document.activeElement.classList.contains("fib-input");
      if (isFibInput && key.length === 1) {
        const t = performance.now();
        if (state.lastKeyTs > 0) {
          const delta = t - state.lastKeyTs;
          logEvent("typing_interval", "info", { deltaMs: Math.round(delta) });
          if (delta < CONFIG.minKeystrokeIntervalMs) {
            enforceZeroStrike(
              "typing_anomaly",
              "INPUT_TIMING_ANOMALY",
              "Typing cadence anomaly detected.",
              { deltaMs: delta }
            );
          }
        }
        state.lastKeyTs = t;
      }
    });

    document.querySelectorAll(".fib-input").forEach((inputEl) => {
      inputEl.addEventListener("input", (e) => {
        const inputEvent = e;
        if (inputEvent.inputType && inputEvent.inputType.includes("insertFromPaste")) {
          enforceZeroStrike("paste_input_type", "PASTE_INPUT", "Paste-like input mutation detected.");
        }
        if ((inputEvent.data || "").length > 1) {
          logEvent("bulk_input_observed", "high", { dataLength: inputEvent.data.length, qid: inputEl.dataset.qid });
        }
      });
      inputEl.addEventListener("focus", () => {
        state.lastKeyTs = 0;
      });
    });
  }

  function collectAnswers() {
    const mcqAnswers = {};
    const mcqs = state.questions.filter(q => q.type === "mcq");
    for (const q of mcqs) {
      const checked = document.querySelector(`input[name="${q.id}"]:checked`);
      mcqAnswers[q.id] = checked ? checked.value : "";
    }

    const fibAnswers = {};
    const fibInputs = document.querySelectorAll(".fib-input");
    for (const input of fibInputs) {
      const v = input.value.trim();
      fibAnswers[input.dataset.qid] = v;
    }

    return { mcqAnswers, fibAnswers };
  }

  function buildSubmissionPayload(allAnswers) {
    const mcqKeys = Object.keys(allAnswers.mcqAnswers);
    const fibKeys = Object.keys(allAnswers.fibAnswers);
    return {
      nonce: `${crypto.randomUUID()}-${Date.now()}`,
      q1: mcqKeys.length > 0 ? allAnswers.mcqAnswers[mcqKeys[0]] : "",
      q2: fibKeys.length > 0 ? allAnswers.fibAnswers[fibKeys[0]] : "",
      mcqAnswers: allAnswers.mcqAnswers,
      fibAnswers: allAnswers.fibAnswers
    };
  }

  function countTextLengths(answersMap) {
    let total = 0;
    for (const v of Object.values(answersMap)) total += String(v).length;
    return total;
  }

  function showResult(grading) {
    const { total, correct, wrong, scorePercent, results } = grading;
    el.startScreen.classList.add("hidden");
    el.examScreen.classList.add("hidden");
    el.terminatedScreen.classList.add("hidden");
    el.resultScreen.classList.remove("hidden");

    el.resultSummary.textContent = `Score: ${correct}/${total} (${scorePercent}%). Wrong: ${wrong}.`;
    el.resultBreakdown.innerHTML = results.map((r, idx) => `
      <article class="card">
        <strong>Q${idx + 1} (${r.type.toUpperCase()}): ${r.correct ? "Correct" : "Wrong"}</strong>
        <p class="small muted">Your answer: ${String(r.given || "(blank)")}</p>
        <p class="small muted">Expected: ${String(r.expected)}</p>
      </article>
    `).join("");
  }

  function submitExam() {
    if (state.terminated) return;
    const answers = collectAnswers();

    const payload = buildSubmissionPayload(answers);
    fetch("/api/session/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${state.sessionToken}`
      },
      body: JSON.stringify(payload)
    })
      .then(async (resp) => {
        const data = await resp.json().catch(() => ({}));
        if (!resp.ok) {
          if (resp.status === 403) {
            terminateSession(data.reasonCode || "SERVER_TERMINATED", "Server reported session termination.");
            return;
          }
          alert(data.error || "Submission failed.");
          return;
        }
        logEvent("exam_submitted", "info", {
          mcqCount: Object.keys(answers.mcqAnswers).length,
          fibCount: Object.keys(answers.fibAnswers).length,
          fibTextLength: countTextLengths(answers.fibAnswers)
        });
        if (!data.grading) {
          alert("Submission accepted.");
          window.location.reload();
          return;
        }
        showResult(data.grading);
      })
      .catch(() => {
        alert("Network error while submitting.");
      });
  }

  function init() {
    el.consent.addEventListener("change", () => {
      el.startBtn.disabled = !el.consent.checked;
    });
    el.startBtn.addEventListener("click", enterSecureMode);
    el.submitBtn.addEventListener("click", submitExam);
    el.restartBtn.addEventListener("click", () => window.location.reload());
    el.resultRestartBtn.addEventListener("click", () => window.location.reload());
  }

  init();
  function startPerformanceMonitor() {
    let lastTs = performance.now();
    const loop = (ts) => {
      if (state.terminated) return;
      const delta = ts - lastTs;
      lastTs = ts;

      const fps = 1000 / Math.max(delta, 1);
      state.frameSamples.push(fps);
      if (state.frameSamples.length > CONFIG.rAFWindowSize) {
        state.frameSamples.shift();
      }

      if (state.frameSamples.length === CONFIG.rAFWindowSize) {
        const avg = state.frameSamples.reduce((a, b) => a + b, 0) / state.frameSamples.length;
        if (avg < CONFIG.fpsDropThreshold) {
          logEvent("fps_drop_suspicious", "medium", { averageFps: Number(avg.toFixed(2)) });
        }
      }

      requestAnimationFrame(loop);
    };

    requestAnimationFrame(loop);
  }

})();
