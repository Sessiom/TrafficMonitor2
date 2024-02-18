<template>
  <div class = "container">
    <h1 style="text-align: center;">Latest Posts</h1>
    <div style="text-align: center;">
      <button @click="showForm = !showForm">Enter Manually</button>
    </div>
    <form @submit.prevent = "createPost" v-if="showForm" class="create-post">
      <label for="create-sign1">Sign 1</label>
      <input type="number" id="create-sign1" v-model.number="sign1" placeholder="Number of cars">
      <br>
      <label for="create-sign2">Sign 2</label>
      <input type="number" id="create-sign2" v-model.number="sign2" placeholder="Number of cars">
      <br>
      <label for="create-total">Total</label>
      <input type="number" id="create-total" :value="total" placeholder="Total number of cars" readonly>
      <br>
      <div><button type="submit">Post!</button></div>
    </form>
    <hr>
    <p class="error" v-if="error">{{ error }}</p>
    <div v-if="loading">Loading...</div>
    <div class = "posts-container" v-else>
      <div class="post"
        v-for="(post, index) in posts"
        v-bind:item="post"
        v-bind:index="index"
        v-bind:key="post._id">
        <button class ="delete-button" v-on:click="deletePost(post._id)">Delete</button>
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
      </div>
    </div>
  </div>
</template>

<script>
import PostService from '../PostService';
import { useToast } from 'vue-toastification';
const toast = useToast();

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
      showForm: false, // New data property to control form visibility
    }
  },
  async created() {
    this.loading = true;
    toast.info('Loading posts...');
    try {
      const posts = await PostService.getPosts();
      this.posts = posts.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      toast.clear();
    } catch (err) {
      this.error = err.message;
      toast.error('Failed to load posts.');
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
      try {
        toast.info('Working...');
        await PostService.insertPost(this.sign1, this.sign2, this.total);
        const posts = await PostService.getPosts();
        this.posts = posts.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        toast.clear();
        toast.success('New post added successfully!');
      } catch (error) {
        toast.error('Failed to add new post.');
      }
  },
    async deletePost(id) {
      try {
        toast.info('Working...');
        await PostService.deletePost(id);
        const posts = await PostService.getPosts();
        this.posts = posts.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        toast.clear();
        toast.success('Post deleted successfully!');
      } catch (error) {
        toast.error('Failed to delete post.');
      }
    },
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
  text-align: left;
  display: grid;
  background-color: white;
  box-shadow: 2px 2px 12px 1px rgba(140,140,140,.5);
  padding: 20px;
  margin: 15px;
}
.delete-button {
  position: absolute;
  top: 0;
  right: 0;
  margin: 5px;
  background-color: red;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  float: right;
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
