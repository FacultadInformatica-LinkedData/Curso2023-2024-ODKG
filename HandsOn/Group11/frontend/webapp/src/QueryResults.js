import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const darkTheme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#ff4d00',
        }
    },
});

export default function QueryResults({ results }) {
    return (
        <ThemeProvider theme={darkTheme}>
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 6,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Typography component="h1" variant="h2" fontWeight={900}>
                        Results
                    </Typography>
                    <Box component="form" sx={{ mt: 5 }} style={{ width: "100%" }}>
                        {
                            results.map(function (object, index) {
                                return (
                                    <Grid item xs={12} sx={{ marginTop: 2 }}>
                                        <Card variant='outlined'>
                                            <React.Fragment>
                                                <CardContent>
                                                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                                        {object.year}
                                                    </Typography>
                                                    <Typography variant="h5" component="div">
                                                        {object.title}
                                                    </Typography>
                                                    <Typography sx={{ mb: 1.5 }} color="text.secondary">
                                                        {object.author}
                                                    </Typography>
                                                    <Typography variant="body2">
                                                        {object.description}
                                                    </Typography>
                                                </CardContent>
                                            </React.Fragment>
                                        </Card>
                                    </Grid>
                                );
                            })
                        }
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
}