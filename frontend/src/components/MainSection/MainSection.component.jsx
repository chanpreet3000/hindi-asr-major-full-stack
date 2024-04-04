import './MainSection.styles.css';
import Lottie from 'react-lottie';
import animationData from '../../animations/temp2.json';

const MainSection = () => {
  const defaultOptions = {
    loop: true,
    autoplay: true,
    animationData: animationData,
    renderer: 'svg',
  };
  return (
    <section className="main-section">
      <div className="main-section-title-container">
        <span className="main-section__title highlighted">
          Empowering Safety Through
        </span>
        <span className="main-section__title"> - Audio Analysis</span>
        <div className="main-section-items">
          <div className="main-section-item left-section">
            <p className="main-section__description">
              We aim to provide a proactive solution for individuals in need,
              offering timely assistance and support when it matters most.
              Whether it's detecting distress calls, identifying potential
              hazards.
            </p>
            <div className="main-section__button">
              <a href="#record-section">Try Major Project Demo</a>
            </div>
          </div>
          <div className="main-section-item">
            <Lottie options={defaultOptions} />
          </div>
        </div>
      </div>
    </section>
  );
};

export default MainSection;
