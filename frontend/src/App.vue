<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between h-16">
          <div class="flex">
            <router-link to="/" class="flex items-center px-2 py-2 text-gray-700 hover:text-gray-900">
              Home
            </router-link>
            <router-link to="/posts" class="flex items-center px-2 py-2 text-gray-700 hover:text-gray-900">
              Posts
            </router-link>
            <router-link to="/categories" class="flex items-center px-2 py-2 text-gray-700 hover:text-gray-900">
              Categories
            </router-link>
            <router-link to="/tags" class="flex items-center px-2 py-2 text-gray-700 hover:text-gray-900">
              Tags
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>