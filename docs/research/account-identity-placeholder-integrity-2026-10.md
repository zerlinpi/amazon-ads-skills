# Account identity placeholder integrity

Date: 2026-10-28

## Internal gap

The measurement and realization history projectors accepted whole-label unresolved account identity values such as Unknown, N/A, or padded strings as usable advertiser/account provenance. That could let unresolved identity pass through the merge/projection boundary.

## RED to GREEN

- RED tests: 33463cb2d4adcb2b6637a6b1b750fc2b9bb45b24
- Production fixes: 0c5f680c9191118846dae6e135db84a6c1c5f2fd, 856461f8d1e20a0e80b067ec01f1da574e08c26c2

The tests cover unresolved event identity, padded identity, and a concrete opaque identifier containing a placeholder substring.

## Boundary

This is a read-only provenance consistency check. It does not authenticate Amazon Ads account data, prove connector completeness, or add write/retry/idempotency/reconciliation authority. Missing identity remains missing, never zero or false. No third-party implementation was copied.
