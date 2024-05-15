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
## Rotation
 the fact that the locator pattern has a unique boxes has a jIn order to detect unique pattern which is 1:1:3:1:1 from that we deduced that we just need to check on the fourth corner of the qr code if the pattern exists in both the designated row and column then the qr code is rotated if not then it's in the fight orientation.
Moreover,
if the pattern exists in the fourth corner (bottom right corner), t eabottom left and the top right (test case 3) then rotate by 180 degrees
if the pattern exists in the fourth corner and bottom left only 
then rotate by 90 degrees
if the pattern exists in the fourth corner and top right only
then rotate by 270 degrees

 QR code is rotated we utilize
## Reflection
## Formate Info Validation
## Encoding Modes
## V4

# References