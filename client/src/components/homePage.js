import React from 'react';
import '../styleSheet/homePage.css'; // Import the CSS file
import aImage from '../images/d.png'; // Import the image

const HomePage = () => {
  return (
    <div className="home-page">
      {/* Left side content */}
      <div className="left-content">
        <img src={aImage} alt="Face to analyze" className="left-image" />
      </div>
      {/* Right side content */}
      <div className="right-content">
        <h2>face2fate: גלו את עצמכם בתוך דקות!</h2>
        <p>
          נמאס לכם לתהות מי אתם באמת?<br />
          רוצים להבין לעומק את אישיותכם?<br />
          face2fate פה כדי לעזור!<br />
          השתמשו בטכנולוגיה פורצת דרך לזיהוי תכונות אופי מתוך תמונה פשוטה של פניכם.<br />
          בתוך דקות ספורות, תגלו:
          <ul>
            <li>הצדדים החזקים והחלשים שלכם</li>
            <li>המוטיבציות המניעות אתכם</li>
            <li>ההתנהגויות המאפיינות אתכם</li>
            <li>ההזדמנויות הטמונות בכם</li>
          </ul>
          face2fate יעזור לכם:
          <ul>
            <li>לשפר את ההבנה העצמית שלכם</li>
            <li>לקבל החלטות טובות יותר בחייכם</li>
            <li>ליצור קשרים משמעותיים יותר</li>
            <li>להגשים את הפוטנציאל המלא שלכם</li>
          </ul>
          אז למה אתם מחכים?<br />
          הצטרפו ל-face2fate וגלו את עצמכם!
        </p>
      </div>
    </div>
  );
};

export default HomePage;
