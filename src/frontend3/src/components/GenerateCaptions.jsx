import React from 'react';
import { Button } from '@mui/material';
import { AutoFixHigh } from '@mui/icons-material';
import { motion } from 'framer-motion';

const GenerateCaptions = ({ videoUrl, onGenerate, loading }) => {
  if (!videoUrl) return null;

  return (
    <Button
      variant="contained"
      color="secondary"
      onClick={onGenerate}
      disabled={loading}
      startIcon={<AutoFixHigh />}
      component={motion.button}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      sx={{
        mt: 3,
        borderRadius: 2,
        fontWeight: 'bold',
        textTransform: 'none',
        px: 3,
        py: 1.5,
        boxShadow: '0 3px 10px rgba(0,0,0,0.1)',
      }}
    >
      {loading ? 'Generating...' : 'Generate Captions'}
    </Button>
  );
};

export default GenerateCaptions;
