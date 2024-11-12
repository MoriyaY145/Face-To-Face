import dlib
import cv2
import numpy as np
import pymongo
from Code.model_loader import model_cnn, scaler_eyebrow, model_eyebrow, scaler_jaw, model_jaw

# Define MongoDB client and collection
client = pymongo.MongoClient(
    "mongodb+srv://moriya0556796269:iRBJbjSB9Ywk6SGz@cluster0.wnesgpm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["face2fateHeb"]
col = db["face_regions"]


def resize_image_with_margins(image, target_size=(64, 64), background_color=(255, 255, 255), save_path=None):
    # Get original image size
    original_height, original_width, _ = image.shape
    original_aspect_ratio = original_width / original_height

    # Calculate the aspect ratio of the target size
    target_aspect_ratio = target_size[0] / target_size[1]

    # Calculate the size of the resized image while preserving the aspect ratio
    if original_aspect_ratio > target_aspect_ratio:
        # Original image is wider than the target size, so resize based on width
        new_width = target_size[0]
        new_height = int(new_width / original_aspect_ratio)
    else:
        # Original image is taller than the target size, so resize based on height
        new_height = target_size[1]
        new_width = int(new_height * original_aspect_ratio)

    # Resize the image
    resized_img = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

    # Calculate the margins
    top = (target_size[1] - new_height) // 2
    bottom = target_size[1] - new_height - top
    left = (target_size[0] - new_width) // 2
    right = target_size[0] - new_width - left

    # Add margins using cv2.copyMakeBorder
    resized_img_with_margins = cv2.copyMakeBorder(resized_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=background_color)

    # Save the resized image if save_path is provided
    if save_path:
        cv2.imwrite(save_path, resized_img_with_margins)

    return resized_img_with_margins


def detect_and_crop_faces(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialize dlib's face detector (HOG-based)
    detector = dlib.get_frontal_face_detector()

    # Detect faces in the image
    faces = detector(gray, 1)

    # Get the dimensions of the original image
    height, width, _ = image.shape

    # Filter faces that are too small
    faces = [face for face in faces if face.width() > (0.06 * width) and face.height() > (0.06 * height)]

    cropped_faces = []
    for i, face in enumerate(faces):
        # Get the coordinates of the face rectangle
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())

        # Extract the region of interest (ROI) corresponding to the face
        face_roi = image[y:y + h, x:x + w]

        # Resize the face ROI to 64x64 pixels
        face_roi_resized = resize_image_with_margins(face_roi)

        # Add the resized face to the list of cropped faces
        cropped_faces.append(face_roi_resized)

    return cropped_faces


def get_facial_key_points(face):
    face_batch = np.expand_dims(face, axis=0)
    key_points = model_cnn.predict(face_batch)
    return key_points[0]

def pointOnThePicture(visualization_image, points):
    visualization_image = cv2.resize(visualization_image, (500, 500))
    for iEyes in range(12):
         x = int(points[iEyes])
         y = int(points[iEyes + 12])
         cv2.circle(visualization_image, (x, y), 2, (255, 0, 0), -1)
    for iEyebrow in range(24, 34):
         x = int(points[iEyebrow])
         y = int(points[iEyebrow + 10])
         cv2.circle(visualization_image, (x, y), 2, (255, 0, 0), -1)
    for iJaw in range(44, 61):
         x = int(points[iJaw])
         y = int(points[iJaw + 17])
         cv2.circle(visualization_image, (x, y), 2, (255, 0, 0), -1)
    for iMouth in range(78, 98):
         x = int(points[iMouth])
         y = int(points[iMouth + 20])
         cv2.circle(visualization_image, (x, y), 2, (255, 0, 0), -1)
    for iNose in range(118, 127):
         x = int(points[iNose])
         y = int(points[iNose + 9])
         cv2.circle(visualization_image, (x, y), 2, (255, 0, 0), -1)
    return visualization_image


def eyebrow_classification(points_eyebrow):
    # Reshape input array to 2D (assuming it represents a single sample with multiple features)
    points_eyebrow = np.array(points_eyebrow).reshape(1, -1)
    x_new_scaled = scaler_eyebrow.transform(points_eyebrow)
    # Make predictions
    classification = model_eyebrow.predict(x_new_scaled)
    if classification == 'Straight':
        return 'ישרות'
    if classification == 'Arch':
        return 'קשתיות'
    return 'מעגליות'


def jaw_classification(points_jaw):
    points_jaw = np.array(points_jaw).reshape(1, -1)
    points_jaw = scaler_jaw.transform(points_jaw)
    classification = model_jaw.predict(points_jaw)

    # # Convert predictions to class labels
    classification = classification.argmax(axis=1)

    if classification[0] == 0:
        return "מעגליות"
    elif classification[0] == 1:
        return "סגלגליות"
    elif classification[0] == 2:
        return "מרובעות"
    elif classification[0] == 3:
        return "משולשות"

    return classification


# Function to extract attribute analysis based on classification
def extract_attribute(classification_name, feature_name):
    result = col.find_one({"name": classification_name})
    if result:
        features = result["features"]
        for feature in features:
            if feature["name"] == feature_name:
                return feature["analysis"]
    return "Analysis not found"


