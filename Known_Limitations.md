# Known Limitations

## Runtime Limitations

- Some optional backend endpoints return 404 in the live production browser session.
- The browser console is not clean during the full workflow traversal.
- Live ECS, ALB, and CloudWatch operational metrics were not directly queryable from this workspace.

## Security Limitations

- The reviewed code paths did not show a dedicated HSTS or CSP policy.
- Secret handling appears reasonable in the repository evidence, but live secret store validation was not performed here.

## Product Limitations

- The platform is optimized for a guided judge demo rather than uncontrolled public traffic.
- Fallbacks preserve the workflow, but they also mask some missing supporting data paths.

## Release Impact

These limitations are non-blocking for the demo experience, but they keep the final release status below GREEN.
