import express from 'express';
import { promisify } from 'util';
import redis from 'redis';

// Create Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Create Express app
const app = express();
const PORT = 1245;

// Product list
const listProducts = [
  { itemId: 1, itemName: "Suitcase 250", price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: "Suitcase 450", price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: "Suitcase 650", price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: "Suitcase 1050", price: 550, initialAvailableQuantity: 5 }
];

// Function to get item by ID
const getItemById = (id) => {
  return listProducts.find(item => item.itemId === id);
};

// Function to reserve stock by ID
const reserveStockById = async (itemId, stock) => {
  await setAsync(`item.${itemId}`, stock);
};

// Async function to get current reserved stock by ID
const getCurrentReservedStockById = async (itemId) => {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock, 10) : 0; // Convert stock to an integer
};

// Route to list all products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Route to get product details
app.get('/list_products/:itemId', async (req, res) => {
  const id = parseInt(req.params.itemId, 10);
  const product = getItemById(id);

  if (!product) {
    return res.json({ status: "Product not found" });
  }

  const currentQuantity = await getCurrentReservedStockById(id);
  res.json({ ...product, currentQuantity });
});

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const id = parseInt(req.params.itemId, 10);
  const product = getItemById(id);

  if (!product) {
    return res.json({ status: "Product not found" });
  }

  const currentQuantity = await getCurrentReservedStockById(id);

  if (currentQuantity >= product.initialAvailableQuantity) {
    return res.json({ status: "Not enough stock available", itemId: id });
  }

  await reserveStockById(id, currentQuantity + 1); // Reserve one item
  res.json({ status: "Reservation confirmed", itemId: id });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
