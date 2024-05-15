# Computer_Vision_QR_Reader
CSE 483: Computer Vision QR Reader

The goal of the project is to be able to decode given samples of QR codes with a robust and reliable image processing pipeline using only classical vision algorithms to implement the QR code standard in ISO/IEC 18004. 

# Video


https://github.com/Sasa-Indeed/Computer_Vision_QR_reader/assets/28220731/e9f30acc-2742-4c42-90c5-67dd6352263e


# Our Approach
## Skewed Image histograms
We noticed that some images have their histograms positively skewed or negatively skewed with their values mainly in only one half of the pixel ranges, for exampl an image that has pixel values that are all under 127, or the other way around, so we tested for this and applied histogram equalization on all images that match this criteria.
## Remove anomaly frequencies
To remove anomaly frequencies, we first calculate the average of the magnitudes of the frequencies and then we zero out any frequency that has a magnitude larger than the average multiplied by some factor that have been determined by trial and error, 3 seems to work for the test cases in our mini universe, we also added a condition to add a factor to the average if the average is less than 1, however this case doesn't occur in this mini universe
## Remove salt and pepper noise
Salt and pepper noise can be seen as high frequency noise, which means that we can check the average of the magnitude spectrum, if noise and pepper exists then the average of the spectrum will be much higher than the test cases in this universe, so if the average of the spectrum is higher than a specific value, that is determined by analysing the average of all test cases, then low pass filter is applied to the image since as mentioned before salt and pepper noise is just high frequency noise so we can just eliminate the high frequencies.
## Inversion
Once again we test for the average but this time the average of the image pixel values not the frequency magnitude spectrum, since we know the QR code is almost half and hald black and white and white is more dominante than the black, we know the average is going to be somewhere around the 127 mark, so we could say that if the image is inverted the average would be below the 127 mark, so we test for the pixel value average and if it matches the condition we bitwise not the image
## Making sure the images are binary
Now that we have applied all the fixes that we have, it's time to make sure the image is binary via thresholding, we choose 100 because at this point we are sure that the important parts of the QR code are almost perfectly black meaning near zero and we want anything that is not strongly black to be white so we choose 100.
## Capturing the good part!
Based on the fact that (after thresholding) Most of the QR code body will be black while the rest of the image is white, If the QR code resides in a small part of the image then its surroundings are white, the detection algorithm needs the QR code to take most of the space in the image (to be able to detect edges and corners clearly) so we need to cut the useless giant white border around the QR code.
1- Perform closing with small kernel (10x10 as smaller will be ineffective and larger will erase the QR code itself it it is small in the image) to fill any black noise outside the QR code (shadows and such)
2- Find the first black pixel in each row and column and crop the image to the smallest rectangle that contains all the black pixels.
3.1- If the borders are close to the image original borders (The threshold is 80% to represent that the QR code is dominating the image) then no need for capturing, the QR is already filling the image.
3.2- Else, crop the image while adding a margin to work like a quiet zone for the QR code.
4- Resize the image to its original size.
## Tilt Correction
This will work on images that just needs slight rotation (no prespective)
1- Find the angle of rotation needed to make the QR code horizontal: we calculate the angle of the line connecting the top left and top right corners of the QR code with the horizontal line.
1.1- Perform Canny edge detection on the blob image: upper and lower thresholds are 50 and 150 respectively, this was fine-tuned so that only the 4 main edges of the QR code (and any big noises) are detected and any other noises (from inclined edges having zigzag effect) are considered weak edges and are not detected.
1.2- Perform Hough Line Transform on the Canny image: we set the threshold to 70 which barely captures weak edges, any lower, and it will start capturing noisy edges, any higher, and it may fail to capture the real edges.
1.3- If more than 130 angles found this means the image tilting can't be corrected here or it needs straightening: later step.
1-4- filter the edges that should have angle of 0 (or 180) (between -45 and 45 and between 135 and 225)
1.5- Calculate median of the angles found, this will have general approximation of the angle of the QR code as noises will cansel each other (similar to the concept of salt and pepper).
2- If the angle is less than 5 degrees, then no need for rotation as it can be tolerated by the decoder.
3- Rotate the image by the calculated angle.
## detecting QR Code Frame
In this step we find the frame of the QR code and stretching it into a square shape covering the whole image if needed.
1- Pad the image with white border (big kernel but not big enough to revert the capturing stage), this is to make sure after all previous steps the QR code is not near the border.
2- Do opening on the padded image with large kernel (100x100): this will fill the white blocks inside the QR code and transform the QR code into a single black blob.
Why did we do that? because we want to detect the 4 corners of the QR code and this is ineffective since the QR code modules (small boxes composing it) are full of corners! that's why we need to make the QR code a single black blob so that its real corners are more visible and the other fake corners inside it vanish (that justifies the 100x100 padding so that opening doesn't cause the QR code to kill the quiet zone).
Both Harris Corner detection and Contour detection failed to detect the corners of the QR code, the reason is that even after making the QR code one big black blob, if the QR code edges are inclined then the resulting blob will not be a smooth square (thus fake corners not entirely eradicated), so we had to come up with a new method to detect the corners of the QR code.
3- Perform Canny edge detection on the blob image: upper and lower thresholds are 200 and 100 respectively, this was fine-tuned so that only the 4 main edges of the QR code (and any big noises) are detected and any other noises (from inclined edges having zigzag effect) are considered weak edges and are not detected.
4- Perform Hough Line Transform on the Canny image: we set the threshold to 100 which barely captures weak edges (like those of BANANAAA), any lower, and it will start capturing noisy edges, any higher, and it may fail to capture the real edges.
5- Find the lines that make the least difference in angel with 0 and 90 degrees: As the earlier steps might produce many borders for inclined and zoomed QR codes, we need to filter out the fake borders and keep the real ones, so we calculate the angle of each line with 0 and 90 degrees and keep the ones that are the closest to these angles.
![img.png](img.png)
Now we got 4 clear lines that represent the QR code frame, but they are not the corners of the QR code, they are the lines that the corners lie on, so we need to find the corners themselves.
6- Harris Corner detection: we perform Harris Corner detection on the Canny image with a small block size (3) and a small ksize (3), this will detect the corners of the QR code, the parameters won't make a big difference here, we already preprocessed the image very well.
7- Filter the found corners: remove corners that are:
7.1- Weak corners: corners that have a low response value (less than 0.5 of the maximum response value, this value was fine-tuned to filter out the fake corners and keep the real ones that may be weaker than the strongest of them).
7.2- Close corners: corners that are too close to each other (in the same quarter), this is to filter out multiple corners generated from a single corner spanning on multiple pixels.
8- Sort found corners in the order: top left, top right, bottom left, bottom right.
9- Find if the QR code needs straightening: if the any corner is farther than 200 pixels (this threshold means lines making more than 10 degrees difference from 0/90) from the edge of the image (even after capturing) this means that corners are likely not forming horizontal/vertical lines with each other as the other cornerl will be really close to the edge (around 100 pixel difference), thus needs straightening.
10- Straighten the QR code: if the QR code needs straightening, we rotate the image so that the corners are horizontal/vertical with each other.
11- Resize into 1050 x 1050: which is 50x21 x 50x21, 50x50 modules and 21x21 pixels per module.
Long process but never failed with the 19 TCs we tested on.

# QR Code Orientation Detection

![image](https://github.com/Sasa-Indeed/Computer_Vision_QR_reader/assets/105253730/6954d6ac-4c42-4bf8-a343-cd2d86642dc8)

Our approach to detecting the orientation of a QR code is based on the unique pattern of the locator boxes, which follows a 1:1:3:1:1 ratio. This pattern allows us to determine whether the QR code is rotated or in its correct orientation.

## Methodology

We focus on the fourth corner of the QR code. If the unique pattern exists in both the designated row and column of this corner, we deduce that the QR code is rotated. If not, the QR code is in the correct orientation.

To account for potential variations, we have incorporated a tolerance margin. We check the mean of the values in a single grid cell and consider the pattern to exist if the corresponding value from the pattern matches that of the grid cells we check.

## Reflection
The problem with reflection on y-axis is that we need to differentiate between it and 90-degree rotation, one solution would be to rotate the image by 90 degrees, and check the FEC data on the top left and right locators, if they match then it was rotated by 90 degrees if not invert the rotation and try reflecting it on the y-axis if they match then it was reflected if not then the FEC might be corrupted or the ECL or the MASK are corrupted.  

## Rotation Rules

Based on the existence of the pattern in the corners, we apply the following rotation rules:

- If the pattern exists in the fourth corner (bottom right corner), the bottom left, and the top right (test case 3), we rotate the QR code by **180 degrees**.
- If the pattern exists in the fourth corner and bottom left only, we rotate the QR code by **90 degrees**.
- If the pattern exists in the fourth corner and top right only, we rotate the QR code by **270 degrees**.

These rules ensure that the QR code is always presented in the correct orientation for further processing.

# Format Information Correction and Validation

![image](https://github.com/Sasa-Indeed/Computer_Vision_QR_reader/assets/105253730/5143b9b7-f80d-4262-a2fa-456f2edcb1b5)

This section outlines our approach to correcting and validating the format information in QR codes. Our method is designed to handle cases where the top left locator is damaged, which is a common issue in many test cases.

## Reading Location Adjustment

We have adjusted the location from where we read the format information. Instead of the usual location, we now read from the second location, which is beside the bottom locator (specifically column 8) and the top right locator (row 8). More details about the exact locations of the format information bits are provided in the code.

## Damage Correction

If the format information is damaged, we can correct it by performing a lookup of all 32 combinations of valid format information strings. The extended format information is acquired through the first 5 bits, which include 2 bits for the error correction level and 3 bits for the mask.

## Validation Process

If we get a perfect match with one of the 32 valid format information strings, then the format information is returned with no change. If not, we check to see the string that has the minimum Hamming distance from the string acquired from the image (the faulty one), and that string is returned instead.

For more information about how the 32 valid format information strings were formed, please refer to the ISO/IEC 18004:2015 standard on Automatic Identification and Data Capture Techniques — QR Code bar code symbology specification. This standard provides a comprehensive guide to the structure and encoding of QR codes.
# Decoding Alphanumeric V1 QR Codes

This section outlines our method for decoding alphanumeric V1 QR codes. The process involves reading the data in a specific order, checking the encoding, and converting binary data to alphanumeric characters.

## Encoding Check

The first step is to check the encoding. If the encoding is `[0,0,1,0]`, the QR code is recognized as alphanumeric.

## Length Determination

Next, we read the following 9 bits to determine the length of the data. For each pair of characters read, we decrement the length by 2.

## Character Reading

Each pair of characters is read by transforming 11 bits into an integer. This integer is then checked against the `ALPHANUMERIC_TABLE` to obtain the corresponding alphanumeric characters.

# Binary to Alphanumeric Conversion

In the process of decoding alphanumeric V1 QR codes, we utilize a predefined table, referred to as the `ALPHANUMERIC_TABLE`. This table is a dictionary that maps integers to their corresponding alphanumeric characters, including digits (0-9), uppercase letters (A-Z), and some special characters (like space, $, %, *, +, -, ., /, :).

When converting binary data to alphanumeric characters, we follow these steps:

1. **Binary to Integer**: We first convert the binary string to an integer. For example, a binary string '1101' would be converted to the integer 13.

2. **Integer to Alphanumeric**: We then map this integer to two alphanumeric characters using the `ALPHANUMERIC_TABLE`. This is done in two steps:
    - We divide the integer by 45 (the size of the `ALPHANUMERIC_TABLE`) to get the first number. This number is then mapped to the first character.
    - We find the remainder of the integer when divided by 45 to get the second number. This number is then mapped to the second character.

This process is similar to saying that 78 equals 7 * 10 + 8. If we're encoding alphanumeric characters, for example, 'TH' (where T is 29 and H is 17 in the `ALPHANUMERIC_TABLE`), we would get the binary string by converting 29 * 45 + 17 to binary.

## Handling Odd Lengths

If the length of the data is odd, the last character is read using only 6 bits. This is because we normally decrement the length by two for each pair of characters read. Therefore, if the length is 1, it indicates that the original length was odd.

# Decoding Version 4 QR Codes

![image](https://github.com/Sasa-Indeed/Computer_Vision_QR_reader/assets/105253730/8f4557d8-dc22-460f-8631-050fced9b983)
from the image above we figured out the new directions we needed to decode higher versions


This section outlines our approach to decoding Version 4 QR codes. The process involves adding more directions, reading the data in a specific order, and converting binary data to ASCII characters.

## Adding Directions

The first step in decoding Version 4 QR codes is to add more directions that are suitable for higher-order versions of QR codes. This ensures that we can accurately navigate and read the data in these more complex codes.

## Reading Data

Next, we proceed to read the data by applying the data indices that are specific to a Version 4 QR code. This includes specifying the row, column, and direction in which each data byte should be read. This step is crucial for ensuring that we correctly interpret the data in the QR code.

## Concatenating Bytes

After reading the data, we concatenate all the bytes to form a single binary string. From this string, we exclude the encoding bits and the length.

## Binary to ASCII Conversion

Finally, we read the binary string 8 bits at a time, converting each 8-bit segment to an integer and then to an ASCII character. This step transforms the binary data into a human-readable format.

By following these steps, we can accurately decode Version 4 QR codes, regardless of their complexity or orientation. This method ensures that the QR code data is always presented in the correct format for further processing.

# References
- [ISO IEC 18004 2015 Standard](https://raw.githubusercontent.com/yansikeim/QR-Code/master/ISO%20IEC%2018004%202015%20Standard.pdf)
- [Module Placement Matrix](https://www.thonky.com/qr-code-tutorial/module-placement-matrix#:~:text=The%20timing%20patterns%20are%20two,QR%20code%20between%20the%20separators)
- [Alphanumeric Table](https://www.thonky.com/qr-code-tutorial/alphanumeric-table)
- [Data Encoding](https://www.thonky.com/qr-code-tutorial/data-encoding)
- [Error Correction Coding](https://www.thonky.com/qr-code-tutorial/error-correction-coding)
- [Format Version Information](https://www.thonky.com/qr-code-tutorial/format-version-information#:~:text=format%20string%20table.-,Generate%20the%20Format%20String,generate%20ten%20error%20correction%20bits.)

