import './DevItem.styles.css';

const DevItem = ({ dev_info }) => {
  const { student_name, image_url, roll_no, batch, semester, word_done } =
    dev_info;
  return (
    <div className="dev-item-container">
      <div className="dev-item-image"></div>
      <div className="dev-item-content">
        <div className="dev-item-name">
          <h1>{student_name}</h1>
          <p>Student</p>
        </div>
        <div className="dev-item-data">
          <div className="dev-item-data-row">
            <div className="dev-item-data-row-item">
              <p className="dev-item-data-row-item-title">Roll No</p>
              <p className="dev-item-data-row-item-description">{roll_no}</p>
            </div>
            <div className="dev-item-data-row-item">
              <p className="dev-item-data-row-item-title">Batch</p>
              <p className="dev-item-data-row-item-description">{batch}</p>
            </div>
          </div>
          <div className="dev-item-data-row">
            <div className="dev-item-data-row-item">
              <p className="dev-item-data-row-item-title">Semester</p>
              <p className="dev-item-data-row-item-description">
                {semester}
                <sup>th</sup>
              </p>
            </div>
            <div className="dev-item-data-row-item">
              <p className="dev-item-data-row-item-title">Work Done</p>
              <p className="dev-item-data-row-item-description">{word_done}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default DevItem;
