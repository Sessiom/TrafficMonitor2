import axios from 'axios';

const url = 'http://localhost:5000/api/posts/';

class PostService {
    // Get Posts
    static getPosts() {
        return axios.get(url)
            .then(res => {
                const data = res.data;
                return data.map(post => ({
                    ...post,
                    createdAt: new Date(post.createdAt)
                }));
            })
            .catch(err => {
                throw err;
            });
    }

    // Create Post
    static insertPost(text, title, likes) {         // added title parameter
        return axios.post(url, {
            text,
            title,
            likes
        });
    }

    // Update Post
    static updatePost(id, updatedPost) { // New updatePost method
        return axios.patch(`${url}${id}`, updatedPost);
    }

    // Delete Post
    static deletePost(id) {
        return axios.delete(`${url}${id}`);
    }
}

export default PostService;