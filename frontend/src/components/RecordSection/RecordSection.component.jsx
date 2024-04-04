import axios from 'axios';
import React, { useState } from 'react';
import { AudioRecorder, useAudioRecorder } from 'react-audio-voice-recorder';
import './RecordSection.styles.css';

const RecordSection = () => {
  const recorderControls = useAudioRecorder();
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState(null);
  const [helperText, sethelperText] = useState('Please Upload Audio File');

  const handleFileUpload = event => {
    setFile(event.target.files[0]);
  };
  const uploadFile = async () => {
    setData(null);
    sethelperText('Audio Sent for processing...');
    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    axios
      .post('http://localhost:5000/upload', formData)
      .then(response => {
        console.log(response);
        setIsLoading(false);
        sethelperText('Data Results');
        setData(response.data);
      })
      .catch(error => {
        console.log(error);
        setIsLoading(false);
        sethelperText('Please Upload Audio File');
        setData(null);
      });
  };

  const uploadRecordedAudio = async blob => {
    setData(null);
    sethelperText('Audio Sent for processing...');
    setIsLoading(true);
    const formData = new FormData();
    formData.append('audioFile', blob, 'audio.webm');
    axios
      .post('http://localhost:5000/convert', formData)
      .then(response => {
        console.log(response);
        setIsLoading(false);
        sethelperText('Data Results');
        setData(response.data);
      })
      .catch(error => {
        console.log(error);
        setIsLoading(false);
        sethelperText('Please Upload Audio File');
        setData(null);
      });
  };
  return (
    <section className="record-section" id="record-section">
      <div className="record-container">
        <div className="file-upload-container">
          <h1>Upload Audio</h1>
          <input type="file" onChange={handleFileUpload} />
          <button onClick={uploadFile}>Upload Audio</button>
        </div>
        <div
          style={{
            width: '2px',
            height: '250px',
            backgroundColor: '#ddd',
          }}
        ></div>
        <div className="file-record-container">
          <h1>Record Audio</h1>
          <AudioRecorder
            onRecordingComplete={blob => uploadRecordedAudio(blob)}
            recorderControls={recorderControls}
          />
        </div>
      </div>
      {<h1>{helperText}</h1>}
      {isLoading === true ? <div className="loader"></div> : <></>}
      {data === null ? (
        <></>
      ) : (
        <div className="result-items">
          <div className="result-item">
            <div className="result-item_title">Transcription</div>
            <div className="result-item_description">{data.text}</div>
          </div>
          <div
            className={
              `result-item ` + (data.is_danger ? 'danger' : 'no-danger')
            }
          >
            <div className="result-item_title">Threat Detected?</div>
            <div className="result-item_description">
              {data.is_danger
                ? 'Threat is detected, sending an email to the authorities!'
                : 'No threat detected!'}
            </div>
          </div>
        </div>
      )}
    </section>
  );
};
export default RecordSection;
