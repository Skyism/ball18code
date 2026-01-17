# Discovery: OpenCV-Based Mouth Detection

## Research Question

What are the best approaches to replace MediaPipe Face Mesh with OpenCV-only solutions for real-time mouth detection?

## Approaches Identified

### Approach 1: OpenCV Facemark API (opencv-contrib-python)

**What it is**: OpenCV's native facial landmark detection API with implementations like FacemarkLBF and FacemarkKazemi.

**How it works**:
1. Use Haar Cascade or HOG for initial face detection
2. Load pre-trained Facemark model (lbfmodel.yaml)
3. Apply facemark.fit() to get 68 facial landmarks
4. Access mouth via landmarks [48-68]

**Pros**:
- Pure OpenCV solution (no external dependencies beyond opencv-contrib-python)
- 68-point landmark model provides precise mouth landmarks
- Good performance for real-time applications
- Official OpenCV implementation

**Cons**:
- Requires opencv-contrib-python instead of opencv-python (larger install)
- Requires downloading separate model file (lbfmodel.yaml ~60MB)
- Python bindings added in 2019, less mature than MediaPipe
- More complex setup than Haar cascades alone

**Performance**: Real-time capable on Raspberry Pi with optimization

### Approach 2: Haar Cascade Classifiers (mouth-specific)

**What it is**: OpenCV's classical computer vision approach using pre-trained Haar cascades for direct mouth detection.

**How it works**:
1. Use haarcascade_frontalface_default for face detection
2. Use haarcascade_mcs_mouth for mouth region detection within face
3. Calculate mouth bounding box dimensions
4. Use height/width ratio as proxy for open/closed state

**Pros**:
- Simplest implementation (few lines of code)
- No additional dependencies beyond opencv-python
- No model downloads needed (cascades included with OpenCV)
- Fastest performance (classical CV, no neural networks)
- Well-documented and stable

**Cons**:
- Less precise than landmark-based approaches
- Mouth state detection via bounding box is less accurate than landmark distance
- May struggle with head rotation and lighting variations
- Cannot provide specific lip landmark positions for visualization

**Performance**: Very fast, excellent for Raspberry Pi

### Approach 3: dlib + OpenCV Hybrid

**What it is**: Use dlib's shape_predictor_68_face_landmarks for landmark detection with OpenCV for video handling.

**How it works**:
1. Use dlib's HOG-based face detector or OpenCV Haar cascade
2. Apply dlib's shape predictor to get 68 landmarks
3. Access mouth landmarks [48-68]
4. Calculate distance between upper/lower lip landmarks

**Pros**:
- Most accurate landmark detection
- Well-established library with extensive documentation
- 68-point model matches MediaPipe's landmark approach
- Can extract exact lip positions (inner/outer landmarks)

**Cons**:
- Adds dlib as external dependency (compilation required on some systems)
- Requires downloading shape predictor model (~100MB)
- Slower than Haar cascades (HOG + shape predictor overhead)
- Compilation issues on Raspberry Pi ARM architecture reported by some users

**Performance**: May be challenging on Raspberry Pi, requires optimization

## Recommendation

**Approach 2 (Haar Cascade)** for initial implementation, with **Approach 1 (Facemark API)** as a potential upgrade path.

### Rationale

1. **Simplicity**: Haar cascades require minimal code changes and no additional dependencies
2. **Raspberry Pi compatibility**: Lightest computational load, proven to work well on ARM
3. **No external models**: Cascade files included with OpenCV, no downloads needed
4. **Upgrade path**: If accuracy is insufficient, we can migrate to Facemark API (same opencv-contrib-python package)

### Implementation Strategy

**Phase 1: Haar Cascade Implementation**
- Replace MediaPipe with haarcascade_frontalface_default + haarcascade_mcs_mouth
- Use mouth bounding box aspect ratio for open/closed detection
- Maintain all existing features (distance, coordinates, serial communication)

**Future consideration**: If Haar cascade accuracy proves insufficient, migrate to Facemark API for precise lip landmark tracking.

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Start with Haar Cascades | Simplest, fastest, most compatible with Raspberry Pi |
| Keep opencv-python (not opencv-contrib) | Avoid unnecessary bloat unless Facemark API becomes necessary |
| Use mouth bounding box dimensions | Simpler than landmark distances, sufficient for binary open/closed detection |
| Preserve existing feature set | Distance calculation, normalized coordinates, serial output all remain |

## References

- [OpenCV Facemark API Tutorial](https://learnopencv.com/facemark-facial-landmark-detection-using-opencv/)
- [Face Detection with OpenCV](https://www.datacamp.com/tutorial/face-detection-python-opencv)
- [Detect eyes, nose, lips with dlib](https://pyimagesearch.com/2017/04/10/detect-eyes-nose-lips-jaw-dlib-opencv-python/)
- [Mouth Detection with OpenCV](https://github.com/nishitbohra/Mouth-Detection-System)
- [GSoC 2019 Python Facemark Bindings](https://gist.github.com/saiteja-talluri/1d0e4fc4c75774b936b99c7c52b65fe6)
