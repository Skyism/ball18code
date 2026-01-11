# Real-Time Mouth Detection System

## What This Is

A real-time computer vision application that detects when a user's mouth is open using webcam input. The system uses MediaPipe Face Mesh for facial landmark detection and OpenCV for video processing, calculating the distance between specific lip landmarks to determine mouth state with high accuracy.

## Core Value

Detection accuracy — correctly identifying mouth open/closed states with minimal false positives is the most critical requirement. Everything else can be compromised, but detection must be reliable.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Real-time webcam feed processing with OpenCV
- [ ] MediaPipe Face Mesh integration for facial landmark detection
- [ ] Distance calculation between inner top lip (Landmark 13) and inner bottom lip (Landmark 14)
- [ ] Threshold-based mouth state detection (Mouth Aspect Ratio or simple distance threshold)
- [ ] Live video display with visual feedback (lip landmarks drawn on screen)
- [ ] Text overlay showing "MOUTH OPEN" or "MOUTH CLOSED" based on threshold
- [ ] Keyboard control to quit application (press 'q')
- [ ] Clear code comments explaining threshold calculation for easy adjustment
- [ ] Configurable threshold value for different camera setups

### Out of Scope

- Recording or saving video feed — focus is real-time detection only
- Multiple face detection — system handles one face at a time
- Advanced gesture recognition — no yawning detection, smile detection, or other mouth movements beyond open/closed binary state
- GUI configuration interface — threshold adjustment done in code

## Context

This is a focused computer vision project using established libraries (MediaPipe and OpenCV) to demonstrate real-time facial landmark detection and analysis. The user has expertise in Python and computer vision engineering. The specific use of lip landmarks 13 and 14 suggests research into MediaPipe's Face Mesh model structure.

## Constraints

- **Hardware Compatibility**: Must eventually run on Raspberry Pi — performance optimization and ARM architecture compatibility are critical considerations
- **Tech Stack**: Python with mediapipe and opencv-python (cv2) — no flexibility on core libraries
- **Detection Method**: Must use MediaPipe Face Mesh model with specific lip landmarks (13 and 14)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use MediaPipe Face Mesh over other landmark detectors | Industry-standard, accurate, well-documented facial landmark detection | — Pending |
| Threshold-based detection over ML classifier | Simpler, more interpretable, easier to adjust for different users/cameras | — Pending |
| Single face limitation in v1 | Reduces complexity, ensures reliable detection for primary use case | — Pending |
| Raspberry Pi as eventual deployment target | Enables portable, embedded applications; constrains performance requirements | — Pending |

---
*Last updated: 2026-01-11 after initialization*
