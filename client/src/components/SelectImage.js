import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import JSZip from 'jszip';
import { RingLoader } from 'react-spinners'; // ניתן להשתמש בספריה להוספת אנימציות

const FileUploadPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [originalImageSrc, setOriginalImageSrc] = useState(null);
  const [cameraStream, setCameraStream] = useState(null);
  const [cameraImageSrc, setCameraImageSrc] = useState(null);
  const [loading, setLoading] = useState(false); // מצב להראות את האנימציה
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    return () => {
      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
      }
    };
  }, [cameraStream]);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);

    const reader = new FileReader();
    reader.onload = (e) => {
      setOriginalImageSrc(e.target.result);
    };
    reader.readAsDataURL(file);
  };

  const handleClick = async () => {
    if (!selectedFile) {
      alert('Please select an image file first.');
      return;
    }

    setLoading(true); // הפעלת האנימציה

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob',
      });

      const zip = new JSZip();
      const zipContent = await zip.loadAsync(response.data);

      const imageFiles = zipContent.file(/modified_image_\d+\.jpg/);
      const jsonFile = zipContent.file('analysis_results.json');

      if (imageFiles.length > 0 && jsonFile) {
        const imageUrls = await Promise.all(
          imageFiles.map(async (imageFile) => {
            const imageBlob = await imageFile.async('blob');
            return URL.createObjectURL(imageBlob);
          })
        );

        const jsonText = await jsonFile.async('string');
        const analysisData = JSON.parse(jsonText);

        navigate('/analysis', { state: { originalImageSrc, processedImageSrc: imageUrls, analysisResults: analysisData.result } });
      } else {
        alert('No processed images or analysis results found.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload and process file');
    } finally {
      setLoading(false); // סיום האנימציה
    }
  };

  const handleCameraClick = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      setCameraStream(stream);

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
    } catch (error) {
      console.error('Error accessing camera:', error);
      alert('Failed to access camera. Make sure your camera is connected and not being used by another application.');
    }
  };

  const handleCapture = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      canvasRef.current.width = videoRef.current.videoWidth;
      canvasRef.current.height = videoRef.current.videoHeight;
      context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
      const imageSrc = canvasRef.current.toDataURL('image/jpeg');
      setCameraImageSrc(imageSrc);

      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        setCameraStream(null);
      }
    }
  };

  const handleSendCameraImage = async () => {
    if (!cameraImageSrc) {
      alert('Please capture an image first.');
      return;
    }

    setLoading(true); // הפעלת האנימציה

    const response = await fetch(cameraImageSrc);
    const blob = await response.blob();

    const formData = new FormData();
    formData.append('file', blob, 'captured_image.jpg');

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob',
      });

      const zip = new JSZip();
      const zipContent = await zip.loadAsync(response.data);

      const imageFiles = zipContent.file(/modified_image_\d+\.jpg/);
      const jsonFile = zipContent.file('analysis_results.json');

      if (imageFiles.length > 0 && jsonFile) {
        const imageUrls = await Promise.all(
          imageFiles.map(async (imageFile) => {
            const imageBlob = await imageFile.async('blob');
            return URL.createObjectURL(imageBlob);
          })
        );

        const jsonText = await jsonFile.async('string');
        const analysisData = JSON.parse(jsonText);

        navigate('/analysis', { state: { originalImageSrc: cameraImageSrc, processedImageSrc: imageUrls, analysisResults: analysisData.result } });
      } else {
        alert('No processed images or analysis results found.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload and process file');
    } finally {
      setLoading(false); // סיום האנימציה
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#000000' }}>
      <div style={{ color: 'white', textAlign: 'center', marginBottom: '20px' }}>
        <h2>הוראות לצילום והעלאת תמונה:</h2>
        <p>כדי שנוכל לנתח את תכונות האופי שלך בצורה מיטבית, יש להקפיד על ההנחיות הבאות:</p>
        <ul>
          <li>הסר משקפיים: נא להצטלם או להעלות תמונה ללא משקפיים.</li>
          <li>לא לחייך: שמרו על פנים נייטרליות ללא חיוך.</li>
          <li>בלי איפור: הימנעו מאיפור לצורך דיוק בזיהוי.</li>
          <li>תמונה ישרה: ודאו שהתמונה מצולמת בצורה ישרה וברורה, כשאתם מביטים ישירות למצלמה.</li>
        </ul>
        <p>תודה על שיתוף הפעולה!</p>
      </div>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        style={{
          marginBottom: '20px',
          padding: '10px',
          fontSize: '16px',
          color: 'white',
          backgroundColor: '#f78605',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      />
      <button
        onClick={handleClick}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          color: 'white',
          backgroundColor: '#f78605',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        שליחה
      </button>
      <button
        onClick={handleCameraClick}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          color: 'white',
          backgroundColor: '#f78605',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginTop: '20px',
        }}
      >
        פתיחת מצלמה
      </button>
      {cameraStream && (
        <>
          <video
            ref={videoRef}
            style={{
              width: '320px',
              height: '240px',
              backgroundColor: 'black',
              marginTop: '20px',
            }}
          ></video>
          <button
            onClick={handleCapture}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              color: 'white',
              backgroundColor: '#f78605',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              marginTop: '20px',
            }}
          >
            לכידת התמונה
          </button>
          <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
          {cameraImageSrc && (
            <div>
              <img
                src={cameraImageSrc}
                alt="Captured"
                style={{ width: '320px', height: '240px', marginTop: '20px' }}
              />
              <button
                onClick={handleSendCameraImage}
                style={{
                  padding: '10px 20px',
                  fontSize: '16px',
                  color: 'white',
                  backgroundColor: '#f78605',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  marginTop: '20px',
                }}
              >
                שליחת התמונה
              </button>
            </div>
          )}
        </>
      )}
      {loading && (
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          position: 'fixed',
          top: '0',
          left: '0',
          right: '0',
          bottom: '0',
          backgroundColor: 'rgba(0, 0, 0, 0.80)', // שינוי הצבע כאן, חצי שקוף כהה
          color: 'white',
          fontSize: '18px',
          zIndex: '1000',
        }}>
          <div style={{ textAlign: 'center' }}>
            <RingLoader color="#f78605" />
            <p>התמונה נשלחה לפיענוח אנא המתן...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUploadPage;
