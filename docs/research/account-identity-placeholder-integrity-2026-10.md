# Account identity placeholder integrity

Date: 2026-10-28

## Internal gap

The measurement and realization history projectors accepted whole-label unresolved account identity values such as Unknown, N/A, or padded strings as usable advertiser/account provenance. That could let unresolved identity pass through the merge/projection boundary.

## RED to GREEN

- RED tests: 2577f1218a37b94fc681dc65bf02a505829f0896
- Production fixes: 0778b6cf357602f033a0d2e3903e929fd1563c82, 9ef024de3db31a512937db45bdac5cfdc7ccc3d4

The tests cover unresolved event identity, padded identity, and a concrete opaque identifier containing a placeholder substring.

## Boundary

This is a read-only provenance consistency check. It does not authenticate Amazon Ads account data, prove connector completeness, or add write/retry/idempotency/reconciliation authority. Missing identity remains missing, never zero or false. No third-party implementation was copied.
