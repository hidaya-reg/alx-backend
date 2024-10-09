import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', function() {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter(); // Enter test mode before running each test
  });

  afterEach(() => {
    queue.testMode.clear(); // Clear the queue after each test
    queue.testMode.exit();  // Exit test mode
  });

  it('should display an error message if jobs is not an array', function() {
    expect(() => createPushNotificationsJobs('not an array', queue)).to.throw(
      Error,
      'Jobs is not an array'
    );
  });

  it('should create two new jobs in the queue', function() {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account',
      },
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2); // Assert two jobs were added
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
  });
});
