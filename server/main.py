from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import io
import numpy as np
import cv2
import json
import zipfile
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
from matplotlib import pyplot as plt

from Code.AlgorithmsForClassification.allAlgorithm import eye_classification, nose_classification, mouth_classification
from Code.help_function import detect_and_crop_faces, get_facial_key_points, eyebrow_classification, jaw_classification, \
    extract_attribute, pointOnThePicture

app = Flask(__name__)
CORS(app)

def convert_to_list(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        print('File received:', file.filename)

        # Ensure the file is read correctly
        try:
            file_content = file.read()
            img = Image.open(io.BytesIO(file_content)).convert('RGB')
        except Exception as e:
            print('Error processing image:', str(e))
            return jsonify({'error': 'Failed to process image file'}), 400

        # Save the uploaded file temporarily
        img_path = os.path.join(UPLOAD_FOLDER, 'temp_image.jpg')
        img.save(img_path)

        faces = detect_and_crop_faces(img_path)
        analysis_results = []
        face_images = []

        if not faces:
            return jsonify({'error': 'No faces detected'}), 400

        for idx, face in enumerate(faces):
            key_points = get_facial_key_points(face / 255)
            face_points_img = pointOnThePicture(face, key_points)
            eyebrow_class = eyebrow_classification(key_points[24:44])  # 20
            eye_class = eye_classification(key_points[0:24])  # 24
            nose_class = nose_classification(key_points[118:137])  # 18
            mouth_class = mouth_classification(key_points[78:118])  # 40
            jaw_class = jaw_classification(key_points[44:78])  # 34

            eyebrow = extract_attribute("גבות", eyebrow_class)
            eye = extract_attribute("עיניים", eye_class)
            nose = extract_attribute("אף", nose_class)
            mouth = extract_attribute("פה", mouth_class)
            jaw = extract_attribute("פנים", jaw_class)

            print("Eyebrow Analysis:", eyebrow)
            print("Eye Analysis:", eye)
            print("Nose Analysis:", nose)
            print("Mouth Analysis:", mouth)
            print("Jaw Analysis:", jaw)

            face_analysis = {
                "name": "גבות",
                "features": {
                    "name": convert_to_list(eyebrow_class),
                    "analysis": convert_to_list(eyebrow)
                }
            }

            eye_analysis = {
                "name": "עיניים",
                "features": {
                    "name": convert_to_list(eye_class),
                    "analysis": convert_to_list(eye)
                }
            }

            nose_analysis = {
                "name": "אף",
                "features": {
                    "name": convert_to_list(nose_class),
                    "analysis": convert_to_list(nose)
                }
            }

            mouth_analysis = {
                "name": "פה",
                "features": {
                    "name": convert_to_list(mouth_class),
                    "analysis": convert_to_list(mouth)
                }
            }

            jaw_analysis = {
                "name": "לסת",
                "features": {
                    "name": convert_to_list(jaw_class),
                    "analysis": convert_to_list(jaw)
                }
            }

            analysis_results.append({
                "eyebrow_analysis": face_analysis,
                "eye_analysis": eye_analysis,
                "nose_analysis": nose_analysis,
                "mouth_analysis": mouth_analysis,
                "jaw_analysis": jaw_analysis
            })

            # Save the modified face image
            modified_img_path = os.path.join(UPLOAD_FOLDER, f'modified_image_{idx}.jpg')
            cv2.imwrite(modified_img_path, face_points_img)
            face_images.append(modified_img_path)

        # Save the analysis results as a JSON file
        analysis_json_path = os.path.join(UPLOAD_FOLDER, 'analysis_results.json')
        with open(analysis_json_path, 'w') as json_file:
            json.dump({'result': analysis_results}, json_file)

        # Create a zip file containing all the images and the JSON file
        zip_path = os.path.join(UPLOAD_FOLDER, 'result.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for img_path in face_images:
                zipf.write(img_path, os.path.basename(img_path))
            zipf.write(analysis_json_path, os.path.basename(analysis_json_path))

        return send_file(zip_path, mimetype='application/zip')

    except ValueError as e:
        print('ValueError:', str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print('Exception:', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/send-mail', methods=['POST'])
def send_email_image():
    try:
        to_mail = request.form.get('to_mail')
        name = request.form.get('name')
        image_data_list = [request.form.get(f'image{i}') for i in range(10)]  # Adjust range as needed

        if not to_mail or not image_data_list:
            return jsonify({"error": "Missing data"}), 400

        # Prepare the email
        sender_email = "resultsFaces@gmail.com"
        receiver_email = to_mail

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Face2Fate - תוצאות ניתוח אשיות"

        body = f"שלום {name},\n\nתודה שהייתם איתנו!😊" if name else "שלום,\n\nתודה שהייתם איתנו!😊"
        msg.attach(MIMEText(body, 'plain'))

        for i, image_data in enumerate(image_data_list):
            if image_data:
                try:
                    # Decode the image data
                    image_data = image_data.split(",")[1]
                    image_bytes = base64.b64decode(image_data)
                    image_stream = io.BytesIO(image_bytes)

                    # Attach the image
                    img = MIMEImage(image_stream.read())
                    img.add_header('Content-Disposition', 'attachment', filename=f'image{i+1}.jpg')
                    msg.attach(img)
                except Exception as e:
                    print(f"Error processing image data: {e}")

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = "resultsFaces@gmail.com"
        smtp_password = "gpxd ksyi aemd tzqw"  # Replace with the actual password

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            return jsonify({"message": "Email sent successfully!"}), 200
        except Exception as e:
            print(f"Failed to send email: {e}")
            return jsonify({"error": f"Failed to send email: {str(e)}"}), 500

    except Exception as e:
        print(f"Exception in send_email_image: {e}")
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
