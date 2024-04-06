import React, { useState } from 'react';
import {
  TextField,
  IconButton,
  InputAdornment,
  FormControl,
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';

export default function FormField({ label, name, type, formik }) {
  const [showPassword, setShowPassword] = useState(false);
  const isPassword = type === 'password';

  return (
    <FormControl fullWidth margin="normal">
      <TextField
        fullWidth
        variant="outlined"
        label={label}
        name={name}
        type={isPassword && !showPassword ? 'password' : 'text'}
        value={formik.values[name]}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
        error={formik.touched[name] && Boolean(formik.errors[name])}
        helperText={formik.touched[name] && formik.errors[name]}
        InputProps={{
          endAdornment: isPassword ? (
            <InputAdornment position="end">
              <IconButton
                onClick={() => setShowPassword((s) => !s)}
                edge="end"
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ) : null,
        }}
      />
    </FormControl>
  );
}
