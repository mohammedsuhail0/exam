"use strict";

const crypto = require("crypto");

const SESSION_TTL_MS = 30 * 60 * 1000;
const NONCE_TTL_MS = 10 * 60 * 1000;
const MAX_AUDIT_EVENTS = 2000;

const STORE = global.__secureExamStore || {
  usedNonces: new Map(),
  auditEvents: []
};
global.__secureExamStore = STORE;

function getSecret() {
  return process.env.EXAM_SIGNING_SECRET || "dev-only-secret-change-me";
}

function now() {
  return Date.now();
}

function hmac(payload) {
  return crypto.createHmac("sha256", getSecret()).update(payload).digest("base64url");
}

function signSessionToken(data) {
  const body = Buffer.from(JSON.stringify(data)).toString("base64url");
  const sig = hmac(body);
  return `${body}.${sig}`;
}

function verifySessionToken(token) {
  const [body, sig] = String(token || "").split(".");
  if (!body || !sig) return null;
  const expected = hmac(body);
  if (!crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) {
    return null;
  }
  try {
    const parsed = JSON.parse(Buffer.from(body, "base64url").toString("utf8"));
    if (!parsed || !parsed.sessionId || !parsed.exp) return null;
    if (parsed.exp < now()) return null;
    return parsed;
  } catch (_) {
    return null;
  }
}

function createSession(questionIds = []) {
  const sessionId = crypto.randomUUID();
  const issuedAt = now();
  const exp = issuedAt + SESSION_TTL_MS;
  const token = signSessionToken({ sessionId, issuedAt, exp, version: 1, questionIds });
  return { sessionId, token, expiresAt: exp };
}

function addAuditEvent(event) {
  STORE.auditEvents.push(event);
  if (STORE.auditEvents.length > MAX_AUDIT_EVENTS) {
    STORE.auditEvents.shift();
  }
}

function consumeNonce(sessionId, nonce) {
  const key = `${sessionId}:${nonce}`;
  const existing = STORE.usedNonces.get(key);
  if (existing && existing > now()) return false;
  STORE.usedNonces.set(key, now() + NONCE_TTL_MS);
  return true;
}

function cleanup() {
  const t = now();
  for (const [nonce, exp] of STORE.usedNonces.entries()) {
    if (exp < t) STORE.usedNonces.delete(nonce);
  }
}

module.exports = {
  createSession,
  verifySessionToken,
  addAuditEvent,
  consumeNonce,
  cleanup
};
