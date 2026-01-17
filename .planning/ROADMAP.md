# Roadmap: Real-Time Mouth Detection System

## Overview

This roadmap takes us from initial Python environment setup through to a production-ready mouth detection system optimized for Raspberry Pi deployment. We start by establishing the foundation with OpenCV webcam integration, then layer in MediaPipe Face Mesh for landmark detection, implement the core mouth state detection logic, and finally optimize performance for embedded ARM hardware.

## Domain Expertise

None

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundation Setup** - Environment, dependencies, and basic webcam feed (Completed 2026-01-11)
- [x] **Phase 2: Face Mesh Integration** - MediaPipe landmark detection and visualization (Completed 2026-01-11)
- [x] **Phase 3: Mouth Detection Logic** - Distance calculation and threshold-based state detection (Completed 2026-01-11)
- [ ] **Phase 4: Raspberry Pi Optimization** - Performance tuning for ARM deployment
- [x] **Phase 5: Describe Distance Face Away From Camera** - Display face distance from camera for calibration and debugging (Completed 2026-01-11)
- [x] **Phase 6: Normalized Mouth Center Coordinates** - Calculate mouth center position relative to screen center with normalized range [-1, 1] (Completed 2026-01-17)
- [ ] **Phase 7: Arduino Serial Communication** - Use pyserial to send mouth open state as boolean to Arduino

## Phase Details

### Phase 1: Foundation Setup
**Goal**: Establish Python environment with required dependencies and verify basic webcam capture and display functionality
**Depends on**: Nothing (first phase)
**Research**: Unlikely (standard Python setup, established libraries)
**Status**: Complete
**Completed**: 2026-01-11

Plans:
- [x] 01-01: Python environment setup and basic webcam capture - 7 min

### Phase 2: Face Mesh Integration
**Goal**: Integrate MediaPipe Face Mesh model to detect facial landmarks in real-time and visualize specific lip landmarks (13 and 14) on the video feed
**Depends on**: Phase 1
**Research**: Likely (MediaPipe Face Mesh landmark indices, API usage patterns)
**Research topics**: MediaPipe Face Mesh landmark mapping (specifically landmarks 13 & 14), initialization parameters, performance settings for real-time processing
**Status**: Complete
**Completed**: 2026-01-11

Plans:
- [x] 02-01: MediaPipe Face Landmarker integration with landmark visualization - 7 min

### Phase 3: Mouth Detection Logic
**Goal**: Implement Euclidean distance calculation between lip landmarks and threshold-based mouth state detection with clear visual feedback
**Depends on**: Phase 2
**Research**: Unlikely (mathematical distance calculation, threshold tuning is experimental)
**Status**: Complete
**Completed**: 2026-01-11

Plans:
- [x] 03-01: Distance calculation and threshold-based state detection with visual feedback - 1 min

### Phase 4: Raspberry Pi Optimization
**Goal**: Optimize code for ARM architecture and resource-constrained environments to ensure smooth real-time performance on Raspberry Pi
**Depends on**: Phase 3
**Research**: Likely (ARM-specific optimizations, resource constraints)
**Research topics**: MediaPipe on Raspberry Pi (ARM compatibility and installation), OpenCV performance tuning for ARM, camera interface compatibility, frame rate optimization strategies
**Plans**: TBD

Plans: (To be determined during phase planning)

### Phase 5: Describe Distance Face Away From Camera
**Goal**: Display face distance from camera for calibration and debugging
**Depends on**: Phase 3
**Research**: Unlikely (extending existing landmark measurement patterns)
**Status**: Complete
**Completed**: 2026-01-11

Plans:
- [x] 05-01: Face width calculation and distance indicator with threshold-based feedback - 1 min

### Phase 6: Normalized Mouth Center Coordinates
**Goal**: Calculate mouth center position (mouthX, mouthY) relative to screen center (0,0) with normalized range [-1, 1]
**Depends on**: Phase 3
**Research**: Unlikely (coordinate transformation and normalization)
**Status**: Complete
**Completed**: 2026-01-17

Plans:
- [x] 06-01: Calculate and display normalized mouth center coordinates - 1 min

### Phase 7: Arduino Serial Communication
**Goal**: Use pyserial to send mouth open state as boolean to Arduino
**Depends on**: Phase 3
**Research**: Unlikely (standard serial communication library)
**Plans**: 0 plans

Plans:
- [ ] TBD (run /gsd:plan-phase 7 to break down)

**Details:**
[To be added during planning]

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation Setup | 1/1 | Complete | 2026-01-11 |
| 2. Face Mesh Integration | 1/1 | Complete | 2026-01-11 |
| 3. Mouth Detection Logic | 1/1 | Complete | 2026-01-11 |
| 4. Raspberry Pi Optimization | 0/? | Not started | - |
| 5. Describe Distance Face Away From Camera | 1/1 | Complete | 2026-01-11 |
| 6. Normalized Mouth Center Coordinates | 1/1 | Complete | 2026-01-17 |
| 7. Arduino Serial Communication | 0/? | Not started | - |
