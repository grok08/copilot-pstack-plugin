---
name: make-bot-ui
description: Build a local web UI that sends requests to an existing, user-provided webhook endpoint. Use when a page or dashboard should trigger an external service.
---

# Build a webhook UI

Copilot does not provide Cursor's webhook routines or a secure credential-request tool. Do not invent a Copilot webhook URL or claim to create a routine. This skill can connect a UI to an endpoint and service the user already configured.

## Confirm the integration

Ask which external service receives the request and use its documentation for the endpoint, authentication, request shape, response, rate limits, and test mode. If no endpoint exists, explain that it must be provisioned through that service; do not imply Copilot can create it.

Do not ask the user to paste a secret into chat. Have them configure credentials directly in the local environment or an OS secret manager. Read them only in the server process, keep secret files out of version control, and redact credentials from logs and errors. Never put a key in browser code.

## Build the UI and server

Keep the webhook call on the local server. The browser sends a small, validated JSON payload to that server, which then makes the provider-specific request. Follow the provider's documented authentication and response contract; do not assume an authorization header, a success status, or that a successful HTTP response wakes a bot.

Bind to loopback by default. Expose the server to a tailnet or other network only when the user asks for remote access, and use that network provider's documented setup for the current OS. Do not install software or change network access as an unrequested prerequisite.

Set a bounded timeout. Retry only when the provider supports a safe idempotency mechanism. If delivery must survive an outage, persist a minimal queue locally and document how it is drained. Do not log secret-bearing request headers or bodies.

## Verify delivery

Use the provider's test mode or a harmless payload if available. Confirm the server response and the provider-side effect before saying the UI is live. If no safe test path exists, stop before sending a real request and explain what confirmation is needed.
