// Scene setup and rendering for the 3-sphere demo.

import { AxisSet, Octahedron, Color } from './shapes.js';

const PI = Math.PI;

function createVAO(gl, program, posData, colData) {
  const vao = gl.createVertexArray();
  gl.bindVertexArray(vao);

  const posLoc = gl.getAttribLocation(program, 'a_position');
  const colLoc = gl.getAttribLocation(program, 'a_color');

  const posBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
  gl.bufferData(gl.ARRAY_BUFFER, posData, gl.STATIC_DRAW);
  gl.enableVertexAttribArray(posLoc);
  gl.vertexAttribPointer(posLoc, 4, gl.FLOAT, false, 0, 0);

  const colBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, colBuf);
  gl.bufferData(gl.ARRAY_BUFFER, colData, gl.STATIC_DRAW);
  gl.enableVertexAttribArray(colLoc);
  gl.vertexAttribPointer(colLoc, 3, gl.FLOAT, false, 0, 0);

  gl.bindVertexArray(null);

  const vertexCount = posData.length / 4;
  return { vao, vertexCount };
}

export function createScene(gl, program) {
  const axes = new AxisSet();
  axes.addAllAxes();
  const axesObj = createVAO(gl, program, axes.posArray(), axes.colArray());

  const sphere = new Octahedron(undefined, PI, 6);
  const sphereObj = createVAO(gl, program, sphere.posArray(), sphere.colArray());

  const sphere2 = new Octahedron(undefined, PI / 4, 0, Color.Red, Color.Cyan);
  const sphere2Obj = createVAO(gl, program, sphere2.posArray(), sphere2.colArray());

  return { axesObj, sphereObj, sphere2Obj };
}

export function renderScene(gl, scene) {
  const { axesObj, sphereObj, sphere2Obj } = scene;

  gl.bindVertexArray(axesObj.vao);
  gl.drawArrays(gl.LINES, 0, axesObj.vertexCount);

  gl.bindVertexArray(sphereObj.vao);
  gl.drawArrays(gl.TRIANGLES, 0, sphereObj.vertexCount);

  gl.bindVertexArray(sphere2Obj.vao);
  gl.drawArrays(gl.TRIANGLES, 0, sphere2Obj.vertexCount);

  gl.bindVertexArray(null);
}
