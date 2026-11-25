# BountyCode — MongoDB to PostgreSQL Rollback Runbook (Phase 7, PART I)

## When to Rollback

Rollback is triggered when any of the following conditions are met after cutover:

1. Application error rate > 5% for 10+ minutes
2. User login success rate < 95%
3. XP reconciliation mismatch > 10%
4. Data integrity check failures (missing users, broken foreign keys)
5. Critical feature failure (registration, login, coding submission)
6. Reconciliation shows > 1% data loss

## Rollback Steps

### Phase 1: Stop Write Traffic

1. Enable maintenance mode on the application
2. Stop all new writes to both PostgreSQL and MongoDB
3. Drain existing request queue

### Phase 2: Verify MongoDB Integrity

1. Confirm MongoDB is still running and accessible
2. Verify pre-cutover backup is intact:
   ```
   mongorestore --uri="mongodb://localhost:27017" --db=placementpro --drop /backups/mongodb-pre-cutover-<date>
   ```
3. Verify application code can connect to MongoDB

### Phase 3: Revert Application Code

1. Revert to the pre-cutover Git commit (before PostgreSQL route changes):
   ```
   git revert <cutover-commit-sha>
   ```
   Or checkout the pre-cutover branch:
   ```
   git checkout <pre-cutover-branch>
   ```
2. Rebuild and redeploy application
3. Verify application starts and connects to MongoDB

### Phase 4: Verify Application Functionality

1. Test registration endpoint
2. Test login endpoint
3. Test coding submission endpoint
4. Test assessment endpoints
5. Verify user data is accessible from MongoDB

### Phase 5: Lift Maintenance Mode

1. Disable maintenance mode
2. Monitor application for 30 minutes
3. Confirm normal operation

## Data Loss Assessment

After rollback, assess data loss:

1. **Users registered during cutover:** Lost (must re-register)
2. **XP earned during cutover:** Lost (must re-earn)
3. **Assessment results during cutover:** Lost (must re-take)
4. **All data before cutover:** Preserved (MongoDB was not modified)

## Rollback Verification Checklist

- [ ] MongoDB is running and accessible
- [ ] Application connects to MongoDB (not PostgreSQL)
- [ ] Registration works
- [ ] Login works
- [ ] Coding submission works
- [ ] Assessment submission works
- [ ] User data from before cutover is accessible
- [ ] Error rate is < 1%
- [ ] No 5xx errors for 10+ minutes

## Escalation Contacts

- Database administrator: For PostgreSQL/MongoDB issues
- Application team: For route/code issues
- DevOps: For deployment/infrastructure issues
