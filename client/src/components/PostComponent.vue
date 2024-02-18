<template>
  <div class = "container">
    <h1 style="text-align: center;">Latest Posts</h1>
    <div style="text-align: center;">
      <button @click="showForm = !showForm">Enter Manually</button>
    </div>
    <form v-if="showForm" class="create-post">
      <label for="create-sign1">Sign 1</label>
      <input type="number" id="create-sign1" v-model.number="sign1" placeholder="Number of cars">
      <br>
      <label for="create-sign2">Sign 2</label>
      <input type="number" id="create-sign2" v-model.number="sign2" placeholder="Number of cars">
      <br>
      <label for="create-total">Total</label>
      <input type="number" id="create-total" :value="total" placeholder="Total number of cars" readonly>
      <br>
      <div><button v-on:click="createPost">Post!</button></div>
    </form>
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
        <p class="date">
          {{
            (new Date(post.createdAt).getMonth() + 1) + '/' +
            new Date(post.createdAt).getDate() + '/' +
            new Date(post.createdAt).getFullYear()
          }}
        </p>
        <p class="sign1">Sign 1: {{ post.sign1 }}</p>
        <p class="sign2">Sign 2: {{ post.sign2 }}</p>
        <p class="total">Total: {{ post.total }}</p>
        <button @click="showEditForm = !showEditForm" v-on:click="editPost(index)">Edit</button> <!-- New "Edit" button -->
        <div v-if="showEditForm && (editingIndex === index)"> <!-- New edit form -->
          <input type="text" v-model="editedPost.sign1" @input="editedPost.sign1 = $event.target.value" placeholder="Number of cars">
          <input type="text" v-model="editedPost.sign2" @input="editedPost.sign2 = $event.target.value" placeholder="Number of cars">
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
      sign1: 0,
      sign2: 0,
      total: 0,
      loading: false,
      editingIndex: null, // New data property to track which post is being edited
      editedPost: {}, // New data property to hold the edited post data
      showForm: false, // New data property to control form visibility
      showEditForm: false,
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
  computed: {
    calculatedTotal() {
      return this.sign1 + this.sign2;
    }
  },
  watch: {
    calculatedTotal(newTotal) {
      this.total = newTotal;
    }
  },
  methods: {
    async createPost() {
      await PostService.insertPost(this.sign1, this.sign2, this.total);
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
.create-post {
  text-align: center;
  display: grid;
  background-color: white;
  box-shadow: 2px 2px 12px 1px rgba(140,140,140,.5);
  padding: 20px;
  margin: 15px;
}

</style>
