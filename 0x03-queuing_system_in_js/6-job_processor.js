// Import Kue to manage the queue
const kue = require('kue');

// Create the queue
const queue = kue.createQueue();

// Function to send the notification
function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// Queue process for 'push_notification_code'
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message);
  done(); // Notify Kue that the job is done
});
