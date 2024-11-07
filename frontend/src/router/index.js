import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PostsView from '../views/PostsView.vue'
import PostDetailView from '../views/PostDetailView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import TagsView from '../views/TagsView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/posts', name: 'posts', component: PostsView },
  { path: '/posts/:slug', name: 'post-detail', component: PostDetailView },
  { path: '/categories', name: 'categories', component: CategoriesView },
  { path: '/tags', name: 'tags', component: TagsView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router