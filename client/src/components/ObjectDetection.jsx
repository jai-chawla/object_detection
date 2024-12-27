import React, { useState } from 'react';
import { FiUpload } from 'react-icons/fi'; // Upload Icon
import { toast } from 'react-toastify';
import axios from 'axios';
import Loader from '../assets/Loader';

const ObjectDetection = () => {
  const [image, setImage] = useState(null); // State to store the uploaded image
  const [file, setFile] = useState(null); // State to store the actual file to upload
  const [annotatedImage, setAnnotatedImage] = useState(null);

  const [video, setVideo] = useState(null); // State to store the uploaded video
  const [videoFile, setVideoFile] = useState(null); // State to store the actual video file to upload
  const [annotatedVideo, setAnnotatedVideo] = useState(null);

  const [loading, setLoading] = useState(false);

  // Handle image file upload
  const handleFileSelect = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      const imageURL = URL.createObjectURL(selectedFile); // Create a temporary URL for the image
      setImage(imageURL);
      setFile(selectedFile); // Store the actual file for uploading
      toast.success("File selected successfully!");
    }
  };

  // Handle video file upload
  const handleVideoSelect = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      const videoURL = URL.createObjectURL(selectedFile); // Create a temporary URL for the video
      setVideo(videoURL);
      setVideoFile(selectedFile); // Store the actual video file for uploading
      toast.success("Video selected successfully!");
      console.log(videoURL);
    }
  };

  // Handle object detection for images
  const handleObjectDetection = async () => {
    if (!file) {
      toast.error("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5000/detect-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('this is response', response.data);

      const base64Image = response.data.imageBase64;
      setAnnotatedImage(base64Image);

      toast.success("Object detection completed!");
      setLoading(false);
    } catch (error) {
      console.error('Error in object detection:', error.response ? error.response.data : error.message);
      toast.error("Object detection failed!");
      setLoading(false);
    }
  };

  // Handle object detection for videos
  const handleVideoDetection = async () => {
    if (!videoFile) {
      toast.error("Please select a video first!");
      return;
    }

    const formData = new FormData();
    formData.append('video', videoFile);

    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5000/detect-video', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('this is response', response.data);

      // Extract the base64 video string from the response
      const base64Video = response.data.videoBase64;

      // Create a Blob from the Base64 string
      const videoBlob = await fetch(base64Video)
        .then(res => res.blob());

      // Create a URL from the Blob for the video element
      setAnnotatedVideo(URL.createObjectURL(videoBlob));

      toast.success("Video detection completed!");
      setLoading(false);
    } catch (error) {
      console.error('Error in video detection:', error.response ? error.response.data : error.message);
      toast.error("Video detection failed!");
      setLoading(false);
    }
  };



  return (
    <div className="flex flex-col space-y-10 items-center justify-center min-h-screen bg-gray-100">
      <div>
        <h1 className='text-4xl font-semibold'>OBJECT DETECTION</h1>
      </div>

      {/* Image Section */}
      <div className="text-center">
        <div className="mb-6 flex items-center justify-center space-x-5">
          {image ? (
            <div className='mt-6'>
              <h3 className="mb-4 font-semibold">Original Image:</h3>
              <div className='w-56 h-56 overflow-hidden border border-gray-300'>
                <img
                  src={image}
                  alt="Uploaded Preview"
                  className="w-full h-full object-contain rounded-lg border border-gray-300"
                />
              </div>
            </div>
          ) : (
            <FiUpload className="w-24 h-24 text-blue-600" />
          )}

          {!loading && annotatedImage && (
            <div className="mt-6">
              <h3 className="mb-4 font-semibold">Annotated Image:</h3>
              <div className="w-56 h-56 overflow-hidden border border-gray-300 ">
                <img
                  src={annotatedImage}
                  alt="Annotated Preview"
                  className="object-contain  w-full h-full rounded-lg"
                />
              </div>
            </div>
          )}

          {loading && <Loader />}
        </div>

        <div className='flex space-x-3 items-center justify-center'>
          <label className="relative inline-block bg-blue-600 text-white font-medium px-6 py-3 rounded cursor-pointer hover:bg-blue-700">
            Select Image
            <input
              type="file"
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              accept="image/*"
              onChange={handleFileSelect}
            />
          </label>

          {image && (
            <button
              onClick={handleObjectDetection}
              className=" bg-green-600 text-white font-medium px-6 py-3 rounded cursor-pointer hover:bg-green-700"
            >
              Detect Objects
            </button>
          )}
        </div>
      </div>

      {/* Video Section */}
      <div className="text-center mt-10">
        <div className="mb-6 flex items-center justify-center space-x-5">
          {video ? (
            <div className='mt-6'>
              <h3 className="mb-4 font-semibold">Original Video:</h3>
              <div className='w-56 h-56 overflow-hidden border border-gray-300'>
                <video
                  src={video}
                  autoPlay={true}
                  loop={true}
                  muted={true}
                  className="w-full h-full object-contain rounded-lg border border-gray-300"
                />
              </div>
            </div>
          ) : (
            <FiUpload className="w-24 h-24 text-blue-600" />
          )}

          {!loading && annotatedVideo && (
            <div className="mt-6">
              <h3 className="mb-4 font-semibold">Annotated Video:</h3>
              <div className="w-full h-full overflow-hidden border border-gray-300">
                <video
                  src={annotatedVideo}
                  controls
                  autoPlay={true}
                  loop={true}
                  muted={true}
                  className="object-contain w-full h-full rounded-lg"
                />
              </div>
            </div>
          )}


          {loading && <Loader />}
        </div>

        <div className='flex space-x-3 items-center justify-center'>
          <label className="relative inline-block bg-blue-600 text-white font-medium px-6 py-3 rounded cursor-pointer hover:bg-blue-700">
            Select Video
            <input
              type="file"
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              accept="video/*"
              onChange={handleVideoSelect}
            />
          </label>

          {video && (
            <button
              onClick={handleVideoDetection}
              className=" bg-green-600 text-white font-medium px-6 py-3 rounded cursor-pointer hover:bg-green-700"
            >
              Detect Objects in Video
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ObjectDetection;
