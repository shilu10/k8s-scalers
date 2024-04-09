import React, { useState, useEffect } from 'react';
import {
  Box,
  CircularProgress,
  Paper,
  Snackbar,
  TextField,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import VideoUpload from '../components/VideoUpload';
import GenerateCaptions from '../components/GenerateCaptions';

const HomePage = () => {
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);
  const [captions, setCaptions] = useState('');
  const [email, setEmail] = useState('');
  const [language, setLanguage] = useState('en');
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const navigate = useNavigate();

  const presignedUrlApi = 'http://localhost:8000/api/v1/upload/generate-presigned-url';
  const captionGenerationApi = 'https://api.yourdomain.com/generate-captions';

  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      navigate('/login');
    }
  }, [navigate]);

  const generateCaptions = async () => {
    if (!videoUrl) {
      toast.error('Please upload a video first.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(captionGenerationApi, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ videoUrl, language }),
      });

      const data = await response.json();
      if (data.success) {
        setCaptions(data.captions);
        toast.success('Captions generated successfully!');
      } else {
        toast.error('Failed to generate captions');
      }
    } catch (error) {
      toast.error('Error generating captions.');
    } finally {
      setLoading(false);
    }
  };

  const handleVideoUploadSuccess = (url) => {
    setVideoUrl(url);
    toast.success('Video uploaded successfully!');
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
      bgcolor="#eaeff1"
      padding={2}
    >
      <Box maxWidth="600px" width="100%">
        <Paper
          elevation={6}
          sx={{
            p: 5,
            borderRadius: 4,
            bgcolor: '#ffffff',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 3,
          }}
        >
          <Typography variant="h4" fontWeight="bold">
            Video Caption Generator
          </Typography>

          <Typography variant="body1" color="text.secondary" align="center">
            Upload a video to start generating captions in your preferred language.
          </Typography>

          <VideoUpload
            getPresignedUrlEndpoint={presignedUrlApi}
            onUploadSuccess={handleVideoUploadSuccess}
          />

          {videoUrl && (
            <>
              <FormControl fullWidth sx={{ mt: 2 }}>
                <InputLabel>Language</InputLabel>
                <Select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  label="Language"
                >
                  <MenuItem value="en">English</MenuItem>
                  <MenuItem value="es">Spanish</MenuItem>
                  <MenuItem value="fr">French</MenuItem>
                  <MenuItem value="de">German</MenuItem>
                  <MenuItem value="hi">Hindi</MenuItem>
                  <MenuItem value="zh">Chinese</MenuItem>
                  {/* Add more languages as needed */}
                </Select>
              </FormControl>

              <TextField
                label="Email (optional)"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                fullWidth
              />

              <GenerateCaptions
                videoUrl={videoUrl}
                onGenerate={generateCaptions}
                loading={loading}
              />
            </>
          )}

          {loading && <CircularProgress />}
        </Paper>

        {captions && (
          <Paper
            elevation={4}
            sx={{
              mt: 4,
              p: 3,
              borderRadius: 3,
              bgcolor: '#fff',
              boxShadow: '0 4px 15px rgba(0,0,0,0.05)',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Captions
            </Typography>
            <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }} color="text.secondary">
              {captions}
            </Typography>
          </Paper>
        )}

        <Snackbar
          open={snackbarOpen}
          autoHideDuration={3000}
          onClose={handleSnackbarClose}
          message="Video uploaded and captions generated!"
        />
      </Box>
    </Box>
  );
};

export default HomePage;
