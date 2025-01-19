import axios from 'axios';

// Definir la URL de la API
//const API_URL = 'https://creatures.network-telemetrix.com'
const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL 
//const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:5000'; // Valor predeterminado si la variable de entorno no está definida

console.log('API_URL:', API_URL);  // Esto debería mostrar "https://creatures.network-telemetrix.com/api"


export const generateCreature = async (clientName, birthDate, clientEmail, creatureDetails) => {
  try {
    console.log('Full endpoint URL:', `${API_URL}/api/generate_creature`); 
    const response = await axios.post(
      `${API_URL}/api/generate_creature`, 
      {
        client_name: clientName,
        birth_date: birthDate,
        client_email: clientEmail,
        creature_details: creatureDetails
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    return response.data;
  } 
  catch (error) {
    console.error('Error generating creature:', error.response ? error.response.data : error.message);
    throw error;
  }
};

export const buyCreature = async (clientName, clientEmail, birthDate, creature) => {
  try {
    const response = await axios.post(
      `${API_URL}/api/buy_creature`, 
      {
        client_name: clientName,
        client_email: clientEmail,
        birth_date: birthDate,
        creature_name: creature.name,
        creature_description: creature.description,
        wheel_number: creature.unique_number,
        image_url: creature.image_url
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    return response.data;  
  } catch (error) {
    console.error('Error buying creature:', error.response ? error.response.data : error.message);
    throw error;
  }
};
