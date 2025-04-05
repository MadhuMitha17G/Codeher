import React, { useState } from 'react';
import './App.css';

function App() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [detectionResult, setDetectionResult] = useState(''); // State for detection message

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setUploadStatus('Please select a file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        setUploadStatus('Processing...');
        setDetectionResult(''); // Clear previous result

        try {
            const response = await fetch('http://localhost:5000/upload-file', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const responseData = await response.json();
                setUploadStatus(responseData.message);
                setDetectionResult(responseData.detection_result); // Get the detection message
                console.log("Detection Result:", responseData.detection_result); // Log to React console
            } else {
                const errorData = await response.json();
                setUploadStatus(`Processing failed: ${errorData.error || 'Something went wrong.'}`);
                setDetectionResult('');
            }
            setSelectedFile(null);
        } catch (error) {
            console.error('Processing error:', error);
            setUploadStatus('Error connecting to the server.');
            setDetectionResult('');
        }
    };

    return (
        <div className="App">
            <h1>Abuse Detection</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={!selectedFile}>Upload and Analyze</button>
            {uploadStatus && <p>{uploadStatus}</p>}
            {detectionResult && <p>Detection Result: {detectionResult}</p>} {/* Display the detection message */}
        </div>
    );
}

export default App;