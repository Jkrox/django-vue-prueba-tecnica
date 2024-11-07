<template>
  <div class="container">
    <h1>Categories</h1>
    <div class="category-list">
      <div class="category-card" v-for="category in categories" :key="category.id">
        <h2>{{ category.name }}</h2>
        <p>{{ category.description }}</p>
        <p>Posts: {{ category.posts_count }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CategoriesView',
  data() {
    return {
      categories: []
    }
  },
  mounted() {
    this.fetchCategories()
  },
  methods: {
    fetchCategories() {
      axios.get('/api/categories/')
        .then(response => {
          this.categories = response.data
        })
        .catch(error => {
          console.error('Error fetching categories:', error)
        })
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

.category-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  grid-gap: 1rem;
}

.category-card {
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  padding: 1rem;
}

.category-card h2 {
  margin-top: 0;
}
</style>