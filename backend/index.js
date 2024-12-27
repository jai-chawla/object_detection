const express = require('express');
const multer = require('multer');
const { spawn,exec } = require('child_process');
const cors = require('cors');
const path = require('path');
const fs = require('fs'); 

const app = express();
const PORT = 5000;

// Middleware
app.use(cors({ origin: '*' }));
app.use(express.json());
app.use('/processed', express.static(path.join(__dirname, 'processed')));

app.use('/uploads', express.static('uploads')); 

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, 'uploads/'); // Directory where images will be uploaded
    },
    filename: (req, file, cb) => {
      cb(null, Date.now() + path.extname(file.originalname)); // Use current timestamp as filename
    }
  });
  
  const upload = multer({ storage: storage });


// API Endpoint to handle file uploads
app.post('/detect-image', upload.single('image'), (req, res) => {
    if (!req.file) {
      return res.status(400).json({ error: 'No image file uploaded' });
    }
  
    console.log('File received:', req.file);
  
    // Path to the uploaded image
    const imagePath = path.join(__dirname, 'uploads', req.file.filename);
  
    const pythonPath = "C:\\Users\\JAI CHAWLA\\Desktop\\project_2\\backend\\myenv\\Scripts\\python.exe";  // Update this path to your Python environment
    const pythonScriptPath = 'original_script.py';  // Path to your Python script
  
    // Spawn the Python process with the image path as an argument
    const pythonProcess = spawn(pythonPath, [pythonScriptPath, imagePath], {
      stdio: ['pipe', 'pipe', 'pipe'],  // Enable communication via stdin, stdout, and stderr
    });
  
    let output = '';
  
    // Collect the base64-encoded image output from stdout
    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });
  
    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python error: ${data.toString()}`);
    });
  
    pythonProcess.on('error', (err) => {
      console.error('Failed to start Python process:', err);
    });
  
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        const base64Image = `data:image/jpeg;base64,${output.trim()}`;
        res.status(200).json({
          message: 'Image detection completed!',
          imageBase64: base64Image,
        });

        fs.unlink(imagePath, (err) => {
            if (err) {
                console.error(`Error deleting file ${imagePath}:`, err);
            } else {
                console.log(`Image deleted: ${imagePath}`);
            }
        });

      } else {
        res.status(500).json({ error: 'Image detection failed!' });
      }
    });
  });

  app.post('/detect-video', upload.single('video'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No video file uploaded' });
    }

    console.log('Video received, processing...');

    // Path to the uploaded video
    const videoPath = path.resolve(req.file.path);

    // Path to Python executable and script
    const pythonPath = "C:\\Users\\JAI CHAWLA\\Desktop\\project_2\\backend\\myenv\\Scripts\\python.exe"; // Update this to your Python path
    const pythonScriptPath = path.resolve('original_video.py'); // Path to your Python script

    // Spawn the Python process
    const pythonProcess = spawn(pythonPath, [pythonScriptPath, videoPath]);

    let output = '';
    let errorOutput = '';

    // Collect the base64-encoded video from stdout
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    // Collect any error messages from stderr
    pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
    });

    // Handle Python process completion
    pythonProcess.on('close', (code) => {
        console.log('completed');
        fs.unlink(videoPath, (err) => {
            if (err) console.error(`Failed to delete file: ${videoPath}`);
        });

        if (code === 0) {
            // Send the base64-encoded annotated video as the response
            res.status(200).json({
                message: 'Video detection completed!',
                videoBase64: `data:video/mp4;base64,${output.trim()}`,
            });
        } else {
            console.error(`Python script exited with code ${code}`);
            console.error(`Python script errors: ${errorOutput}`);
            res.status(500).json({
                error: 'Video detection failed!',
                details: errorOutput,
            });
        }
    });

    // Handle Python process errors
    pythonProcess.on('error', (err) => {
        console.error('Failed to start Python process:', err);
        res.status(500).json({ error: 'Failed to start Python process' });
    });
});



// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
