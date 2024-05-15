# Computer_Vision_QR_Reader
CSE 483: Computer Vision QR Reader

The goal of the project is to be able to decode given samples of QR codes with a robust and reliable image processing pipeline using only classical vision algorithms to implement the QR code standard in ISO/IEC 18004. 

# Video

![]()

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
Based on the fact that (after thresholding) Most of the QR code body will be black while the rest of the image is white, If the QR code resides in a small part of the image then its surroundings are white, the detection algorithm needs the QR code to take most of the space in the image (to be able to detect edges and corners clearly) so we need to cut the useless giant white border around the 
## detecting QR Code Frame 
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

# Format Information Correction and Validation

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

## V4

# References