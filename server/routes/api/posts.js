const express = require('express');
const mongodb = require('mongodb');
require('dotenv').config();

const router = express.Router();

let dbClient;

async function initializeDbConnection() {
  dbClient = await mongodb.MongoClient.connect(process.env.MONGODB_URI, {});
}

initializeDbConnection();

async function loadPostsCollection() {
  return dbClient.db(process.env.MONGODB_NAME).collection(process.env.MONGODB_COLLECTION);
}

// Get Posts
router.get('/', async (req, res) => {
  const posts = await loadPostsCollection();
  const limit = parseInt(req.query.limit) || 10; // default limit to 10 documents
  const skip = parseInt(req.query.skip) || 0; // default skip to 0 documents
  res.send(await posts.find({}).limit(limit).skip(skip).toArray());
});

// Add Post
router.post('/', async (req, res) => {
  const posts = await loadPostsCollection();
  await posts.insertOne({
    createdAt: new Date(),
    sign1: req.body.sign1,
    sign2: req.body.sign2,
    total: req.body.total,
    start: req.body.start,
    end: req.body.end,
    duration: req.body.duration,
    location: req.body.location
  });
  res.status(201).send();
});

// Update Post
router.patch('/:id', async (req, res) => {
  const posts = await loadPostsCollection();
  await posts.updateOne(
    { _id: new mongodb.ObjectID(req.params.id) },
    { $set: {
        sign1: req.body.sign1,
        sign2: req.body.sign2,
        total: req.body.total,
        start: req.body.start,
        end: req.body.end,
        duration: req.body.duration,
        location: req.body.location
      }
    }
  );
  res.status(200).send();
});

// Delete Post
router.delete('/:id', async (req, res) => {
  const posts = await loadPostsCollection();
  await posts.deleteOne({_id: new mongodb.ObjectId(req.params.id)});
  res.status(200).send();
});


module.exports = router;