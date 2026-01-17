# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-11)

**Core value:** Detection accuracy — correctly identifying mouth open/closed states with minimal false positives
**Current focus:** Phase 3 — Mouth Detection Logic

## Current Position

Phase: 6 of 6 (Normalized Mouth Center Coordinates)
Plan: 1 of 1 in current phase
Status: Phase complete
Last activity: 2026-01-17 — Completed 06-01-PLAN.md

Progress: ██████████ 100%

## Performance Metrics

**Velocity:**
- Total plans completed: 5
- Average duration: 3 min
- Total execution time: 0.28 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-foundation-setup | 1 | 7 min | 7 min |
| 02-face-mesh-integration | 1 | 7 min | 7 min |
| 03-mouth-detection-logic | 1 | 1 min | 1 min |
| 05-describe-distance-face-away-from-camera | 1 | 1 min | 1 min |
| 06-normalized-mouth-center-coordinates | 1 | 1 min | 1 min |

**Recent Trend:**
- Last 5 plans: 7, 7, 1, 1, 1 min
- Trend: Steady (recent phases straightforward implementations building on foundation)

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

| Phase | Decision | Rationale |
|-------|----------|-----------|
| 01 | Use opencv-python instead of opencv-contrib-python | Avoid unnecessary modules for lean Raspberry Pi deployment |
| 01 | Specify mediapipe>=0.10.0 | Ensure Face Mesh API compatibility for Phase 2 |
| 02 | Use MediaPipe FaceLandmarker API (new v0.10.31) instead of legacy solutions API | Installed MediaPipe version uses new tasks-based architecture requiring explicit model download |
| 03 | Use absolute pixel distance (20px threshold) instead of normalized coordinates | Absolute pixel distance provides more reliable detection across different face sizes in frame |
| 03 | Implement dual visual feedback: text labels + colored landmark circles | Text provides explicit state while colored circles offer immediate visual confirmation |
| 05 | Use landmarks 234 and 454 for face width measurement | Widest horizontal points of face provide stable metric that inversely correlates with camera distance |
| 05 | Threshold-based distance indicator: CLOSE > 250px, OK 150-250px, FAR < 150px | Provides qualitative zones for optimal user positioning with typical webcam setup |
| 06 | Use landmarks 13 and 14 center point for mouth position | Consistent with mouth detection logic, provides stable center reference |
| 06 | Normalize to [-1, 1] range with screen center at (0, 0) | Intuitive directional control where edges are ±1 and center is origin |

### Deferred Issues

None yet.

### Blockers/Concerns

None yet.

### Roadmap Evolution

- Phase 5 added: describe distance the face is away from the camera
- Phase 6 added: i want to have values mouthx and mouthy to be the center of the mouth relative to the center of the screen (0,0), the range of mouthx and mouthy should be [-1,-1]
- Phase 7 added: use pyserial to send a message of ismouthopen as a boolean to an arduino

## Session Continuity

Last session: 2026-01-17 03:21
Stopped at: Completed 06-01-PLAN.md (Phase 6 complete)
Resume file: None
