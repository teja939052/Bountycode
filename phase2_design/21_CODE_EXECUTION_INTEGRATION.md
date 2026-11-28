# 21 CODE EXECUTION INTEGRATION CONTRACT

**BountyCode — Phase 2B Scope-Completeness Review**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define the contract between BountyCode's backend and the external code execution service (OnlineCompiler.io). This document specifies:

- How code is sent to the external compiler
- How test case results are received and interpreted
- How verdicts are mapped to BountyCode's grading policy
- How evidence is persisted to PostgreSQL
- How secrets (API keys) are managed
- Rate limiting, quota management, and cost control
- Privacy and data handling

This is a design document. No implementation is authorized.

---

## 2. Architecture Overview

```
┌─────────────────┐      HTTPS REST      ┌─────────────────────────┐
│   BountyCode    │ <──────────────────> │   OnlineCompiler.io     │
│   Backend       │      (API calls)     │   External Code Service │
│                 │                      │                         │
│  • API Gateway  │                      │  • /api/run-tests       │
│  • Code Service │                      │  • /api/run-code        │
│  • Auth Service │                      │  • Authentication       │
│  • Metrics      │                      │  • Rate limiting        │
└─────────────────┘                      └─────────────────────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL     │
│   • evidence    │
│   • submissions │
│   • test runs   │
└─────────────────┘
```

---

## 3. External Service Configuration

### 3.1 Service Endpoint

| Field | Value |
|-------|-------|
| Base URL | `https://api.onlinecompiler.io` (to be configured via env var) |
| Authentication | API Key in `Authorization: Bearer <token>` header |
| Timeout | 30 seconds per request |
| Retry Policy | 3 retries with exponential backoff |
| Circuit Breaker | Open after 5 consecutive failures |

### 3.2 API Key Management

| Requirement | Specification |
|-------------|---------------|
| Storage | Stored in environment variable `ONLINE_COMPILER_API_KEY` |
| Exposure | Never exposed to frontend JavaScript |
| Rotation | Rotated quarterly |
| Access | Only backend code_execution service can read |
| Logging | Never logged in plain text |

---

## 4. API Contract

### 4.1 Execute Test Cases (Primary Endpoint)

**Endpoint:** `POST /api/run-tests`

**Request:**

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `source_code` | string | Required | Student's source code |
| `language` | string | Required | `"c"`, `"cpp"`, `"python"`, `"java"` |
| `test_cases` | array | Required | Array of test case objects |
| `timeout_ms` | integer | Required | Global timeout in milliseconds |
| `memory_limit_mb` | integer | Required | Memory limit in MB |

**Test Case Object:**

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `input` | string | Required | Input data for the problem (stdin format) |
| `expected_output` | string | Required | Expected output (stdout format) |
| `test_case_id` | string | Required | Unique test case identifier |

**Example Request:**

```json
{
  "source_code": "def two_sum(nums, target):\n    left = 0\n    right = len(nums) - 1\n    while left < right:\n        s = nums[left] + nums[right]\n        if s == target:\n            return [left, right]\n        elif s < target:\n            left += 1\n        else:\n            right -= 1\n    return None",
  "language": "python",
  "test_cases": [
    {
      "input": "[1, 2, 4, 6, 8]\\n10",
      "expected_output": "[1, 4]",
      "test_case_id": "tc_001"
    },
    {
      "input": "[]\\n5",
      "expected_output": "None",
      "test_case_id": "tc_002"
    }
  ],
  "timeout_ms": 5000,
  "memory_limit_mb": 256
}
```

**Response:**

| Field | Type | Description |
|-------|------|-------------|
| `execution_id` | UUID | Unique execution identifier |
| `status` | string | `"completed"`, `"timeout"`, `"error"` |
| `results` | array | Array of test case results |
| `total_time_ms` | integer | Total execution time |
| `memory_used_kb` | integer | Memory used |

**Test Case Result Object:**

| Field | Type | Description |
|-------|------|-------------|
| `test_case_id` | string | Test case identifier |
| `verdict` | string | `"passed"`, `"failed"`, `"timeout"`, `"runtime_error"` |
| `actual_output` | string | Actual output from execution |
| `expected_output` | string | Expected output |
| `execution_time_ms` | integer | Execution time in milliseconds |
| `error_message` | string | Error message if failed |
| `stderr` | string | Standard error output |

**Example Response:**

```json
{
  "execution_id": "exec_abc123",
  "status": "completed",
  "results": [
    {
      "test_case_id": "tc_001",
      "verdict": "passed",
      "actual_output": "[1, 4]",
      "expected_output": "[1, 4]",
      "execution_time_ms": 45,
      "error_message": null,
      "stderr": ""
    },
    {
      "test_case_id": "tc_002",
      "verdict": "passed",
      "actual_output": "None",
      "expected_output": "None",
      "execution_time_ms": 12,
      "error_message": null,
      "stderr": ""
    }
  ],
  "total_time_ms": 57,
  "memory_used_kb": 10240
}
```

### 4.2 Execute Code (Simple Execution)

**Endpoint:** `POST /api/run-code`

Used for simple code execution without test case comparison.

**Request:**

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `source_code` | string | Required | Student's source code |
| `language` | string | Required | `"c"`, `"cpp"`, `"python"`, `"java"` |
| `input` | string | Required | Input data (stdin format) |
| `timeout_ms` | integer | Required | Maximum execution time |

**Response:**

| Field | Type | Description |
|-------|------|-------------|
| `execution_id` | UUID | Unique execution identifier |
| `status` | string | `"completed"`, `"timeout"`, `"error"` |
| `output` | string | Standard output |
| `stderr` | string | Standard error output |
| `execution_time_ms` | integer | Execution time in milliseconds |
| `memory_used_kb` | integer | Memory used |

---

## 5. Idempotency

### 5.1 Idempotency Key

Each execution request must include an `X-Idempotency-Key` header to prevent duplicate executions.

| Header | Value |
|--------|-------|
| `X-Idempotency-Key` | UUID v4 |

### 5.2 Idempotency Behavior

| Scenario | Behavior |
|----------|----------|
| First request with key | Process normally, return result |
| Repeat request with same key within 24h | Return cached result, do not re-execute |
| Repeat request with different body | Return 409 Conflict |
| Key older than 24h | Process normally, return result |

---

## 6. Rate Limiting & Quota Management

### 6.1 Free Plan Limits

| Metric | Limit |
|--------|-------|
| Requests per month | 100,000 |
| Test cases per request | 32 |
| Timeout per request | 30 seconds |
| Memory per request | 256 MB |

### 6.2 Rate Limit Headers

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Request limit per minute |
| `X-RateLimit-Remaining` | Remaining requests in current window |
| `X-RateLimit-Reset` | Time when rate limit resets (Unix timestamp) |

### 6.3 Rate Limit Exceeded Response

```json
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Try again in 45 seconds.",
  "retry_after_seconds": 45
}
```

### 6.3 Rate Limit Headers

| Header | Value |
|--------|-------|
| `Retry-After` | Seconds to wait before retrying |

---

## 7. Evidence Persistence

### 7.1 Execution Record

Each code execution must be recorded in PostgreSQL:

| Field | Type | Description |
|-------|------|-------------|
| `execution_id` | UUID | Primary key |
| `user_id` | UUID | Student identifier |
| `question_id` | string | Question identifier |
| `skill_id` | string | Canonical skill ID |
| `language` | string | Programming language |
| `source_code` | text | Student's source code |
| `status` | string | `"accepted"`, `"wrong_answer"`, `"timeout"`, `"runtime_error"`, `"compile_error"` |
| `test_cases_passed` | integer | Number of test cases passed |
| `test_cases_total` | integer | Total number of test cases |
| `execution_time_ms` | integer | Total execution time |
| `memory_used_kb` | integer | Memory used |
| `verdict` | string | `"accepted"`, `"wrong_answer"`, `"timeout"`, `"runtime_error"`, `"compile_error"` |
| `created_at` | timestamp | Server timestamp |

### 7.2 Test Case Result Record

Each test case result must be recorded:

| Field | Type | Description |
|-------|------|-------------|
| `test_result_id` | UUID | Primary key |
| `execution_id` | UUID | Foreign key to execution |
| `test_case_id` | string | Test case identifier |
| `verdict` | string | `"passed"`, `"failed"`, `"timeout"`, `"runtime_error"` |
| `actual_output` | string | Actual output |
| `expected_output` | string | Expected output |
| `execution_time_ms` | integer | Execution time |
| `error_message` | string | Error message if failed |
| `stderr` | string | Standard error output |

### 7.3 Idempotency Key Persistence

| Field | Type | Description |
|-------|------|-------------|
| `idempotency_key` | string | Primary key |
| `execution_id` | UUID | Foreign key to execution |
| `created_at` | timestamp | Timestamp when first processed |
| `expires_at` | timestamp | Expiration timestamp (24h) |

---

## 8. Error Handling

### 8.1 External Service Errors

| HTTP Status | Meaning | BountyCode Action |
|-------------|---------|-------------------|
| 200 | Success | Process results normally |
| 400 | Bad Request | Validate request, return error to student |
| 401 | Unauthorized | Check API key, return error |
| 403 | Forbidden | Check API key permissions, return error |
| 429 | Too Many Requests | Return rate limit error to student |
| 500 | Internal Server Error | Retry with exponential backoff |
| 502 | Bad Gateway | Retry with exponential backoff |
| 503 | Service Unavailable | Retry with exponential backoff |
| 504 | Gateway Timeout | Treat as timeout |

### 8.2 Retry Policy

| Failure Type | Retry Count | Backoff |
|--------------|-------------|---------|
| Network error | 3 | Exponential (1s, 2s, 4s) |
| 502 Bad Gateway | 3 | Exponential (1s, 2s, 4s) |
| 503 Service Unavailable | 3 | Exponential (1s, 2s, 4s) |
| 504 Gateway Timeout | 3 | Exponential (1s, 2s, 4s) |
| 429 Rate Limited | 0 | Return rate limit error |
| 401 Unauthorized | 0 | Return authentication error |
| 403 Forbidden | 0 | Return authorization error |

### 8.3 Circuit Breaker

| State | Condition | Action |
|-------|-----------|--------|
| Closed | Normal operation | Process requests normally |
| Open | 5 consecutive failures | Reject all requests, return error |
| Half-Open | After timeout | Allow one request to test recovery |

---

## 8. Timeout Handling

| Timeout Type | Value | Action |
|--------------|-------|--------|
| Request timeout | 30 seconds | Return timeout error to student |
| Execution timeout | Per test case | Mark test case as timeout |
| Connection timeout | 10 seconds | Retry with exponential backoff |
| Read timeout | 25 seconds | Return timeout error to student |

---

## 9. Privacy and Data Handling

### 9.1 Data Flow

```
Student Code → BountyCode Backend → OnlineCompiler.io → Results → BountyCode Backend → PostgreSQL
```

### 9.2 Data Retention

| Data | Retention Period |
|------|-----------------|
| Source code | Pilot duration + 30 days |
| Execution results | Pilot duration + 30 days |
| Test case results | Pilot duration + 30 days |
| Idempotency keys | 24 hours |

### 9.3 Privacy Considerations

- Student code is never logged in plain text to external logging services
- API keys are never logged
- Student PII is never sent to OnlineCompiler.io
- Only source code and input data are sent to the external service

---

## 10. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | API key stored securely (env var, not in code)? | ☐ |
| 2 | API key never exposed to frontend? | ☐ |
| 3 | Idempotency key implemented? | ☐ |
| 4 | Rate limiting handled? | ☐ |
| 5 | Error handling for all HTTP status codes? | ☐ |
| 6 | Retry policy with exponential backoff? | ☐ |
| 7 | Circuit breaker implemented? | ☐ |
| 8 | Timeout handling for all scenarios? | ☐ |
| 9 | Evidence persisted to PostgreSQL? | ☐ |
| 10 | Test case results persisted? | ☐ |
| 11 | Privacy considerations addressed? | ☐ |
| 12 | Data retention policy defined? | ☐ |
| 13 | No student PII sent to external service? | ☐ |
| 14 | No secrets in logs? | ☐ |

---

**End of 21 CODE EXECUTION INTEGRATION CONTRACT**
