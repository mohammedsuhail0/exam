"use strict";

const {
  verifySessionToken,
  addAuditEvent,
  cleanup
} = require("./_lib/security");

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

  const event = req.body || {};
  const normalized = {
    sessionId: payload.sessionId,
    ts: event.ts || new Date().toISOString(),
    type: event.type || "unknown",
    confidence: event.confidence || "low",
    details: event.details || {}
  };

  addAuditEvent(normalized);

  res.status(200).json({ ok: true });
};
