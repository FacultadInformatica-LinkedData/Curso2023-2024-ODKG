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
import Link from '@mui/material/Link';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import SouthIcon from '@mui/icons-material/South';
import NorthIcon from '@mui/icons-material/North';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import DEFAULT_IMAGE from './assets/images/default_image.jpg';

const primaryColor = '#ff4d00'
const darkTheme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: primaryColor,
        }
    },
});

function queryString(endpoint, params) {
    let result = [];

    for (const [key, value] of Object.entries(params)) {
        if (value != null) {
            result.push(`${key}=${value}`);
        }
    }

    if (result.length > 0) {
        return endpoint + '?' + result.join('&');
    }

    return endpoint;
}

export default function SearchForm() {
    const [authorAscending, setAuthorAscending] = React.useState(true);
    const [yearAscending, setYearAscending] = React.useState(true);
    const [queryResults, setQueryResults] = React.useState(null);
    const [caseSensitiveChecked, setCaseSensitiveChecked] = React.useState(false);
    const [limitValue, setLimitValue] = React.useState(-1);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const params = new FormData(event.currentTarget);

        console.log({
            title: params.get('title'),
            author: params.get('author')
        });

        let query = queryString(`http://0.0.0.0:8081/api/artwork`, {
            artist_name: params.get('author').length > 0 ? params.get('author').replace(' ', '%20') : null,
            title: params.get('title').replace(' ', '%20'),
            made_in_year: null
        });

        console.log('request: ' + query)

        try {
            const data = await (await fetch(
                query,
                {
                    method: 'GET',
                    mode: "cors",
                    headers: {
                        'Upgrade-Insecure-Requests': '1',
                        'Host': '0.0.0.0:8081',
                        'Access-Control-Allow-Origin': '*',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Encoding': 'gzip, deflate',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                    }
                }
            )).json()

            console.log('response: ')
            console.log(data)

            setQueryResults(data)
        } catch (err) {
            console.log('error: ' + err.message)
        }
    };

    if (queryResults != null) {
        if (authorAscending) queryResults.sort((a, b) => a.link.localeCompare(b.link));
        else queryResults.sort((a, b) => b.link.localeCompare(a.link));

        if (yearAscending) queryResults.sort((a, b) => a.made_in_year.localeCompare(b.made_in_year));
        else queryResults.sort((a, b) => b.made_in_year.localeCompare(a.made_in_year));
    }

    return (
        <ThemeProvider theme={darkTheme}>
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                {
                    queryResults == null ?
                        <Box
                            sx={{
                                marginTop: 8,
                                display: 'flex',
                                flexDirection: 'column',
                                alignItems: 'center',
                            }}
                        >
                            <Typography component="h1" variant="h2" fontWeight={900}>
                                Artworks
                            </Typography>
                            <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 5 }}>
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <TextField
                                            fullWidth
                                            id="title"
                                            label="Title"
                                            name="title"
                                            autoComplete="title"
                                            variant='filled'
                                        />
                                    </Grid>
                                    <Grid item xs={12}>
                                        <TextField
                                            fullWidth
                                            name="author"
                                            label="Author"
                                            type="author"
                                            id="author"
                                            autoComplete="author"
                                            variant='filled'
                                        />
                                    </Grid>
                                    <Grid item xs={12} sx={{ maxWidth: "100% !important" }}>
                                        <FormControl variant="filled" sx={{ width: "100%" }}>
                                            <InputLabel id="limit-results-query">Limit</InputLabel>
                                            <Select
                                                labelId="limit-results-query"
                                                id="demo-simple-select-filled"
                                                sx={{ width: "100%" }}
                                                value={limitValue}
                                                onChange={(event) => setLimitValue(event.target.value)}
                                            >
                                                <MenuItem value={-1}>
                                                    <em>None</em>
                                                </MenuItem>
                                                <MenuItem value={10}>10</MenuItem>
                                                <MenuItem value={50}>50</MenuItem>
                                                <MenuItem value={100}>100</MenuItem>
                                                <MenuItem value={500}>500</MenuItem>
                                                <MenuItem value={1000}>1000</MenuItem>
                                                <MenuItem value={10000}>10000</MenuItem>
                                            </Select>
                                        </FormControl>
                                    </Grid>
                                    <Grid item xs={12}>
                                        <FormControlLabel
                                            control={<Switch value="caseSensitive" color="primary" checked={caseSensitiveChecked} onChange={(event) => setCaseSensitiveChecked(event.target.checked)} />}
                                            label="Case sensitive"
                                        />
                                    </Grid>
                                </Grid>
                                <Button
                                    type="submit"
                                    fullWidth
                                    variant="outlined"
                                    sx={{ mt: 5, mb: 2 }}
                                    size='large'
                                >
                                    Search
                                </Button>
                            </Box>
                        </Box>
                        : <Box
                            sx={{
                                marginTop: 8,
                                display: 'flex',
                                flexDirection: 'column',
                                alignItems: 'center',
                            }}
                        >
                            <Typography component="h1" variant="h2" fontWeight={900}>
                                Results
                            </Typography>

                            <Stack direction="row" spacing={2} sx={{ mt: 5 }} style={{ width: "100%" }}>
                                <Button variant='outlined' endIcon={authorAscending ? <NorthIcon /> : <SouthIcon />} onClick={() => setAuthorAscending(!authorAscending)}>
                                    Author
                                </Button>
                                <Button variant='outlined' endIcon={yearAscending ? <NorthIcon /> : <SouthIcon />} onClick={() => setYearAscending(!yearAscending)}>
                                    Year
                                </Button>
                            </Stack>

                            {
                                queryResults.length > 0 ?
                                    <Box component="form" sx={{ mt: 3 }} style={{ width: "100%" }}>
                                        {
                                            queryResults.map(function (object, index) {
                                                let imageUrl = object.thumbnail_url.replace('www', 'media').replace('8.jpg', '10.jpg')
                                                return (
                                                    <Grid key={index} item xs={12} sx={{ marginTop: 2 }}>
                                                        <Card variant='outlined' sx={{ border: '1px solid', borderColor: 'primary.main' }}>
                                                            <React.Fragment>
                                                                <CardMedia
                                                                    style={{ backgroundImage: 'url(' + imageUrl + '), url(' + DEFAULT_IMAGE + ')' }}
                                                                    sx={{ height: 140 }}
                                                                    title={object.title}
                                                                    image={imageUrl}
                                                                />
                                                                <CardContent>
                                                                    {
                                                                        object.made_in_year > 0 ?
                                                                            <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                                                                {object.made_in_year}
                                                                            </Typography>
                                                                            : <></>
                                                                    }
                                                                    <Typography variant="h5" component="div">
                                                                        {object.title}
                                                                    </Typography>
                                                                    <Typography sx={{ mb: 1.5 }} color="text.secondary" noWrap>
                                                                        <Link href={object.link} color="text.secondary">
                                                                            {object.link}
                                                                        </Link>
                                                                    </Typography>
                                                                    <Divider variant="middle">
                                                                        <Chip label="Details" color='primary' />
                                                                    </Divider>
                                                                    <Typography sx={{ my: 1.5 }} variant="body2" noWrap>
                                                                        {object.art_medium}
                                                                    </Typography>
                                                                    <Typography sx={{ mb: 1.5 }} variant="body2" noWrap>
                                                                        {object.width} x {object.height} cm
                                                                    </Typography>
                                                                    <Divider variant="middle" />
                                                                    <Typography sx={{ mt: 1.5 }} variant="body2" color="text.secondary">
                                                                        {object.credit_text}
                                                                    </Typography>
                                                                    <Typography sx={{ fontSize: 14, mt: 1.5 }} color="text.secondary" gutterBottom>
                                                                        {object.copyright_notice}
                                                                    </Typography>
                                                                </CardContent>
                                                            </React.Fragment>
                                                        </Card>
                                                    </Grid>
                                                );
                                            })
                                        }
                                    </Box>
                                    : <Typography sx={{ mt: 3 }} variant="body">
                                        Sorry! No results were found.
                                    </Typography>
                            }
                        </Box>
                }
            </Container>
        </ThemeProvider>
    );
}