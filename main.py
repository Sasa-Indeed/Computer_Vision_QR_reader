import cv2
import qr_detector as detector

image_path = 'CSE483 Sp24 Project Test Cases/01-Getting-started.png'

frame = cv2.imread(image_path)
frame_resized = cv2.resize(frame, (600, 600))
output_image = detector.detect(frame_resized)

# Save the output image with detected QR code
cv2.imwrite('test_results/01-result.png', output_image)

# Display the output image
cv2.imshow("Output Image", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
