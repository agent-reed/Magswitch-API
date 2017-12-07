from unit import Unit
import part

def holdingCalc(unit, material, thickness):

    unitToCalc = Unit(unit)
    materialToCalc = part.Material(material)
    partToCalc = part.Geometry(1,1,thickness) # eventually the first two args with be used as well, but for now are left to unit standards

    # start with thicknesses to scan through the data that we have.
    myList = unitToCalc.thicknesses

    #Start at the front and iterate forwards until we find a value lower than the entered thickness
    index=0
    for i,value in enumerate(myList):
        print(i, value)
        if value>float(thickness):
            index=i-1
            break

    # once we have the index of the lower bound, we know that the next index is the upper bound
    x1 = myList[index]
    x2 = myList[index + 1]
    y1 = unitToCalc.forces[index]
    y2 = unitToCalc.forces[index +1]

    print (x1, x2 , y1, y2)


    # with our two coordinates we can perform a linear interpolation
    intForce = y1 + ((float(thickness) - x1)*((y2-y1)/(x2-x1))) 

    return str(intForce)

