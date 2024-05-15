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
