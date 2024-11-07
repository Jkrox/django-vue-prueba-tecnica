<template>
  <div class="comment-form">
    <h3>Add a Comment</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <textarea 
          v-model="content"
          placeholder="Write your comment..."
          required
        ></textarea>
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Posting...' : 'Post Comment' }}
      </button>
    </form>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'CommentForm',
  props: {
    postId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      content: '',
      loading: false
    }
  },
  methods: {
    handleSubmit() {
      this.loading = true
      api.createComment({
        post: this.postId,
        content: this.content
      })
        .then(() => {
          this.content = ''
          this.$emit('comment-added')
        })
        .catch(error => {
          console.error('Error posting comment:', error)
        })
        .finally(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style scoped>
.comment-form {
  margin-top: 2rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

textarea {
  width: 100%;
  min-height: 100px;
  margin-bottom: 1rem;
  padding: 0.5rem;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
}
</style>