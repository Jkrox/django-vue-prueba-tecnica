import axios from 'axios'

const api = {
  // Posts
  getPosts(params) {
    return axios.get('/posts/', { params })
  },
  getPost(slug) {
    return axios.get(`/posts/${slug}/`)
  },
  createPost(data) {
    return axios.post('/posts/', data)
  },
  
  // Categories
  getCategories() {
    return axios.get('/categories/')
  },
  
  // Tags
  getTags() {
    return axios.get('/tags/')
  },
  
  // Comments
  createComment(data) {
    return axios.post('/comments/', data)
  }
}

export default api