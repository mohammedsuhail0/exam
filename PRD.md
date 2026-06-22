# Product Requirement Document (PRD)
## Project Name: Secure Online Exam Portal (Zero-Tolerance Mode)
## Version: 2.0 (Security Hardened & Defeat Matrix Integrated)

---

## 1. Objective
Build a browser-based exam portal that detects suspicious behavior in real time, enforces strict session integrity, and terminates the attempt on high-confidence violations. This portal serves as a hardened developer playground to analyze client-side security limits against kernel-level automated browser manipulation.

---

## 2. Scope
* Fullscreen exam workspace.
* Focus/visibility monitoring.
* Restricted shortcuts and context actions.
* Behavioral telemetry (typing cadence, input anomalies).
* One-strike termination policy.
* Audit logging for proctor review.
* **Open-Source CDP Agent Compatability:** Built to interface with Chrome DevTools Protocol testing scripts for defensive security evaluation.

---

## 3. Threat Model
* Tab switching / window blur.
* Hidden/background automation.
* Clipboard paste into protected answers.
* DevTools/open-inspection attempts.
* Screen-capture or performance anomalies.
* Synthetic high-speed input injection.
* **Kernel-Level Remote Puppeteering:** Automation scripts hijacking Chrome via port 9222 debugging pipelines to manipulate DOM nodes directly without generating standard user interface pointer coordinates.

---

## 4. Functional Requirements

### 4.1 Secure Session Start
* User must explicitly start secure mode.
* Attempt fullscreen lock at start.
* If fullscreen permission fails, block exam start or terminate per policy.

### 4.2 Focus & Visibility Guard
* Detect blur, visibilitychange, fullscreen exit.
* Immediate termination on violation (configurable).

### 4.3 Pointer Boundary Monitoring
* Track cursor exit (mouseleave) and pointer lock state where supported.
* Log and terminate based on strictness profile.

### 4.4 Keyboard Policy
* Block/flag disallowed shortcuts (copy/paste/devtools-related combos, print screen where detectable).
* Record key event metadata (not raw content for privacy unless required).

### 4.5 Input Integrity Monitoring
* Measure inter-keystroke timing for typed responses.
* Detect bulk insertion patterns (sudden multi-char injection, paste events).
* Treat suspicious anomalies as infractions. Real-time typing speeds must fit standard human limits (>15ms intervals between keydowns).

### 4.6 Rendering/Performance Watch
* Use requestAnimationFrame and long-task observation to detect unusual runtime disruptions.
* Mark as suspicious signal (should not be sole termination trigger without corroboration).

### 4.7 Zero-Strike Policy
* One high-confidence violation ends session instantly.
* Exam UI is replaced with terminated state.
* Submission disabled.

### 4.8 Audit Trail
* Store timestamped events:
  * Event type.
  * Confidence level.
  * Client fingerprint/session ID.
  * Question context (if relevant).
* Send data packets to the backend in near real time.

---

## 5. Non-Functional Requirements
* **Latency:** Monitoring overhead < 5% on mid-range devices.
* **Reliability:** Works on latest Chrome/Edge/Firefox (degraded mode documented).
* **Privacy:** Minimize PII, encrypt logs in transit and at rest.
* **Accessibility:** Documented accommodations mode (separate policy profile).

---

## 6. Security Architecture
Client-side checks are only one layer. Final trust must be server-side:
* Signed session tokens with short TTL.
* Server validation of event sequence and timestamps.
* Rate/consistency checks for answers.
* Immutable audit log storage.
* Anti-replay protection on submission payloads.

---

## 7. Policy Engine
Define severity levels:
* **Critical:** Blur, hidden tab, fullscreen exit, confirmed paste injection.
* **High:** Shortcut abuse, repeated suspicious timing anomalies.
* **Medium:** FPS anomalies, non-critical behavior spikes.
* **Zero-Tolerance Mode:** Terminate on first Critical (or first High if configured).

---

## 8. UX Requirements
* Clear pre-exam consent screen listing monitoring rules.
* Real-time “secure mode active” indicator.
* Deterministic termination message with reason code.
* No misleading “you passed security” messages.

---

## 9. Compliance & Legal
* Explicit consent before monitoring.
* Retention policy for logs (e.g., 30/90 days).
* Jurisdiction-specific privacy alignment (FERPA/GDPR-like constraints if applicable).
* Accommodations flow for accessibility/legal exceptions.

---

## 10. Test Plan
* Unit tests for each detector.
* Integration tests for termination flow.
* Cross-browser matrix verification.
* False-positive calibration with real typing datasets.
* Load tests for event ingestion backend.

---

## 11. Risks
* False positives (fast typists, accessibility tools).
* Browser API limitations.
* Client-side tampering (must assume possible).
* Legal/privacy constraints by region.

---

## 12. Success Metrics
* < 1% false-positive termination rate (target).
* 95% detection of known cheating behavior patterns in controlled tests.
* 100% audit event integrity for terminated sessions.

---

## 13. Defensive Validation Matrix (CDP Detection Mapping)
This section maps the client-side detection gaps against deep-level Chromium browser manipulation, defining how the server validation layer must catch advanced external scripts.


| Target Security Indicator | Monitored Element Code | Automated Vulnerability Vector | Required Server-Side Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Focus Lock Integrity** | `window.onblur`<br>`document.hidden` | Hidden CDP WebSocket Connection (`port 9222`) | **Challenge Tokens:** Client-side focus listeners cannot see background ports. The server must issue random interactive check popups that require localized human input to verify active presence. |
| **Pointer Mechanics** | `document.onmouseleave` | Zero-Coordinate Script Mutation | **Movement Profiling:** Real users generate cursor drift before clicking a radio button. The server must reject form inputs that arrive with zero prior mouse-movement data. |
| **Keyboard Bypass** | `e.preventDefault()` on `Ctrl+C / V` | Direct DOM Variable Injection (`field.value`) | **Event Validation:** Reject inputs that do not fire sequential `keydown`, `keypress`, and `keyup` loops. JavaScript variable mutation misses these native interface signals. |
| **Input Cadence Analytics** | Inter-keystroke speeds (<15ms) | Human-Emulated Delay Chunking (60ms–140ms) | **Biometric Behavioral Baselines:** Implement a server-side AI model to track the variation patterns in typing. Scripted delays are often perfectly random, whereas human typing shows structural patterns based on key placement. |
| **Source Data Protection** | `document.onselectstart`<br>`document.oncontextmenu` | Headless Memory-Buffer Scraping (`page.content()`) | **Server-Side Rendering (SSR):** Prevent the browser from loading the full quiz text into the DOM at once. Render questions as obfuscated canvas elements or encrypted fragments. |
