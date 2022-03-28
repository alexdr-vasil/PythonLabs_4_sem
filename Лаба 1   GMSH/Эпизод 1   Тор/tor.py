import gmsh
import math
import os
import sys
import time

t = time.time()  # Выполняется примерно за 4 секунды

gmsh.initialize()

# Let's merge an STL mesh that we would like to remesh (from the parent
# directory):
path = os.path.dirname(os.path.abspath(__file__))
gmsh.merge(os.path.join(path, 'tor.stl'))

# Angle between two triangles above which an edge is considered as sharp:
angle = 9

# For complex geometries, patches can be too complex, too elongated or too large
# to be parametrized; setting the following option will force the creation of
# patches that are amenable to reparametrization:
forceParametrizablePatches = False

# For open surfaces include the boundary edges in the classification process:
includeBoundary = True

# Force curves to be split on given angle:
curveAngle = 180
gmsh.model.mesh.MeshSizeFromPoints = 0
gmsh.model.mesh.MeshSizeFromCurvature = 0
gmsh.model.mesh.MeshSizeExtendFromBoundary = 0

gmsh.model.mesh.classifySurfaces(angle * math.pi / 180., includeBoundary,
                                 forceParametrizablePatches,
                                 curveAngle * math.pi / 180.)

# Create a geometry for all the discrete curves and surfaces in the mesh, by
# computing a parametrization for each one
gmsh.model.mesh.createGeometry()

# Create a volume from all the surfaces
s = gmsh.model.getEntities(2)
l = gmsh.model.geo.addSurfaceLoop([s[i][1] for i in range(len(s))])
gmsh.model.geo.addVolume([l])

gmsh.model.geo.synchronize()

# We specify element sizes imposed by a size field, just because we can :-)
f = gmsh.model.mesh.field.add("MathEval")
gmsh.model.mesh.field.setString(f, "F", "4")
gmsh.model.mesh.field.setAsBackgroundMesh(f)

gmsh.model.mesh.generate(3)
gmsh.write('tor.msh')

t_work = time.time() - t
print('\n Program running time while creating mesh: ', t_work, 'seconds')

# Launch the GUI to see the results:
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
