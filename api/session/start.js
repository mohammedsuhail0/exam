"use strict";

const { createSession, cleanup } = require("../_lib/security");
const { getQuestionsForSession } = require("../_lib/questions");

module.exports = async (req, res) => {
  cleanup();
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const { questionIds, questions } = getQuestionsForSession();
  const session = createSession(questionIds);
  res.status(200).json({
    ok: true,
    sessionId: session.sessionId,
    token: session.token,
    expiresAt: session.expiresAt,
    questions
  });
};
