import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


export default function DenseTable(props) {
  const { data, format } = props;
  const propertyNames = Object.keys(data);

  return (
    <TableContainer component={Paper}>
      <Table size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell><strong>Detalles</strong></TableCell>
            <TableCell align="right"></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>

          {propertyNames.map((row) => {
            return (
              <TableRow
                key={row}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  <strong>{format[row]}</strong>
                </TableCell>

                {
                  row.toUpperCase().includes("URL") ? 
                    <TableCell align="right"><a href={data[row]} target="_blank">Ver Más &#128279;</a></TableCell> : 
                    <TableCell align="right">{data[row]}</TableCell>
                }
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
