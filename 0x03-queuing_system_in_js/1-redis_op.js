// 1-redis_op.js
import redis from 'redis';

// Create a Redis client
const client = redis.createClient();

// Handle connection events
client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.error('Redis client not connected to the server:', err);
});

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
function displaySchoolValue(schoolName) {
    client.get(schoolName, (err, reply) => {
        if (err) {
            console.error('Error retrieving value:', err);
            return;
        }
        console.log(reply);
    });
}

// Call the functions as required
displaySchoolValue('Holberton'); // Attempt to display value for non-existing key
setNewSchool('HolbertonSanFrancisco', '100'); // Set value for new key
displaySchoolValue('HolbertonSanFrancisco'); // Display value for new key
