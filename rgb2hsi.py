'''
This file contains an rgb to hsi and hsi to rgb conversion function
This function needs to be optimized as the conversion is too slow
For now, this is used so that histogramEqualization can operate on color images
This will be updated and optimized shortly, if possible
'''

import numpy as np
from math import pi, cos, acos, sqrt
from copy import deepcopy


def rgb_to_hsi(img, size):

    imgSize = size

    B = img[:, :, 0]/255.0
    G = img[:, :, 1]/255.0
    R = img[:, :, 2]/255.0

    H = np.zeros([imgSize[0], imgSize[1]], dtype=np.double)
    S = deepcopy(H)
    I = deepcopy(H)
    output = np.zeros([imgSize[0], imgSize[1], 3], dtype=np.double)

    for i in range(imgSize[0]):
        for j in range(imgSize[1]):
            if(((R[i, j] - G[i, j])**2) + ((R[i, j] - B[i, j])*(G[i, j] - B[i, j])) == 0.0):
                H[i, j] = 2*pi
            elif(B[i, j] <= G[i, j]):
                H[i, j] = acos(((R[i, j] - G[i, j]) + (R[i, j] - B[i, j]))/(2*sqrt(((R[i, j] - G[i, j])**2) + ((R[i, j] - B[i, j])*(G[i, j] - B[i, j])))))
            elif(B[i, j] > G[i, j]):
                H[i, j] = 2*pi - acos(((R[i, j] - G[i, j]) + (R[i, j] - B[i, j]))/(2*sqrt(((R[i, j] - G[i, j])**2) + ((R[i, j] - B[i, j])*(G[i, j] - B[i, j])))))

            I[i, j] = (R[i, j] + B[i, j] + G[i, j])/3.0
            if(I[i, j] != 0.0):
                S[i, j] = 1 - min(B[i, j], G[i, j], R[i, j]) / I[i, j]
            else:
                S[i, j] = 1.0

    H = H*255.0/(2*pi)
    S = S*255.0
    I = I*255.0

    output[:, :, 0] = H
    output[:, :, 1] = S
    output[:, :, 2] = I

    output = np.array(output, dtype=np.uint8)

    return output


def hsi_to_rgb(img, size):
    
    imgSize = size

    H = (2*pi)*img[:, :, 0]/255.0
    S = img[:, :, 1]/255.0
    I = img[:, :, 2]/255.0
    B = np.zeros([imgSize[0], imgSize[1]], dtype=np.double)
    G = np.zeros([imgSize[0], imgSize[1]], dtype=np.double)
    R = np.zeros([imgSize[0], imgSize[1]], dtype=np.double)
    output = np.zeros([imgSize[0], imgSize[1], 3], dtype=np.double)

    for i in range(imgSize[0]):
        for j in range(imgSize[1]):

            if(H[i, j] >= 0 and H[i, j] < pi*(2.0/3.0)):
                B[i, j] = I[i, j]*(1-S[i, j])
                R[i, j] = I[i, j] +\
                    (I[i, j]*S[i, j]*cos(H[i, j]))/cos((pi/3.0) - H[i, j])
                G[i, j] = 3*I[i, j] - R[i, j] - B[i, j]

            elif(H[i, j] >= pi*(2.0/3.0) and H[i, j] < pi*(4.0/3.0)):
                Hprime = H[i, j] - pi*(2.0/3.0)
                R[i, j] = I[i, j]*(1-S[i, j])
                G[i, j] = I[i, j] +\
                    (I[i, j]*S[i, j]*cos(Hprime))/cos((pi/3.0) - Hprime)
                B[i, j] = 3*I[i, j] - R[i, j] - G[i, j]

            elif(H[i, j] >= pi*(4.0/3.0)):
                Hdoubleprime = H[i, j] - pi*(4.0/3.0)
                G[i, j] = I[i, j]*(1-S[i, j])
                B[i, j] = I[i, j] +\
                    (I[i, j]*S[i, j]*cos(Hdoubleprime))\
                    / cos((pi/3.0) - Hdoubleprime)
                R[i, j] = 3*I[i, j] - B[i, j] - G[i, j]

    R = R*255.0
    B = B*255.0
    G = G*255.0

    for i in range(imgSize[0]):
        for j in range(imgSize[1]):
            if(R[i, j] > 255.0):
                R[i, j] = 255.0
            if(B[i, j] > 255.0):
                B[i, j] = 255.0
            if(G[i, j] > 255.0):
                G[i, j] = 255.0
                
    output[:, :, 0] = B
    output[:, :, 1] = G
    output[:, :, 2] = R

    output = np.array(output, dtype=np.uint8)

    return output
