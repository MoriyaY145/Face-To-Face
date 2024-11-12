import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import axios from 'axios';
import html2canvas from 'html2canvas';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const ImageAnalysisPage = () => {
  const location = useLocation();
  const { originalImageSrc, processedImageSrc, analysisResults } = location.state || {};

  const [modalOpen, setModalOpen] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const handleOpenModal = () => setModalOpen(true);
  const handleCloseModal = () => {
    setModalOpen(false);
    setName('');
    setEmail('');
    setEmailError('');
    setResponseMessage('');
  };

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  };

  const handleSendMail = async () => {
    if (!validateEmail(email)) {
      setEmailError('כתובת אימייל לא חוקית');
      return;
    }

    const images = [];
    for (let i = 0; i < analysisResults.length; i++) {
      const canvas = await html2canvas(document.querySelector(`#capture-${i}`));
      const image = canvas.toDataURL("image/jpeg");
      images.push(image);
    }

    const formData = new FormData();
    formData.append('to_mail', email);
    formData.append('name', name || ''); // אם השם ריק, יוכנס ערך ריק
    images.forEach((image, index) => {
      formData.append(`image${index + 1}`, image);
    });

    try {
      const response = await axios.post('http://127.0.0.1:5000/send-mail', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if (response.status === 200) {
        setResponseMessage('ההודעה נשלחה בהצלחה!');
        setTimeout(() => {
          handleCloseModal(); // Close modal after 2 seconds
        }, 2000); // 2 seconds delay
      } else {
        setResponseMessage('שליחת המייל נכשלה. אנא נסה שוב.');
        setTimeout(() => {
          handleCloseModal(); // Close modal after 2 seconds
        }, 2000); // 2 seconds delay
      }
    } catch (error) {
      console.error('Failed to send email:', error);
      setResponseMessage('שליחת המייל נכשלה. אנא נסה שוב.');
      setTimeout(() => {
        handleCloseModal(); // Close modal after 2 seconds
      }, 2000); // 2 seconds delay
    }
  };

  return (
    <div style={{ paddingTop: '60px', display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: 'black', color: 'white', flexDirection: 'column' }}>
      {analysisResults && analysisResults.map((result, index) => (
        <div id={`capture-${index}`} key={index} style={{ textAlign: 'center', backgroundColor: 'black', color: 'white', width: '100%', marginBottom: '40px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px' }}>
            {originalImageSrc && (
              <img src={originalImageSrc} alt="Original" style={{ width: '200px', height: 'auto', marginRight: '10px' }} />
            )}
            <div style={{ margin: '0 10px' }}>
              <strong>←</strong>
            </div>
            {processedImageSrc && (
              <img src={processedImageSrc[index]} alt="Processed" style={{ width: '200px', height: 'auto', marginRight: '10px' }} />
            )}
            <div style={{ margin: '0 10px' }}>
              <strong>←</strong>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <table style={{ borderCollapse: 'collapse', width: '300px', backgroundColor: 'white', color: 'black', margin: '10px 0' }}>
                <thead>
                  <tr>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Feature</th>
                    <th style={{ border: '1px solid black', padding: '10px' }}>Classification</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style={{ border: '1px solid black', padding: '10px' }}>פנים</td>
                    <td style={{ border: '1px solid black', padding: '10px' }}>{result.jaw_analysis.features.name}</td>
                  </tr>
                  <tr>
                    <td style={{ border: '1px solid black', padding: '10px' }}>עיניים</td>
                    <td style={{ border: '1px solid black', padding: '10px' }}>{result.eye_analysis.features.name}</td>
                  </tr>
                  <tr>
                    <td style={{ border: '1px solid black', padding: '10px' }}>גבות</td>
                    <td style={{ border: '1px solid black', padding: '10px' }}>{result.eyebrow_analysis.features.name}</td>
                  </tr>
                  <tr>
                    <td style={{ border: '1px solid black', padding: '10px' }}>פה</td>
                    <td style={{ border: '1px solid black', padding: '10px' }}>{result.mouth_analysis.features.name}</td>
                  </tr>
                  <tr>
                    <td style={{ border: '1px solid black', padding: '10px' }}>אף</td>
                    <td style={{ border: '1px solid black', padding: '10px' }}>{result.nose_analysis.features.name}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div style={{ color: 'white', textAlign: 'right', width: '70%', margin: '0 auto' }}>
            <h2>ניתוח אישיות:</h2>
            <ul>
              <li><strong>פנים:</strong> {result.jaw_analysis.features.analysis}</li>
              <li><strong>עיניים:</strong> {result.eye_analysis.features.analysis}</li>
              <li><strong>גבות:</strong> {result.eyebrow_analysis.features.analysis}</li>
              <li><strong>פה:</strong> {result.mouth_analysis.features.analysis}</li>
              <li><strong>אף:</strong> {result.nose_analysis.features.analysis}</li>
            </ul>
          </div>
        </div>
      ))}
      <Button variant="contained" style={{ marginTop: '20px', backgroundColor: '#f78605' }} onClick={handleOpenModal}>
        שליחה למייל
      </Button>
      <Modal
        open={modalOpen}
        onClose={handleCloseModal}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            שליחה למייל
          </Typography>
          <TextField
            label="שם"
            fullWidth
            margin="normal"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <TextField
            label="כתובת אימייל"
            fullWidth
            margin="normal"
            type="email"
            required
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setEmailError('');
            }}
            error={!!emailError}
            helperText={emailError}
          />
          <Button variant="contained" style={{ backgroundColor: '#f78605' }} onClick={handleSendMail}>
            לשליחה
          </Button>
          {responseMessage && (
            <Typography variant="body1" style={{ marginTop: '20px', color: responseMessage.includes('בהצלחה') ? 'green' : 'red' }}>
              {responseMessage}
            </Typography>
          )}
        </Box>
      </Modal>
    </div>
  );
};

export default ImageAnalysisPage;
