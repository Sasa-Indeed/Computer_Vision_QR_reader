# Computer_Vision_QR_Reader
CSE 483: Computer Vision QR Reader

The goal of the project is to be able to decode given samples of QR codes with a robust and reliable image processing pipeline using only classical vision algorithms to implement the QR code standard in ISO/IEC 18004. 

# Video

![]()

# Our Approach
## Skewed Image histograms
## Remove anomaly frequencies
## 
# QR Code Orientation Detection

Our approach to detecting the orientation of a QR code is based on the unique pattern of the locator boxes, which follows a 1:1:3:1:1 ratio. This pattern allows us to determine whether the QR code is rotated or in its correct orientation.

## Methodology

We focus on the fourth corner of the QR code. If the unique pattern exists in both the designated row and column of this corner, we deduce that the QR code is rotated. If not, the QR code is in the correct orientation.

To account for potential variations, we have incorporated a tolerance margin. We check the mean of the values in a single grid cell and consider the pattern to exist if the corresponding value from the pattern matches that of the grid cells we check.

## Rotation Rules

Based on the existence of the pattern in the corners, we apply the following rotation rules:

- If the pattern exists in the fourth corner (bottom right corner), the bottom left, and the top right (test case 3), we rotate the QR code by **180 degrees**.
- If the pattern exists in the fourth corner and bottom left only, we rotate the QR code by **90 degrees**.
- If the pattern exists in the fourth corner and top right only, we rotate the QR code by **270 degrees**.

These rules ensure that the QR code is always presented in the correct orientation for further processing.
## Reflection
## Formate Info Validation
## Encoding Modes
## V4
