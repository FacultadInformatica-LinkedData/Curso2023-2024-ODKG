import './App.css';
import React, { useEffect, useState } from 'react';
import Accordion from './components/Accordion.jsx';
import DatePick from './components/DatePick.jsx';
import DependentDropdown from './components/DependentDropdown.jsx';
import Tabs from './components/Tabs.jsx';
import Typography from '@mui/material/Typography';

function App() {
  const [districtOptions, setDistrictOptions] = useState([]);
  const [district, setDistrict] = useState('');
  const [neighborhood, setNeighborhood] = useState('');
  const [date, setDate] = useState(null);

  const [valueTab, setValueTab] = React.useState(0);
  const [parkData, setParkData] = useState([]);
  const [activityData, setActivityData] = useState([]);

  const handleDate = (date) => {
    const dateF = new Date(date)
    setDate(dateF);
  };

  const handleDistrict = (event, value) => {
    setDistrict(value);
    setNeighborhood('');
    setDate(null);
  };

  const handleNeighborhood = (value) => {
    setNeighborhood(value);
    setDate(null);
  };

  useEffect( () => {
    if (valueTab == 1) { //parks
    const fetchData = async () => {
      const response = await fetch(`http://localhost:8080/query-parks?district=${district}&neighborhood=${neighborhood}`);
      const json = await response.json();
      setParkData(json);
      return json;
    }
    fetchData().catch(console.error);
    }

    if (valueTab == 0) { //activities
      const fetchData = async () => {
        const start = date ? new Date(date.getFullYear(), date.getMonth(), 1): null;
        const end = date ? new Date(date.getFullYear(), date.getMonth() + 1, 0) : null;
        const startFormatted = start ? start.toISOString().split('T')[0] + 'T00:00:00' : null;
        const endFormatted = end ? end.toISOString().split('T')[0] + 'T23:59:59' : null;
        const response = await fetch(`http://localhost:8080/query-activities?district=${district}&neighborhood=${neighborhood}&startDate=${startFormatted}&endDate=${endFormatted}`);
        const json = await response.json();
        setActivityData(json);
        return json;
      }
      fetchData().catch(console.error);
      }
    
  }, [valueTab, district, neighborhood, date])



  useEffect( () => {
    const fetchData = async () => {
      const response_parks = await fetch(`http://localhost:8080/query-park-district`);
      const response_activities = await fetch(`http://localhost:8080/query-activities-district`);
      const json_response_parks = await response_parks.json();
      const json_response_activities = await response_activities.json();
      const mergedJSON = json_response_parks.concat(json_response_activities);
      const result = mergedJSON.filter(
        (obj, index, self) =>
          index === self.findIndex((o) => o.nameDistrict === obj.nameDistrict)
      );
      setDistrictOptions(result.map((dist) => dist.nameDistrict));
      return result;
    }
    fetchData().catch(console.error);
    
  }, [])

  const formatActivities = {
    addressName: "Dirección",
    contentURL: "URL del Contenido",
    description: "Descripción",
    districtName: "Distrito",
    endDate: "Fecha de Fin",
    id: "Referencia Actividad",
    locationAccessibility: "Accesibilidad de Instalación",
    locationName: "Nombre de Instalación",
    locationUrl: "URL de Instalación",
    neighborhoodName: "Barrio",
    startDate: "Fecha de Inicio",
    title: "Nombre", 
    wikidataUrlDistrict: "URL Distrito en Wikidata"
  }

  const formatParks = {
    district_name: "Distrito",
    id_park: "Referencia Parque",
    neighboardhood_name: "Barrio",
    title: "Nombre",
    wikidataUrlDistrict: "URL Distrito Wikidata"
  }

  return (
    <div>
      <header>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '50px' }}>
          <img src="/logo-img.png" style={{ paddingRight: '10px', width: '100px', marginBottom: '30px' }} />
          <Typography variant="h2" component="h2" sx={{ color: '#282C34' }}>
                Vida Activa Madrid
          </Typography>
        </div>
      </header>
      <div className="App">
        <div style={{display: 'flex'}}>
          <DependentDropdown
            districtOptions={districtOptions}
            district={district}
            handleDistrict={handleDistrict}
            neighborhood={neighborhood}
            handleNeighborhood={handleNeighborhood}
          />
          <DatePick
            date={date}
            handleDate={handleDate}
          />
        </div>
        <Tabs
          value={valueTab}
          setValue={setValueTab}
          componenetActivities={<Accordion data={activityData} format={formatActivities} />}
          componenetParks={<Accordion data={parkData} format={formatParks} />}
        />
      </div>
    </div>
  );
}

export default App;
