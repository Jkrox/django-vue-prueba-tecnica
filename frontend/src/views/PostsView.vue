<template>
  <div class="container">
    <h1>Blog Posts</h1>
    <div class="posts-grid">
      <PostCard 
        v-for="post in posts" 
        :key="post.id" 
        :post="post"
      />
    </div>
    <div v-if="loading">Loading...</div>
  </div>
</template>

<script>
import PostCard from '@/components/PostCard.vue'
import api from '@/services/api'

export default {
  name: 'PostsView',
  components: {
    PostCard
  },
  data() {
    return {
      posts: [],
      loading: false
    }
  },
  mounted() {
    this.fetchPosts()
  },
  methods: {
    fetchPosts() {
      this.loading = true
      api.getPosts()
        .then(response => {
          this.posts = response.data.results
        })
        .catch(error => {
          console.error('Error fetching posts:', error)
        })
        .finally(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style scoped>
.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}
</style>