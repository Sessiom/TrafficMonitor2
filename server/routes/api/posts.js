const express = require('express');
const mongodb = require('mongodb');

const router = express.Router();

// Get Posts
router.get('/', async (req, res) => {
  const posts = await loadPostsCollection();
  res.send(await posts.find({}).toArray());
});

// Add Post
router.post('/', async (req, res) => {
  const posts = await loadPostsCollection();
  const likes = parseInt(req.body.likes, 10);
  await posts.insertOne({
    title: req.body.title,
    text: req.body.text,
    likes: req.body.likes,
    createdAt: new Date()
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
  const client = await mongodb.MongoClient.connect('mongodb+srv://asdf:asdf@cluster0.fk1xdy4.mongodb.net/?retryWrites=true&w=majority', {
  });

  return client.db('amazify').collection('Traffic');
}

module.exports = router;