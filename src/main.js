// Spherical World - WebGL2 demo
// 3-sphere visualization with quaternion-based camera

import { SphericalTransform } from './geo.js';
import { createScene, renderScene } from './scene.js';
import vertSrc from './shaders/demo.vert.glsl?raw';
import fragSrc from './shaders/demo.frag.glsl?raw';

// --- Projection matrix (matches Python frustum function) ---

function frustum(left, right, bottom, top, nearVal, farVal) {
  const A = (right + left) / (right - left);
  const B = (top + bottom) / (top - bottom);
  const C = -(farVal + nearVal) / (farVal - nearVal);
  const D = -(2 * farVal * nearVal) / (farVal - nearVal);
  // Column-major for WebGL (transposed from row-major Python)
  return new Float32Array([
    2*nearVal/(right-left), 0, 0, 0,
    0, 2*nearVal/(top-bottom), 0, 0,
    -A, -B, -C, 1,   // note: w row becomes column, Python has +1 not -1
    0, 0, D, 0,
  ]);
}

function projectionMatrix() {
  return frustum(0.0002, -0.0002, 0.0002, -0.0002, 0.0002, 5000.0);
}

// --- Shader compilation ---

function compileShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.error('Shader compile error:', gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
    return null;
  }
  return shader;
}

function createProgram(gl, vsSource, fsSource) {
  const vs = compileShader(gl, gl.VERTEX_SHADER, vsSource);
  const fs = compileShader(gl, gl.FRAGMENT_SHADER, fsSource);
  const program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.error('Program link error:', gl.getProgramInfoLog(program));
    return null;
  }
  return program;
}

// --- Camera ---

class Camera {
  constructor(tickMs, anglePerSecond = Math.PI / 4, distancePerSecond = Math.PI / 10) {
    this.qp = new SphericalTransform();
    this.input = { roll: 0, yaw: 0, pitch: 0, ahead: 0 };
    this.anglePerTick = anglePerSecond * tickMs / 1000;
    this.distancePerTick = distancePerSecond * tickMs / 1000;
  }

  tick() {
    this.qp.yaw(this.input.yaw * this.anglePerTick);
    this.qp.pitch(this.input.pitch * this.anglePerTick);
    this.qp.roll(this.input.roll * this.anglePerTick);
    this.qp.translate(this.input.ahead * this.distancePerTick);
  }

  updateInput(name, direction, reset) {
    if (this.input[name] === direction) {
      if (reset) this.input[name] = 0;
    } else {
      if (!reset) this.input[name] = direction;
    }
  }

  handleKey(code, down) {
    const reset = !down;
    switch (code) {
      case 'KeyW': this.updateInput('pitch', +1, reset); break;
      case 'KeyS': this.updateInput('pitch', -1, reset); break;
      case 'KeyA': this.updateInput('yaw', +1, reset); break;
      case 'KeyD': this.updateInput('yaw', -1, reset); break;
      case 'KeyQ': this.updateInput('roll', +1, reset); break;
      case 'KeyE': this.updateInput('roll', -1, reset); break;
      case 'ArrowUp': this.updateInput('ahead', +1, reset); break;
      case 'ArrowDown': this.updateInput('ahead', -1, reset); break;
    }
  }
}

// --- Main ---

function main() {
  const canvas = document.getElementById('canvas');
  canvas.width = canvas.clientWidth * devicePixelRatio;
  canvas.height = canvas.clientHeight * devicePixelRatio;

  const gl = canvas.getContext('webgl2', { antialias: true });
  if (!gl) {
    document.body.textContent = 'WebGL2 not supported';
    return;
  }

  gl.enable(gl.DEPTH_TEST);
  gl.clearColor(0, 0, 0, 0);
  gl.viewport(0, 0, canvas.width, canvas.height);

  const program = createProgram(gl, vertSrc, fragSrc);
  gl.useProgram(program);

  // Set projection matrix
  const projLoc = gl.getUniformLocation(program, 'proj');
  gl.uniformMatrix4fv(projLoc, false, projectionMatrix());

  const viewSLoc = gl.getUniformLocation(program, 'view_s');
  const viewTLoc = gl.getUniformLocation(program, 'view_t');

  const scene = createScene(gl, program);

  const TICK_MS = 10;
  const camera = new Camera(TICK_MS);
  let lastTick = performance.now();

  // Keyboard handling
  document.addEventListener('keydown', (e) => {
    camera.handleKey(e.code, true);
    if (['ArrowUp', 'ArrowDown'].includes(e.code)) e.preventDefault();
  });
  document.addEventListener('keyup', (e) => {
    camera.handleKey(e.code, false);
  });

  // Handle canvas resize
  function resize() {
    canvas.width = canvas.clientWidth * devicePixelRatio;
    canvas.height = canvas.clientHeight * devicePixelRatio;
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  window.addEventListener('resize', resize);

  // Game loop
  function frame(now) {
    // Fixed-timestep ticks
    while (lastTick + TICK_MS < now) {
      camera.tick();
      lastTick += TICK_MS;
    }

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Pass view quaternions to shader (as xyzw)
    const s = camera.qp.s;
    const t = camera.qp.t;
    gl.uniform4f(viewSLoc, s[1], s[2], s[3], s[0]);
    gl.uniform4f(viewTLoc, t[1], t[2], t[3], t[0]);

    renderScene(gl, scene);

    requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
}

main();
