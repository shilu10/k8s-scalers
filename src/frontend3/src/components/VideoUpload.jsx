import React, { useState } from 'react';
import { Box, Button, Typography, LinearProgress } from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export default function VideoUpload({ getPresignedUrlEndpoint, onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      navigate('/login');
      return;
    }

    if (!file) return;
    setUploading(true);

    try {
      // Presigned URL logic (replace with your actual upload logic)
      const res = await fetch(getPresignedUrlEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: file.name }),
      });

      const { url, fileUrl } = await res.json();

      await fetch(url, {
        method: 'PUT',
        body: file,
      });

      onUploadSuccess(fileUrl);
    } catch (error) {
      console.error('Upload failed', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      p={4}
      borderRadius={2}
      boxShadow={3}
      bgcolor="#ffffff"
      component={motion.div}
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      maxWidth={500}
      mx="auto"
    >
      <Typography variant="h6" gutterBottom>
        Upload Your Video
      </Typography>

      <input
        type="file"
        accept="video/*"
        onChange={handleFileChange}
        style={{ marginTop: '20px' }}
      />
      {file && <Typography mt={2}>{file.name}</Typography>}

      <Button
        variant="contained"
        onClick={handleUpload}
        disabled={!file || uploading}
        sx={{ mt: 3 }}
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </Button>

      {uploading && <LinearProgress sx={{ width: '100%', mt: 2 }} />}
    </Box>
  );
}
