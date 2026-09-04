"use strict";

const QUESTIONS_POOL = {
  mcq: [
    {
      id: "hard_mcq_1",
      type: "mcq",
      text: "In JavaScript V8 engine, what optimization transforms polymorphic property access into monomorphic inline caches (ICs)?",
      options: [
        "Hidden classes (Shapes/Maps) transitions tracking",
        "Eager JIT bytecode decompression",
        "Stack-allocated prototype pinning"
      ],
      answer: "Hidden classes (Shapes/Maps) transitions tracking"
    },
    {
      id: "hard_mcq_2",
      type: "mcq",
      text: "Which HTTP header is strictly required to enable Cross-Origin Isolation for SharedArrayBuffer usage?",
      options: [
        "Cross-Origin-Opener-Policy: same-origin and Cross-Origin-Embedder-Policy: require-corp",
        "Access-Control-Allow-Origin: * and Access-Control-Allow-Credentials: true",
        "Content-Security-Policy: isolate-workers"
      ],
      answer: "Cross-Origin-Opener-Policy: same-origin and Cross-Origin-Embedder-Policy: require-corp"
    },
    {
      id: "hard_mcq_3",
      type: "mcq",
      text: "What is the output of `typeof (class {})` in JavaScript?",
      options: [
        "function",
        "object",
        "class"
      ],
      answer: "function"
    },
    {
      id: "hard_mcq_4",
      type: "mcq",
      text: "Which event loop microtask phase executes immediately after the current execution context stack empties but before rendering?",
      options: [
        "Microtask Queue (Promise callbacks and queueMicrotask)",
        "Timers Phase (setTimeout / setInterval)",
        "Check Phase (setImmediate)"
      ],
      answer: "Microtask Queue (Promise callbacks and queueMicrotask)"
    },
    {
      id: "hard_mcq_5",
      type: "mcq",
      text: "What prevents prototype pollution attacks in modern JavaScript objects without prototypes?",
      options: [
        "Creating objects with Object.create(null)",
        "Freezing only the top-level keys with Object.freeze()",
        "Using standard object literal syntax {}"
      ],
      answer: "Creating objects with Object.create(null)"
    },
    {
      id: "hard_mcq_6",
      type: "mcq",
      text: "In OAuth 2.1 authorization code flow for public clients (SPAs), which mechanism prevents authorization code interception attacks?",
      options: [
        "PKCE (Proof Key for Code Exchange) with S256 code challenge",
        "Client Secret rotation over mTLS",
        "Implicit Token Grant in URL fragments"
      ],
      answer: "PKCE (Proof Key for Code Exchange) with S256 code challenge"
    },
    {
      id: "hard_mcq_7",
      type: "mcq",
      text: "How does JavaScript's `WeakMap` prevent memory leaks compared to a standard `Map`?",
      options: [
        "Keys must be objects/symbols held weakly, allowing them to be garbage collected when unreachable elsewhere",
        "Values are automatically evicted using an LRU cache algorithm",
        "Keys are stored in Web Worker isolated heap memory"
      ],
      answer: "Keys must be objects/symbols held weakly, allowing them to be garbage collected when unreachable elsewhere"
    },
    {
      id: "hard_mcq_8",
      type: "mcq",
      text: "Which CSS property establishes a new 'stacking context' without creating a new block formatting context (BFC)?",
      options: [
        "isolation: isolate",
        "overflow: hidden",
        "display: flow-root"
      ],
      answer: "isolation: isolate"
    },
    {
      id: "hard_mcq_9",
      type: "mcq",
      text: "What happens when `Promise.allSettled()` is executed on an array of promises where two reject?",
      options: [
        "It resolves with an array of outcome objects describing each promise's status and value/reason",
        "It rejects immediately with an AggregateError containing both rejection reasons",
        "It hangs indefinitely waiting for manual rejection handling"
      ],
      answer: "It resolves with an array of outcome objects describing each promise's status and value/reason"
    },
    {
      id: "hard_mcq_10",
      type: "mcq",
      text: "Which HTTP/3 protocol innovation eliminates TCP Head-of-Line (HoL) blocking at the transport layer?",
      options: [
        "QUIC protocol operating over independent UDP streams",
        "HPACK header table dynamic compression",
        "TLS 1.3 0-RTT early data replication"
      ],
      answer: "QUIC protocol operating over independent UDP streams"
    },
    {
      id: "hard_mcq_11",
      type: "mcq",
      text: "What does the JavaScript `Reflect.apply(target, thisArgument, argumentsList)` method accomplish?",
      options: [
        "Calls a target function with specified this and arguments, behaving as Function.prototype.apply without prototype lookup hijacking",
        "Compiles the function into WebAssembly bytecode",
        "Clones the target function scope"
      ],
      answer: "Calls a target function with specified this and arguments, behaving as Function.prototype.apply without prototype lookup hijacking"
    },
    {
      id: "hard_mcq_12",
      type: "mcq",
      text: "In CSS Grid, what does `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))` do compared to `auto-fill`?",
      options: [
        "auto-fit collapses empty repeated tracks to 0px allowing remaining items to stretch to fill the container",
        "auto-fit retains empty tracks maintaining fixed slot allocations",
        "auto-fit creates masonry column breaks"
      ],
      answer: "auto-fit collapses empty repeated tracks to 0px allowing remaining items to stretch to fill the container"
    },
    {
      id: "hard_mcq_13",
      type: "mcq",
      text: "What is the primary vulnerability prevented by the HTTP `X-Content-Type-Options: nosniff` header?",
      options: [
        "MIME-type sniffing attacks where browsers execute non-executable files as script/css",
        "Cross-site request forgery on multipart form uploads",
        "DOM-based cross-site scripting via innerHTML"
      ],
      answer: "MIME-type sniffing attacks where browsers execute non-executable files as script/css"
    },
    {
      id: "hard_mcq_14",
      type: "mcq",
      text: "In JavaScript, what is the value of `[1, 2, 3] + [4, 5, 6]`?",
      options: [
        "'1,2,34,5,6'",
        "[1, 2, 3, 4, 5, 6]",
        "NaN"
      ],
      answer: "'1,2,34,5,6'"
    },
    {
      id: "hard_mcq_15",
      type: "mcq",
      text: "Which Web API allows background synchronization of data even if the user closes the web tab or browser?",
      options: [
        "Service Worker Background Sync API",
        "WebSockets Reconnect Worker",
        "BroadcastChannel Synchronization"
      ],
      answer: "Service Worker Background Sync API"
    },
    {
      id: "hard_mcq_16",
      type: "mcq",
      text: "What does the `Subresource Integrity (SRI)` hash check ensure during external script loading?",
      options: [
        "Ensures fetched CDN resource has not been altered or tampered with by verifying its cryptographic hash",
        "Encrypts payload transmission between CDN and client",
        "Guarantees the script executes before DOMContentLoaded"
      ],
      answer: "Ensures fetched CDN resource has not been altered or tampered with by verifying its cryptographic hash"
    },
    {
      id: "hard_mcq_17",
      type: "mcq",
      text: "In React 18 Concurrent Mode, what does the `useDeferredValue` hook do?",
      options: [
        "Defers updating a secondary value until urgent UI updates (like typing inputs) have finished rendering",
        "Delays network API requests using an automatic debounce timer",
        "Prevents re-renders across parent component trees"
      ],
      answer: "Defers updating a secondary value until urgent UI updates (like typing inputs) have finished rendering"
    },
    {
      id: "hard_mcq_18",
      type: "mcq",
      text: "What is the result of `Number.MIN_VALUE > 0` in JavaScript?",
      options: [
        "true",
        "false",
        "TypeError"
      ],
      answer: "true"
    },
    {
      id: "hard_mcq_19",
      type: "mcq",
      text: "Which CSS property modernizes container-based responsive design by querying parent component widths?",
      options: [
        "@container / container-type: inline-size",
        "@media (component-width)",
        "flex-basis: auto-query"
      ],
      answer: "@container / container-type: inline-size"
    },
    {
      id: "hard_mcq_20",
      type: "mcq",
      text: "In Cryptography, what is the main advantage of the ChaCha20-Poly1305 cipher suite over AES-GCM on mobile devices?",
      options: [
        "Performs faster in software without requiring dedicated hardware AES instruction sets",
        "Requires 4096-bit symmetric keys",
        "Provides quantum-proof asymmetric key generation"
      ],
      answer: "Performs faster in software without requiring dedicated hardware AES instruction sets"
    },
    {
      id: "hard_mcq_21",
      type: "mcq",
      text: "What does the JavaScript `Structured Clone Algorithm` handle that `JSON.parse(JSON.stringify(obj))` fails on?",
      options: [
        "Circular references, Maps, Sets, Dates, and ArrayBuffers",
        "Private class methods and closures",
        "DOM Node clones with event listeners"
      ],
      answer: "Circular references, Maps, Sets, Dates, and ArrayBuffers"
    },
    {
      id: "hard_mcq_22",
      type: "mcq",
      text: "In Node.js event loop, which queue has the highest priority and executes between every event loop transition?",
      options: [
        "process.nextTick() queue",
        "setImmediate() check queue",
        "setTimeout() timer queue"
      ],
      answer: "process.nextTick() queue"
    },
    {
      id: "hard_mcq_23",
      type: "mcq",
      text: "What is the purpose of the HTTP `Clear-Site-Data` response header?",
      options: [
        "Instructs the browser to clear cookies, storage, cache, or execution contexts for the host origin",
        "Forces an immediate DOM hard-refresh without service worker caching",
        "Purges edge proxy server CDN caches"
      ],
      answer: "Instructs the browser to clear cookies, storage, cache, or execution contexts for the host origin"
    },
    {
      id: "hard_mcq_24",
      type: "mcq",
      text: "In JavaScript, what does `Object.is(-0, +0)` return?",
      options: [
        "false",
        "true",
        "NaN"
      ],
      answer: "false"
    },
    {
      id: "hard_mcq_25",
      type: "mcq",
      text: "Which browser security mechanism prevents CSS Exfiltration attacks that leak sensitive input values via attribute selectors?",
      options: [
        "Strict Content Security Policy (style-src nonce / strict CSP)",
        "X-Frame-Options: SAMEORIGIN",
        "CORS Preflight Options Header"
      ],
      answer: "Strict Content Security Policy (style-src nonce / strict CSP)"
    }
  ],
  multi_mcq: [
    {
      id: "hard_multi_1",
      type: "multi_mcq",
      text: "Select ALL HTTP security headers that mitigate Cross-Site Scripting (XSS) or Data Exfiltration (Select all that apply):",
      options: [
        "Content-Security-Policy",
        "X-Content-Type-Options: nosniff",
        "Accept-Encoding: gzip",
        "Cache-Control: public"
      ],
      answer: ["Content-Security-Policy", "X-Content-Type-Options: nosniff"]
    },
    {
      id: "hard_multi_2",
      type: "multi_mcq",
      text: "Which of the following JavaScript features introduce block-scoped bindings without creating window global properties? (Select all that apply):",
      options: [
        "let declaration",
        "const declaration",
        "var declaration in global scope",
        "function declaration in global scope"
      ],
      answer: ["let declaration", "const declaration"]
    },
    {
      id: "hard_multi_3",
      type: "multi_mcq",
      text: "Select ALL mechanisms that queue a JavaScript Microtask in modern browsers (Select all that apply):",
      options: [
        "Promise.prototype.then()",
        "queueMicrotask()",
        "MutationObserver callback",
        "setTimeout(..., 0)"
      ],
      answer: ["Promise.prototype.then()", "queueMicrotask()", "MutationObserver callback"]
    },
    {
      id: "hard_multi_4",
      type: "multi_mcq",
      text: "Which of the following create a new Block Formatting Context (BFC) in CSS? (Select all that apply):",
      options: [
        "display: flow-root",
        "overflow: hidden on non-inline element",
        "float: left",
        "position: static"
      ],
      answer: ["display: flow-root", "overflow: hidden on non-inline element", "float: left"]
    },
    {
      id: "hard_multi_5",
      type: "multi_mcq",
      text: "Select ALL valid JSON data types supported by the ECMA-404 standard (Select all that apply):",
      options: [
        "Array",
        "Boolean",
        "Undefined",
        "Function"
      ],
      answer: ["Array", "Boolean"]
    },
    {
      id: "hard_multi_6",
      type: "multi_mcq",
      text: "Which cookie attributes directly defend against Cross-Site Request Forgery (CSRF) and XSS session theft? (Select all that apply):",
      options: [
        "SameSite=Strict (or Lax)",
        "HttpOnly",
        "Secure",
        "Domain=*"
      ],
      answer: ["SameSite=Strict (or Lax)", "HttpOnly", "Secure"]
    }
  ],
  dropdown: [
    {
      id: "hard_dropdown_1",
      type: "dropdown",
      text: "Select the HTTP Status Code for 'Too Many Requests' rate limiting:",
      options: [
        "400 Bad Request",
        "403 Forbidden",
        "429 Too Many Requests",
        "503 Service Unavailable"
      ],
      answer: "429 Too Many Requests"
    },
    {
      id: "hard_dropdown_2",
      type: "dropdown",
      text: "Select the CSS property that forces sub-pixel font antialiasing in WebKit engines:",
      options: [
        "-webkit-font-smoothing: antialiased",
        "text-rendering: optimizeLegibility",
        "font-variant: subpixel",
        "font-optical-sizing: auto"
      ],
      answer: "-webkit-font-smoothing: antialiased"
    },
    {
      id: "hard_dropdown_3",
      type: "dropdown",
      text: "Select the HTTP Status Code returned when an origin server rejects a CORS preflight request:",
      options: [
        "403 Forbidden",
        "405 Method Not Allowed",
        "401 Unauthorized",
        "412 Precondition Failed"
      ],
      answer: "403 Forbidden"
    },
    {
      id: "hard_dropdown_4",
      type: "dropdown",
      text: "Select the JavaScript Proxy trap handler used to intercept property access operations:",
      options: [
        "get(target, prop, receiver)",
        "apply(target, thisArg, argArray)",
        "construct(target, argArray)",
        "has(target, prop)"
      ],
      answer: "get(target, prop, receiver)"
    },
    {
      id: "hard_dropdown_5",
      type: "dropdown",
      text: "Select the CSS layout property that stops flex items from shrinking below their content size:",
      options: [
        "flex-shrink: 0",
        "flex-grow: 1",
        "flex-basis: max-content",
        "align-self: stretch"
      ],
      answer: "flex-shrink: 0"
    }
  ],
  fib: [
    {
      id: "hard_fib_1",
      type: "fib",
      text: "Fill in: In JavaScript, standard function `this` binding is evaluated at ______ time (runtime/lexical/parse).",
      answer: ["runtime", "call", "execution"]
    },
    {
      id: "hard_fib_2",
      type: "fib",
      text: "Fill in: The CSS property that controls whether an element creates a 3D rendering context for children is transform-______: preserve-3d.",
      answer: ["style"]
    },
    {
      id: "hard_fib_3",
      type: "fib",
      text: "Fill in: The HTTP status code for 'Payload Too Large' (Request Entity Too Large) is ______.",
      answer: ["413"]
    },
    {
      id: "hard_fib_4",
      type: "fib",
      text: "Fill in: In cryptographic hashing, HMAC stands for Hash-based Message ______ Code.",
      answer: ["Authentication", "authentication"]
    },
    {
      id: "hard_fib_5",
      type: "fib",
      text: "Fill in: In JSON Web Tokens (JWT), the three segments separated by dots are Header, Payload, and ______.",
      answer: ["Signature", "signature"]
    },
    {
      id: "hard_fib_6",
      type: "fib",
      text: "Fill in: The V8 engine optimization compiler that produces machine code from bytecode is named Turbo______.",
      answer: ["Fan", "fan", "turbofan", "Turbofan"]
    },
    {
      id: "hard_fib_7",
      type: "fib",
      text: "Fill in: In modern web networking, TLS stands for Transport Layer ______.",
      answer: ["Security", "security"]
    },
    {
      id: "hard_fib_8",
      type: "fib",
      text: "Fill in: The JavaScript Symbol used to customize how an object converts to a primitive value is Symbol.to______.",
      answer: ["Primitive", "primitive"]
    }
  ],
  textarea: [
    {
      id: "hard_textarea_1",
      type: "textarea",
      text: "Code Response: What is the exact keyword used in ES Modules to export a variable under a different alias name? (e.g. export { x ___ y })",
      answer: ["as", "as keyword", "export as"]
    },
    {
      id: "hard_textarea_2",
      type: "textarea",
      text: "Technical Term: What is the single word term for the security vulnerability where malicious script tags are injected into an application and stored in a database?",
      answer: ["Stored XSS", "stored xss", "XSS", "Persistent XSS", "persistent xss"]
    },
    {
      id: "hard_textarea_3",
      type: "textarea",
      text: "Architecture Term: In REST API design, what is the term for an operation where producing the same request multiple times has the exact same side-effects as a single request?",
      answer: ["Idempotence", "idempotence", "Idempotent", "idempotent"]
    }
  ]
};

function sample(arr, n) {
  const shuffled = [...arr].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, n);
}

function getQuestionsForSession() {
  // Balanced sample: 14 single MCQs + 3 multi-select MCQs + 3 Dropdowns + 3 FIBs + 2 Textareas = 25 Questions
  const singleMcqs = sample(QUESTIONS_POOL.mcq, 14);
  const multiMcqs = sample(QUESTIONS_POOL.multi_mcq, 3);
  const dropdowns = sample(QUESTIONS_POOL.dropdown, 3);
  const fibs = sample(QUESTIONS_POOL.fib, 3);
  const textareas = sample(QUESTIONS_POOL.textarea, 2);

  const selected = [...singleMcqs, ...multiMcqs, ...dropdowns, ...fibs, ...textareas];
  // Shuffle overall question order so formats are interwoven!
  const randomizedList = selected.sort(() => 0.5 - Math.random());

  // Client-safe questions mapping (strip answers)
  const clientSafe = randomizedList.map((q) => {
    const item = {
      id: q.id,
      text: q.text,
      type: q.type
    };
    if (q.options) {
      item.options = q.options;
    }
    return item;
  });

  return {
    questionIds: randomizedList.map((q) => q.id),
    questions: clientSafe
  };
}

function getCorrectAnswers(questionIds) {
  const answerKey = {};
  const allMap = new Map();
  
  QUESTIONS_POOL.mcq.forEach(q => allMap.set(q.id, q));
  QUESTIONS_POOL.multi_mcq.forEach(q => allMap.set(q.id, q));
  QUESTIONS_POOL.dropdown.forEach(q => allMap.set(q.id, q));
  QUESTIONS_POOL.fib.forEach(q => allMap.set(q.id, q));
  QUESTIONS_POOL.textarea.forEach(q => allMap.set(q.id, q));

  for (const id of questionIds) {
    const q = allMap.get(id);
    if (q) {
      answerKey[id] = q.answer;
    }
  }

  return answerKey;
}

module.exports = {
  QUESTIONS_POOL,
  getQuestionsForSession,
  getCorrectAnswers
};
