var Filters = Filters || {};

// Space for your helper functions
// ----------- STUDENT CODE BEGIN ------------
// ----------- Our reference solution uses 105 lines of code.
// ----------- STUDENT CODE END ------------

// Translate all selected vertices in the mesh by the given x,y,z offsets.
Filters.translation = function(mesh, x, y, z) {
  const verts = mesh.getModifiableVertices(); 

  if(verts.length === 0)
    verts = mesh.getModifiableVertices(); 

  const n_vertices = verts.length;
  for (let i = 0; i < n_vertices; ++i) {
    verts[i].position.add(t);
  }

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Given x,y,z, the desired rotation around each axis, in radians,
// apply this rotation to all selected vertices in the mesh.
Filters.rotation = function(mesh, x, y, z) {
  const verts = mesh.getModifiableVertices(); 

  // ----------- STUDENT CODE BEGIN ------------
  rotation_matrix = new THREE.Euler(x, y, z, 'XYZ')
  for(let vert of verts)
    vert.position.applyEuler(rotation_matrix)
  // ----------- STUDENT CODE END ------------
  // Gui.alertOnce("Rotation is not implemented yet");

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Uniformly scale the position of all selected vertices in the mesh
// by the provided scale factor s
Filters.scale = function(mesh, s) {
  const verts = mesh.getModifiableVertices(); 

  // ----------- STUDENT CODE BEGIN ------------
  matrix = new THREE.Matrix3()
  matrix.multiplyScalar(s);

  for(let vert of verts)
  {
    vert.position.applyMatrix3(matrix);
  }
  // ----------- STUDENT CODE END ------------
  // Gui.alertOnce("Scaling is not implemented yet");

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// estimate the per-vertex gaussian curvature of the mesh at each vertex.
// set that vertex's color to some value based on its curvature value.
// (the precise mapping of curvature to color is left to you)
Filters.curvature = function(mesh) {
  // ----------- STUDENT CODE BEGIN ------------

  // ----------- STUDENT CODE END ------------
  Gui.alertOnce("Curvature is not implemented yet");
};

// Apply a random offset to each selected vertex in the direction of its normal
// scale the random offset by the provided factor and by
// the average length of edges at that vertex
Filters.noise = function(mesh, factor) {
  const verts = mesh.getModifiableVertices(); 

  // ----------- STUDENT CODE BEGIN ------------
  for(vertex of verts)
  {
    let normal = vertex.normal.clone();
    normal.normalize();
    
    vertex.position.addScaledVector(normal,  
          factor * mesh.averageEdgeLength(vertex) * (1.9999999999 * Math.random() - 1));
  }
  // ----------- STUDENT CODE END ------------
  //   Gui.alertOnce("Noise is not implemented yet");

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Smooth the mesh using the specified weighting scheme.
// In the standard case, this is done using uniform Laplacian smoothing,
// by moving each vertex towards the average position of its neighbors.
//
// Arguments:
//  - mesh: the mesh to smooth
//  - iter: the number of iterations of smoothing to apply
//  - delta: a scaling factor for the amount of smoothing
//  - curvFlow: a bool. if true, use cotangent weights instead of uniform (requires triangular mesh)
//  - scaleDep: a bool. if true, scale offsets differently for each vertex (see spec.)
//  - implicit: a bool. if true, perform implicit smoothing (see spec.)
//
// Note that the reference solution calls a giant utility function so the line
// count is not terribly representative of the true solution
//
// For implicit, you will want to compute I - M*L*delta, where I is the identity
// matrix, M is a diagonal "mass" matrix, and L is a Laplacian matrix. Then
// you will want to call math.lup() on your result in order to decompose the
// matrix. Finally, call math.lusolve() to compute the X,Y, and Z positions of
// vertices. Note that the decomposition step allows for fast solving multiple
// times. It would be possible to replace a few of these steps with simple matrix
// inversion; however, matrix inversion is far slower and less numerically stable
//
Filters.smooth = function(mesh, iter, delta, curvFlow, scaleDep, implicit) {
  const verts = mesh.getModifiableVertices(); 

  // ----------- STUDENT CODE BEGIN ------------
  if (curvFlow)
  {
      this.triangulate(mesh);
  }   

  let neighbors = [];
  
  for(vertex of verts)
  {
      neighbors.push(mesh.verticesOnVertex(vertex));
  }

  while(iter--)
  {
      let vertex_assosiated_area = [], sum_area = 0;
      let new_verts = [];

      for(let i in verts)
      {
        new_verts.push(verts[i].position.clone());

        let max_ca = max_cb = -Infinity , min_ca = min_cb = Infinity;
        let sum_of_weighted_neighbors = new THREE.Vector3(), neighbor_weight_sum = .0;
        for(let j in neighbors[i])
        {
            if(curvFlow)
            {   
              let he = mesh.edgeBetweenVertices(verts[i], neighbors[i][j]);
              let v1 = he.next.vertex.position.clone(), v2 = he.opposite.next.vertex.position.clone();
              
              let edge_1 = verts[i].position.clone(), edge_2 = neighbors[i][j].position.clone();
              
              edge_1.sub(v1);
              edge_2.sub(v1);
              
              let cos_alpha = edge_1.clone().dot(edge_2);
              let sin_alpha = edge_1.clone().cross(edge_2).length();

              let cot_alpha = cos_alpha / sin_alpha;
              
              edge_1 = verts[i].position.clone(), edge_2 = neighbors[i][j].position.clone();
              
              edge_1.sub(v2);
              edge_2.sub(v2);

              let cos_beta = edge_1.clone().dot(edge_2);
              let sin_beta = edge_1.clone().cross(edge_2).length();

              let cot_beta = cos_beta / sin_beta;

              let wij = .5 * (cot_alpha + cot_beta);

              sum_of_weighted_neighbors.addScaledVector(neighbors[i][j].position.clone(), wij);
              
              neighbor_weight_sum += wij;
            }
            else
            {
              sum_of_weighted_neighbors.add(neighbors[i][j].position.clone());
              neighbor_weight_sum += 1;
            }
        }

        faces = mesh.facesOnVertex(verts[i]);

        let associated_area = .0
        for(let face of faces)
        {
          if(scaleDep)
            associated_area += mesh.calculateFaceArea(face);
        }
        if(scaleDep)
        {
          vertex_assosiated_area.push(associated_area);
          sum_area += associated_area;
        }
        else
        {
          vertex_assosiated_area.push(1);
          sum_area += 1;
        }

        new_verts[i].addScaledVector(
          sum_of_weighted_neighbors.addScaledVector(
                                                      verts[i].position.clone().negate(), 
                                                      neighbor_weight_sum
                                                    ), 
          delta / vertex_assosiated_area[i]
          );
      }

      for(let i in new_verts)
      {
        let avg_area = sum_area / new_verts.length;

        new_verts[i].sub(verts[i].position);
        new_verts[i].multiplyScalar(avg_area);
        new_verts[i].add(verts[i].position);

        verts[i].position.set(new_verts[i].x,
                              new_verts[i].y,
                              new_verts[i].z);
      }
  }
  // ----------- STUDENT CODE END ------------
  //   Gui.alertOnce("Smooth is not implemented yet");
  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Sharpen the mesh by moving selected vertices away from the average position
// of their neighbors (i.e. Laplacian smoothing in the negative direction)
Filters.sharpen = function(mesh, iter, delta) {
  const verts = mesh.getModifiableVertices(); 
  // ----------- STUDENT CODE BEGIN ------------
  this.smooth(mesh, iter, -delta, false, false, false);
  // ----------- STUDENT CODE END ------------
  //   Gui.alertOnce("Sharpen is not implemented yet");
  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Move every selected vertex along its normal direction
// Scale the amount by the provided factor and average edge length at that vertex
Filters.inflate = function(mesh, factor) {
  const verts = mesh.getModifiableVertices(); 
  // ----------- STUDENT CODE BEGIN ------------
  for(let vertex of verts)
  {
      let normal = vertex.normal.clone();
      normal.normalize();
      
      vertex.position.addScaledVector(normal, factor);
  }
  // ----------- STUDENT CODE END ------------
//   Gui.alertOnce("Inflate is not implemented yet");

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// rotate selected vertices around the Y axis by an amount
// proportional to its Y value times the scale factor.
Filters.twist = function(mesh, factor) {
   const verts = mesh.getModifiableVertices(); 
  // ----------- STUDENT CODE BEGIN ------------

  for(let vert of verts)
  {
    rotation_matrix = new THREE.Euler(0, vert.position.y * factor, 0, 'XYZ');
    vert.position.applyEuler(rotation_matrix);
  }
  // ----------- STUDENT CODE END ------------
//   Gui.alertOnce("Twist is not implemented yet");

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// warp a mesh using a nonlinear mapping of your choice
Filters.wacky = function(mesh, factor) {
  const verts = mesh.getModifiableVertices(); 
  // ----------- STUDENT CODE BEGIN ------------
  for(let vertex of verts)
  {
      let normal = vertex.normal.clone();
      normal.normalize();
      vertex.position.addScaledVector(normal, factor * Math.floor((Math.random() * 10) + 1));
  }
  // ----------- STUDENT CODE END ------------
//   Gui.alertOnce("Wacky is not implemented yet");

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Convert the selected faces from arbitrary polygons into all triangles
Filters.triangulate = function(mesh) {
  const faces = mesh.getModifiableFaces(); 
  // ----------- STUDENT CODE BEGIN ------------
  for(let face of faces)
  {   
      let verts = mesh.verticesOnFace(face);
      for(let i in verts)
        if(i > 1 && i < verts.length - 1)
            mesh.splitFaceMakeEdge(face, verts[0], verts[i]);
  }
  // ----------- STUDENT CODE END ------------
//   Gui.alertOnce("triangulate is not implemented yet");

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// wrapper for splitEdgeMakeVert in mesh.js
Filters.splitEdge = function(mesh, factor=.5) {
  const verts = mesh.getSelectedVertices();
  if (verts.length === 2) {
    mesh.splitEdgeMakeVert(verts[0], verts[1], factor);
  } else {
    console.log("ERROR: to use split edge, select exactly 2 adjacent vertices");
  }

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// wrapper for joinEdgeKillVert in mesh.js
Filters.joinEdges = function(mesh) {
  const verts = mesh.getSelectedVertices();

  if (verts.length === 3) {
    let v0 = verts[0],
      v1 = verts[1],
      v2 = verts[2];

    const he01 = mesh.edgeBetweenVertices(v0, v1);
    const he12 = mesh.edgeBetweenVertices(v1, v2);

    if (he01) {
      if (he12) {
        mesh.joinEdgeKillVert(verts[0], verts[1], verts[2]);
      } else {
        mesh.joinEdgeKillVert(verts[1], verts[0], verts[2]);
      }
    } else {
      if (he12) {
        mesh.joinEdgeKillVert(verts[0], verts[2], verts[1]);
      } else {
        console.log(
          "ERROR: to use join edge, select exactly 3 vertices such that one only has edges to the other two"
        );
      }
    }
  } else {
    console.log("ERROR: to use join edge, select exactly 3 vertices");
  }

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// wrapper for splitFaceMakeEdge in mesh.js
Filters.splitFace = function(mesh) {
  const verts = mesh.getSelectedVertices();
  const faces = mesh.getModifiableFaces();

  if (verts.length === 2 && faces.length === 1) {
    mesh.splitFaceMakeEdge(faces[0], verts[0], verts[1]);
  } else {
    console.log("ERROR: to use split face, select exactly 1 face and 2 nonadjacent vertices on it");
  }

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// wrapper for joinFaceKillEdge in mesh.js
Filters.joinFaces = function(mesh) {
  const verts = mesh.getSelectedVertices();
  const faces = mesh.getModifiableFaces();

  if (verts.length === 2 && faces.length === 2) {
    mesh.joinFaceKillEdge(faces[0], faces[1], verts[0], verts[1]);
  } else {
    console.log(
      "ERROR: to use split face, select exactly 2 adjacent faces the 2 vertices between them"
    );
  }

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// extrude the selected faces from the mesh in the direction of their normal
// vector, scaled by the provided factor.
// See the spec for more detail.
Filters.extrude = function(mesh, factor) {
  const _faces = mesh.getModifiableFaces();

  let faces = [..._faces];
  // ----------- STUDENT CODE BEGIN ------------
  for(let face of faces)
  {
    let halfedges = mesh.edgesOnFace(face);
    let new_verts = [];
    
    for(let i=0; i < halfedges.length; i++)
    {
      let new_vert = mesh.splitEdgeMakeVert(halfedges[i].vertex,
      halfedges[i].opposite.vertex, 0);
      
      let adj_face = new_vert.halfedge.opposite.face;
      
      mesh.splitFaceMakeEdge(adj_face, new_vert.halfedge.vertex, 
      new_vert.halfedge.opposite.next.vertex);
      new_verts.push(new_vert);
    }
    
    for(let i = 0; i < new_verts.length; i++)
    {
      mesh.splitFaceMakeEdge(face, new_verts[i], new_verts[(i + 1) % new_verts.length]);
      
      mesh.joinFaceKillEdge(
        new_verts[i].halfedge.opposite.next.next.opposite.face,
        new_verts[i].halfedge.opposite.face,
        new_verts[i].halfedge.opposite.next.vertex,
        new_verts[i].halfedge.vertex
        );
    }
      
    console.log(faces.length);
    for(let new_vert of new_verts)
    {
        new_vert.position.addScaledVector(face.normal.normalize(), factor);
    }
  }
  // ----------- STUDENT CODE END ------------
//   Gui.alertOnce("Extrude is not implemented yet");
  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Truncate the selected vertices of the mesh by "snipping off" corners
// and replacing them with faces. factor specifies the size of the truncation.
// See the spec for more detail.
Filters.truncate = function(mesh, factor) {
  const _verts = mesh.getModifiableVertices(); 
  let verts = [..._verts];
  // ----------- STUDENT CODE BEGIN ------------
  let vert_positons = [];
  for(let vertex of verts)
  {
    vert_positons.push(vertex.position.clone());
  }

  let vertex_movement_list = [];

  for(let i=0; i < verts.length; i++)
  {
      let old_neighbors = mesh.verticesOnVertex(verts[i]);
      for(let j=0; j < old_neighbors.length - 1; j++)
      {
        mesh.setSelectedVertices([verts[i].id, old_neighbors[j].id]);
        this.splitEdge(mesh);
      }

      let new_neighbors = new Set(mesh.verticesOnVertex(verts[i]));

      let left_out_old_neighbor = old_neighbors.filter(x => new_neighbors.has(x));
      let old_neighbors_set = new Set(old_neighbors);
      let newly_add_neighbors = [...new_neighbors].filter(x => !old_neighbors_set.has(x));

    
      for(let j=0; j<newly_add_neighbors.length; j++) 
      {
        newly_add_neighbors[j].position.set( verts[i].position.x, 
                                             verts[i].position.y, 
                                             verts[i].position.z);

        if(newly_add_neighbors[j].halfedge.vertex.id === verts[i].id)
        {
          vertex_movement_list.push([newly_add_neighbors[j], 
                      newly_add_neighbors[j].halfedge.opposite.next.vertex.position.clone()
                          .sub(newly_add_neighbors[j].position)]);
        }

        else
        {
          vertex_movement_list.push([newly_add_neighbors[j],
                                    newly_add_neighbors[j].halfedge.vertex.position.clone()
                                        .sub( newly_add_neighbors[j].position)]);

        }
      }

      let halfedge_1 = mesh.edgeBetweenVertices(verts[i], newly_add_neighbors[0]);
      let halfedge_2 = mesh.edgeBetweenVertices(verts[i], newly_add_neighbors[1]);
      
      let faces_on_he1 = new Set([halfedge_1.face, halfedge_1.opposite.face]);
      let faces_on_he2 = new Set([halfedge_2.face, halfedge_2.opposite.face]);

      let common_face = [...faces_on_he1].filter(x=>faces_on_he2.has(x));

      mesh.setSelectedFaces([common_face[0].id]);
      mesh.setSelectedVertices([newly_add_neighbors[0].id, newly_add_neighbors[1].id]);
      this.splitFace(mesh);

      let direction_to_move = left_out_old_neighbor[0].position.clone().sub(verts[i].position);

      vert_positons[i].addScaledVector(direction_to_move, factor);
  }

  for(let [v, dir] of vertex_movement_list)
  {
    v.position.addScaledVector( dir, factor);
  }
  for(let i=0; i < verts.length; i++)
  {
    verts[i].position.set(vert_positons[i].x,
                      vert_positons[i].y,
                      vert_positons[i].z);
  }
  // ----------- STUDENT CODE END ------------
  //   Gui.alertOnce("Truncate is not implemented yet");
  mesh.setSelectedFaces([]);
  mesh.setSelectedVertices([]);
  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Apply the bevel operation to the mesh, scaling the degree of bevelling by factor
Filters.bevel = function ( mesh, factor ) {

    var verts = mesh.getModifiableVertices();

    // ----------- STUDENT CODE BEGIN ------------
    this.truncate(mesh, factor);
    let _faces = mesh.getModifiableFaces();

    _faces = [..._faces]
    let faces = [];
    for(let face of _faces)
    {
      if(mesh.verticesOnFace(face).length == 3)
      {
        faces.push(face);
      }
    }
    
    let new_verts_face = [];
    for(let face of faces)
    {
      let halfedges = mesh.edgesOnFace(face);
      for(let he of halfedges)
      {
        new_verts_face.push([mesh.splitEdgeMakeVert(he.vertex, he.opposite.vertex, .5), he.opposite.face]);
      }
    }

    let remove_edge_set = new Set();
    
    for(let i = 0; i < new_verts_face.length; i++)
    {
      mesh.splitFaceMakeEdge(
        new_verts_face[i][1],
        new_verts_face[i][0], 
        new_verts_face[i][0].halfedge.opposite.next.next.next.vertex
      );

      remove_edge_set.add(mesh.edgeBetweenVertices(
        new_verts_face[i][0].halfedge.opposite.next.vertex,
        new_verts_face[i][0].halfedge.opposite.next.next.vertex)
      );
    }

    for(let edge of remove_edge_set) {
      let v1 = edge.vertex, v2 = edge.opposite.vertex;
      mesh.joinFaceKillEdge(edge.face, edge.opposite.face, v1, v2);
      mesh.joinEdgeKillVert(v1.halfedge.vertex, v1, v1.halfedge.opposite.next.vertex)
    }

    // ----------- STUDENT CODE END ------------
    // Gui.alertOnce ('Bevel is not implemented yet');

    mesh.calculateFacesArea();
    mesh.updateNormals();
};

// Split the longest edges in the mesh into shorter edges.
// factor is a float in [0,1]. it tells the proportion
// of the total number of edges in the mesh that should be split.
Filters.splitLong = function(mesh, factor) {
  // ----------- STUDENT CODE BEGIN ------------
  let split_count = 0;
  let total_edges = 0;

  const _faces = mesh.getModifiableFaces();
  let faces = [..._faces];
  for(let face of faces)
  {
    total_edges += mesh.edgesOnFace(face).length;
  }
  total_edges /= 2;
  do{
    if(factor == 0)
      break;
    
    let max_half_edge = null, face_1_corner=null, face_2_corner=null;
    let max_half_edge_length=0;

    for(let face of faces)
    {
      let halfedges = mesh.edgesOnFace(face);
      for(let he of halfedges)
      {
        let cur_edge_len = he.vertex.position.clone().sub(he.opposite.vertex.position).length()

        if(max_half_edge_length < cur_edge_len)
        {
          max_half_edge_length = cur_edge_len;
          max_half_edge = he;
          face_1_corner = he.next.vertex;
          face_2_corner = he.opposite.next.vertex;
        }
      }
    }

    let new_vert = mesh.splitEdgeMakeVert(max_half_edge.vertex, max_half_edge.opposite.vertex, .5);
    mesh.splitFaceMakeEdge(max_half_edge.face, new_vert, face_1_corner);
    mesh.splitFaceMakeEdge(max_half_edge.opposite.face, new_vert, face_2_corner);
    split_count++;

    faces = [...mesh.getModifiableFaces()];

  }while(parseInt(factor * total_edges) > split_count);
  // ----------- STUDENT CODE END ------------
  // Gui.alertOnce("Split Long Edges is not implemented yet");

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Triangulate a mesh, and apply triangular subdivision to its faces.
// Repeat for the specified number of levels.
Filters.triSubdiv = function(mesh, levels) {
  Filters.triangulate(mesh);
 for (let l = 0; l < levels; l++) {
     const _faces = mesh.getModifiableFaces();

    // ----------- STUDENT CODE BEGIN ----------
    let faces = [..._faces];
    let face_old_edges_dest = []
    for(let face of faces)
    {
      halfedges = mesh.edgesOnFace(face);
      let old_edges_dest = [];
      for(let halfedge of halfedges)
      {
        old_edges_dest.push([halfedge, halfedge.vertex.position.clone()]);
      }
      face_old_edges_dest.push(old_edges_dest);
    }

    for(let i=0; i<face_old_edges_dest.length; i++)
    {
      let new_verts = [];
      for(let [he, v] of face_old_edges_dest[i])
      {
        let temp = he.vertex.position.clone().sub(v);
        if(temp.x==0 && temp.y==0 && temp.z==0)
        {
          let new_vert = mesh.splitEdgeMakeVert(he.vertex, he.opposite.vertex, .5);
  
          new_verts.push(new_vert);
        }
        else{
          new_verts.push(he.vertex)
        }
      }

      for(let v=0; v<new_verts.length; v++)
      {
        mesh.splitFaceMakeEdge(faces[i], new_verts[v], new_verts[(v+1)%new_verts.length]);
      }
    }
    // ----------- STUDENT CODE END ------------
    // Gui.alertOnce("Triangle subdivide is not implemented yet");
  }
  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Triangulate the mesh and apply loop subdivision to the faces
// repeat for the specified number of levels.
Filters.loop = function(mesh, levels) {
  Filters.triangulate(mesh);

  for (let l = 0; l < levels; l++) {
    const faces = mesh.getModifiableFaces();
    // ----------- STUDENT CODE BEGIN ------------
    // ----------- Our reference solution uses 123 lines of code.
    // ----------- STUDENT CODE END ------------
    Gui.alertOnce("Triangle subdivide is not implemented yet");
  }

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Requires a quad mesh. Apply quad subdivision to the faces of the mesh.
// Repeat for the specified number of levels.
Filters.quadSubdiv = function(mesh, levels) {
  for (let l = 0; l < levels; l++) {
    const faces = mesh.getModifiableFaces();
    // ----------- STUDENT CODE BEGIN ------------
    // ----------- Our reference solution uses 55 lines of code.
    // ----------- STUDENT CODE END ------------
    Gui.alertOnce("Quad subdivide is not implemented yet");
  }

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// Apply catmull clark subdivision to the faces of the mesh.
// Repeat for the specified number of levels.
Filters.catmullClark = function(mesh, levels) {
  for (let l = 0; l < levels; l++) {
    const faces = mesh.faces;
    // ----------- STUDENT CODE BEGIN ------------
    // ----------- Our reference solution uses 102 lines of code.
    // ----------- STUDENT CODE END ------------
    Gui.alertOnce("Catmull-Clark subdivide is not implemented yet");
  }

  mesh.calculateFacesArea();
  mesh.updateNormals();
};

// ================= internal functions =======================

// internal function for selecting faces in the form of a loop
Filters.procFace = function(mesh, f) {
  const faceFlags = new Array(mesh.faces.length);
  for (let i = 0; i < mesh.faces.length; i++) {
    faceFlags[i] = 0;
  }
  let sum = f.area;
  const start_he = f.halfedge.opposite.next;
  let curr_he = start_he;
  do {
    if (faceFlags[curr_he.face.id] > 0) {
      break;
    }
    sum += curr_he.face.area;
    curr_he.face.selected = true;
    faceFlags[curr_he.face.id]++;
    const last_he = curr_he;
    curr_he = curr_he.opposite.next;
    if (curr_he.face == f) {
      curr_he = last_he.next.opposite.next;
    }
  } while (true);
};

Filters.parseSelected = function(sel) {
  if (sel === undefined || sel.replace === undefined) {
    return [];
  }
  if (typeof sel === "number") {
    return [sel];
  }
  // sel = sel.replace(/[\(\)]/g,'');
  sel = sel.split(",");
  const parsedSel = [];
  for (let i = 0; i < sel.length; i++) {
    const idx = parseInt(sel[i]);
    if (!isNaN(idx)) {
      parsedSel.push(idx);
    }
  }
  return parsedSel;
};

// internal filter for updating selection
Filters.selection = function(mesh, vertIdxs, faceIdxs) {
  mesh.setSelectedVertices(Filters.parseSelected(vertIdxs));
  mesh.setSelectedFaces(Filters.parseSelected(faceIdxs));
};

// internal filter for setting display settings
Filters.displaySettings = function(
  mesh,
  showLabels,
  showHalfedge,
  shading,
  showVN,
  showFN,
  showGrid,
  showVertDots,
  showAxes,
  showVC,
  meshColor
) {
  Main.displaySettings.showIdLabels = showLabels;
  Main.displaySettings.wireframe = showHalfedge;
  Main.displaySettings.shading = shading;
  Main.displaySettings.showVN = showVN;
  Main.displaySettings.showFN = showFN;
  Main.displaySettings.showGrid = showGrid;
  Main.displaySettings.showVertDots = showVertDots;

  Main.displaySettings.showAxes = showAxes;
  Main.displaySettings.showVC = showVC;
  // Main.displaySettings.meshColor = meshColor;

  // Main.refreshDisplaySettings();
};
