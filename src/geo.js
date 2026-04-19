// Quaternion math for spherical geometry.
// Quaternions stored as [w, x, y, z] arrays.

const PI = Math.PI;

export const unit = [1, 0, 0, 0];
export const qi = [0, 1, 0, 0];
export const qj = [0, 0, 1, 0];
export const qk = [0, 0, 0, 1];

export function qmul(a, b) {
  return [
    a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3],
    a[0]*b[1] + a[1]*b[0] + a[2]*b[3] - a[3]*b[2],
    a[0]*b[2] - a[1]*b[3] + a[2]*b[0] + a[3]*b[1],
    a[0]*b[3] + a[1]*b[2] - a[2]*b[1] + a[3]*b[0],
  ];
}

export function qconj(q) {
  return [q[0], -q[1], -q[2], -q[3]];
}

export function qinv(q) {
  // For unit quaternions, inverse = conjugate
  return qconj(q);
}

export function qneg(q) {
  return [-q[0], -q[1], -q[2], -q[3]];
}

export function qpow(q, e) {
  // q^e for unit quaternion q
  // q = cos(theta) + sin(theta) * axis
  // q^e = cos(e*theta) + sin(e*theta) * axis
  const w = q[0];
  const vx = q[1], vy = q[2], vz = q[3];
  const sinTheta = Math.sqrt(vx*vx + vy*vy + vz*vz);

  if (sinTheta < 1e-10) {
    // Near identity — return identity
    return [1, 0, 0, 0];
  }

  const theta = Math.atan2(sinTheta, w);
  const newTheta = theta * e;
  const s = Math.sin(newTheta) / sinTheta;

  return [
    Math.cos(newTheta),
    vx * s,
    vy * s,
    vz * s,
  ];
}

export function qscale(q, s) {
  return [q[0]*s, q[1]*s, q[2]*s, q[3]*s];
}

export function slerp(start, end, ratio) {
  const startInv = qinv(start);
  return qmul(start, qpow(qmul(startInv, end), ratio));
}

export class SphericalTransform {
  constructor() {
    this.s = [...unit];
    this.t = [...unit];
  }

  applyInner(a, b) {
    this.s = qmul(a, this.s);
    this.t = qmul(this.t, b);
  }

  transform(point) {
    return qmul(qmul(this.s, point), this.t);
  }

  yaw(alpha) { this.rotate(alpha, qj); }
  pitch(alpha) { this.rotate(alpha, qi); }
  roll(alpha) { this.rotate(alpha, qk); }

  rotate(alpha, axis) {
    const e = alpha / PI;
    this.applyInner(
      qpow(axis, -e),
      qpow(qneg(axis), -e)
    );
  }

  translate(alpha) {
    const axis = qk;
    const e = alpha / PI;
    this.applyInner(
      qpow(axis, -e),
      qpow(axis, -e)
    );
  }
}
