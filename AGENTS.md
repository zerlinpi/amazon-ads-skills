## Realization observed-scope integrity

When a realization event supplies marketplace/profile/entity scope, validate all scope fields even if expected_scope is omitted. Unresolved placeholders and padded values are invalid provenance; an absent scope object remains distinct from an unresolved supplied scope. Do not convert unresolved or missing scope to zero, false, or a usable identity.

null