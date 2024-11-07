<template>
  <div class="container">
    <h1>Tags</h1>
    <div class="tag-list">
      <div class="tag-card" v-for="tag in tags" :key="tag.id">
        <h2>{{ tag.name }}</h2>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TagsView',
  data() {
    return {
      tags: []
    }
  },
  mounted() {
    this.fetchTags()
  },
  methods: {
    fetchTags() {
      axios.get('/api/tags/')
        .then(response => {
          this.tags = response.data
        })
        .catch(error => {
          console.error('Error fetching tags:', error)
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

.tag-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  grid-gap: 1rem;
}

.tag-card {
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  padding: 1rem;
  text-align: center;
}

.tag-card h2 {
  margin-top: 0;
}