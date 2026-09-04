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
      id: "hard_multi_1",
      type: "multi_mcq",
      text: "Select ALL headers that directly enhance web application security (Select all that apply):",
      options: [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "Accept-Encoding",
        "User-Agent"
      ],
      answer: ["Content-Security-Policy", "Strict-Transport-Security"]
    },
    {
      id: "hard_multi_2",
      type: "multi_mcq",
      text: "Which of the following JavaScript features introduce block-scoped variables? (Select all that apply):",
      options: [
        "let",
        "const",
        "var",
        "function"
      ],
      answer: ["let", "const"]
    },
    {
      id: "hard_multi_3",
      type: "multi_mcq",
      text: "Which of the following cause JavaScript microtasks to be queued? (Select all that apply):",
      options: [
        "Promise.resolve().then()",
        "queueMicrotask()",
        "setTimeout()",
        "setImmediate()"
      ],
      answer: ["Promise.resolve().then()", "queueMicrotask()"]
    },
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
        "-webkit-font-smoothing",
        "text-rendering",
        "font-variant",
        "font-optical-sizing"
      ],
      answer: "-webkit-font-smoothing"
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
      id: "hard_textarea_1",
      type: "textarea",
      text: "Code Explanation: What is the exact keyword used in JavaScript to export a single default value from an ES module?",
      answer: ["default", "export default"]
    }
  ]
};

function sample(arr, n) {
  const shuffled = [...arr].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, n);
}

function getQuestionsForSession() {
  const mcqs = sample(QUESTIONS_POOL.mcq, 20);
  const fibs = sample(QUESTIONS_POOL.fib, 5);

  const selected = [...mcqs, ...fibs];

  // Client-safe questions mapping
  const clientSafe = selected.map((q) => {
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
    questionIds: selected.map((q) => q.id),
    questions: clientSafe
  };
}

function getCorrectAnswers(questionIds) {
  const answerKey = {};
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
