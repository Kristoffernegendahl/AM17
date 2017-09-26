"""
Livestock Heat transfer - Transmission. Calculates the transmission losses and gains of various geometries under stationary conditions
-----
Please notice only type of geometry type is allowed as input 
-----
LIVESTOCK made by Kristoffer Negendahl, DTU.BYG

    Args:
        Geo: List of Surfaces, Breps or Meshes
        U: List of U-values [W/(m2K)] for each Geometry (if only one U, all Geometries will be evaluated on the single U-value)
        Ti: Temperature (C) on the inner side of the geometry (20C is set as default)
        To: Temperature (C) on the outside of the geometry (-12C is set as default)
    Returns:
        Q: Output the transmission heat balance [kW] - if negative the transmission is considered as a loss from inside to the outside, and if positive the transmission is a gain from outside to the inside
        Qi: Output the individual geometry transmission heat balance [W]
"""

# Add the message thingie underneath the component
ghenv.Component.Name = 'Livestock_Heat_Transmission'
ghenv.Component.NickName = 'Livestock Heat Transmission'
ghenv.Component.Message = 'Transmission v.0.1'

# Importing classes and modules
import Rhino as rc

# Setting defaults 

U_def = [0]
Ti_def = 20
To_def = -12

### Ordering inputs into dedicated lists
## Supports three types of geometry 
srfs = []
breps = []
meshes = []

for g in Geo:
    #print type(g)
    if isinstance(g,rc.Geometry.Surface): #is surface
        #print("a surface")
        srfs.append(g)
    elif isinstance(g,rc.Geometry.Brep): #is Brep
        #print("a brep")
        breps.append(g)
    elif isinstance(g,rc.Geometry.Mesh): #is Mesh
        #print("a mesh")
        meshes.append(g)
    else:
        print("not a geometry I can work with")

# Output relevant information
noSrfs = str(len(srfs))
noBreps = str(len(breps))
noMeshes = str(len(meshes))

print "Transmission from {} surfaces,".format(noSrfs), "{} breps,".format(noBreps), "{} meshes".format(noMeshes)

# Function that calucalates an area of a geometry
def area(list_of_geometry):
    area = []
    areaerror = []
    #try: # -- can't use this - only works on breps and srfs
        #for i in range(len(list_of_geometry)):
            #area.append(list_of_geometry[i].GetArea())
    #except:
        #print "Geometry had no GetArea properties"
    try:
        for i in range(len(list_of_geometry)):
            area.append(rc.Geometry.AreaMassProperties.Compute(list_of_geometry[i]).Area)
            areaerror.append(rc.Geometry.AreaMassProperties.Compute(list_of_geometry[i]).AreaError)
    except:
        print "Geometry had no AreaMassProperties properties"
    #print(areaerror)
    return area

# Function that calculates the transmission balance
def transm(areas, Uvals, ti, to):
    qli = []
    if len(areas) > 1 and len(areas) == len(Uvals): #when multiple Uvals
        for i in range(len(areas)):
            qli.append(areas[i]*Uvals[i]*(to-ti))
    else: #when only one Uval
        for i in range(len(areas)):
            qli.append(areas[i]*Uvals[0]*(to-ti))
    Qi = qli
    Q = round(sum(qli)/1000,2)
    return Q, Qi

# Setting defaults if nothing else is assigned 
if not U:
    U = U_def
if not Ti:
    Ti = Ti_def
if not To:
    To = To_def


# Check geometry lists and assign area function

if srfs:
    try: A = area(srfs)
    except: print("not a geometry I can work with")
elif breps:
    try: A = area(breps)
    except: print("not a geometry I can work with")
elif meshes:
    try: A = area(meshes)
    except: print("not a geometry I can work with")

# Calculate heat transmission

Transmission = transm(A, U, Ti, To)
Q = Transmission[0]
Qi = Transmission[1] 

