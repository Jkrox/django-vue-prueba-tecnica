<template>
  <div class="post-card">
    <h2>{{ post.title }}</h2>
    <p class="meta">
      By {{ post.author.username }} on {{ formatDate(post.published_date) }}
    </p>
    <router-link :to="{ name: 'post-detail', params: { slug: post.slug }}" class="read-more">
      Read More
    </router-link>
  </div>
</template>

<script>
import { format } from 'date-fns'

export default {
  name: 'PostCard',
  props: {
    post: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(date) {
      return format(new Date(date), 'MMM d, yyyy')
    }
  }
}
</script>

<style scoped>
.post-card {
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
}

.meta {
  color: #666;
  font-size: 0.9rem;
}

.read-more {
  color: #007bff;
  text-decoration: none;
}
</style>