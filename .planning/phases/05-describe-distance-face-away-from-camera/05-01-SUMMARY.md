---
phase: 05-describe-distance-face-away-from-camera
plan: 01
subsystem: ui
tags: [opencv, mediapipe, face-landmarks, distance-detection, calibration]

# Dependency graph
requires:
  - phase: 03-mouth-detection-logic
    provides: Face landmark detection, pixel-based measurements, visual feedback patterns
provides:
  - Face width calculation using landmarks 234 and 454
  - Real-time distance metric (face width in pixels)
  - Qualitative distance indicator (CLOSE/OK/FAR)
  - Color-coded calibration feedback
affects: [04-raspberry-pi-optimization, debugging, threshold-tuning]

# Tech tracking
tech-stack:
  added: []
  patterns: [face-width-measurement, threshold-based-indicators, multi-metric-display]

key-files:
  created: []
  modified: [main.py]

key-decisions:
  - "Use landmarks 234 and 454 for face width (widest points of face)"
  - "Use absolute pixel distance (inverse correlation with camera distance)"
  - "Threshold-based indicators: CLOSE > 250px, OK 150-250px, FAR < 150px"
  - "Color-code distance indicator: green for OK, red for suboptimal"

patterns-established:
  - "Multi-metric display pattern: stacked text at consistent Y-offsets (30, 60, 90, 120)"
  - "Qualitative indicators with color coding for user guidance"

issues-created: []

# Metrics
duration: 1 min
completed: 2026-01-11
---

# Phase 5 Plan 1: Face Distance Metric Summary

**Face width measurement with CLOSE/OK/FAR indicator provides real-time calibration feedback for optimal mouth detection positioning**

## Performance

- **Duration:** 1 min
- **Started:** 2026-01-11T22:33:28Z
- **Completed:** 2026-01-11T22:34:20Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments

- Face width calculation using landmarks 234 (left boundary) and 454 (right boundary)
- Real-time face width display showing pixel distance between face boundaries
- Qualitative distance indicator (CLOSE/OK/FAR) with threshold-based classification
- Color-coded visual feedback: green for optimal range (150-250px), red for suboptimal (too close or too far)
- Enhanced calibration feedback helps users position themselves at optimal distance for reliable mouth detection

## Task Commits

Each task was committed atomically:

1. **Task 1: Calculate face width metric from landmarks** - `15ac238` (feat)
2. **Task 2: Display face distance metric with visual indicator** - `e237e53` (feat)

## Files Created/Modified

- `main.py` - Added face width calculation using landmarks 234/454, distance indicator with thresholds (CLOSE > 250px, OK 150-250px, FAR < 150px), color-coded display at (10, 90) and (10, 120)

## Decisions Made

**1. Use landmarks 234 and 454 for face width**
- Rationale: These represent the widest horizontal points of the face (left and right boundaries), providing stable measurement that inversely correlates with camera distance

**2. Use absolute pixel distance instead of normalized coordinates**
- Rationale: Consistent with mouth distance measurement pattern established in Phase 3, easier to interpret and tune

**3. Threshold values: CLOSE > 250px, OK 150-250px, FAR < 150px**
- Rationale: Estimated thresholds for typical webcam setup, provide qualitative feedback zones for user positioning

**4. Color-code distance indicator: green for OK, red for CLOSE/FAR**
- Rationale: Follows established color convention from Phase 3 (green=normal, red=alert), provides immediate visual feedback about optimal positioning

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## Next Phase Readiness

Phase 5 complete. Face distance metric provides real-time calibration feedback showing whether user is at optimal distance for mouth detection. Enhanced debugging capabilities ready for Phase 4 (Raspberry Pi Optimization) where performance tuning and threshold adjustment may benefit from this metric.

All existing functionality preserved:
- Mouth detection working with 20px threshold
- State display (OPEN/CLOSED) with color coding
- Landmark visualization
- Real-time video processing

Ready to proceed with Raspberry Pi optimization with enhanced diagnostic information.

---
*Phase: 05-describe-distance-face-away-from-camera*
*Completed: 2026-01-11*
