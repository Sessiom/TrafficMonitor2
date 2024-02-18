const express = require('express');
const mongodb = require('mongodb');
require('dotenv').config();

const router = express.Router();

// Get Posts
router.get('/', async (req, res) => {
  const posts = await loadPostsCollection();
  res.send(await posts.find({}).toArray());
});

// Add Post
router.post('/', async (req, res) => {
  const posts = await loadPostsCollection();
  await posts.insertOne({
    createdAt: new Date(),
    sign1: req.body.sign1,
    sign2: req.body.sign2,
    total: req.body.total
  });
  res.status(201).send();
});

// Update Post
router.patch('/:id', async (req, res) => {
  const posts = await loadPostsCollection();
  const update = { $set: {} };
  if (req.body.title !== undefined) {
    update.$set.title = req.body.title;
  }
  if (req.body.text !== undefined) {
    update.$set.text = req.body.text;
  }
  if (req.body.likes !== undefined) {
    update.$set.likes = req.body.likes;
  }
  await posts.updateOne(
    { _id: new mongodb.ObjectId(req.params.id) },
    update
  );
  res.status(200).send();
});

// Delete Post
router.delete('/:id', async (req, res) => {
  const posts = await loadPostsCollection();
  await posts.deleteOne({_id: new mongodb.ObjectId(req.params.id)});
  res.status(200).send();
});

async function loadPostsCollection() {
  const client = await mongodb.MongoClient.connect(process.env.MONGODB_URI, {
  });

  return client.db(process.env.MONGODB_NAME).collection(process.env.MONGODB_COLLECTION);
}

module.exports = router;