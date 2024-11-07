<template>
  <div class="container">
    <div v-if="post">
      <h1>{{ post.title }}</h1>
      <p>{{ post.author.username }} - {{ formatDate(post.published_date) }}</p>
      <p>{{ post.content }}</p>
      <div v-if="post.tags.length > 0">
        <h3>Tags:</h3>
        <div class="tag" v-for="tag in post.tags" :key="tag.id">{{ tag.name }}</div>
      </div>
      <div v-if="post.comments.length > 0">
        <h3>Comments:</h3>
        <div class="comment" v-for="comment in post.comments" :key="comment.id">
          <p><strong>{{ comment.author.username }}</strong> - {{ formatDate(comment.created_at) }}</p>
          <p>{{ comment.content }}</p>
        </div>
      </div>
    </div>
    <p v-else>Loading...</p>
  </div>
</template>

<script>
import axios from 'axios'
import { format } from 'date-fns'

export default {
  name: 'PostDetailView',
  data() {
    return {
      post: null
    }
  },
  mounted() {
    this.fetchPostDetail()
  },
  methods: {
    fetchPostDetail() {
      const slug = this.$route.params.slug
      axios.get(`/api/posts/${slug}/`)
        .then(response => {
          this.post = response.data
        })
        .catch(error => {
          console.error('Error fetching post:', error)
        })
    },
    formatDate(dateString) {
      return format(new Date(dateString), 'MMM d, yyyy')
    }
  }
}
</script>

<style>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.tag {
  display: inline-block;
  background-color: #007bff;
  color: #fff;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  margin-right: 0.5rem;
}

.comment {
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1rem;
}
</style>