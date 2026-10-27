# Task 4 — Engineering Escalation (Simulation)

> **Context:** Vision Bank and the Nora balance endpoint are scenarios from an agent-engineering assessment. No real production incident response or backend modification is represented here.

**Subject:** Vision Bank — Nora Account Balance Service Outage

Hi Engineering Team,

I wanted to flag an ongoing issue with Nora's `check_account_balance` tool. The endpoint is currently returning HTTP 500 errors on every request, which means Nora is unable to retrieve account balances. The exact start time hasn't been confirmed yet, but the issue is still affecting requests.

As a temporary workaround, I've updated Nora's prompt to stop using the failing balance tool. When a customer asks about their balance, Nora explains that the information is temporarily unavailable, avoids providing unverified amounts, and offers other verified bank channels or support options where available. The rest of her customer service workflows can continue as normal.

On the backend, we need to identify the cause of the 500 errors, restore the endpoint, and confirm that it returns accurate and properly authorized balance data. I'd also recommend reviewing the error logs, monitoring, and alerting so we can catch similar problems earlier.

Given the current engineering estimate of 3–6 hours, I'd prioritize investigation now and target recovery within that window, subject to the root cause. Once a fix is deployed, I'd like us to run functional and negative-case tests, verify the returned balance against a trusted source, and monitor error rates before we re-enable balance checks in Nora's prompt.

Please keep me updated on the investigation and let me know when the endpoint is stable enough for retesting.

Thanks for your support.

Best regards,  
Ahmed Almufarriji

---

## Recovery checklist

- [ ] Identify the first confirmed failing request and incident start time
- [ ] Trace HTTP 500s through logs and dependencies
- [ ] Restore `check_account_balance` without weakening authorization checks
- [ ] Verify successful and unsuccessful paths with controlled test accounts
- [ ] Confirm safe error payloads and monitoring alerts
- [ ] Validate the assistant no longer invents balances
- [ ] Re-enable the tool **only after** backend verification
