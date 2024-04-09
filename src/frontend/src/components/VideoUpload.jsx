import React, { useState } from 'react';
import { Box, Button, Typography, LinearProgress } from '@mui/material';

export default function VideoUpload({ getPresignedUrlEndpoint, onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const accessToken = localStorage.getItem('accessToken');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);

    try {
      // Step 1: Request presigned URLs for all parts
      const presignedRes = await fetch(getPresignedUrlEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          filename: file.name,
          filesize: file.size}),
      });

      const presignedData = await presignedRes.json();
      console.log(presignedData)
      const parts = presignedData.data.parts;
      const uploadId = presignedData.data.uploadId;
      console.log(parts)

      const partETags = [];

      // Step 2: Upload each part
      const chunkSize = 5 * 1024 * 1024; // 5MB
      for (let i = 0; i < parts.length; i++) {
        const part = parts[i];
        const start = (part.partNumber - 1) * chunkSize;
        const end = Math.min(start + chunkSize, file.size);
        const blob = file.slice(start, end);

        const uploadRes = await fetch(part.url, {
          method: 'PUT',
          body: blob,
        });
  
        console.log(uploadRes)

        const eTag = uploadRes.headers.get('ETag');
        partETags.push({
          PartNumber: part.partNumber,
          ETag: eTag.replaceAll('"', ''), // S3 returns quoted ETags
        });
      }

      // Step 3: Complete the upload
      const completeRes = await fetch('http://localhost:8000/api/v1/complete-multipart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          uploadId,
          filename: file.name,
          parts: partETags,
        }),
      });

      const result = await completeRes.json();
      if (result.success) {
        onUploadSuccess(result.fileUrl);
      } else {
        throw new Error('Completion failed');
      }
    } catch (err) {
      console.error('Upload error', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6">Upload Your Video</Typography>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      {file && <Typography mt={1}>{file.name}</Typography>}
      <Button variant="contained" sx={{ mt: 2 }} disabled={!file || uploading} onClick={handleUpload}>
        {uploading ? 'Uploading...' : 'Upload'}
      </Button>
      {uploading && <LinearProgress sx={{ mt: 2 }} />}
    </Box>
  );
}
