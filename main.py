import cv2
import qr_detector as detector
import os

test_cases = [
    'CSE483 Sp24 Project Test Cases/01-Getting-started.png',
    'CSE483 Sp24 Project Test Cases/02-Matsawar-3edel-ya3am.png',
    'CSE483 Sp24 Project Test Cases/03-Leffy-bina-ya-donya.png',
    'CSE483 Sp24 Project Test Cases/06-Railfence-cipher.png',
    'CSE483 Sp24 Project Test Cases/07-THE-MIGHTY-FINGER.png',
    'CSE483 Sp24 Project Test Cases/15-beast-mode-computer-vision-(this-one-is-from-wikipedia).jpg',
    'CSE483 Sp24 Project Test Cases/16-V3-QR-Code...-can-you-do-it.png'
]

for image_path in test_cases:
    frame = cv2.imread(image_path)
    frame_resized = cv2.resize(frame, (600, 600))
    output_image = detector.detect(frame_resized)

    test_case_number = os.path.basename(image_path).split('-')[0]
    cv2.imwrite(f'test_results/{test_case_number}-result.png', output_image)

    cv2.imshow(f"Output Image {test_case_number}", output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

