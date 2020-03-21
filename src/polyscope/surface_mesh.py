import polyscope_bindings as psb

from polyscope.core import str_to_datatype, str_to_vectortype, glm3

class SurfaceMesh:

    # This class wraps a _reference_ to the underlying object, whose lifetime is managed by Polyscope

    # End users should not call this constrctor, use register_surface_mesh instead
    def __init__(self, name=None, vertices=None, faces=None, instance=None):


        # TODO ragged vertex arrays

        if instance is not None:
            # Wrap an existing instance
            self.bound_mesh = instance

        else:
            # Create a new instance
            self.check_shape(vertices)

            if (len(faces.shape) != 2):
                raise ValueError("surface mesh face array should have shape (F,D) for some D; shape is " + str(faces.shape))

            if vertices.shape[1] == 3:
                self.bound_mesh = psb.register_surface_mesh(name, vertices, faces) 
            elif vertices.shape[1] == 2:
                self.bound_mesh = psb.register_surface_mesh2D(name, vertices, faces) 

    def check_shape(self, points):
        # Helper to validate arrays
        if (len(points.shape) != 2) or (points.shape[1] not in (2,3)):
            raise ValueError("surface mesh node positions should have shape (N,3) or (N,2); shape is " + str(points.shape))
      

    def n_vertices(self):
        return self.bound_mesh.n_vertices()
    def n_faces(self):
        return self.bound_mesh.n_faces()
    def n_edges(self):
        return self.bound_mesh.n_edges()
    def n_halfedges(self):
        return self.bound_mesh.n_halfedges()
    def n_corners(self):
        return self.bound_mesh.n_corners()

    ## Structure management
    
    def remove(self):
        '''Remove the structure itself'''
        self.bound_mesh.remove()
    def remove_all_quantities(self):
        '''Remove all quantities on the structure'''
        self.bound_mesh.remove_all_quantities()
    def remove_quantity(self, name):
        '''Remove a single quantity on the structure'''
        self.bound_mesh.remove_quantity(name)

    # Enable/disable
    def set_enabled(self, val=True):
        self.bound_mesh.set_enabled(val)
    def is_enabled(self):
        return self.bound_mesh.is_enabled()

    # Update
    def update_vertex_positions(self, vertices):
        self.check_shape(vertices)
        
        if vertices.shape[1] == 3:
            self.bound_mesh.update_vertex_positions(vertices)
        elif vertices.shape[1] == 2:
            self.bound_mesh.update_vertex_positions2D(vertices)
        else:
            raise ValueError("bad node shape")

    ## Options

    
    # Color
    def set_color(self, val):
        self.bound_mesh.set_color(glm3(val))
    def get_color(self):
        return self.bound_mesh.get_color().as_tuple()
    
    # Edge Color
    def set_edge_color(self, val):
        self.bound_mesh.set_edge_color(glm3(val))
    def get_edge_color(self):
        return self.bound_mesh.get_edge_color().as_tuple()
    
    # Edge width
    def set_edge_width(self, val):
        self.bound_mesh.set_edge_width(val)
    def get_edge_width(self):
        return self.bound_mesh.get_edge_width()
    
    # Smooth shade
    def set_smooth_shade(self, val):
        self.bound_mesh.set_smooth_shade(val)
    def get_smooth_shade(self):
        return self.bound_mesh.get_smooth_shade()
    
    # Material
    def set_material(self, mat):
        self.bound_mesh.set_material(mat)
    def get_material(self):
        return self.bound_mesh.get_material()


    ## Permutations and bases

    def set_vertex_permutation(self, perm, expected_size=None):
        if len(perm.shape) != 1 or perm.shape[0] != self.n_vertices(): raise ValueError("'perm' should be an array with one entry per vertex")
        if expected_size is None: expected_size = 0
        self.bound_mesh.set_vertex_permutation(perm, expected_size)

    def set_face_permutation(self, perm, expected_size=None):
        if len(perm.shape) != 1 or perm.shape[0] != self.n_faces(): raise ValueError("'perm' should be an array with one entry per face")
        if expected_size is None: expected_size = 0
        self.bound_mesh.set_face_permutation(perm, expected_size)
    
    def set_edge_permutation(self, perm, expected_size=None):
        if len(perm.shape) != 1 or perm.shape[0] != self.n_edges(): raise ValueError("'perm' should be an array with one entry per edge")
        if expected_size is None: expected_size = 0
        self.bound_mesh.set_edge_permutation(perm, expected_size)
    
    def set_corner_permutation(self, perm, expected_size=None):
        if len(perm.shape) != 1 or perm.shape[0] != self.n_corners(): raise ValueError("'perm' should be an array with one entry per corner")
        if expected_size is None: expected_size = 0
        self.bound_mesh.set_corner_permutation(perm, expected_size)
    
    def set_halfedge_permutation(self, perm, expected_size=None):
        if len(perm.shape) != 1 or perm.shape[0] != self.n_halfedges(): raise ValueError("'perm' should be an array with one entry per halfedge")
        if expected_size is None: expected_size = 0
        self.bound_mesh.set_halfedge_permutation(perm, expected_size)
    
    def set_all_permutations(self, 
            vertex_perm=None, vertex_perm_size=None,
            face_perm=None, face_perm_size=None,
            edge_perm=None, edge_perm_size=None,
            corner_perm=None, corner_perm_size=None,
            halfedge_perm=None, halfedge_perm_size=None):

        if vertex_perm is not None: self.set_vertex_permutation(vertex_perm, vertex_perm_size)
        if face_perm is not None: self.set_face_permutation(face_perm, face_perm_size)
        if edge_perm is not None: self.set_edge_permutation(edge_perm, edge_perm_size)
        if corner_perm is not None: self.set_corner_permutation(corner_perm, corner_perm_size)
        if halfedge_perm is not None: self.set_halfedge_permutation(halfedge_perm, halfedge_perm_size)
    
    def set_vertex_tangent_basisX(self, vectors):
        if len(vectors.shape) != 2 or vectors.shape[0] != self.n_vertices() or vectors.shape[1] not in (2,3): 
            raise ValueError("'vectors' should be an array with one entry per vertex")

        if vectors.shape[1] == 2:
            self.bound_mesh.set_vertex_tangent_basisX2D(vectors)
        elif vectors.shape[1] == 3:
            self.bound_mesh.set_vertex_tangent_basisX(vectors)
    
    def set_face_tangent_basisX(self, vectors):
        if len(vectors.shape) != 2 or vectors.shape[0] != self.n_faces() or vectors.shape[1] not in (2,3): 
            raise ValueError("'vectors' should be an array with one entry per face")

        if vectors.shape[1] == 2:
            self.bound_mesh.set_face_tangent_basisX2D(vectors)
        elif vectors.shape[1] == 3:
            self.bound_mesh.set_face_tangent_basisX(vectors)
    
         


    ## Quantities

    # Scalar
    def add_scalar_quantity(self, name, values, defined_on='vertices', enabled=None, datatype="standard", vminmax=None, cmap=None):

        if len(values.shape) != 1: raise ValueError("'values' should be a length-N array")

        if defined_on == 'vertices':
            if values.shape[0] != self.n_vertices(): raise ValueError("'values' should be a length n_vertices array")
            q = self.bound_mesh.add_vertex_scalar_quantity(name, values, str_to_datatype(datatype))
        elif defined_on == 'faces':
            if values.shape[0] != self.n_faces(): raise ValueError("'values' should be a length n_faces array")
            q = self.bound_mesh.add_face_scalar_quantity(name, values, str_to_datatype(datatype))
        elif defined_on == 'edges':
            if values.shape[0] != self.n_edges(): raise ValueError("'values' should be a length n_edges array")
            q = self.bound_mesh.add_edge_scalar_quantity(name, values, str_to_datatype(datatype))
        elif defined_on == 'halfedges':
            if values.shape[0] != self.n_halfedges(): raise ValueError("'values' should be a length n_halfedges array")
            q = self.bound_mesh.add_halfedge_scalar_quantity(name, values, str_to_datatype(datatype))
        else:
            raise ValueError("bad `defined_on` value {}, should be one of ['vertices', 'faces', 'edges', 'halfedges']".format(defined_on))
            

        # Support optional params
        if enabled is not None:
            q.set_enabled(enabled)
        if vminmax is not None:
            q.set_map_range(vminmax)
        if cmap is not None:
            q.set_color_map(cmap)
    
    
    # Color
    def add_color_quantity(self, name, values, defined_on='vertices', enabled=None):
        if len(values.shape) != 2 or values.shape[1] != 3: raise ValueError("'values' should be an Nx3 array")
        
        if defined_on == 'vertices':
            if values.shape[0] != self.n_vertices(): raise ValueError("'values' should be a length n_vertices array")
            q = self.bound_mesh.add_vertex_color_quantity(name, values)
        elif defined_on == 'faces':
            if values.shape[0] != self.n_faces(): raise ValueError("'values' should be a length n_faces array")
            q = self.bound_mesh.add_face_color_quantity(name, values)
        else:
            raise ValueError("bad `defined_on` value {}, should be one of ['vertices', 'faces']".format(defined_on))

        # Support optional params
        if enabled is not None:
            q.set_enabled(enabled)
    
    
    # Distance
    def add_distance_quantity(self, name, values, defined_on='vertices', enabled=None, signed=False, vminmax=None, stripe_size=None, stripe_size_relative=True, cmap=None):

        if len(values.shape) != 1: raise ValueError("'values' should be a length-N array")

        if defined_on == 'vertices':
            if values.shape[0] != self.n_vertices(): raise ValueError("'values' should be a length n_vertices array")

            if signed:
                q = self.bound_mesh.add_vertex_signed_distance_quantity(name, values)
            else:
                q = self.bound_mesh.add_vertex_distance_quantity(name, values)
        else:
            raise ValueError("bad `defined_on` value {}, should be one of ['vertices']".format(defined_on))
            

        # Support optional params
        if enabled is not None:
            q.set_enabled(enabled)
        if stripe_size is not None:
            q.set_stripe_size(stripe_size, stripe_size_relative)
        if vminmax is not None:
            q.set_map_range(vminmax)
        if cmap is not None:
            q.set_color_map(cmap)
    
    '''
    
    # Vector
    def add_vector_quantity(self, name, values, defined_on='vertices', enabled=None, vectortype="standard", length=None, radius=None, color=None):
        if len(values.shape) != 2 or values.shape[1] not in [2,3]: raise ValueError("'values' should be an Nx3 array (or Nx2 for 2D)")
        
        
        if defined_on == 'vertices':
            if values.shape[0] != self.n_nodes(): raise ValueError("'values' should be a length n_nodes array")

            if values.shape[1] == 2:
                q = self.bound_mesh.add_node_vector_quantity2D(name, values, str_to_vectortype(vectortype))
            elif values.shape[1] == 3:
                q = self.bound_mesh.add_node_vector_quantity(name, values, str_to_vectortype(vectortype))

        elif defined_on == 'faces':
            if values.shape[0] != self.n_edges(): raise ValueError("'values' should be a length n_edges array")
            
            if values.shape[1] == 2:
                q = self.bound_mesh.add_edge_vector_quantity2D(name, values, str_to_vectortype(vectortype))
            elif values.shape[1] == 3:
                q = self.bound_mesh.add_edge_vector_quantity(name, values, str_to_vectortype(vectortype))

        else:
            raise ValueError("bad `defined_on` value {}, should be one of ['vertices', 'faces']".format(defined_on))

        # Support optional params
        if enabled is not None:
            q.set_enabled(enabled)
        if length is not None:
            q.set_length(length, True)
        if radius is not None:
            q.set_radius(radius, True)
        if color is not None:
            q.set_color(glm3(color))
    '''


def register_surface_mesh(name, vertices, faces, enabled=None, color=None, edge_color=None, smooth_shade=None, 
                          edge_width=None, material=None):
    """Register a new surface mesh"""

    p = SurfaceMesh(name, vertices, faces)

    # == Apply options
    if enabled is not None:
        p.set_enabled(enabled)
    if color is not None:
        p.set_color(color)
    if edge_color is not None:
        p.set_edge_color(edge_color)
    if edge_width is not None:
        p.set_edge_width(edge_width)
    if smooth_shade is not None:
        p.set_smooth_shade(smooth_shade)
    if material is not None:
        p.set_material(material)

    return p

def remove_surface_mesh(name, error_if_absent=True):
    """Remove a surface mesh by name"""
    psb.remove_surface_mesh(name, error_if_absent)

def get_surface_mesh(name):
    """Get surface mesh by name"""
    if not has_surface_mesh(name):
        raise ValueError("no surface mesh with name " + str(name))

    raw = psb.get_surface_mesh(name)

    # Wrap the instance
    return SurfaceMesh(instance=raw)

def has_surface_mesh(name):
    """Check if a surface mesh exists by name"""
    return psb.has_surface_mesh(name)
    