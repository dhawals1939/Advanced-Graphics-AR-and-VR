// In this file you will implement traversal and analysis for your assignment.
// Make sure to familiarize yourself with the utility functions in meshUtils.js
// they might be useful for the second part of your assignment!

////////////////////////////////////////////////////////////////////////////////
// Traversal
////////////////////////////////////////////////////////////////////////////////

// Return all vertices on face f
Mesh.prototype.verticesOnFace = function(f) {
  const vertices = [];
  let he = f.halfedge;
  const first = he;
  while (true) {
    vertices.push(he.vertex);
    he = he.next;
    if (he === first) {
      break;
    }
  }
  return vertices;
};

// Return all halfedges on face f
Mesh.prototype.edgesOnFace = function(f) {
  const halfedges = [];

  // ----------- STUDENT CODE BEGIN ------------
  let first = f.halfedge
  let he = first;
  while(true)
  {
    halfedges.push(he);
    he = he.next;

    if(first == he)
      break;
  }
  // ----------- STUDENT CODE END ------------

  return halfedges;
};

// Return all faces adjacent to input face, not
// including input face.
Mesh.prototype.facesOnFace = function(f) {
  const faces = [];
  // ----------- STUDENT CODE BEGIN ------------
  halfedges = this.edgesOnFace(f)
  for(let he of halfedges)
  {
    if (he.opposite.face == f)
      continue
    // console.log(he.opposite)
    faces.push(he.opposite.face)
  }
  // console.log(faces)
  // ----------- STUDENT CODE END ------------

  return faces;
};

// Return one-ring neighbors of input vertex, not
// including the input vertex itself
Mesh.prototype.verticesOnVertex = function(v) {
  const vertices = [];

  // ----------- STUDENT CODE BEGIN ------------
  halfedges = this.edgesOnVertex(v);
  for(let he of halfedges)
  {
    vertices.push(he.vertex);
  }
  // ----------- STUDENT CODE END --------------

  return vertices;
};

// Return all halfedges that point away from v
Mesh.prototype.edgesOnVertex = function(v) {
  const halfedges = [];

  // ----------- STUDENT CODE BEGIN ------------
  let first = he = v.halfedge;
  while(true)
  {
    if(halfedges.includes(he))
      break
    halfedges.push(he);
    he = he.opposite.next;

    if(first == he)
      break;
  }
  // ----------- STUDENT CODE END ------------

  return halfedges;
};

// Return all faces that include v as a vertex.
Mesh.prototype.facesOnVertex = function(v) {
  const faces = [];

  // ----------- STUDENT CODE BEGIN ------------
  halfedges = this.edgesOnVertex(v);
  for(let halfedge of halfedges)
  {
    if(!faces.includes(halfedge.face))
      faces.push(halfedge.face)

    if(!faces.includes(halfedge.opposite.face))
      faces.push(halfedge.opposite.face)
  }

  // console.log(v.id, faces);
  // ----------- STUDENT CODE END ------------

  return faces;
};

// Return the vertices that form the endpoints of a given edge
Mesh.prototype.verticesOnEdge = function(e) {
  const vertices = [];

  // ----------- STUDENT CODE BEGIN ------------
  vertices.push(e.vertex);
  vertices.push(e.opposite.vertex);
  // ----------- STUDENT CODE END ------------

  return vertices;
};

// Return the faces that include a given edge
Mesh.prototype.facesOnEdge = function(e) {
  const faces = [];
  // ----------- STUDENT CODE BEGIN ------------
  faces.push(e.face);
  faces.push(e.opposite.face);
  // ----------- STUDENT CODE END ------------
  return faces;
};

// Return the edge pointing from v1 to v2
Mesh.prototype.edgeBetweenVertices = function(v1, v2) {
  let out_he = undefined;
  // ----------- STUDENT CODE BEGIN ------------
  halfedges = this.edgesOnVertex(v1);
  for(let halfedge of halfedges)
  {
    if (halfedge.vertex == v2)
    {
      out_he = halfedge;
      break;
    }
  }
  // console.log(v1.id, v2.id, out_he);
  // ----------- STUDENT CODE END ------------
  return out_he;
};

////////////////////////////////////////////////////////////////////////////////
// Analysis
////////////////////////////////////////////////////////////////////////////////

// Return the surface area of a provided face f.
Mesh.prototype.calculateFaceArea = function(f) {
  let area = 0.0;
  // ----------- STUDENT CODE BEGIN ------------
  let edge_list = this.edgesOnFace(f);

  let vertex_list = []
  let centroid = new THREE.Vector3();
  for(let edge of edge_list)
  {
    vertex_list.push(edge.vertex.position);
    centroid.add(edge.vertex.position);
  }

  centroid.divideScalar(vertex_list.length);

  for(let i =0; i < vertex_list.length; i++)
  {
    let a = vertex_list[i % vertex_list.length].distanceTo(centroid);
    let b = vertex_list[(i + 1) % vertex_list.length].distanceTo(centroid);
    let c = vertex_list[(i + 1) % vertex_list.length].distanceTo(vertex_list[i % vertex_list.length])

    let s = (a + b + c) /2 ;
    area += (s*(s-a) * (s-b)*(s-c)) ** 0.5;
  }
    

  // console.log(vertex_list, area);
  // ----------- STUDENT CODE END ------------
  f.area = area;
  return area;
};

// Update the area attributes of all faces in the mesh
Mesh.prototype.calculateFacesArea = function() {
  for (let i = 0; i < this.faces.length; ++i) {
    this.calculateFaceArea(this.faces[i]);
  }
};

// Calculate the vertex normal at a given vertex,
// using the face normals of bordering faces, weighted by face area
Mesh.prototype.calculateVertexNormal = function(v) {
  const v_normal = new THREE.Vector3(0, 0, 0);
  // ----------- STUDENT CODE BEGIN ------------
  let associated_faces = this.facesOnVertex(v);

  let total_area = 0.0
  for(face of associated_faces)
  {
    let current_normal = face.normal.clone();
    current_normal.multiplyScalar(face.area);
    
    v_normal.add(current_normal);
    total_area += face.area;
  }
  v_normal.divideScalar(total_area);
  // console.log(v_normal);
  // ----------- STUDENT CODE END ------------
  v.normal = v_normal;
  return v_normal;
};

// update the vertex normals of every vertex in the mesh
Mesh.prototype.updateVertexNormals = function() {
  for (let i = 0; i < this.vertices.length; ++i) {
    this.calculateVertexNormal(this.vertices[i]);
  }
};

// compute the average length of edges touching v
Mesh.prototype.averageEdgeLength = function(v) {
  let avg = 0.0;

  // ----------- STUDENT CODE BEGIN ------------
  let vertex_list = this.verticesOnVertex(v);
  
  for(vertex of vertex_list)
  {
    avg += vertex.position.distanceTo(v.position);
  }
  avg /= vertex_list.length;

  console.log(avg);
  // ----------- STUDENT CODE END ------------

  return avg;
};

////////////////////////////////////////////////////////////////////////////////
// Topology
////////////////////////////////////////////////////////////////////////////////

// Given a face in the shape of an arbitrary polygon,
// split that face so it consists only of several triangular faces. 
Mesh.prototype.triangulateFace = function(f) {
  // ----------- STUDENT CODE BEGIN ------------
  // ----------- Our reference solution uses 8 lines of code.
  // ----------- STUDENT CODE END ------------
};
