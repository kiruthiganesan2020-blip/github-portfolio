# Detailed Edge Cases: AI-Powered Restaurant Recommendation System

This document lists important edge cases for each project phase, along with expected handling behavior.  
Use this as a validation checklist during development, QA, and demo preparation.

## Phase 1: Foundation and Data Pipeline (Ingestion + Preprocessing)

### Data Source and Availability
- **Dataset URL unavailable or timeout**
  - **Risk**: Pipeline fails at startup.
  - **Expected Handling**: Retry with backoff, surface clear error, and support local cached snapshot.
- **Dataset schema changes unexpectedly**
  - **Risk**: Missing expected columns (`location`, `cuisine`, etc.).
  - **Expected Handling**: Schema validation step with explicit failure message and mapping fallback.
- **Partial/corrupted download**
  - **Risk**: Silent bad data.
  - **Expected Handling**: File checksum/row-count sanity checks before processing.

### Data Quality
- **Missing values in critical fields (`name`, `location`, `rating`)**
  - **Risk**: Broken filtering or poor recommendations.
  - **Expected Handling**: Impute or drop based on rule priority; log dropped row counts.
- **Invalid numeric formats (`rating="N/A"`, `cost="₹₹"`)**
  - **Risk**: Comparison errors.
  - **Expected Handling**: Strong parsers with default/null-safe conversion.
- **Out-of-range values (`rating > 5`, negative cost)**
  - **Risk**: Ranking distortion.
  - **Expected Handling**: Clamp or exclude invalid records and log anomalies.
- **Duplicate restaurants with slight name variants**
  - **Risk**: Repeated recommendations.
  - **Expected Handling**: Deduplicate by normalized name + location keys.
- **Encoding and character issues (special symbols, multilingual names)**
  - **Risk**: Parse failures or garbled output.
  - **Expected Handling**: UTF-8 normalization and sanitization.

---

## Phase 2: User Preference Collection Layer

### Input Validation
- **User provides empty input for required fields**
  - **Risk**: Broad or meaningless recommendations.
  - **Expected Handling**: Prompt user for required values or apply explicit defaults.
- **Invalid budget value (for example `ultra-low`)**
  - **Risk**: Filter mismatch.
  - **Expected Handling**: Strict enum validation with helpful correction hints.
- **Invalid rating format (`"four"`, `7`, `-1`)**
  - **Risk**: Filter logic errors.
  - **Expected Handling**: Type/range check (0.0 to 5.0) before query execution.
- **User inputs location with typo (`Banglore`)**
  - **Risk**: Zero candidates.
  - **Expected Handling**: Fuzzy match suggestions (`Did you mean Bangalore?`).

### Intent Ambiguity
- **Multiple cuisines in one field (`Italian, Chinese`)**
  - **Risk**: Parser confusion.
  - **Expected Handling**: Split multi-select inputs and apply OR/AND logic explicitly.
- **Conflicting preferences (`budget=low`, `min_rating=4.9`)**
  - **Risk**: No results.
  - **Expected Handling**: Detect conflict and ask to relax one constraint.
- **Unclear additional preference (`nice ambience`)**
  - **Risk**: Non-deterministic filtering.
  - **Expected Handling**: Map to known tags where possible; pass remaining text to LLM context only.

### Security and Robustness
- **Prompt injection-like text in user inputs**
  - **Risk**: LLM behavior manipulation.
  - **Expected Handling**: Treat user input as data, escape/quote values in prompt.
- **Very long free-text preferences**
  - **Risk**: Token bloat and latency.
  - **Expected Handling**: Input length limits + summarization/truncation.

---

## Phase 3: Retrieval and Candidate Generation

### Filter Result Extremes
- **No restaurants match strict filters**
  - **Risk**: Empty final response.
  - **Expected Handling**: Progressive relaxation strategy (rating -> budget -> cuisine), with disclosure.
- **Too many matches (thousands)**
  - **Risk**: Slow processing and oversized prompts.
  - **Expected Handling**: Pre-rank and cap candidates (top 10-20) before LLM.
- **Only one match available**
  - **Risk**: Weak recommendation diversity.
  - **Expected Handling**: Return it with alternatives from nearby constraints.

### Matching Logic
- **Cuisine string mismatch (`North Indian` vs `North-Indian`)**
  - **Risk**: False negatives.
  - **Expected Handling**: Normalize tokens (case, punctuation, synonyms).
- **Location hierarchy mismatch (city vs locality)**
  - **Risk**: Missed candidates.
  - **Expected Handling**: Support city-level fallback when locality has no hits.
- **Budget bracket boundaries (`cost` exactly on threshold)**
  - **Risk**: Inconsistent inclusion.
  - **Expected Handling**: Define inclusive boundary rules and keep consistent across code.

### Ranking Before LLM
- **All candidates have identical scores**
  - **Risk**: Arbitrary ordering.
  - **Expected Handling**: Add deterministic tie-breakers (rating, review count, name).
- **Missing features needed for pre-ranking**
  - **Risk**: Biased candidate shortlist.
  - **Expected Handling**: Null-safe scoring with feature availability penalties.

---

## Phase 4: LLM Recommendation and Reasoning Engine

### Prompt and Context Issues
- **Prompt exceeds token limit**
  - **Risk**: Truncation or API failure.
  - **Expected Handling**: Candidate cap, compact context format, dynamic truncation policy.
- **Context missing key fields for some candidates**
  - **Risk**: Poor explanations or wrong ranking.
  - **Expected Handling**: Fill unknown fields as `Not available`; ask LLM not to invent values.

### LLM Output Reliability
- **LLM recommends restaurants not present in candidate set**
  - **Risk**: Hallucinated results.
  - **Expected Handling**: Post-validation against candidate IDs; regenerate or correct output.
- **LLM ignores user constraints (budget/rating)**
  - **Risk**: Loss of trust.
  - **Expected Handling**: Rule-based post-filter after LLM ranking.
- **LLM response in unexpected format**
  - **Risk**: Parsing failure.
  - **Expected Handling**: Structured output schema + retry with stricter format prompt.
- **Generic explanations repeated for all restaurants**
  - **Risk**: Low personalization quality.
  - **Expected Handling**: Prompt template enforcing item-specific evidence.

### Service Reliability
- **LLM API timeout/rate limit**
  - **Risk**: Failed recommendation request.
  - **Expected Handling**: Retries with jitter, graceful fallback to rule-based ranking.
- **LLM API outage**
  - **Risk**: Complete downtime.
  - **Expected Handling**: Circuit breaker + fallback mode with non-LLM explanations.

---

## Phase 5: Response Presentation Layer

### UI/Output Integrity
- **Missing fields in final response (cost/rating unavailable)**
  - **Risk**: Broken UI components or confusing display.
  - **Expected Handling**: Display safe placeholders like `N/A`.
- **Overly verbose explanation text**
  - **Risk**: Poor readability.
  - **Expected Handling**: Enforce max length per explanation.
- **Duplicate restaurants shown in top N**
  - **Risk**: Lower perceived quality.
  - **Expected Handling**: Deduplicate before rendering.

### User Experience
- **User asks for more options after first list**
  - **Risk**: Repeated same suggestions.
  - **Expected Handling**: Pagination or "show next best" logic with exclusion of already shown IDs.
- **Very slow response in UI**
  - **Risk**: User drop-off.
  - **Expected Handling**: Loading states, partial rendering, latency metrics.
- **No recommendation case**
  - **Risk**: Dead-end UX.
  - **Expected Handling**: Show actionable suggestions to relax filters.

---

## Phase 6: Quality, Evaluation, and Iteration

### Testing and Evaluation
- **Test set not representative (only major cities)**
  - **Risk**: Inflated quality perception.
  - **Expected Handling**: Stratified test scenarios by city size, budget, cuisine mix.
- **Feedback data is sparse or biased**
  - **Risk**: Wrong optimization decisions.
  - **Expected Handling**: Minimum sample thresholds before tuning.
- **Metric conflicts (high relevance but low diversity)**
  - **Risk**: One-dimensional recommendations.
  - **Expected Handling**: Multi-objective evaluation and weighted score policy.

### Drift and Maintenance
- **Restaurant data becomes stale**
  - **Risk**: Inaccurate recommendations over time.
  - **Expected Handling**: Scheduled refresh + freshness monitoring.
- **Prompt changes improve one cohort but hurt others**
  - **Risk**: Regression.
  - **Expected Handling**: A/B testing by segment and rollback-ready prompt versions.

---

## Cross-Cutting Edge Cases (System-Wide)

### Performance
- **High concurrent traffic**
  - **Expected Handling**: Request queueing, caching repeated queries, autoscaling where available.
- **Cold-start latency**
  - **Expected Handling**: Warm-up jobs and model/client connection reuse.

### Observability
- **No logging for failed recommendations**
  - **Expected Handling**: Structured logs with request ID, phase-wise timings, and failure reason.
- **Hard-to-debug ranking outcomes**
  - **Expected Handling**: Store intermediate filter outputs and candidate scores.

### Privacy and Compliance
- **Sensitive user preferences stored without masking**
  - **Expected Handling**: Data minimization and masked logs.
- **Prompt payload contains unnecessary user data**
  - **Expected Handling**: Send only fields needed for ranking and explanation.

### Resilience
- **One phase fails and crashes entire flow**
  - **Expected Handling**: Fail-soft design with phase-level fallbacks.
- **Unexpected exception in parsing/formatting**
  - **Expected Handling**: Global exception handler returning user-safe error messages.

---

## Suggested Priority for Implementation

1. **Critical**: No-result handling, schema validation, hallucination prevention, API failure fallback  
2. **High**: Input validation, deduplication, budget/rating boundary consistency, output formatting checks  
3. **Medium**: Fuzzy matching, explanation quality controls, diversity balancing  
4. **Low**: Advanced personalization tuning and cohort-specific optimization

---

## Ready-to-Use QA Scenarios (Quick Start)

- Query with strict filters that should produce zero results -> verify fallback relaxation.
- Query with typo location -> verify suggestion/correction behavior.
- Query with malicious input text -> verify prompt safety and stable output.
- Query during simulated LLM timeout -> verify rule-based fallback response.
- Query with incomplete dataset rows -> verify no crashes and proper placeholders.
- Query returning many candidates -> verify candidate cap and response latency control.
