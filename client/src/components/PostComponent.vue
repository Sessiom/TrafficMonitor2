<template>
  <div class = "container">
    <h1>Latest Posts</h1>
    <div class="create-post">
      <label for="create-title">Title</label>
      <input type="text" id="create-title" v-model="title" placeholder="Title of the post">
      <br>
      <label for="create-likes">Likes</label>
      <input type="number" id="create-likes" v-model.number="likes" placeholder="Number of likes">
      <br>
      <label for="create-post"> Say Something...</label>
      <input type="text" id="create-post" v-model="text" placeholder="Create a post">
      <button v-on:click="createPost">Post!</button>
    </div>
    <hr>
    <p class="error" v-if="error">{{ error }}</p>
    <div v-if="loading">Loading...</div>
    <div class = "posts-container" v-else>
      <div class="post"
        v-for="(post, index) in posts"
        v-bind:item="post"
        v-bind:index="index"
        v-bind:key="post._id"
        v-on:dblclick="deletePost(post._id)"
      >
        <h2 class="title">{{ post.title }}</h2>
        <p class="date">
          {{
            (new Date(post.createdAt).getMonth() + 1) + '/' +
            new Date(post.createdAt).getDate() + '/' +
            new Date(post.createdAt).getFullYear()
          }}
        </p>
        <p class="text">{{ post.text }}</p>
        <h6 class="likes">Likes: {{ post.likes }}</h6>
        <button v-on:click="editPost(index)">Edit</button> <!-- New "Edit" button -->
        <div v-if="editingIndex === index"> <!-- New edit form -->
          <input type="text" v-model="editedPost.title" @input="editedPost.title = $event.target.value" placeholder="Title of the post">
          <input type="text" v-model="editedPost.text" @input="editedPost.text = $event.target.value" placeholder="Create a post">
          <input type="number" v-model.number="editedPost.likes" @input="editedPost.likes = $event.target.value" placeholder="Number of likes">
          <button v-on:click="updatePost(post._id)">Update</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PostService from '../PostService';

export default {
  name: 'PostComponent',
  data() {
    return {
      posts: [],
      error: '',
      text: '',
      title: '',
      likes: 0,
      loading: false,
      editingIndex: null, // New data property to track which post is being edited
      editedPost: {}, // New data property to hold the edited post data
    }
  },
  async created() {
    this.loading = true;
    try {
      this.posts = await PostService.getPosts();
    } catch (err) {
      this.error = err.message;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async createPost() {
      await PostService.insertPost(this.text, this.title, this.likes);
      this.posts = await PostService.getPosts();
    },
    async deletePost(id) {
      await PostService.deletePost(id);
      this.posts = await PostService.getPosts();
    },
    editPost(index) { // New method to handle the "Edit" button click
      this.editingIndex = index;
      this.editedPost = {}; // Reset to an empty object
      Object.assign(this.editedPost, this.posts[index]);
    },
    async updatePost(id) { // New method to handle the form submission and update the post
      await PostService.updatePost(id, this.editedPost);
      this.posts = await PostService.getPosts();
      this.editingIndex = null;
      this.editedPost = {}; // Reset to an empty object
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div.container {
  margin: 0 auto;
  width: 50%;
  text-align: left;
}
p.error {
  border: 1px solid red;
  background-color: pink;
  padding: 10px;
  margin-bottom: 15px;
}

div.post{
  position: relative;
  border: 1px solid green;
  background-color: lightgreen;
  padding: 10px 10px 30px 10px;
  margin-bottom: 15px;
}

div.created-at {
  position: absolute;
  bottom: 0;
  right: 0;
  font-size: 10px;
  color: grey;
  padding: 5px;
  background-color: white;
  border: 1px solid grey;
  border-radius: 5px;
}

p.text {
  font-size: 20px;
  color: black;
  margin-bottom: 10px;
}

</style>
