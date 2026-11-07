# World 2 Browser QA Procedure

## Prerequisites
- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:5173`
- Authenticated session (login first)
- DevTools open for console/network inspection

## Test Matrix

| Lesson | Route | Expected Steps |
|--------|-------|----------------|
| Two Pointers | `/lesson/arrays-1` | story → discover/manipulate → predict → build → transfer → assess → complete |
| Sliding Window | `/lesson/arrays-2` | story → discover/manipulate → predict → build → transfer → assess → complete |
| Hash Map Lookup | `/lesson/arrays-3` | story → discover/manipulate → predict → build → transfer → assess → complete |
| Binary Search | `/lesson/arrays-4` | story → discover/manipulate → predict → build → transfer → assess → complete |
| Arrays Boss | `/lesson/arrays-boss` | story → discover/manipulate → predict → build → transfer → assess → complete |

## Viewport Matrix

| Viewport | Width | Expected |
|----------|-------|----------|
| Small mobile | 390px | No horizontal scroll, readable text, touch targets ≥44px |
| Medium mobile | 430px | Same as above |
| Desktop | 1440px | Full layout, no crowding |

## Per-Lesson Checklist

### 1. Story Phase
- [ ] Title renders
- [ ] Character/NPC renders
- [ ] "Enter the Palace" / Continue button works
- [ ] Transitions smoothly to discover

### 2. Discover Phase
- [ ] Step title and content render
- [ ] **D-01 FIX**: `select-value` interaction renders as buttons
- [ ] Clicking a value selects it (highlighted)
- [ ] "Check Answer" button appears after selection
- [ ] Clicking Check reveals correct/incorrect feedback
- [ ] Correct answer highlights green, incorrect highlights red
- [ ] Explanation text appears after checking
- [ ] Previous/Next buttons navigate between discovery steps
- [ ] Last discovery step shows "Continue" to predict

### 3. Predict Phase
- [ ] Question text renders
- [ ] Code snippet renders (if present)
- [ ] Radio options render
- [ ] Selecting an option highlights it
- [ ] "Check Prediction" button works
- [ ] Feedback shows after check
- [ ] "Continue to Build" advances to build phase

### 4. Build Phase
- [ ] Step title and description render
- [ ] Step counter shows correctly
- [ ] XP badge shows if present
- [ ] **D-07 FIX**: If `is_debug`, buggy code renders in red read-only block above editor
- [ ] Monaco editor renders and is editable
- [ ] Language selector shows Python
- [ ] Hint buttons render and open hints sequentially
- [ ] "Run" button executes code and shows output/error
- [ ] "Submit Solution" button submits to backend
- [ ] Build results render (passed/failed test cases)
- [ ] **D-05 FIX**: Retry limit respects `max_attempts`, not `passing_score`
- [ ] Repair steps appear after failed attempt (if present)
- [ ] "Next Exercise" or "Continue to Challenge" advances correctly

### 5. Transfer Phase
- [ ] Transfer title and description render
- [ ] Signature renders (if present)
- [ ] Monaco editor renders with starter code
- [ ] Hints render and expand
- [ ] "Submit Transfer Challenge" submits to backend
- [ ] Build results render
- [ ] Repair steps appear after failed attempt
- [ ] Retry limit works correctly

### 6. Assessment Phase
- [ ] Assessment title renders
- [ ] "Pass: X%" badge shows threshold
- [ ] Questions render (code_tracing, concept, debug types)
- [ ] Answer inputs render for each question type
- [ ] "Submit Assessment" grades all questions
- [ ] Score displays correctly
- [ ] Pass/fail message shows
- [ ] "Retry Assessment" resets and allows retake
- [ ] "Claim Rewards" appears only when passed

### 7. Complete Phase
- [ ] "Lesson Complete!" header renders
- [ ] Final score displays
- [ ] XP earned displays
- [ ] **D-04 FIX**: "Continue Learning" navigates via router (no full reload)
- [ ] Rewards claimed list shows correctly

### 8. XP and Persistence
- [ ] XP is awarded exactly once per lesson completion
- [ ] Re-submitting completion does not grant more XP
- [ ] Completion persists after page refresh
- [ ] SRS enrollment persists (check backend)

## Mobile-Specific Checks (390px, 430px)

- [ ] No horizontal scroll on any phase
- [ ] Editor height is usable (not cramped)
- [ ] Buttons are ≥44px tall
- [ ] Text is readable without zooming
- [ ] Discovery step buttons stack vertically
- [ ] Build/transfer editor doesn't overflow
- [ ] Assessment questions are readable
- [ ] Primary CTA is visible without scrolling

## Wrong-Answer Path Testing

For each lesson:
1. **Predict**: Select wrong answer → verify feedback shows "Not quite" + explanation
2. **Build**: Submit failing code → verify repair steps appear → verify retry works
3. **Transfer**: Submit failing code → verify repair steps appear → verify retry stops at max_attempts
4. **Assessment**: Answer questions wrong → verify score < threshold → verify "Retry Assessment" works
5. **Debug**: Submit wrong fix → verify feedback shows expected fix

## Backend Verification

```bash
# Check lesson loads
curl -s http://localhost:8000/api/v1/lesson/arrays-1 | jq .lesson_id

# Check build submission
curl -s -X POST http://localhost:8000/api/v1/lesson/arrays-1/build \
  -H "Content-Type: application/json" \
  -d '{"code":"def two_sum(nums, target): pass","function_name":"two_sum","language":"python"}' | jq

# Check transfer submission
curl -s -X POST http://localhost:8000/api/v1/lesson/arrays-1/transfer \
  -H "Content-Type: application/json" \
  -d '{"code":"def max_area(heights): pass","function_name":"max_area","language":"python"}' | jq

# Check prediction
curl -s -X POST http://localhost:8000/api/v1/lesson/arrays-1/predict \
  -H "Content-Type: application/json" \
  -d '{"answer":"wrong"}' | jq

# Check assessment
curl -s -X POST http://localhost:8000/api/v1/lesson/arrays-1/assess \
  -H "Content-Type: application/json" \
  -d '{"answers":{}}' | jq

# Check completion
curl -s -X POST http://localhost:8000/api/v1/lesson/arrays-1/complete \
  -H "Content-Type: application/json" \
  -d '{"score":100,"time_spent_seconds":60}' | jq
```

## Evidence to Capture

For each lesson, capture:
1. Screenshot of each phase (story, discover, predict, build, transfer, assess, complete)
2. API response from `/api/v1/lesson/{slug}`
3. API response from `/build`, `/transfer`, `/predict`, `/assess`, `/complete`
4. Any console errors
5. Any network errors
6. Mobile screenshots at 390px and 430px

## Pass Criteria

- All 5 lessons complete without crashes
- All 7 phases render correctly
- D-01 fix verified: select-value buttons appear and work
- D-04 fix verified: no full page reload on completion
- D-05 fix verified: transfer retry respects max_attempts
- D-06 fix verified: debug grading accepts normalized code
- D-07 fix verified: buggy code visible in debug steps
- D-08 fix verified: no horizontal overflow at 390px/430px
- XP awarded exactly once
- Completion persists after refresh
- No console errors during normal flow
