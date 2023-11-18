import * as React from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Table from '../components/Table';
// import Button from '@mui/material/Button';
// import Modal from '../components/Modal';


export default function ControlledAccordions(props) {
  const [expanded, setExpanded] = React.useState(false);
  const { data, format } = props;

  // const [open, setOpen] = React.useState(false);
  // const handleOpen = () => setOpen(true);
  // const handleClose = () => setOpen(false);


  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  return (
    <div>
        {
          data && data.map((value, index) => {
            return (
              <Accordion key={index} expanded={expanded === `panelInput${index}` } onChange={handleChange(`panelInput${index}`)}>
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="panel1bh-content"
                  id="panel1bh-header"
                >
                  <Typography sx={{ width: '70%', flexShrink: 0, fontSize: '20px'}}>
                    <strong>{value['title']}</strong>
                  </Typography>
                  <Typography sx={{ color: 'text.secondary', fontSize: '15px' }}>Mostrar mas</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    {/* <Button onClick={handleOpen}>Open modal</Button> */}
                    {/* {
                      open ? (<Modal open={open} setOpen={setOpen} />) : (<div></div>)
                    } */}
                    <Table data={value} format={format} /> 
                </AccordionDetails>
              </Accordion>
            )
          })
        }
    </div>
  );
}
