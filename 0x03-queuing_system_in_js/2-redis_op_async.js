import redis from 'redis';
import { promisify } from 'util';
// Create a Redis client
const client = redis.createClient();

// Handle connection events
client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.error('Redis client not connected to the server:', err);
});

// Promisify the Redis GET function
const getAsync = promisify(client.get).bind(client);

// Function to set a new school value
function setNewSchool(schoolName, value) {
    client.set(schoolName, value, (err, reply) => {
        if (err) {
            console.error('Error setting value:', err);
            return; // Exit the function if there's an error
        }
        redis.print(reply); // Log the success message if there is no error
    });
}

// Function to display the value of a school
async function displaySchoolValue(schoolName) {
    try {
        const value = await getAsync(schoolName);
        console.log(value);
    } catch (err) {
        console.error('Error retrieving value:', err);
    }
}

// Call the functions as required
displaySchoolValue('Holberton'); // Attempt to display value for non-existing key
setNewSchool('HolbertonSanFrancisco', '100'); // Set value for new key
displaySchoolValue('HolbertonSanFrancisco'); // Display value for new key
