---
phase: 06-normalized-mouth-center-coordinates
plan: 01
subsystem: ui
tags: [opencv, mediapipe, coordinate-transformation, normalization, real-time-display]

# Dependency graph
requires:
  - phase: 03-mouth-detection-logic
    provides: landmarks 13 and 14 for mouth position tracking
  - phase: 05-describe-distance-face-away-from-camera
    provides: multi-metric stacked display pattern at Y-offsets
provides:
  - Normalized mouth center coordinates (mouthX, mouthY) in [-1, 1] range
  - Screen-centered coordinate system with (0,0) at center
  - Real-time mouth position tracking for directional control
affects: [gameplay-integration, cursor-control, position-based-features]

# Tech tracking
tech-stack:
  added: []
  patterns: [coordinate-normalization, screen-space-mapping]

key-files:
  created: []
  modified: [main.py]

key-decisions:
  - "Use landmarks 13 and 14 center point for mouth position (consistent with mouth detection logic)"
  - "Normalize to [-1, 1] range with screen center at (0, 0) for intuitive directional control"
  - "Display at Y-offset 150 following established stacked layout pattern"

patterns-established:
  - "Screen-centered coordinate normalization: (pixel - center) / half_dimension"
  - "Multi-metric display with consistent Y-offsets (30, 60, 90, 120, 150)"

issues-created: []

# Metrics
duration: 1 min
completed: 2026-01-17
---

# Phase 6 Plan 1: Normalized Mouth Center Coordinates Summary

**Mouth center position tracking with normalized [-1, 1] coordinate system, calculated from landmarks 13 and 14 and displayed in real-time**

## Performance

- **Duration:** 1 min
- **Started:** 2026-01-17T03:20:45Z
- **Completed:** 2026-01-17T03:21:37Z
- **Tasks:** 3
- **Files modified:** 1

## Accomplishments

- Calculated mouth center position as average of landmarks 13 and 14
- Normalized coordinates to [-1, 1] range with screen center at (0, 0)
- Real-time display of mouthX and mouthY values with 2 decimal precision
- Maintained all existing functionality (mouth detection, distance metrics)

## Task Commits

Each task was committed atomically:

1. **Task 1: Calculate mouth center coordinates** - `1e182e4` (feat)
2. **Task 2: Normalize coordinates relative to screen center** - `4039a44` (feat)
3. **Task 3: Display normalized mouth coordinates** - `23fc2d1` (feat)

## Files Created/Modified

- `main.py` - Added mouth center calculation, coordinate normalization, and real-time display at Y-offset 150

## Decisions Made

**Coordinate system orientation:**
- Used OpenCV's default coordinate system (top-left origin)
- Y-axis: negative values = up, positive values = down
- Rationale: Consistent with OpenCV conventions, can be inverted if needed for specific use cases

**Display format:**
- 2 decimal places for readability (e.g., X=0.23 Y=-0.45)
- White color for neutral information display
- Rationale: Balances precision with visual clarity

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - straightforward implementation with existing landmark infrastructure.

## Next Phase Readiness

Phase 6 complete. Normalized mouth position tracking ready for integration with gameplay or cursor control systems.

All core mouth detection features now implemented:
- Mouth open/closed detection
- Face distance from camera
- Normalized mouth position relative to screen center

---
*Phase: 06-normalized-mouth-center-coordinates*
*Completed: 2026-01-17*
