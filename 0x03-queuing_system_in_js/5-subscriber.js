import redis from 'redis';
// Create a Redis client
const subscriber = redis.createClient();

// Handle connection events
subscriber.on('connect', () => {
    console.log('Redis client connected to the server');
});

subscriber.on('error', (err) => {
    console.error('Redis client not connected to the server:', err);
});

// Subscribe to the 'holberton school channel'
subscriber.subscribe('holberton school channel');

// Handle received messages
subscriber.on('message', (channel, message) => {
    console.log(message); // Log the message received

    // If the message is 'KILL_SERVER', unsubscribe and quit
    if (message === 'KILL_SERVER') {
        subscriber.unsubscribe();
        subscriber.quit();
    }
});
