import React from 'react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';

export default function DatePick({date, handleDate}) {

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DatePicker
          label="Fecha"
          value={date}
          openTo="year"
          views={['year', 'month']}
          onChange={handleDate}
        />
    </LocalizationProvider>
  );
}