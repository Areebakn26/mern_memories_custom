import express from 'express';
import bodyParser from 'body-parser';
import mongoose from 'mongoose';
import cors from 'cors';
import dotenv from 'dotenv';

import postRoutes from './routes/posts.js';

const app = express();
dotenv.config(); // .env file load karega

// Middleware
app.use(bodyParser.json({ limit: '30mb', extended: true }));
app.use(bodyParser.urlencoded({ limit: '30mb', extended: true }));
app.use(cors());

// Routes
app.use('/posts', postRoutes);

// Port from env or fallback
const PORT = process.env.PORT || 5000;

// MongoDB Connection
mongoose.connect(process.env.CONNECTION_URL, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
  .then(() => app.listen(PORT, () =>
    console.log(`✅ Server Running on Port: http://localhost:${PORT}`)
  ))
  .catch((error) => console.log(`❌ Database connection error: ${error.message}`));

// To avoid mongoose deprecation warnings
mongoose.set('strictQuery', true);
