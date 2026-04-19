# A Spherical World

A demo on how to render spherically curved 3D space (the 3-sphere) with WebGL. Originally written in Python with PyGame and ModernGL (see commit `6c750b4`), later rewritten in JavaScript with vanilla WebGL2 and Vite.

## What is the 3-sphere?

A regular sphere (2-sphere) is a 2D surface curving through 3D space. The 3-sphere is the next step up: a 3D space curving through 4D. Every point is described by a unit quaternion (four numbers satisfying a² + b² + c² + d² = 1). There are no edges or boundaries — if you walk in any direction, you eventually return to where you started, much like walking along a great circle on a globe. This demo lets you explore the inside of such a space.

## Demo

![Screenshot of the spherical rendering demo](demo.png)

### Desktop controls

| Key | Action |
|-----|--------|
| W/S | Pitch (look up/down) |
| A/D | Yaw (look left/right) |
| Q/E | Roll |
| Up/Down | Move forward/backward |
| H | Toggle overlay |

### Mobile controls

- **Drag** to look around
- **On-screen buttons** for roll and forward/backward movement
- **Tap overlay** to toggle it

## Running

```sh
npm ci
npm run dev
```

Then open the displayed URL in a browser.

## What you're seeing

- **Six colored great circles** — the coordinate axes of the 3-sphere. Each circle lies in a different quaternion plane (e.g. the red circle spans 1 and i, the yellow one spans i and j). They serve as a fixed reference frame.
- **Large gray checkerboard sphere** — a geodesic mesh at radius pi from the camera's starting point, built by recursively subdividing an octahedron and projecting onto the 3-sphere. The checkerboard pattern makes the curvature visible.
- **Small colored octahedron** — a simpler mesh (cyan and red faces) placed elsewhere on the 3-sphere, giving you a landmark to navigate toward.

Objects dim as they get farther away on the 3-sphere and are brightest when nearby.

## Rendering pipeline

Each vertex is a unit quaternion (a point on S3). The rendering pipeline has three stages:

1. **Camera transform** — the vertex shader applies an SO(4) isometry using a pair of quaternions `s` and `t`: the transformed point is `s * p * t`. This pair encodes both the camera's position and orientation on the 3-sphere.
2. **Stereographic projection** — the shader maps the 4D point to 3D by dividing `(x, y, z)` by `(w + 1)`, analogous to how you project a globe onto a flat map.
3. **Shading and depth** — the fragment shader dims objects based on their spherical distance from the camera (brightest nearby, darkest at the antipodal point) and writes `gl_FragDepth` as normalized spherical distance for correct z-ordering.

## Further reading

- The [Hyperbolica Devlog playlist](https://www.youtube.com/watch?v=EMKLeS-Uq_8&list=PLh9DXIT3m6N4qJK9GKQB3yk61tVe6qJvA) on YouTube provides a great introduction to hyperbolic and spherical space. Its [third video](https://www.youtube.com/watch?v=pXWRYpdYc7Q&list=PLh9DXIT3m6N4qJK9GKQB3yk61tVe6qJvA&index=4) is a great starting point to the topic of rendering hyperbolic or spherical space.
- Grant Sanderson's and Ben Eater's explorable video series [Visualizing Quaternions](https://eater.net/quaternions/) is very helpful to get an intuitive feeling for quaternions.
- Jeff Weeks' [Topology and Geometry Software](https://www.geometrygames.org/) site provides some cool software to get to know unusual spaces. The [Curved Spaces](https://www.geometrygames.org/CurvedSpaces/index.html) app is the most relevant for the topic of 3-sphere rendering.
