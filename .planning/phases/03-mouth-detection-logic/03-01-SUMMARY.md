---
phase: 03-mouth-detection-logic
plan: 01
subsystem: detection-logic
tags: [euclidean-distance, threshold-detection, opencv, real-time-feedback]

# Dependency graph
requires:
  - phase: 02-face-mesh-integration
    provides: Landmarks 13 and 14 tracked and visualized with MediaPipe FaceLandmarker
provides:
  - Euclidean distance calculation between lip landmarks
  - Threshold-based mouth state detection (OPEN/CLOSED)
  - Color-coded real-time visual feedback system
affects: [04-raspberry-pi-optimization]

# Tech tracking
tech-stack:
  added: []
  patterns: [threshold-based-state-detection, color-coded-feedback]

key-files:
  created: []
  modified: [main.py]

key-decisions:
  - "Use absolute pixel distance (20px threshold) instead of normalized coordinates for reliable detection across face sizes"
  - "Implement dual visual feedback: text labels + colored landmark circles"

patterns-established:
  - "Threshold-based detection: MOUTH_OPEN_THRESHOLD constant for tunable state detection"
  - "Color-coding convention: green=CLOSED, red=OPEN for consistent visual feedback"

issues-created: []

# Metrics
duration: 1 min
completed: 2026-01-11
---

# Phase 3 Plan 1: Mouth Detection Logic Summary

**Real-time mouth state detection with Euclidean distance calculation, 20-pixel threshold, and color-coded visual feedback (green=closed, red=open)**

## Performance

- **Duration:** 1 min
- **Started:** 2026-01-11T22:23:58Z
- **Completed:** 2026-01-11T22:25:06Z
- **Tasks:** 3
- **Files modified:** 1

## Accomplishments

- Euclidean distance calculation between landmarks 13 and 14 displayed in real-time
- Threshold-based state detection (OPEN when distance > 20px, CLOSED otherwise)
- Color-coded visual feedback with dual indicators: text labels and landmark circles
- Clean minimal display maintaining real-time performance

## Task Commits

Each task was committed atomically:

1. **Task 1: Calculate and display Euclidean distance** - `70ac976` (feat)
2. **Task 2: Implement threshold-based mouth state detection** - `378d513` (feat)
3. **Task 3: Add color-coded visual feedback** - `91b4cd9` (feat)

**Plan metadata:** (to be committed with docs)

## Files Created/Modified

- `main.py` - Added distance calculation, threshold-based state detection, and color-coded visual feedback system

## Decisions Made

**Use absolute pixel distance instead of normalized coordinates**
- Rationale: Absolute pixel distance (20px threshold) provides more reliable detection across different face sizes in frame compared to normalized percentages

**Dual visual feedback system**
- Rationale: Text labels provide explicit state information while colored landmark circles offer immediate visual confirmation without needing to read text

**Color convention: green=CLOSED, red=OPEN**
- Rationale: Red signals active/alert state (mouth open) while green indicates normal/resting state (mouth closed)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - all tasks completed successfully with expected behavior.

## Next Phase Readiness

Phase 3 complete, ready for Phase 4 (Raspberry Pi Optimization). Mouth state detection working with tunable MOUTH_OPEN_THRESHOLD constant for calibration based on camera setup.

---
*Phase: 03-mouth-detection-logic*
*Completed: 2026-01-11*
