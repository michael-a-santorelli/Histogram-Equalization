'''
This file contains a histogram equalization digital image processing function.
This function can perform 4 types of histogram equalization. 
    - Global, color histogram equalization,
    - Global, grayscale histogram equalization,
    - Local, color histogram equalization, and
    - Local, grayscale histogram equalization
Global, color histogram equalization is used by calling histogramEqualization("file_name"),
Global, grayscale histogram equalization is used by calling histogramEqualization("file_name", colorInfo="gray"),
Local, color histogram equalization is used by calling histogramEqualization("file_name", "local"),
Local, grayscale histogram equalization is used by calling histogramEqualization("file_name", "local", "gray"),
'''
import cv2
import rgb2hsi


# Histogram Equalization function
def histogramEqualization(image: str, adjustType: str = "global", colorInfo: str = "color"):

    # Load image
    img = cv2.imread(image)
    # If user wants grayscale output, reload as grayscale image
    if(colorInfo == "gray"):
        img = cv2.imread(image, 0)
    # Determine image size; used for creating output image
    imgSize = img.shape

    # If image number of dimensions is 2 perform grayscale operations
    if(img.ndim == 2):
        # Perform global histogram equilazation
        if(adjustType == 'global'):
            output = cv2.equalizeHist(img)

        # Perform local adaptive histogram equilazation
        else:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            output = clahe.apply(img)

    # If image dimension is not 2 it will be 3; perform color manipulations
    else:
        # Create HSI representation of image
        # Used to manipulate Intensity channel of image
        HSI = rgb2hsi.rgb_to_hsi(img, imgSize)
        I = HSI[:, :, 2]

        # Perform global histogram equilazation
        if(adjustType == 'global'):
            equalized = cv2.equalizeHist(I)

        # Perform local adaptive histogram equilazation
        else:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            equalized = clahe.apply(I)

        # Use new Intensity channel to form HSI image
        HSI[:, :, 2] = equalized

        # Return back to rgb space
        output = rgb2hsi.hsi_to_rgb(HSI, imgSize)

    # Display input and output image
    cv2.imshow("intput", img)
    cv2.imshow("output", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
