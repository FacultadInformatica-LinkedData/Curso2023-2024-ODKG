import React, { useEffect, useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

export default function DependentDropdown({
  districtOptions,
  district,
  handleDistrict,
  neighborhood,
  handleNeighborhood
}) {

  const [neighborhoodOptions, setNeighborhoodOptions] = useState([]);

  useEffect( () => {
  const fetchData = async () => {
    const response_parks = await fetch(`http://localhost:8080/query-park-neighborhood?district=${district}`);
    const response_activities = await fetch(`http://localhost:8080/query-activities-neighborhood?district=${district}`);
    const json_response_parks = await response_parks.json();
    const json_response_activities = await response_activities.json();
    const mergedJSON = json_response_parks.concat(json_response_activities);
    const result = mergedJSON.filter(
      (obj, index, self) =>
        index === self.findIndex((o) => o.nameNeighborhood === obj.nameNeighborhood)
    );
    setNeighborhoodOptions(result.map((neigh) => neigh.nameNeighborhood));
    return result;
  }
  fetchData().catch(console.error)
}, [district])

  return (
    <div style={{ display: 'flex' }}>
      <Autocomplete
        value={district}
        onChange={handleDistrict}
        options={districtOptions}
        renderInput={(params) => <TextField {...params} label="Distritos" />}
        style={{ width: 270 }}
      />
      <Autocomplete
        value={neighborhood}
        onChange={(event, value) => handleNeighborhood(value)}
        options={neighborhoodOptions}
        disabled={!district}
        renderInput={(params) => (
          <TextField {...params} label="Barrios" />
        )}
        style={{ width: 270 }}
      />
    </div>
  );
}
