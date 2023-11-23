import * as React from 'react';
import PropTypes from 'prop-types';
import SwipeableViews from 'react-swipeable-views';
import { useTheme } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `full-width-tab-${index}`,
    'aria-controls': `full-width-tabpanel-${index}`,
    
  };
}

export default function FullWidthTabs(props) {
  const theme = useTheme();
  
  const {
    componenetActivities,
    componenetParks,
    value,
    setValue
  } = props;

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleChangeIndex = (index) => {
    setValue(index);
  };

  return (
    <Box sx={{ bgcolor: 'background.paper', width: '80%', marginTop: '5%' }}>
      <AppBar position="static">
        <Tabs
          value={value}
          onChange={handleChange}
          indicatorColor="white"
          textColor="inherit"
          variant="fullWidth"
          aria-label="Tabs for the project"
          centered
          sx={{ background: "#282c34", border: '1px solid #282c34'}}
        >
          <Tab label="Actividades" {...a11yProps(0)} sx={{ background: "#282c34", border: '1px solid white'}} />
          <Tab label="Parques" {...a11yProps(1)}  sx={{ background: "#282c34", border: '1px solid white'}} />
        </Tabs>
      </AppBar>
      <SwipeableViews
        axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
        index={value}
        onChangeIndex={handleChangeIndex}
      >
        <TabPanel value={value} index={0} dir={theme.direction}>
          {componenetActivities}
        </TabPanel>
        <TabPanel value={value} index={1} dir={theme.direction}>
          {componenetParks}
        </TabPanel>
      </SwipeableViews>
    </Box>
  );
}
