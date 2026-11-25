# BountyCode — MongoDB to PostgreSQL Cutover Runbook (Phase 7, PART I)

## Preconditions

1. All PostgreSQL migrations (001-005) applied to target environment
2. Migration engine (`backend/app/scripts/migration/`) tested in dry-run mode
3. UserIdentityMap table empty (will be populated during import)
4. Local Supabase PostgreSQL running and accessible
5. MongoDB source available (read-only for import)
6. Application code deployed with PostgreSQL services (auth, gamification, assessments)
7. Frontend changes staged separately (not part of cutover)

## Backup Requirements

1. **MongoDB full dump** before cutover:
   ```
   mongodump --uri="mongodb://localhost:27017" --db=placementpro --out=/backups/mongodb-pre-cutover-$(date +%Y%m%d)
   ```
2. **PostgreSQL base backup** before cutover:
   ```
   pg_dumpall --host=127.0.0.1 --port=54322 --username=postgres > /backups/postgres-pre-cutover-$(date +%Y%m%d).sql
   ```
3. **Application code** tagged and backed up (Git commit)

## Write-Freeze Strategy

Since MongoDB writes continue during import, a safe cutover requires either:

### Option A: Maintenance Window (Recommended)

1. Stop all application write traffic (maintenance mode)
2. Final MongoDB export
3. Run importer with `--all`
4. Run reconciliation
5. Switch application routes to PostgreSQL
6. Lift maintenance mode

### Option B: Change-Capture (Not Yet Proven)

1. Run initial import
2. Set up MongoDB change streams to capture delta writes
3. Apply deltas to PostgreSQL
4. Switch routes when delta lag is near zero

**Current status:** Option A is the proven approach. Option B requires additional development.

## Final Data Export

```bash
# Export MongoDB collections (read-only)
mongodump --uri="mongodb://localhost:27017" --db=placementpro \
  --collection=users --collection=gamification --collection=gamification_events \
  --collection=skill_graphs --collection=learning_events --collection=coding_challenges \
  --collection=submissions --collection=aptitude_tests --collection=company_mock_tests \
  --collection=oa_sessions --collection=interviews --collection=interview_bookings \
  --collection=interview_chat_sessions --collection=career_profiles --collection=resumes \
  --collection=payments --collection=repair_missions --collection=srs_cards \
  --collection=analytics_events --collection=audit_logs --collection=coupons \
  --out=/backups/mongodb-final-export-$(date +%Y%m%d)
```

## Import Order (Foreign-Key Safe)

1. Users and identity mappings (no dependencies)
2. Gamification profiles (depends on users)
3. Skills and skill prerequisites (no dependencies)
4. Content and assessment metadata (no dependencies)
5. Gamification historical XP events (depends on users + profiles)
6. Learning skill states (depends on users + skills)
7. Learning attempts (depends on users + skills)
8. Learning evidence (depends on learning attempts)
9. Mastery snapshots (depends on learning evidence)
10. SRS cards (depends on users + skills)
11. Repair missions (depends on users + skills)
12. Assessment definitions and variants (no dependencies)
13. Assessment attempts and sections (depends on users + assessment definitions)
14. Responses (depends on assessment attempts)
15. Coding submissions (depends on users)
16. Execution results (depends on coding submissions)
17. OA sessions (depends on users)
18. Interviews (depends on users)
19. Company assessment metadata (no dependencies)
20. Career profiles (depends on users)
21. Resume and uploaded-file metadata (depends on users)
22. Analytics and audit records (depends on users)

## Import Commands

```bash
# Dry-run (validate without writes)
python -m app.scripts.migration run --dry-run --all

# Import specific domain
python -m app.scripts.migration run --domain identity

# Import all domains
python -m app.scripts.migration run --all

# Resume after interruption
python -m app.scripts.migration run --domain <domain>  (checkpoint auto-resumes)

# Clear checkpoint and restart domain
python -m app.scripts.migration run --checkpoint-clear <domain>
```

## Reconciliation Thresholds

| Metric | Threshold | Action if Exceeded |
|--------|-----------|-------------------|
| Source vs imported count match | 100% required | Investigate mismatches |
| Failed imports | 0 required | Fix and retry |
| Quarantined records | Review each | Determine if data is salvageable |
| Duplicate imports | 0 expected | Check idempotency keys |
| XP totals reconciliation | ±5% acceptable | Manual review |

## Route Switching

Routes are switched by deploying application code that uses PostgreSQL services:

| Route File | Before (Motor) | After (PostgreSQL) | Status |
|------------|---------------|-------------------|--------|
| `routes/auth.py` | `users_collection` | `PostgresAuthService` | ✅ Switched |
| `routes/coding.py` | `coding_challenges_collection` | `PostgresAssessmentService` | ✅ Switched |
| `routes/aptitude_tests.py` | `aptitude_tests_collection` | `PostgresAssessmentService` | ⏳ Pending |
| `routes/interview.py` | `interviews_collection` | `PostgresAssessmentService` | ⏳ Pending |
| `routes/oa.py` | `oa_sessions_collection` | `PostgresAssessmentService` | ⏳ Pending |
| `routes/company_mocks.py` | `company_mock_tests_collection` | `PostgresAssessmentService` | ⏳ Pending |
| `routes/resume.py` | `resumes_collection` | PostgreSQL `resumes` table | ⏳ Pending |

## Identity Verification

After import, verify:
1. `UserIdentityMap` has entries for all migrated users
2. `users.email` is unique and matches MongoDB source
3. `gamification_profiles.user_id` resolves to a valid `users.id`
4. JWT tokens issued after cutover contain PostgreSQL UUIDs

## Authentication/Session Handling

1. **Do not import old refresh-token sessions** as active sessions
2. Users receive fresh sessions after cutover (they must log in again)
3. JWT_SECRET must be the same across pre- and post-cutover (or all sessions invalidated)
4. `refresh_jti` column on `users` table tracks current refresh token per user

## Monitoring

Monitor during and after cutover:
- Application error rates (5xx errors)
- Database connection pool usage
- Query latency (P95, P99)
- XP reconciliation (profile totals vs ledger totals)
- User login success rate

## Rollback

See `docs/migration/mongodb-postgres-rollback.md`.

## MongoDB Retention

MongoDB is retained read-only for 30 days post-cutover for reference. No writes to MongoDB after route switching.
