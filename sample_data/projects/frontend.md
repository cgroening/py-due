# Frontend

## Components

- [ ] Build reusable `DataTable` component @due(2026-04-26)
  Support sorting, filtering and pagination.
  Use existing design tokens for styling.

- [ ] Add dark mode support @due(2026/05/15)
  Respect `prefers-color-scheme`, persist preference in localStorage.

- [x] Replace custom date picker with `react-day-picker` @due(2026-04-05)
  All forms migrated, old component removed.

- [.] Extract `Modal` into shared component library @due(2026-05-01)
  Currently duplicated in 4 places.

## Testing

- [ ] Set up Playwright for end-to-end tests @due(2026-04-30)
  Cover login flow, project creation, and settings page.

- [ ] Increase unit test coverage to 80 % @due(2026-05-20)
  Focus on utility functions and hooks first.

- [c] Migrate from Jest to Vitest @due(2026-04-10)
  Decided against it – Jest is sufficient for now.

## Performance

- [ ] Audit and reduce bundle size @due(2026-05-05)
  Run `webpack-bundle-analyzer`, target < 200 kB gzipped.

- [ ] Lazy-load route components @due(2026-04-29)
  Apply `React.lazy` to all top-level route components.

- [/] Investigate server-side rendering
  No timeline yet. Evaluate Next.js vs. Remix.
