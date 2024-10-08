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

// Function to set values in a hash using hset
function createHolbertonSchools(){
    client.hset('HolbertonSchools', 'Portland', 50, redis.print);
    client.hset('HolbertonSchools', 'Seattle', 80, redis.print);
    client.hset('HolbertonSchools', 'New York', 20, redis.print);
    client.hset('HolbertonSchools', 'Bogota', 20, redis.print);
    client.hset('HolbertonSchools', 'Cali', 40, redis.print);
    client.hset('HolbertonSchools', 'Paris', 2, redis.print);
}

// Function to display the values in the hash using hgetall
function displayHolbertonSchools() {
    client.hgetall('HolbertonSchools', (err, reply) => {
        if (err) {
            console.error('Error fetching hash:', err);
        } else {
            console.log(reply);  // Log the hash object returned by hgetall
        }
    });
}
// Call the functions
createHolbertonSchools();
displayHolbertonSchools();
