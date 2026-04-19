// Geometry primitives for the 3-sphere.

import { qi, qj, qk, unit, qmul, qpow, slerp, SphericalTransform, qscale } from './geo.js';

const PI = Math.PI;

// Reorder from [w,x,y,z] to [x,y,z,w] for the shader
function quatToXYZW(q) {
  return [q[1], q[2], q[3], q[0]];
}

export const Color = {
  Blue:      [0.0, 0.0, 1.0],
  Green:     [0.0, 1.0, 0.0],
  Red:       [1.0, 0.0, 0.0],
  Yellow:    [1.0, 1.0, 0.0],
  Magenta:   [1.0, 0.0, 1.0],
  Cyan:      [0.0, 1.0, 1.0],
  White:     [1.0, 1.0, 1.0],
  LightGray: [0.6, 0.6, 0.6],
  DarkGray:  [0.4, 0.4, 0.4],
  Black:     [0.0, 0.0, 0.0],
};

export function circle(subdivisions = 128, base1 = qi, base2 = qj) {
  const positions = [];
  const step = (2 * PI) / subdivisions;

  for (let idx = 0; idx < subdivisions; idx++) {
    const a1 = idx * step;
    const a2 = (idx + 1) * step;
    // sin(a)*base1 + cos(a)*base2 — quaternion linear combination
    for (const angle of [a1, a2]) {
      const s = Math.sin(angle);
      const c = Math.cos(angle);
      const q = [
        s * base1[0] + c * base2[0],
        s * base1[1] + c * base2[1],
        s * base1[2] + c * base2[2],
        s * base1[3] + c * base2[3],
      ];
      positions.push(...quatToXYZW(q));
    }
  }

  return new Float32Array(positions);
}

function uniformColorArray(count, color) {
  const arr = [];
  for (let i = 0; i < count; i++) {
    arr.push(color[0], color[1], color[2]);
  }
  return new Float32Array(arr);
}

export class AxisSet {
  constructor(subdivisions = 128) {
    this.subdivisions = subdivisions;
    this.posArrays = [];
    this.colArrays = [];
  }

  addAxis(color, base1, base2) {
    this.posArrays.push(circle(this.subdivisions, base1, base2));
    this.colArrays.push(uniformColorArray(this.subdivisions * 2, color));
  }

  addAllAxes() {
    this.addAxis(Color.Red, unit, qi);
    this.addAxis(Color.Green, unit, qj);
    this.addAxis(Color.Blue, unit, qk);
    this.addAxis(Color.Yellow, qi, qj);
    this.addAxis(Color.Magenta, qi, qk);
    this.addAxis(Color.Cyan, qj, qk);
  }

  posArray() {
    return concatFloat32Arrays(this.posArrays);
  }

  colArray() {
    return concatFloat32Arrays(this.colArrays);
  }
}

export class Octahedron {
  constructor(center = new SphericalTransform(), radius = PI, subdivisions = 0,
              colorEven = Color.DarkGray, colorOdd = Color.LightGray) {
    this.posData = [];
    this.colData = [];
    this.subdivisions = subdivisions;
    this.center = center;
    this.radius = radius;
    this.colorEven = colorEven;
    this.colorOdd = colorOdd;

    this.addAllFaces();
  }

  getColor(odd) {
    return odd ? this.colorOdd : this.colorEven;
  }

  addAllFaces() {
    const e = this.radius / PI;
    const c = this.center;

    for (const iSign of [1, -1]) {
      for (const jSign of [1, -1]) {
        for (const kSign of [1, -1]) {
          const p1 = c.transform(qpow(qscale(qi, iSign), e));
          const p2 = c.transform(qpow(qscale(qj, jSign), e));
          const p3 = c.transform(qpow(qscale(qk, kSign), e));
          const odd = iSign * jSign * kSign < 0;
          this.addTiledTriangle(p1, p2, p3, odd, this.subdivisions);
        }
      }
    }
  }

  addTiledTriangle(p1, p2, p3, odd, subdiv) {
    if (subdiv === 0) {
      this.addTriangle(p1, p2, p3, odd);
    } else {
      const mid12 = slerp(p1, p2, 0.5);
      const mid13 = slerp(p1, p3, 0.5);
      const mid23 = slerp(p2, p3, 0.5);
      this.addTiledTriangle(p1, mid12, mid13, odd, subdiv - 1);
      this.addTiledTriangle(p2, mid23, mid12, odd, subdiv - 1);
      this.addTiledTriangle(p3, mid13, mid23, odd, subdiv - 1);
      this.addTiledTriangle(mid12, mid23, mid13, !odd, subdiv - 1);
    }
  }

  addTriangle(a, b, c, odd) {
    const color = this.getColor(odd);
    const va = quatToXYZW(a);
    const vb = quatToXYZW(b);
    const vc = quatToXYZW(c);
    this.posData.push(...va, ...vb, ...vc);
    this.colData.push(
      color[0], color[1], color[2],
      color[0], color[1], color[2],
      color[0], color[1], color[2],
    );
  }

  posArray() {
    return new Float32Array(this.posData);
  }

  colArray() {
    return new Float32Array(this.colData);
  }
}

function concatFloat32Arrays(arrays) {
  let totalLen = 0;
  for (const a of arrays) totalLen += a.length;
  const result = new Float32Array(totalLen);
  let offset = 0;
  for (const a of arrays) {
    result.set(a, offset);
    offset += a.length;
  }
  return result;
}
