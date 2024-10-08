# 0x03. Queuing System in JS
## Resources
[Redis quick start](https://redis.io/docs/latest/integrate/)
[Redis client interface](https://redis.io/docs/latest/develop/connect/cli/)
[Redis client for Node JS](https://github.com/redis/node-redis)
[Kue](https://github.com/Automattic/kue) deprecated but still use in the industry

## Learning Objectives
<details>
<summary>How to run a Redis server on your machine</summary>

### Run a Redis server on your machine
#### 1. Install Redis
You can install Redis using the package manager.
```bash
sudo apt update
sudo apt install redis-server
```
#### 2. Configure Redis (Optional)
The configuration file is located at ``/etc/redis/redis.conf``. You can modify this file to change settings such as persistence, memory limits, or binding to specific network interfaces.

#### 3. Start Redis Server
After installation, Redis should automatically start as a service. You can check its status with: `sudo systemctl status redis`

If it's not running, you can start it with: `sudo systemctl start redis`

To ensure Redis starts automatically on boot: `sudo systemctl enable redis`

#### 4. Test Redis
You can verify that Redis is running by connecting to it using the Redis CLI: `redis-cli`

In the Redis CLI, you can try a simple command like: ``ping`` You should get a response: PONG
</details>
<details>
<summary>How to run simple operations with the Redis client</summary>

### Run operations on Redis CLI
#### Step 1: Launch the Redis CLI
Open your terminal and type: `redis-cli`

This connects you to the Redis server. The prompt will change to something like this: `127.0.0.1:6379>`
Where:
- ``127.0.0.1`` is the local IP address of the Redis server.
- ``6379`` is the default Redis port.
Now you are ready to run Redis commands.

#### Step 2: Run Basic Redis Commands
**1. SET** – Store a value in Redis `SET key "value"`
Example: `SET name "Alice"`
This command stores the string "Alice" with the key name.

**2. GET** – Retrieve a value from Redis `GET key`
Example: `GET name`
This will return: `"Alice"`

**3. DEL** – Delete a key `DEL key`
Example: `DEL name`
This will delete the key ``name`` from the Redis store.

**4. EXISTS** – Check if a key exists `EXISTS key`
Example: `EXISTS name`
If the key exists, it returns 1. Otherwise, it returns 0.

**5. INCR/DECR** – Increment or decrement a value
These commands work with integer values.
- Increment a value: `INCR counter`
- Decrement a value: `DECR counter`

Example:
```bash
SET counter 10
INCR counter
GET counter
```
Output: `"11"`

**6. MSET** – Set multiple key-value pairs at once `MSET key1 "value1" key2 "value2" key3 "value3"`
Example: `MSET name "Alice" age "25" city "New York"`

**7. MGET** – Get multiple values at once `MGET key1 key2 key3`
Example: ``MGET name age city``
Output:
```arduino
1) "Alice"
2) "25"
3) "New York"
```

**8. KEYS** – List all keys matching a pattern `KEYS pattern`
Example: `KEYS *` This command lists all keys stored in Redis.

**9. EXPIRE** – Set an expiration time (in seconds) for a key `EXPIRE key seconds`
Example:
```bash
SET tempkey "temporary"
EXPIRE tempkey 10
```
The ``tempkey`` will automatically be deleted after 10 seconds.

**10. TTL** – Check how much time is left before a key expires `TTL key`
Example: `TTL tempkey`
This will return the number of seconds remaining before the key expires.

#### Step 3: Exit the Redis CLI
Once you’re done working with the Redis CLI, you can exit by typing: `exit`
Example Interaction:
```bash
$ redis-cli
127.0.0.1:6379> SET user "John"
OK
127.0.0.1:6379> GET user
"John"
127.0.0.1:6379> INCR visits
(integer) 1
127.0.0.1:6379> INCR visits
(integer) 2
127.0.0.1:6379> GET visits
"2"
127.0.0.1:6379> DEL user
(integer) 1
127.0.0.1:6379> GET user
(nil)
127.0.0.1:6379> exit
```
This is a basic introduction to Redis operations using the command-line client. Redis supports much more advanced data structures (like lists, sets, sorted sets, etc.), which you can also interact with using similar commands.
</details>
<details>
<summary>How to use a Redis client with Node JS for basic operations</summary>

### Redis CLI with Node JS
To use Redis with Node.js, you'll need to install the Redis client library and then connect to the Redis server to perform basic operations. 

#### Step 1: Install Redis Client for Node.js
```bash
npm install redis
```
#### Step 2: Set Up a Simple Node.js Script
Create a Node.js script to connect to the Redis server and perform basic operations like ``SET``, ``GET``, ``DEL``, etc.
Here's an example:
```javascript
// Import the Redis client
const redis = require('redis');

// Create a Redis client
const client = redis.createClient();

// Handle connection events
client.on('connect', () => {
    console.log('Connected to Redis server');
});

client.on('error', (err) => {
    console.error('Error connecting to Redis:', err);
});

// Perform basic Redis operations
client.set('name', 'Alice', (err, reply) => {
    if (err) throw err;
    console.log('SET name:', reply);  // Expected output: OK
});

client.get('name', (err, reply) => {
    if (err) throw err;
    console.log('GET name:', reply);  // Expected output: Alice
});

// Increment a counter
client.incr('counter', (err, reply) => {
    if (err) throw err;
    console.log('INCR counter:', reply);  // Expected output: 1 (or more depending on prior calls)
});

// Delete a key
client.del('name', (err, reply) => {
    if (err) throw err;
    console.log('DEL name:', reply);  // Expected output: 1
});

// Close the Redis client connection
client.quit();
```
#### Step 3: Run the Node.js Script
To run your script, use the following command: `node your_script.js`

Make sure that the Redis server is running before executing the Node.js script.
#### Step 4: Redis Client Configuration Options
The ``createClient`` method allows you to pass options to customize the connection. For example, if your Redis server is running on a different host or port, you can specify that:
```javascript
const client = redis.createClient({
    host: 'your_redis_host',
    port: 6379
});
```
You can also provide a password for authentication if needed:
```javascript
const client = redis.createClient({
    host: 'your_redis_host',
    port: 6379,
    password: 'your_redis_password'
});
```
#### Step 5: Closing the Redis Connection
Make sure to close the Redis client connection when you're done to avoid leaving open connections: `client.quit();`
#### Additional Operations
Redis supports a wide range of commands. Here are some additional examples:

- Check if a key exists:
```javascript
client.exists('name', (err, reply) => {
    console.log('Exists:', reply);  // Output: 1 if exists, 0 if not
});
```
- Set a key with expiration time:
```javascript
client.setex('tempkey', 60, 'Temporary Value', (err, reply) => {
    console.log('SETEX tempkey:', reply);  // Output: OK
});
```
</details>
<details>
<summary>How to store hash values in Redis</summary>

### Hash values in Redis
In Redis, you can store hash values using the HSET command and retrieve them using HGET. Hashes are useful when you want to store and access fields and values in a key, similar to storing a small data structure or object.
#### Step 1: Store Hash Values Using Redis CLI
In Redis CLI, the ``HSET`` command is used to set fields in a hash stored at a key.
Example:
```bash
HSET user:1000 name "Alice" age "25" city "New York"
```
In this example:
- ``user:1000`` is the key for the hash.
- ``name``, ``age``, and ``city`` are fields in the hash with their respective values.
To retrieve a field's value, you can use the ``HGET`` command:

```bash
HGET user:1000 name
```
This will return: `"Alice"`
#### Step 2: Using Redis Hashes with Node.js
To store and retrieve hash values in Redis using Node.js, you can use the following Redis client commands:

1. ``HSET``: Set one or more fields in a hash.
2. ``HGET``: Get the value of a specific field from a hash.
3. ``HGETALL``: Retrieve all the fields and values of a hash.

```javascript
const redis = require('redis');

// Create Redis client
const client = redis.createClient();

// Store hash values using HSET
client.hset('user:1000', 'name', 'Alice', 'age', '25', 'city', 'New York', (err, reply) => {
    if (err) throw err;
    console.log('HSET user:', reply);  // Output: Number of fields added or updated (in this case, 3)
});

// Retrieve a specific field using HGET
client.hget('user:1000', 'name', (err, reply) => {
    if (err) throw err;
    console.log('HGET user name:', reply);  // Output: Alice
});

// Retrieve all fields and values using HGETALL
client.hgetall('user:1000', (err, reply) => {
    if (err) throw err;
    console.log('HGETALL user:', reply);  // Output: { name: 'Alice', age: '25', city: 'New York' }
});

// Close the Redis client connection
client.quit();
```
#### Step 3: Running the Script
To run this Node.js script, save it as a .js file and execute it with: `node your_script.js`

Make sure your Redis server is running before executing the script.

**Redis Hash Commands in Node.js**
- `HSET key field value`: Set a field in the hash stored at key.
- ``HGET key field``: Get the value of a field in the hash stored at key.
- ``HGETALL key``: Get all fields and values stored in the hash at key.
- ``HDEL key field``: Delete a field in the hash stored at key.
- ``HEXISTS key field``: Check if a field exists in the hash stored at key.

Example of Additional Commands
- Delete a field from a hash:
```javascript
client.hdel('user:1000', 'city', (err, reply) => {
    console.log('HDEL user city:', reply);  // Output: 1 (field was deleted)
});
```
- Check if a field exists in the hash:
```javascript
client.hexists('user:1000', 'age', (err, reply) => {
    console.log('HEXISTS user age:', reply);  // Output: 1 if exists, 0 if not
});
```
This is how you can store and retrieve hash values in Redis using Node.js. Redis hashes are highly efficient when storing structured data, and you can access specific fields without retrieving the entire object, making it suitable for small datasets like user profiles or settings.
</details>
<details>
<summary>How to deal with async operations with Redis</summary>

### async operations wxith Redis
In Node.js, many Redis operations are asynchronous, meaning they don’t block the execution of your code and return a promise or use a callback. To handle these **asynchronous operations effectively, you can use **callbacks**, **promises**, or async/await**.
#### 1. Using Callbacks
By default, the Redis client uses callbacks for handling asynchronous operations. You pass a callback function as the last argument to handle the result of the operation.
Example:
```javascript
const redis = require('redis');
const client = redis.createClient();

client.on('connect', () => {
    console.log('Connected to Redis');
});

// Using a callback to handle async operations
client.get('name', (err, reply) => {
    if (err) throw err;
    console.log('GET name:', reply);
});
// Close the Redis connection
client.quit();
```
#### 2. Using Promises
To work with promises, you can **promisify** Redis client methods using Node.js's built-in ``util.promisify`` function. This allows you to convert callback-based methods into promise-based ones, making them easier to work with.
Example:
```javascript
const redis = require('redis');
const { promisify } = require('util');

const client = redis.createClient();

// Promisify Redis methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Using Promises
setAsync('name', 'Alice')
    .then(reply => {
        console.log('SET name:', reply);  // Expected output: OK
        return getAsync('name');
    })
    .then(reply => {
        console.log('GET name:', reply);  // Expected output: Alice
    })
    .catch(err => {
        console.error('Error:', err);
    })
    .finally(() => {
        client.quit();  // Close Redis connection
    });
```
#### 3. Using ``async/await``
Using ``async/await`` allows for cleaner and more readable code when dealing with asynchronous operations. It’s an extension of the promise-based approach.
Example:
```javascript
const redis = require('redis');
const { promisify } = require('util');

const client = redis.createClient();

// Promisify Redis methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

async function performRedisOperations() {
    try {
        // Perform Redis operations using async/await
        const setReply = await setAsync('name', 'Alice');
        console.log('SET name:', setReply);  // Expected output: OK

        const getReply = await getAsync('name');
        console.log('GET name:', getReply);  // Expected output: Alice
    } catch (err) {
        console.error('Error:', err);
    } finally {
        client.quit();  // Close Redis connection
    }
}

// Call the async function
performRedisOperations();
```
**Example of Handling Multiple Async Operations**
If you need to handle multiple async Redis operations at once, you can either chain promises or use async/await. Here’s an example using async/await:
```javascript
async function multiRedisOperations() {
    try {
        // Set multiple values concurrently
        await Promise.all([
            setAsync('name', 'Alice'),
            setAsync('age', '30'),
            setAsync('city', 'New York')
        ]);

        // Get all values concurrently using Promise.all
        const [name, age, city] = await Promise.all([
            getAsync('name'),
            getAsync('age'),
            getAsync('city')
        ]);

        console.log(`Name: ${name}, Age: ${age}, City: ${city}`);
    } catch (err) {
        console.error('Error:', err);
    } finally {
        client.quit();  // Close Redis connection
    }
}
```
- If you do not use ``await`` for asynchronous operations, there is a risk that the connection may close before those operations have completed, leading to incomplete or missing data in Redis.
- It’s important to either ``await`` each operation individually or use ``Promise.all`` to handle multiple operations concurrently while ensuring they complete before closing the connection.
#### Important Notes:
- **Error Handling:** Always handle errors in asynchronous operations. Use ``try/catch`` when using ``async/await``, and ``.catch()`` when working with promises.
- **Closing Connections:** Always ensure to close the Redis client connection with ``client.quit()`` after the operations are done. If left open, it might cause memory leaks or unnecessary open connections.
#### Conclusion:
- **Callbacks** are useful but can become hard to manage with deeply nested operations (callback hell).
- **Promises** provide a cleaner syntax but still require chaining.
- **async/await** is the most modern and clean way to handle asynchronous operations in Node.js. It makes the code more readable and easier to manage when performing multiple Redis operations.

</details>
<details>
<summary>How to use Kue as a queue system</summary>

### Queue System: Kue
Kue is a priority job queue backed by Redis, designed for Node.js applications. It allows you to manage background jobs efficiently. Below are the steps to set up and use Kue as a queue system in a Node.js application.

#### Step 1: Install Dependencies
First, you need to install the necessary packages. You will need ``kue`` and ``redis`` packages. `npm install kue redis`
#### Step 2: Set Up the Queue
Create a file (e.g., ``queue.js``) to configure and create a Kue queue.
```javascript
const kue = require('kue');
const queue = kue.createQueue();

// Export the queue to use it in other parts of your application
module.exports = queue;
```
#### Step 3: Create Jobs
In your application, you can create jobs to add to the queue. You can do this in a separate file or within your main application file.
```javascript
const queue = require('./queue');

// Function to create a job
function createJob(data) {
    const job = queue.create('email', {
        title: 'Welcome Email',
        to: data.email,
        template: 'welcome-email',
    }).save((err) => {
        if (!err) console.log(`Job created: ${job.id}`);
    });

    // Handle job completion
    job.on('complete', (result) => {
        console.log(`Job ${job.id} completed with result: ${result}`);
    });

    // Handle job failure
    job.on('failed attempt', (errorMessage, doneAttempts) => {
        console.log(`Job failed with error: ${errorMessage}`);
    });

    // Handle job failure after all attempts
    job.on('failed', (errorMessage) => {
        console.log(`Job failed with error after all attempts: ${errorMessage}`);
    });
}

// Example usage
createJob({ email: 'user@example.com' });
```
#### Step 4: Process Jobs
To process the jobs you've created, you'll need to set up a worker. Create a file (e.g., ``worker.js``) to process jobs in the queue.
```javascript
const queue = require('./queue');

queue.process('email', (job, done) => {
    console.log(`Processing job ${job.id}: sending email to ${job.data.to}`);

    // Simulate sending an email (replace with actual email sending logic)
    setTimeout(() => {
        console.log(`Email sent to ${job.data.to}`);
        done(); // Call done when the job is finished
    }, 2000); // Simulating a delay of 2 seconds
});
```
#### Step 5: Running Your Queue System
Now, you can run both your job creation and worker scripts.
**1. Start the worker:** Run the worker script to listen for jobs in the queue. `node worker.js`
**2. Create jobs:** In another terminal or through your main application, run the job creation code. `node your_job_creator_file.js`
#### Step 6: Monitor the Queue
Kue provides a built-in UI to monitor your jobs. You can set it up like this:
```javascript
const express = require('express');
const kue = require('kue');
const queue = require('./queue');

const app = express();
const port = 3000;

// Create a Kue UI
app.use('/kue', kue.app);

app.listen(port, () => {
    console.log(`Kue UI is running at http://localhost:${port}/kue`);
});
You can access the Kue UI by navigating to http://localhost:3000/kue in your browser.
```
</details>
<details>
<summary>How to build a basic Express app interacting with a Redis server</summary>

### Basic Express app that interacts with a Redis
#### Step 1: Set Up the Redis Client
Create a file named ``redisClient.js`` to set up the Redis client.
```javascript
// redisClient.js
const redis = require('redis');

// Create a Redis client
const client = redis.createClient();

// Handle Redis connection errors
client.on('error', (err) => {
    console.error('Redis error:', err);
});

// Export the client
module.exports = client;
```
#### Step 2: Create the Express App
Create a file named ``app.js`` for your Express application.
```javascript
// app.js
const express = require('express');
const redisClient = require('./redisClient');

const app = express();
const PORT = 3000;

// Middleware to parse JSON bodies
app.use(express.json());

// Route to set a key-value pair in Redis
app.post('/set', (req, res) => {
    const { key, value } = req.body;
    redisClient.set(key, value, (err, reply) => {
        if (err) {
            return res.status(500).json({ error: 'Error saving to Redis' });
        }
        res.json({ message: `Key ${key} set with value ${value}`, reply });
    });
});

// Route to get a value by key from Redis
app.get('/get/:key', (req, res) => {
    const key = req.params.key;
    redisClient.get(key, (err, reply) => {
        if (err) {
            return res.status(500).json({ error: 'Error retrieving from Redis' });
        }
        if (reply === null) {
            return res.status(404).json({ error: `Key ${key} not found` });
        }
        res.json({ key, value: reply });
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
```
#### Step 3: Start the Redis Server
Make sure your Redis server is running. You can start it by running the following command in your terminal (assuming you have Redis installed):
``redis-server``
#### Step 4: Run the Express App
Start your Express app by running: `node app.js`
#### Step 5: Test Your Application
You can test the application using tools like **Postman** or **cURL**.
**1. Set a key-value pair:**
Make a ``POST`` request to set a key-value pair:
```bash
curl -X POST http://localhost:3000/set -H "Content-Type: application/json" -d '{"key": "name", "value": "Alice"}'
```
This should return a response confirming that the key has been set.

**2. Get the value by key:**
Make a ``GET`` request to retrieve the value by its key:
```bash
curl http://localhost:3000/get/name
```
This should return the value associated with the key name.
</details>
<details>
<summary>How to the build a basic Express app interacting with a Redis server and queue</summary>

### Basic Express app interacting with a Redis server and queue
#### Step 1: Set Up Environment
1. Create a new directory for your project: `mkdir express-redis-queue-app` -> `cd express-redis-queue-app`
2. Initialize a new Node.js project: `npm init -y`
3. Install necessary packages: `npm install express redis bull`
#### Step 2: Set Up the Redis Client
Create a file named ``redisClient.js`` to set up the Redis client.
```javascript
// redisClient.js
const redis = require('redis');

// Create a Redis client
const client = redis.createClient();

// Handle Redis connection errors
client.on('error', (err) => {
    console.error('Redis error:', err);
});

// Export the client
module.exports = client;
```
#### Step 3: Create the Bull Queue
Create a file named ``queue.js`` to set up the Bull queue.
```javascript
// queue.js
const Queue = require('bull');

// Create a queue with the name 'myQueue'
const myQueue = new Queue('myQueue');

// Process jobs in the queue
myQueue.process(async (job) => {
    console.log(`Processing job with data: ${JSON.stringify(job.data)}`);
    // Simulate a time-consuming task (e.g., sending an email)
    await new Promise(resolve => setTimeout(resolve, 2000));
    console.log(`Finished processing job: ${job.id}`);
});

// Handle completed jobs
myQueue.on('completed', (job) => {
    console.log(`Job ${job.id} completed!`);
});

// Handle failed jobs
myQueue.on('failed', (job, err) => {
    console.error(`Job ${job.id} failed with error: ${err.message}`);
});

// Export the queue
module.exports = myQueue;
```
#### Step 4: Create the Express App
Create a file named ``app.js`` for your Express application.
```javascript
// app.js
const express = require('express');
const redisClient = require('./redisClient');
const myQueue = require('./queue');

const app = express();
const PORT = 3000;

// Middleware to parse JSON bodies
app.use(express.json());

// Route to add a job to the queue
app.post('/enqueue', async (req, res) => {
    const { data } = req.body;
    const job = await myQueue.add(data);
    res.json({ message: `Job ${job.id} added to the queue`, jobId: job.id });
});

// Route to get the job status by job ID
app.get('/job/:id', async (req, res) => {
    const jobId = req.params.id;
    const job = await myQueue.getJob(jobId);
    
    if (!job) {
        return res.status(404).json({ error: `Job ${jobId} not found` });
    }

    const jobInfo = {
        id: job.id,
        data: job.data,
        status: job.finishedOn ? 'completed' : job.failedReason ? 'failed' : 'waiting'
    };

    res.json(jobInfo);
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
```
#### Step 5: Start the Redis Server
Make sure your Redis server is running. You can start it by running the following command in your terminal (assuming you have Redis installed):
`redis-server`
#### Step 6: Run the Express App
Start your Express app by running: `node app.js`
#### Step 7: Test Your Application
You can test the application using tools like Postman or cURL.

**1. Enqueue a job:**
cURL example: `curl -X POST http://localhost:3000/enqueue -H "Content-Type: application/json" -d '{"data": {"name": "Alice", "action": "sendEmail"}}'`
This should return a response confirming that the job has been added to the queue.

**2. Check the job status:**
Make a ``GET`` request to check the job status: 
cURL example: `curl http://localhost:3000/job/<jobId>`
Replace <jobId> with the actual job ID returned from the enqueue response.
</details>

## Required Files for the Project
**``package.json``**
<details>
<summary>Show/Hide</summary>
```json
{
    "name": "queuing_system_in_js",
    "version": "1.0.0",
    "description": "",
    "main": "index.js",
    "scripts": {
      "lint": "./node_modules/.bin/eslint",
      "check-lint": "lint [0-9]*.js",
      "test": "./node_modules/.bin/mocha --require @babel/register --exit",
      "dev": "nodemon --exec babel-node --presets @babel/preset-env"
    },
    "author": "",
    "license": "ISC",
    "dependencies": {
      "chai-http": "^4.3.0",
      "express": "^4.17.1",
      "kue": "^0.11.6",
      "redis": "^2.8.0"
    },
    "devDependencies": {
      "@babel/cli": "^7.8.0",
      "@babel/core": "^7.8.0",
      "@babel/node": "^7.8.0",
      "@babel/preset-env": "^7.8.2",
      "@babel/register": "^7.8.0",
      "eslint": "^6.4.0",
      "eslint-config-airbnb-base": "^14.0.0",
      "eslint-plugin-import": "^2.18.2",
      "eslint-plugin-jest": "^22.17.0",
      "nodemon": "^2.0.2",
      "chai": "^4.2.0",
      "mocha": "^6.2.2",
      "request": "^2.88.0",
      "sinon": "^7.5.0"
    }
  }
```
</details>
**``.babelrc``**
```
{
  "presets": [
    "@babel/preset-env"
  ]
}
```
and…
Don’t forget to run ``$ npm install`` when you have the ``package.json``

## Tasks
### 0. Install a redis instance
Download, extract, and compile the latest stable Redis version (higher than 5.0.7 - [https://redis.io/downloads/](https://redis.io/downloads/)):
```bash
$ wget http://download.redis.io/releases/redis-6.0.10.tar.gz
$ tar xzf redis-6.0.10.tar.gz
$ cd redis-6.0.10
$ make
```
- Start Redis in the background with ``src/redis-server`` `$ src/redis-server &`
- Make sure that the server is working with a ping ``src/redis-cli ping`` `PONG`
- Using the Redis client again, set the value School for the key Holberton
```bash
127.0.0.1:[Port]> set Holberton School
OK
127.0.0.1:[Port]> get Holberton
"School"
```
- Kill the server with the process id of the redis-server (hint: use ``ps`` and ``grep``) ``$ kill [PID_OF_Redis_Server]``

Copy the ``dump.rdb`` from the ``redis-5.0.7`` directory into the root of the Queuing project.

Requirements:
Running ``get Holberton`` in the client, should return ``School``

### 1. Node Redis Client
Install [node_redis](https://github.com/redis/node-redis) using npm

Using Babel and ES6, write a script named ``0-redis_client.js``. It should connect to the Redis server running on your machine:
- It should log to the console the message ``Redis client connected to the server`` when the connection to Redis works correctly
- It should log to the console the message ``Redis client not connected to the server``: ERROR_MESSAGE when the connection to Redis does not work
**Requirements:**
To import the library, you need to use the keyword ``import``
```bash
$ ps ax | grep redis-server
 2070 pts/1    S+     0:00 grep --color=auto redis-server
$ 
$ npm run dev 0-redis_client.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "0-redis_client.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 0-redis_client.js`
Redis client not connected to the server: Error: Redis connection to 127.0.0.1:6379 failed - connect ECONNREFUSED 127.0.0.1:6379
Redis client not connected to the server: Error: Redis connection to 127.0.0.1:6379 failed - connect ECONNREFUSED 127.0.0.1:6379
Redis client not connected to the server: Error: Redis connection to 127.0.0.1:6379 failed - connect ECONNREFUSED 127.0.0.1:6379
^C
$ 
$ ./src/redis-server > /dev/null 2>&1 &
[1] 2073
$ ps ax | grep redis-server
 2073 pts/0    Sl     0:00 ./src/redis-server *:6379
 2078 pts/1    S+     0:00 grep --color=auto redis-server
$
$ npm run dev 0-redis_client.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "0-redis_client.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 0-redis_client.js`
Redis client connected to the server
^C
```
### 2. Node Redis client and basic operations
In a file ``1-redis_op.js``, copy the code you previously wrote (``0-redis_client.js``).
Add two functions:
- ``setNewSchool``:
    + It accepts two arguments ``schoolName``, and ``value``.
    + It should set in Redis the value for the key ``schoolName``
    + It should display a confirmation message using ``redis.print``
- ``displaySchoolValue``:
    + It accepts one argument ``schoolName``.
    + It should log to the console the value for the key passed as argument

At the end of the file, call:

- ``displaySchoolValue('Holberton');``
- ``setNewSchool('HolbertonSanFrancisco', '100');``
- ``displaySchoolValue('HolbertonSanFrancisco');``

Requirements:
Use callbacks for any of the operation, we will look at async operations later
```bash
$ npm run dev 1-redis_op.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "1-redis_op.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 1-redis_op.js`
Redis client connected to the server
School
Reply: OK
100
^C
```
### 3. Node Redis client and async operations
In a file ``2-redis_op_async.js``, let’s copy the code from the previous exercise (``1-redis_op.js``)
Using ``promisify``, modify the function ``displaySchoolValue`` to use ES6 ``async / await``
Same result as ``1-redis_op.js``
```bash
$ npm run dev 2-redis_op_async.js

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "2-redis_op_async.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 2-redis_op_async.js`
Redis client connected to the server
School
Reply: OK
100
^C
```
### 4. Node Redis client and advanced operations
In a file named ``4-redis_advanced_op.js``, let’s use the client to store a hash value
**Create Hash:**
Using ``hset``, let’s store the following:
- The key of the hash should be ``HolbertonSchools``
- It should have a value for:
    + ``Portland=50``
    + ``Seattle=80``
    + ``New York=20``
    + ``Bogota=20``
    + ``Cali=40``
    + ``Paris=2``
- Make sure you use ``redis.print`` for each ``hset``
**Display Hash:**
Using ``hgetall``, display the object stored in Redis. It should return the following:
Requirements:
Use callbacks for any of the operation, we will look at async operations later
```bash
$ npm run dev 4-redis_advanced_op.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "4-redis_advanced_op.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 4-redis_advanced_op.js`
Redis client connected to the server
Reply: 1
Reply: 1
Reply: 1
Reply: 1
Reply: 1
Reply: 1
{
  Portland: '50',
  Seattle: '80',
  'New York': '20',
  Bogota: '20',
  Cali: '40',
  Paris: '2'
}
^C
``` 
### 5. Node Redis client publisher and subscriber
In a file named ``5-subscriber.js``, create a redis client:
- On connect, it should log the message ``Redis client connected to the server``
- On error, it should log the message ``Redis client not connected to the server: ERROR MESSAGE``
- It should subscribe to the channel ``holberton school channel``
- When it receives message on the channel ``holberton school channel``, it should log the message to the console
- When the message is ``KILL_SERVER``, it should unsubscribe and quit

In a file named 5-publisher.js, create a redis client:

- On connect, it should log the message ``Redis client connected to the server``
- On error, it should log the message ``Redis client not connected to the server: ERROR MESSAGE``
- Write a function named ``publishMessage``:
    + It will take two arguments: ``message`` (string), and ``time`` (integer - in ms)
    + After ``time`` millisecond:
        - The function should log to the console ``About to send MESSAGE``
        - The function should publish to the channel ``holberton school channel``, the message passed in argument after the time passed in arguments
- At the end of the file, call:
```
publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
```
**Requirements:**
- You only need one Redis server to execute the program
- You will need to have two node processes to run each script at the same time

**Terminal 1:**
```bash
$ npm run dev 5-subscriber.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "5-subscriber.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 5-subscriber.js`
Redis client connected to the server
```
**Terminal 2:**
```bash
$ npm run dev 5-publisher.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "5-publisher.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 5-publisher.js`
Redis client connected to the server
About to send Holberton Student #1 starts course
About to send Holberton Student #2 starts course
About to send KILL_SERVER
About to send Holberton Student #3 starts course
^C
```
**And in the same time in Terminal 1:**
```bash
Redis client connected to the server
Holberton Student #1 starts course
Holberton Student #2 starts course
KILL_SERVER
[nodemon] clean exit - waiting for changes before restart
^C
```
Now you have a basic Redis-based queuing system where you have a process to generate job and a second one to process it. These 2 processes can be in 2 different servers, which we also call “background workers”.

### 6. Create the Job creator
In a file named `6-job_creator.js`:
- Create a queue with `Kue`
- Create an object containing the Job data with the following format:
```
{
  phoneNumber: string,
  message: string,
}
```
- Create a queue named `push_notification_code`, and create a job with the object created before
- When the job is created without error, log to the console ``Notification job created: JOB ID``
- When the job is completed, log to the console ``Notification job completed``
- When the job is failing, log to the console ``Notification job failed``
```bash
$ npm run dev 6-job_creator.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "6-job_creator.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 6-job_creator.js`
Notification job created: 1
```
Nothing else will happen - to process the job, go to the next task!
If you execute multiple time this file, you will see the JOB ID increasing - it means you are storing new job to process…

### 7. Create the Job processor
In a file named ``6-job_processor.js``:
- Create a queue with ``Kue``
- Create a function named ``sendNotification``:
    + It will take two arguments ``phoneNumber`` and ``message``
    + It will log to the console ``Sending notification to PHONE_NUMBER, with message: MESSAGE``
- Write the queue process that will listen to new jobs on ``push_notification_code``:
    + Every new job should call the ``sendNotification`` function with the phone number and the message contained within the job data

**Requirements:**
- You only need one Redis server to execute the program
- You will need to have two node processes to run each script at the same time
- You muse use ``Kue`` to set up the queue

**Terminal 2:**
```bash
$ npm run dev 6-job_processor.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "6-job_processor.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 6-job_processor.js`
Sending notification to 4153518780, with message: This is the code to verify your account
```
**Terminal 1:** let’s queue a new job!
```bash
$ npm run dev 6-job_creator.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "6-job_creator.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 6-job_creator.js`
Notification job created: 2
```
**And in the same time in Terminal 2:**
```bash
Sending notification to 4153518780, with message: This is the code to verify your account
```
BOOM! same as ``5-subscriber.js`` and ``5-publisher.js`` but with a module to manage jobs.
 
### 8. Track progress and errors with Kue: Create the Job creator
In a file named ``7-job_creator.js``:
Create an array ``jobs`` with the following data inside:
```json
const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153518743',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4153538781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153118782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4153718781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4159518782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4158718781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153818782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4154318781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4151218782',
    message: 'This is the code 4321 to verify your account'
  }
];
```
After this array created:
- Create a queue with ``Kue``
- Write a loop that will go through the array ``jobs`` and for each object:
    + Create a new job to the queue ``push_notification_code_2`` with the current object
    + If there is no error, log to the console ``Notification job created: JOB_ID``
    + On the job completion, log to the console ``Notification job JOB_ID completed``
    + On the job failure, log to the console ``Notification job JOB_ID failed: ERROR``
    + On the job progress, log to the console ``Notification job JOB_ID PERCENTAGE% complete``

**Terminal 1:**
```bash
$ npm run dev 7-job_creator.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "7-job_creator.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 7-job_creator.js`
Notification job created: 39
Notification job created: 40
Notification job created: 41
Notification job created: 42
Notification job created: 43
Notification job created: 44
Notification job created: 45
Notification job created: 46
Notification job created: 47
Notification job created: 48
Notification job created: 49
```

### 9. Track progress and errors with Kue: Create the Job processor
In a file named ``7-job_processor.js``:
Create an array that will contain the blacklisted phone numbers. Add in it ``4153518780`` and ``4153518781`` - these 2 numbers will be blacklisted by our jobs processor.
Create a function ``sendNotification`` that takes 4 arguments: ``phoneNumber``, ``message``, ``job``, and ``done``:

- When the function is called, track the progress of the ``job`` of ``0`` out of ``100``
- If ``phoneNumber`` is included in the “blacklisted array”, fail the job with an ``Error`` object and the message: ``Phone number PHONE_NUMBER is blacklisted``
- Otherwise:
    + Track the progress to 50%
    + Log to the console ``Sending notification to PHONE_NUMBER, with message: MESSAGE``
Create a queue with ``Kue`` that will proceed job of the queue ``push_notification_code_2`` with two jobs at a time.

**Requirements:**
- You only need one Redis server to execute the program
- You will need to have two node processes to run each script at the same time
- You muse use ``Kue`` to set up the queue
- Executing the jobs list should log to the console the following:

**Terminal 2:**
```bash
$ npm run dev 7-job_processor.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "7-job_processor.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 7-job_processor.js`
Sending notification to 4153518743, with message: This is the code 4321 to verify your account
Sending notification to 4153538781, with message: This is the code 4562 to verify your account
Sending notification to 4153118782, with message: This is the code 4321 to verify your account
Sending notification to 4153718781, with message: This is the code 4562 to verify your account
Sending notification to 4159518782, with message: This is the code 4321 to verify your account
Sending notification to 4158718781, with message: This is the code 4562 to verify your account
Sending notification to 4153818782, with message: This is the code 4321 to verify your account
Sending notification to 4154318781, with message: This is the code 4562 to verify your account
Sending notification to 4151218782, with message: This is the code 4321 to verify your account
```
**And in the same time in terminal 1:**
```bash
...
Notification job #39 0% complete
Notification job #40 0% complete
Notification job #39 failed: Phone number 4153518780 is blacklisted
Notification job #40 failed: Phone number 4153518781 is blacklisted
Notification job #41 0% complete
Notification job #41 50% complete
Notification job #42 0% complete
Notification job #42 50% complete
Notification job #41 completed
Notification job #42 completed
Notification job #43 0% complete
Notification job #43 50% complete
Notification job #44 0% complete
Notification job #44 50% complete
Notification job #43 completed
Notification job #44 completed
Notification job #45 0% complete
Notification job #45 50% complete
Notification job #46 0% complete
Notification job #46 50% complete
Notification job #45 completed
Notification job #46 completed
Notification job #47 0% complete
Notification job #47 50% complete
Notification job #48 0% complete
Notification job #48 50% complete
Notification job #47 completed
Notification job #48 completed
Notification job #49 0% complete
Notification job #49 50% complete
Notification job #49 completed
```

### 10. Writing the job creation function
In a file named ``8-job.js``, create a function named ``createPushNotificationsJobs``:
- It takes into argument ``jobs`` (array of objects), and ``queue`` (``Kue`` queue)
- If ``jobs`` is not an array, it should throw an ``Error`` with message: ``Jobs is not an array``
- For each job in ``jobs``, create a job in the queue ``push_notification_code_3``
- When a job is created, it should log to the console ``Notification job created: JOB_ID``
- When a job is complete, it should log to the console ``Notification job JOB_ID completed``
- When a job is failed, it should log to the console ``Notification job JOB_ID failed: ERROR``
- When a job is making progress, it should log to the console ``Notification job JOB_ID PERCENT% complete``

```bash
$ cat 8-job-main.js 
import kue from 'kue';

import createPushNotificationsJobs from './8-job.js';

const queue = kue.createQueue();

const list = [
    {
        phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
    }
];
createPushNotificationsJobs(list, queue);

$
$ npm run dev 8-job-main.js 

> queuing_system_in_js@1.0.0 dev /root
> nodemon --exec babel-node --presets @babel/preset-env "8-job-main.js"

[nodemon] 2.0.4
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `babel-node --presets @babel/preset-env 8-job-main.js`
Notification job created: 51
```

### 11. Writing the test for job creation
Now that you created a job creator, let’s add tests:
- Import the function ``createPushNotificationsJobs``
- Create a queue with ``Kue``
- Write a test suite for the ``createPushNotificationsJobs`` function:
    + Use ``queue.testMode`` to validate which jobs are inside the queue
    + etc.

**Requirements:**
- Make sure to enter the test mode without processing the jobs before executing the tests
- Make sure to clear the queue and exit the test mode after executing the tests
```bash
$ npm test 8-job.test.js 

> queuing_system_in_js@1.0.0 test /root
> mocha --require @babel/register --exit "8-job.test.js"



  createPushNotificationsJobs
    ✓ display a error message if jobs is not an array
Notification job created: 1
Notification job created: 2
    ✓ create two new jobs to the queue
...

  123 passing (417ms)
```

### 12. In stock?
#### Data
Create an array ``listProducts`` containing the list of the following products:

- Id: 1, name: ``Suitcase 250``, price: 50, stock: 4
- Id: 2, name: ``Suitcase 450``, price: 100, stock: 10
- Id: 3, name: ``Suitcase 650``, price: 350, stock: 2
- Id: 4, name: ``Suitcase 1050``, price: 550, stock: 5

#### Data access
Create a function named ``getItemById``:
- It will take ``id`` as argument
- It will return the item from ``listProducts`` with the same id

#### Server
Create an ``express`` server listening on the port 1245. (You will start it via: ``npm run dev 9-stock.js``)

#### Products
Create the route ``GET /list_products`` that will return the list of every available product with the following JSON format:
```bash
$ curl localhost:1245/list_products ; echo ""
[{"itemId":1,"itemName":"Suitcase 250","price":50,"initialAvailableQuantity":4},{"itemId":2,"itemName":"Suitcase 450","price":100,"initialAvailableQuantity":10},{"itemId":3,"itemName":"Suitcase 650","price":350,"initialAvailableQuantity":2},{"itemId":4,"itemName":"Suitcase 1050","price":550,"initialAvailableQuantity":5}]
```
#### In stock in Redis
Create a client to connect to the Redis server:
- Write a function ``reserveStockById`` that will take ``itemId`` and ``stock`` as arguments:
    + It will set in Redis the stock for the key ``item.ITEM_ID``
- Write an async function ``getCurrentReservedStockById``, that will take ``itemId`` as an argument:
    + It will return the reserved stock for a specific item

#### Product detail
Create the route ``GET /list_products/:itemId``, that will return the current product and the current available stock (by using ``getCurrentReservedStockById``) with the following JSON format:
```bash
$ curl localhost:1245/list_products/1 ; echo ""
{"itemId":1,"itemName":"Suitcase 250","price":50,"initialAvailableQuantity":4,"currentQuantity":4}
```
If the item does not exist, it should return:
```bash
$ curl localhost:1245/list_products/12 ; echo ""
{"status":"Product not found"}
```
#### Reserve a product
Create the route ``GET /reserve_product/:itemId``:
- If the item does not exist, it should return:
```bash
$ curl localhost:1245/reserve_product/12 ; echo ""
{"status":"Product not found"}
```
- If the item exists, it should check that there is at least one stock available. If not it should return:
```bash
$ curl localhost:1245/reserve_product/1 ; echo ""
{"status":"Not enough stock available","itemId":1}
```
- If there is enough stock available, it should reserve one item (by using ``reserveStockById``), and return:
```bash
$ curl localhost:1245/reserve_product/1 ; echo ""
{"status":"Reservation confirmed","itemId":1}
```
**Requirements:**
- Make sure to use ``promisify`` with Redis
- Make sure to use the ``await``/``async`` keyword to get the value from Redis
- Make sure the format returned by the web application is always JSON and not text

### 13. Can I have a seat?
#### Redis
Create a Redic client:
- Create a function ``reserveSeat``, that will take into argument ``number``, and set the key ``available_seats`` with the number
- Create a function ``getCurrentAvailableSeats``, it will return the current number of available seats (by using ``promisify`` for Redis)
- When launching the application, set the number of available to 50
- Initialize the boolean ``reservationEnabled`` to ``true`` - it will be turn to ``false`` when no seat will be available

#### ``Kue`` queue
Create a ``Kue`` queue

#### Server
Create an express server listening on the port 1245. (You will start it via: ``npm run dev 100-seat.js``)
Add the route ``GET /available_seats`` that returns the number of seat available:
```bash
$ curl localhost:1245/available_seats ; echo ""
{"numberOfAvailableSeats":"50"}
```
Add the route ``GET /reserve_seat`` that:
- Returns ``{ "status": "Reservation are blocked" }`` if ``reservationEnabled`` is ``false``
- Creates and queues a job in the queue ``reserve_seat``:
    + Save the job and return:
        - ``{ "status": "Reservation in process" }`` if no error
        - Otherwise: ``{ "status": "Reservation failed" }``
    + When the job is completed, print in the console: ``Seat reservation job JOB_ID completed``
    + When the job failed, print in the console: ``Seat reservation job JOB_ID failed: ERROR_MESSAGE``
```bash
$ curl localhost:1245/reserve_seat ; echo ""
{"status":"Reservation in process"}
```
Add the route ``GET /process`` that:
- Returns ``{ "status": "Queue processing" }`` just after:
- Process the queue ``reserve_seat`` (async):
    + Decrease the number of seat available by using ``getCurrentAvailableSeats`` and ``reserveSeat``
    + If the new number of available seats is equal to 0, set ``reservationEnabled`` to false
    + If the new number of available seats is more or equal than 0, the job is successful
    + Otherwise, fail the job with an ``Error`` with the message ``Not enough seats available``
```bash
$ curl localhost:1245/process ; echo ""
{"status":"Queue processing"}
$ 
$ curl localhost:1245/available_seats ; echo ""
{"numberOfAvailableSeats":"49"}
```
and in the server terminal:
```
Seat reservation job 52 completed
```
and you can reserve all seats:
```bash
$ for n in {1..50}; do curl localhost:1245/reserve_seat ; echo ""; done
{"status":"Reservation in process"}
{"status":"Reservation in process"}
...
{"status":"Reservation in process"}
{"status":"Reservation in process"}
{"status":"Reservation in process"}
{"status":"Reservation are blocked"}
{"status":"Reservation are blocked"}
{"status":"Reservation are blocked"}
```
**Requirements:**

- Make sure to use ``promisify`` with Redis
- Make sure to use the ``await``/``async`` keyword to get the value from Redis
- Make sure the format returned by the web application is always JSON and not text
- Make sure that only the allowed amount of seats can be reserved
- Make sure that the main route is displaying the right number of seats