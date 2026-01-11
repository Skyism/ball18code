# Phase 2 Discovery: Face Mesh Integration

**Discovery Level**: Standard Research (Level 2)
**Duration**: ~15 minutes
**Date**: 2026-01-11

## Research Goal

Understand MediaPipe Face Mesh API usage, landmark coordinate system, and identify correct landmarks for mouth open/closed detection (specifically validating landmarks 13 and 14 per project requirements).

## Key Findings

### 1. MediaPipe Face Mesh API

**Initialization Parameters:**
```python
import mediapipe as mp
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,      # Video stream mode (reduces latency)
    max_num_faces=1,               # Single face detection
    refine_landmarks=False,        # Optional iris/lip refinement
    min_detection_confidence=0.5,  # Detection threshold
    min_tracking_confidence=0.5    # Tracking threshold
)
```

**Key Parameters for Real-Time Video:**
- `static_image_mode=False`: Treats input as video stream, detects once then tracks (lower latency)
- `max_num_faces=1`: Matches project requirement (single face)
- `refine_landmarks=False`: Basic 468 landmarks sufficient for mouth detection
- Confidence values: 0.5 is reasonable default, can tune if needed

### 2. Landmark System

**Total Landmarks**: 468 3D face landmarks

**Coordinate Format:**
- `x, y`: Normalized to [0.0, 1.0] by image width/height
- `z`: Relative depth (smaller = closer to camera, origin at head center)
- **To get pixel coordinates**: `pixel_x = landmark.x * image_width`

**Output Access:**
```python
results = face_mesh.process(rgb_frame)
if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        landmark = face_landmarks.landmark[INDEX]
        # landmark.x, landmark.y, landmark.z
```

### 3. Lip Landmark Indices

**Complete Lips (40 landmarks):**
`[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 185, 40, 39, 37, 0, 267, 269, 270, 409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78]`

**Upper Lip:**
`[185, 40, 39, 37, 0, 267, 269, 270, 409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78]`

**Lower Lip:**
`[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]`

**Landmarks 13 and 14 Status:**
- Landmark 13: Present in upper lip array
- Landmark 14: Present in lower lip array
- ✅ **User's landmark choices (13, 14) are valid lip landmarks**

### 4. Mouth Aspect Ratio Patterns

**Established Pattern (from drowsiness detection research):**
Uses multiple vertical distances averaged and divided by horizontal width:

```python
mouth_landmarks = [[61, 291], [39, 181], [0, 17], [269, 405]]
# [horizontal_width], [vertical_N1], [vertical_N2], [vertical_N3]

MAR = (N1 + N2 + N3) / (3 * D)
# Where N1, N2, N3 are vertical distances, D is horizontal width
```

**Specific Pairs:**
- Horizontal (width): 61 ↔ 291
- Vertical N1: 39 ↔ 181
- Vertical N2: 0 ↔ 17
- Vertical N3: 269 ↔ 405

**Alternative: Simple Vertical Distance**
For landmarks 13 ↔ 14 (user requirement):
```python
vertical_distance = euclidean_distance(landmark_13, landmark_14)
threshold = CONFIGURABLE_VALUE
mouth_open = vertical_distance > threshold
```

### 5. Drawing Landmarks

**MediaPipe Drawing Utilities:**
```python
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mp_drawing.draw_landmarks(
    image=frame,
    landmark_list=face_landmarks,
    connections=mp_face_mesh.FACEMESH_TESSELATION,  # Full mesh
    landmark_drawing_spec=None,
    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
)
```

**Custom Landmark Drawing (for specific landmarks like 13, 14):**
```python
h, w, _ = frame.shape
landmark_13 = face_landmarks.landmark[13]
x = int(landmark_13.x * w)
y = int(landmark_13.y * h)
cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
```

## Decisions

| Decision | Rationale |
|----------|-----------|
| Use `static_image_mode=False` | Real-time video requires tracking mode for lower latency |
| Set `max_num_faces=1` | Project requirement, simplifies processing |
| Use `refine_landmarks=False` | 468 base landmarks sufficient for mouth detection |
| Implement simple vertical distance (13↔14) first | Matches user specification, simpler than MAR, can evolve to MAR later if needed |
| Draw only landmarks 13 and 14 initially | Focused visualization per project requirement |

## Implementation Approach

### Phase 2 Scope (This Phase)
1. Initialize MediaPipe Face Mesh with appropriate parameters
2. Integrate face mesh processing into existing OpenCV loop
3. Visualize landmarks 13 and 14 on video feed
4. Verify real-time performance (no distance calculation yet)

### Phase 3 Preview (Next Phase)
- Calculate Euclidean distance between landmarks 13 and 14
- Implement threshold-based detection
- Add "MOUTH OPEN" / "MOUTH CLOSED" text overlay

## Technical Notes

**Performance Considerations:**
- Face Mesh runs at 30+ FPS on modern hardware
- RGB conversion required (OpenCV uses BGR by default)
- Landmark normalization requires image dimensions for pixel drawing

**Common Pitfalls:**
- Forgetting BGR→RGB conversion before processing
- Not checking `if results.multi_face_landmarks` (can be None)
- Using normalized coordinates directly for drawing (need to multiply by dimensions)

## Sources

- [MediaPipe Face Mesh Documentation](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/face_mesh.md)
- [MediaPipe Face Mesh Python API](https://github.com/google-ai-edge/mediapipe/blob/master/mediapipe/python/solutions/face_mesh.py)
- [Face Mesh Landmark Indices (Gist)](https://gist.github.com/Asadullah-Dal17/fd71c31bac74ee84e6a31af50fa62961)
- [Drowsiness Detection with MediaPipe](https://github.com/Tandon-A/Drowsiness-Detection-Mediapipe/blob/main/inference.py)
- [MediaPipe Face Mesh Overview](https://mediapipe.readthedocs.io/en/latest/solutions/face_mesh.html)

---
*Discovery completed: 2026-01-11*
*Ready for planning: Phase 2 can proceed with validated landmark indices and API patterns*
