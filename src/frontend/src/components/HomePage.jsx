import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  CircularProgress,
  Paper,
  Snackbar,
  Typography,
  LinearProgress,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import io from 'socket.io-client';
import VideoUpload from './VideoUpload';
import GenerateCaptions from './GenerateCaptions';

const socket = io('http://localhost:5000'); // Make sure this matches your backend host

const HomePage = () => {
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);
  const [captions, setCaptions] = useState('');
  const [progress, setProgress] = useState(0);
  const [jobId, setJobId] = useState(null);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const accessToken = localStorage.getItem('accessToken');
  const navigate = useNavigate();

  const presignedUrlApi = 'http://localhost:8000/api/v1/generate-presigned-url';
  const captionRequestApi = 'http://localhost:8000/api/v1/request';
  const captionResultApi = 'http://localhost:8000/api/v1/result';
  const captionStatusApi = 'http://localhost:8000/api/v1/status';

  useEffect(() => {
    if (!accessToken) navigate('/login');
  }, [navigate, accessToken]);

  useEffect(() => {
    if (!jobId) return;

    socket.emit('subscribe_job', { job_id: jobId });

    socket.on('status_update', async (data) => {
      if (data.job_id !== jobId) return;
      console.log('WebSocket update:', data);

      const status = data.status;

      // If numeric, treat as percentage
      if (!isNaN(status)) {
        setProgress(parseInt(status));
      }

      // When processing is complete
      if (status === 'Processed') {
        try {
          const resultRes = await fetch(`${captionResultApi}/${jobId}`, {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${accessToken}`,
            },
          });
          const resultData = await resultRes.json();
          if (resultData.success) {
            setCaptions(resultData.data.transcript);
            toast.success('Captions ready!');
          } else {
            toast.error('Failed to fetch final captions.');
          }
        } catch (err) {
          toast.error('Error fetching final caption result.');
        } finally {
          setLoading(false);
          setProgress(100);
        }
      }
    });

    return () => {
      socket.emit('unsubscribe_job', { job_id: jobId });
      socket.off('status_update');
    };
  }, [jobId]);

  const generateCaptions = async () => {
    if (!videoUrl) {
      toast.error('Please upload a video first.');
      return;
    }

    setLoading(true);
    setProgress(0);
    setCaptions('');
    try {
      const response = await fetch(captionRequestApi, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ video_url: videoUrl }),
      });

      const data = await response.json();
      if (data.success && data.data.job_id) {
        setJobId(data.data.job_id);
        toast.info('Caption job started...');
      } else {
        toast.error('Failed to start caption generation.');
        setLoading(false);
      }
    } catch (error) {
      toast.error('Error initiating caption generation.');
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
            Upload a video to start generating captions.
          </Typography>

          <VideoUpload
            getPresignedUrlEndpoint={presignedUrlApi}
            onUploadSuccess={handleVideoUploadSuccess}
          />

          {videoUrl && (
            <GenerateCaptions
              videoUrl={videoUrl}
              onGenerate={generateCaptions}
              loading={loading}
            />
          )}

          {loading && (
            <Box sx={{ width: '100%', mt: 2 }}>
              <LinearProgress variant="determinate" value={progress} />
              <Typography align="center" mt={1}>
                {progress}% Processing
              </Typography>
            </Box>
          )}
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
