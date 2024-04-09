import React, { useState } from 'react';
import {
  TextField,
  IconButton,
  InputAdornment,
  FormControl,
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';

export default function FormField({ label, name, type = 'text', formik }) {
  const [showPassword, setShowPassword] = useState(false);

  const isPasswordField = type === 'password';
  const fieldType = isPasswordField && !showPassword ? 'password' : 'text';

  const handleTogglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  return (
    <FormControl fullWidth margin="normal">
      <TextField
        fullWidth
        variant="outlined"
        label={label}
        name={name}
        type={isPasswordField ? fieldType : type}
        value={formik.values[name]}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
        error={Boolean(formik.touched[name] && formik.errors[name])}
        helperText={formik.touched[name] && formik.errors[name]}
        InputProps={{
          endAdornment: isPasswordField && (
            <InputAdornment position="end">
              <IconButton
                onClick={handleTogglePasswordVisibility}
                edge="end"
                aria-label="toggle password visibility"
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
    </FormControl>
  );
}
