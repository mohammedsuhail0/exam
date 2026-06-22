"use strict";

const {
  verifySessionToken,
  consumeNonce,
  cleanup
} = require("../_lib/security");

const { QUESTIONS_POOL } = require("../_lib/questions");

function normalizeText(v) {
  return String(v || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, " ");
}

module.exports = async (req, res) => {
  cleanup();
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const auth = req.headers.authorization || "";
  const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  const payload = verifySessionToken(token);
  if (!payload) {
    res.status(401).json({ error: "Invalid session token" });
    return;
  }

  const body = req.body || {};
  const nonce = String(body.nonce || "");
  if (!nonce || nonce.length < 10) {
    res.status(400).json({ error: "Invalid nonce" });
    return;
  }
  if (!consumeNonce(payload.sessionId, nonce)) {
    res.status(409).json({ error: "Replay detected" });
    return;
  }

  const mcqAnswers = body.mcqAnswers || {};
  const fibAnswers = body.fibAnswers || {};

  const questionIds = payload.questionIds || [];
  if (!Array.isArray(questionIds) || questionIds.length === 0) {
    res.status(400).json({ error: "Invalid session token: missing questions context" });
    return;
  }

  // Map all pool questions for fast lookup
  const allMap = new Map();
  QUESTIONS_POOL.mcq.forEach(q => allMap.set(q.id, q));
  QUESTIONS_POOL.fib.forEach(q => allMap.set(q.id, q));

  const results = [];
  let correct = 0;
  let wrong = 0;

  for (const id of questionIds) {
    const q = allMap.get(id);
    if (!q) continue;

    if (q.type === "mcq") {
      const given = String(mcqAnswers[id] || "");
      const expected = q.answer;
      const isCorrect = given === expected;
      results.push({
        id,
        type: "mcq",
        correct: isCorrect,
        expected,
        given
      });
      if (isCorrect) correct += 1;
      else wrong += 1;
    } else if (q.type === "fib") {
      const given = String(fibAnswers[id] || "");
      const accepted = q.answer;
      const normalizedGiven = normalizeText(given);
      const isCorrect = accepted.some((ans) => normalizeText(ans) === normalizedGiven);
      results.push({
        id,
        type: "fib",
        correct: isCorrect,
        expected: accepted[0],
        given
      });
      if (isCorrect) correct += 1;
      else wrong += 1;
    }
  }

  const total = correct + wrong;
  const scorePercent = total > 0 ? Math.round((correct / total) * 100) : 0;

  res.status(200).json({
    ok: true,
    sessionId: payload.sessionId,
    receivedAt: new Date().toISOString(),
    grading: {
      total,
      correct,
      wrong,
      scorePercent,
      results
    }
  });
};
