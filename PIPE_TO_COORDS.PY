#!/usr/bin/python3

import numpy as np
import jnius_config
import sys
import math
import os

EARTH_RADIUS = 6371000
#EARTH_RADIUS = 6378137.0

utrecht_x = 3899275.0
utrecht_y = 348997.0
utrecht_z = 5026376.0

jnius_config.set_classpath('terra121_classes')
from jnius import autoclass

A = 6378137.0
B = 6356752.3142

ModifiedAirocean = autoclass("io.github.terra121.projection.ModifiedAirocean")
ScaleProjection = autoclass("io.github.terra121.projection.ScaleProjection")
GeographicProjection = autoclass("io.github.terra121.projection.GeographicProjection")
Orientation = autoclass("io.github.terra121.projection.GeographicProjection$Orientation")

base_projection = GeographicProjection.orientProjection(ModifiedAirocean(), Orientation.none)
projection = ScaleProjection(base_projection, 7318261.522857145, -7318261.522857145)

if __name__ == "__main__":
        
    if len(sys.argv)==1:
        print ('converting from pipe')
        COUNTER = 0
        fd_out = open("result.txt", "a")
        for line in sys.stdin:
            lines = np.array([line], dtype=str)
            v = lines
            v = np.char.split(v, " ")
            v = np.array(list(v))[:, 0:2]
            for i in range(len(v)):
#                print( 'LAT=' + v[i, 0] + ' LON=' + v[i, 1]  )

                COUNTER=COUNTER + 1

                LON=float(v[i, 0].astype(float))
                LAT=float(v[i, 1].astype(float))
                COORDS=projection.fromGeo(LON,LAT)

                X=int(COORDS[0]/512)
                Z=int(COORDS[1]/512)
                if X<0:
                    X=X-1
                if Z<0:
                    Z=Z-1
                    print( 
                        'R.' + str(X) + '.' + str(Z) + '.MCA   ' +
                        'X=' + str(int(COORDS[0])) + ' Z=' + str(int(COORDS[1])) + ' ' +
                        '{:8.4f}'.format(LON) + ' ' + '{:8.4f}'.format(LAT) 
                    )
                    fd_out.write( 
                        'R.' + str(X) + '.' + str(Z) + '.MCA   ' +
                        'X=' + str(int(COORDS[0])) + ' Z=' + str(int(COORDS[1])) + ' ' +
                        '{:8.4f}'.format(LON) + ' ' + '{:8.4f}'.format(LAT) + '\n'
                        
                    )

        fd_out.close()

