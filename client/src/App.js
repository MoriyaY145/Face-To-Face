import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, Link } from 'react-router-dom';
import HomePage from './components/homePage';
import FileUploadPage from './components/SelectImage';
import AboutUs from './components/AboutUs';
import ImageAnalysisPage from './components/ImageAnalysisPage';
import './App.css';

const App = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul className="navbar">
            <li>
              <h2>Face2Fate</h2>
              <img src="t.jpg" alt="Logo" className="navbar-logo" />
            </li>
            <li>
              <Link to="/home" className="nav-link">בית</Link>
            </li>
            <li>
              <Link to="/try" className="nav-link">פיענוח</Link>
            </li>
            <li>
              <Link to="/aboutUs" className="nav-link">אודות</Link>
            </li>
          </ul>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/home" />} />
            <Route path="/home" element={<HomePage />} />
            <Route path="/try" element={<FileUploadPage />} />
            <Route path="/aboutUs" element={<AboutUs />} />
            <Route path="/analysis" element={<ImageAnalysisPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
