import React from 'react';
import './App.css';
import Footer from './components/Footer/Footer.component';
import MainSection from './components/MainSection/MainSection.component';
import Navbar from './components/Navbar/Navbar.component';
import RecordSection from './components/RecordSection/RecordSection.component';
function App() {
  return (
    <div className="main">
      <div className="container">
        <Navbar />
        <MainSection />
        <RecordSection />
        <Footer />
      </div>
    </div>
  );
}
export default App;
