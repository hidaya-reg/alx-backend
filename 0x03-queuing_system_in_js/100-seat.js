import express from 'express';
import { promisify } from 'util';
import redis from 'redis';
import kue from 'kue';

// Create Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Create Kue queue
const queue = kue.createQueue();

// Initialize Express app
const app = express();
const PORT = 1245;

// Initialize available seats and reservation status
const INITIAL_AVAILABLE_SEATS = 50;
let reservationEnabled = true;

// Set the initial number of available seats in Redis
setAsync('available_seats', INITIAL_AVAILABLE_SEATS).catch(err => console.error(err));

// Function to reserve seats in Redis
const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

// Function to get current available seats from Redis
const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10); // Convert to integer
};

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: "Reservations are blocked" });
  }

  const job = queue.create('reserve_seat').save(err => {
    if (err) {
      return res.json({ status: "Reservation failed" });
    }
    res.json({ status: "Reservation in process" });
  });
});

// Process the reserve_seat jobs
queue.process('reserve_seat', async (job, done) => {
  try {
    let availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      reservationEnabled = false; // Disable reservations
      return done(new Error("Not enough seats available"));
    }

    availableSeats -= 1; // Decrease available seats
    await reserveSeat(availableSeats); // Update Redis

    console.log(`Seat reservation job ${job.id} completed`);
    done();
  } catch (error) {
    console.log(`Seat reservation job ${job.id} failed: ${error.message}`);
    done(error);
  }
});

// Route to process the queue
app.get('/process', async (req, res) => {
  res.json({ status: "Queue processing" });
  queue.process('reserve_seat'); // Process the queue
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
