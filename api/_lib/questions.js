"use strict";

const QUESTIONS_POOL = {
  mcq: [
    {
      id: "hard_mcq_1",
      type: "mcq",
      text: "What is the primary mechanism of JavaScript's prototype inheritance?",
      options: [
        "Objects have a hidden pointer to their prototype object",
        "Classes copy methods to instances during instantiation",
        "Functions compile into static type schemas"
      ],
      answer: "Objects have a hidden pointer to their prototype object"
    },
    {
      id: "hard_mcq_2",
      type: "mcq",
      text: "Which HTTP header is used to mitigate Clickjacking attacks?",
      options: [
        "Content-Security-Policy",
        "X-Frame-Options",
        "Referrer-Policy"
      ],
      answer: "X-Frame-Options"
    },
    {
      id: "hard_mcq_3",
      type: "mcq",
      text: "What is the output of console.log(0.1 + 0.2 === 0.3) in JavaScript?",
      options: [
        "true",
        "false",
        "undefined"
      ],
      answer: "false"
    },
    {
      id: "hard_mcq_4",
      type: "mcq",
      text: "Which event loop phase executes setTimeout callbacks?",
      options: [
        "Poll phase",
        "Timers phase",
        "Check phase"
      ],
      answer: "Timers phase"
    },
    {
      id: "hard_mcq_5",
      type: "mcq",
      text: "What does the defer attribute do when loading a script tag?",
      options: [
        "Downloads script asynchronously and executes it immediately",
        "Downloads script in parallel and executes it after document parsing finishes",
        "Blocks HTML parsing until script is downloaded and run"
      ],
      answer: "Downloads script in parallel and executes it after document parsing finishes"
    },
    {
      id: "hard_mcq_6",
      type: "mcq",
      text: "Which security policy prevents cross-site request forgery by restricting cookie transmission?",
      options: [
        "SameSite attribute",
        "CORS policy",
        "HttpOnly flag"
      ],
      answer: "SameSite attribute"
    },
    {
      id: "hard_mcq_7",
      type: "mcq",
      text: "What is a closure in JavaScript?",
      options: [
        "A function combined with its lexical environment",
        "A method to close database connections",
        "A built-in method for private classes"
      ],
      answer: "A function combined with its lexical environment"
    },
    {
      id: "hard_mcq_8",
      type: "mcq",
      text: "Which CSS layout feature allows you to change element order visually without changing HTML?",
      options: [
        "order property in Flexbox/Grid",
        "z-index stacking context",
        "float alignment"
      ],
      answer: "order property in Flexbox/Grid"
    },
    {
      id: "hard_mcq_9",
      type: "mcq",
      text: "How does a Promise.all() block behave if one of the promises rejects?",
      options: [
        "It immediately rejects with the error of the first rejected promise",
        "It waits for all promises to settle and returns errors",
        "It ignores the error and returns resolved ones"
      ],
      answer: "It immediately rejects with the error of the first rejected promise"
    },
    {
      id: "hard_mcq_10",
      type: "mcq",
      text: "Which browser mechanism restricts web page scripts from interacting with resources from a different origin?",
      options: [
        "Same-Origin Policy",
        "Content Security Policy",
        "Cross-Origin Resource Sharing"
      ],
      answer: "Same-Origin Policy"
    },
    {
      id: "hard_mcq_11",
      type: "mcq",
      text: "What is the purpose of the aria-live attribute in HTML?",
      options: [
        "To announce dynamic content updates to screen readers",
        "To keep websocket connections alive",
        "To speed up audio rendering"
      ],
      answer: "To announce dynamic content updates to screen readers"
    },
    {
      id: "hard_mcq_12",
      type: "mcq",
      text: "What is the purpose of a CSS transition-timing-function?",
      options: [
        "To specify the speed curve of a transition effect",
        "To delay the start of a transition",
        "To control the duration of a transition"
      ],
      answer: "To specify the speed curve of a transition effect"
    },
    {
      id: "hard_mcq_13",
      type: "mcq",
      text: "In JavaScript, what is 'temporal dead zone' (TDZ)?",
      options: [
        "The state before variable initialization where referencing it throws a ReferenceError",
        "The duration when the browser event loop is blocked",
        "The delay during service worker activation"
      ],
      answer: "The state before variable initialization where referencing it throws a ReferenceError"
    },
    {
      id: "hard_mcq_14",
      type: "mcq",
      text: "What is the difference between Object.freeze() and Object.seal()?",
      options: [
        "freeze prevents new properties and makes existing immutable; seal only prevents new properties",
        "freeze only works on arrays; seal works on objects",
        "seal prevents new properties and makes existing immutable; freeze only prevents new"
      ],
      answer: "freeze prevents new properties and makes existing immutable; seal only prevents new properties"
    },
    {
      id: "hard_mcq_15",
      type: "mcq",
      text: "What does the JavaScript bind() method return?",
      options: [
        "A new function with a pre-configured 'this' context",
        "The immediate return value of the function",
        "An array of bound variables"
      ],
      answer: "A new function with a pre-configured 'this' context"
    },
    {
      id: "hard_mcq_16",
      type: "mcq",
      text: "Which algorithm does the Chrome V8 Garbage Collector use for its young generation?",
      options: [
        "Mark-Sweep-Compact",
        "Scavenge ( Cheney's copying algorithm )",
        "Reference Counting"
      ],
      answer: "Scavenge ( Cheney's copying algorithm )"
    },
    {
      id: "hard_mcq_17",
      type: "mcq",
      text: "What does a CSS 'BFC' (Block Formatting Context) prevent?",
      options: [
        "Margin collapsing between adjacent block boxes",
        "Responsive styling overrides",
        "Inline rendering of text blocks"
      ],
      answer: "Margin collapsing between adjacent block boxes"
    },
    {
      id: "hard_mcq_18",
      type: "mcq",
      text: "In React, what does the 'useTransition' hook help optimize?",
      options: [
        "CSS transition speed variations",
        "Non-blocking rendering of state updates by keeping the UI responsive",
        "Server-side component routing timings"
      ],
      answer: "Non-blocking rendering of state updates by keeping the UI responsive"
    },
    {
      id: "hard_mcq_19",
      type: "mcq",
      text: "Which of the following is true about HTTP/2 multiplexing?",
      options: [
        "It opens a separate TCP connection for every single asset request",
        "It allows multiple request and response messages to be interleaved on a single TCP connection",
        "It compresses headers using GZIP algorithm exclusively"
      ],
      answer: "It allows multiple request and response messages to be interleaved on a single TCP connection"
    },
    {
      id: "hard_mcq_20",
      type: "mcq",
      text: "What does a 'Critical Rendering Path' optimization aim to minimize?",
      options: [
        "Initial page weight by minifying Javascript packages",
        "Time to first render by optimizing CSSOM and DOM construction dependencies",
        "The total count of background API requests"
      ],
      answer: "Time to first render by optimizing CSSOM and DOM construction dependencies"
    },
    {
      id: "hard_mcq_21",
      type: "mcq",
      text: "What is the primary vulnerability prevented by the HTTPOnly flag on cookies?",
      options: [
        "Session Hijacking via Cross-Site Scripting (XSS)",
        "Cross-Site Request Forgery (CSRF)",
        "Man-in-the-Middle (MitM) packet sniffing"
      ],
      answer: "Session Hijacking via Cross-Site Scripting (XSS)"
    },
    {
      id: "hard_mcq_22",
      type: "mcq",
      text: "Which CSS property forces a GPU layer (Hardware Acceleration) to be created?",
      options: [
        "will-change: transform",
        "display: block",
        "position: absolute"
      ],
      answer: "will-change: transform"
    },
    {
      id: "hard_mcq_23",
      type: "mcq",
      text: "What is the output of console.log(typeof NaN) in JavaScript?",
      options: [
        "'number'",
        "'NaN'",
        "'undefined'"
      ],
      answer: "'number'"
    },
    {
      id: "hard_mcq_24",
      type: "mcq",
      text: "Which HTTP header implements client-side restriction of script execution sources?",
      options: [
        "Content-Security-Policy (CSP)",
        "Strict-Transport-Security (HSTS)",
        "Cross-Origin-Embedder-Policy (COEP)"
      ],
      answer: "Content-Security-Policy (CSP)"
    },
    {
      id: "hard_mcq_25",
      type: "mcq",
      text: "What is the main difference between microtasks and macrotasks in the JavaScript Event Loop?",
      options: [
        "Microtasks run in a separate thread; macrotasks run in the main thread",
        "The microtask queue is fully cleared before the loop checks for the next macrotask",
        "Macrotasks have higher priority than microtasks"
      ],
      answer: "The microtask queue is fully cleared before the loop checks for the next macrotask"
    },
    {
      id: "hard_mcq_26",
      type: "mcq",
      text: "What does 'Event Delegation' in JavaScript rely on?",
      options: [
        "Event Bubbling",
        "Event Capturing only",
        "Immediate invocation of custom target listeners"
      ],
      answer: "Event Bubbling"
    },
    {
      id: "hard_mcq_27",
      type: "mcq",
      text: "Which Javascript feature is used to build non-blocking iterators that yield values sequentially?",
      options: [
        "Generator Functions",
        "Async/Await blocks only",
        "Recursive Promises"
      ],
      answer: "Generator Functions"
    },
    {
      id: "hard_mcq_28",
      type: "mcq",
      text: "What is the purpose of the Subresource Integrity (SRI) attribute in script elements?",
      options: [
        "To verify that fetched resources have not been altered in transit",
        "To compress files on CDN hubs before fetching",
        "To speed up cross-domain script execution"
      ],
      answer: "To verify that fetched resources have not been altered in transit"
    },
    {
      id: "hard_mcq_29",
      type: "mcq",
      text: "Which CSS display property renders grid-like structures while keeping layout inline?",
      options: [
        "inline-grid",
        "grid-inline",
        "flex-grid"
      ],
      answer: "inline-grid"
    },
    {
      id: "hard_mcq_30",
      type: "mcq",
      text: "What is the output of console.log([] == ![]) in JavaScript?",
      options: [
        "true",
        "false",
        "TypeError"
      ],
      answer: "true"
    },
    {
      id: "hard_mcq_31",
      type: "mcq",
      text: "Which mechanism allows service workers to intercept network requests and serve cached content directly?",
      options: [
        "Fetch API event listener interception",
        "HTTP/2 Push configuration",
        "Domain Name Server (DNS) routing changes"
      ],
      answer: "Fetch API event listener interception"
    },
    {
      id: "hard_mcq_32",
      type: "mcq",
      text: "What is the security risk of using target='_blank' without rel='noopener'?",
      options: [
        "The opened page can access the origin window's document.referrer and window.opener",
        "It exposes session storage arrays directly",
        "It triggers browser-level cross-site scripting filters"
      ],
      answer: "The opened page can access the origin window's document.referrer and window.opener"
    },
    {
      id: "hard_mcq_33",
      type: "mcq",
      text: "What is the behavior of the JavaScript Object.defineProperty() method when adding a property with no descriptor details?",
      options: [
        "It defaults writable, enumerable, and configurable to false",
        "It defaults writable, enumerable, and configurable to true",
        "It throws a syntax compilation warning"
      ],
      answer: "It defaults writable, enumerable, and configurable to false"
    },
    {
      id: "hard_mcq_34",
      type: "mcq",
      text: "Which CSS property controls how content fits into its box, similar to background-size?",
      options: [
        "object-fit",
        "image-rendering",
        "box-sizing"
      ],
      answer: "object-fit"
    },
    {
      id: "hard_mcq_35",
      type: "mcq",
      text: "How does the 'WeakMap' differ from a standard 'Map' in JavaScript?",
      options: [
        "Its keys must be objects and are held as weak references for garbage collection",
        "It is synchronized across web worker instances",
        "It automatically sorts elements on insertion"
      ],
      answer: "Its keys must be objects and are held as weak references for garbage collection"
    },
    {
      id: "hard_mcq_36",
      type: "mcq",
      text: "What does the CORS 'Preflight' request check?",
      options: [
        "If the target server trusts and accepts the actual cross-origin request method and headers",
        "If the client has valid certificate credentials",
        "If the file size is within limits"
      ],
      answer: "If the target server trusts and accepts the actual cross-origin request method and headers"
    },
    {
      id: "hard_mcq_37",
      type: "mcq",
      text: "What happens when you resolve a Promise inside another Promise's constructor?",
      options: [
        "The outer promise will wait for the inner promise to settle",
        "It throws an unhandled promise rejection error",
        "It creates a synchronous call stack block"
      ],
      answer: "The outer promise will wait for the inner promise to settle"
    },
    {
      id: "hard_mcq_38",
      type: "mcq",
      text: "Which layout standard does 'Grid Template Areas' follow?",
      options: [
        "CSS Grid Layout",
        "Flexbox Layout",
        "Table Layout"
      ],
      answer: "CSS Grid Layout"
    },
    {
      id: "hard_mcq_39",
      type: "mcq",
      text: "What is the output of console.log(1 + '2' - 1) in JavaScript?",
      options: [
        "11",
        "12",
        "1"
      ],
      answer: "11"
    },
    {
      id: "hard_mcq_40",
      type: "mcq",
      text: "What does 'Paint Flashing' dev tool option help visualize?",
      options: [
        "DOM elements that are currently being re-painted by the browser engine",
        "Network latency metrics",
        "Memory leak locations"
      ],
      answer: "DOM elements that are currently being re-painted by the browser engine"
    },
    {
      id: "hard_mcq_41",
      type: "mcq",
      text: "Which Web API is used to measure highly accurate execution timing in scripts?",
      options: [
        "Performance API (performance.now())",
        "Date API (Date.now())",
        "Console API (console.time())"
      ],
      answer: "Performance API (performance.now())"
    },
    {
      id: "hard_mcq_42",
      type: "mcq",
      text: "Which JavaScript scope context holds variables declared with 'var' outside any function?",
      options: [
        "Global Scope",
        "Block Scope",
        "Lexical Scope"
      ],
      answer: "Global Scope"
    },
    {
      id: "hard_mcq_43",
      type: "mcq",
      text: "What does the CSS property 'box-sizing: border-box' include inside width and height calculations?",
      options: [
        "Padding and Border",
        "Margin, Padding, and Border",
        "Only the inner content area"
      ],
      answer: "Padding and Border"
    },
    {
      id: "hard_mcq_44",
      type: "mcq",
      text: "Which CSS selector targeting matches an element that is the only child of its parent?",
      options: [
        ":only-child",
        ":first-child",
        ":last-child"
      ],
      answer: ":only-child"
    },
    {
      id: "hard_mcq_45",
      type: "mcq",
      text: "Which HTTP status code is used for 'Precondition Required'?",
      options: [
        "428",
        "412",
        "403"
      ],
      answer: "428"
    }
  ],
  fib: [
    {
      id: "hard_fib_1",
      type: "fib",
      text: "Fill in: In JavaScript, standard function context `this` is determined at ______ time.",
      answer: ["runtime", "execution", "call"]
    },
    {
      id: "hard_fib_2",
      type: "fib",
      text: "Fill in: The CSS layout property that creates a new stacking context is z-______.",
      answer: ["index"]
    },
    {
      id: "hard_fib_3",
      type: "fib",
      text: "Fill in: The HTTP status code for 'Payload Too Large' is ______.",
      answer: ["413"]
    },
    {
      id: "hard_fib_4",
      type: "fib",
      text: "Fill in: The DOM method used to append a node as the last child of a parent is ______Child().",
      answer: ["append"]
    },
    {
      id: "hard_fib_5",
      type: "fib",
      text: "Fill in: In JWT, the three parts are Header, Payload, and ______.",
      answer: ["signature"]
    },
    {
      id: "hard_fib_6",
      type: "fib",
      text: "Fill in: The mechanism that hoists function declarations to the top of their scope is called ______.",
      answer: ["hoisting"]
    },
    {
      id: "hard_fib_7",
      type: "fib",
      text: "Fill in: The CSS property used to control the wrapping behavior of flex items is flex-______.",
      answer: ["wrap"]
    },
    {
      id: "hard_fib_8",
      type: "fib",
      text: "Fill in: In HTTP caching, the validation token header sent by the server for resources is E____.",
      answer: ["tag", "etag"]
    },
    {
      id: "hard_fib_9",
      type: "fib",
      text: "Fill in: The JavaScript global function used to decode a URI component is decode______Component().",
      answer: ["uri"]
    },
    {
      id: "hard_fib_10",
      type: "fib",
      text: "Fill in: The CSS function used to calculate values dynamically, mixing units (e.g. 100% - 20px), is ______().",
      answer: ["calc"]
    },
    {
      id: "hard_fib_11",
      type: "fib",
      text: "Fill in: The browser storage that persists across sessions and has no expiration date is ______Storage.",
      answer: ["local"]
    },
    {
      id: "hard_fib_12",
      type: "fib",
      text: "Fill in: The CSS selector `:nth-child(______)` matches even elements.",
      answer: ["even", "2n"]
    },
    {
      id: "hard_fib_13",
      type: "fib",
      text: "Fill in: The JavaScript method used to convert an object into a JSON string is JSON.______().",
      answer: ["stringify"]
    },
    {
      id: "hard_fib_14",
      type: "fib",
      text: "Fill in: The HTTP header that enforces connection encryption and restricts browser access to HTTP version is Strict-Transport-______.",
      answer: ["security"]
    },
    {
      id: "hard_fib_15",
      type: "fib",
      text: "Fill in: The CSS property used to control the order of flex items is ______.",
      answer: ["order"]
    }
  ]
};

/**
 * Samples N random elements from an array.
 */
function sample(arr, n) {
  const shuffled = [...arr].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, n);
}

/**
 * Selects 20 MCQs and 5 FIBs randomly and returns client-safe version.
 */
function getQuestionsForSession() {
  const mcqs = sample(QUESTIONS_POOL.mcq, 20);
  const fibs = sample(QUESTIONS_POOL.fib, 5);

  const selected = [...mcqs, ...fibs];

  // Client-safe questions mapping (excluding answers)
  const clientSafe = selected.map((q) => {
    const item = {
      id: q.id,
      text: q.text,
      type: q.type
    };
    if (q.type === "mcq") {
      item.options = q.options;
    }
    return item;
  });

  return {
    questionIds: selected.map((q) => q.id),
    questions: clientSafe
  };
}

/**
 * Retrieves the correct answers for a list of question IDs.
 */
function getCorrectAnswers(questionIds) {
  const answerKey = {};
  
  // Create quick mapping
  const allMap = new Map();
  QUESTIONS_POOL.mcq.forEach(q => allMap.set(q.id, q));
  QUESTIONS_POOL.fib.forEach(q => allMap.set(q.id, q));

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
