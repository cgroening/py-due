# Backend

## API

- [ ] Add pagination to `/users` endpoint @due(2026-04-22)
  Default page size 20, support `limit` and `offset` query params.

- [ ] Write OpenAPI docs for all v2 routes @due(2026-04-30)
  Cover request/response schemas and error codes.

- [x] Remove deprecated `/v1/auth` endpoint @due(2026-04-01)
  Migration guide was published in March.

- [ ] Add rate limiting to public endpoints @due(2026-05-10)
  Use token bucket algorithm, 100 req/min per API key.

- [c] Evaluate GraphQL as alternative to REST @due(2026-03-15)
  Decision made to stay with REST for now.

## Database

- [ ] Migrate to PostgreSQL 16 @due(2026-04-25)
  Test on staging first. Prepare rollback plan.
  @priority(high)

- [ ] Add missing indexes on `events` table @due(2026-04-19)
  Queries over `created_at` and `user_id` are slow in prod.

- [.] Write seed script for local development @due(2026-05-01)
  Cover users, projects, and events with realistic fixtures.

- [x] Drop legacy `sessions` table @due(2026-03-20)
  All sessions now stored in Redis.

## Infrastructure

- [ ] Set up staging environment @due(2026-04-28)
  Mirror prod config, use separate DB instance.

- [ ] Configure log aggregation with Loki @due(nächstes Quartal)
  Replace current ad-hoc log inspection.

- [/] Evaluate moving to managed Kubernetes
  No deadline yet, exploratory work only.
