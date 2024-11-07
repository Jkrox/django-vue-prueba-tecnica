import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import PostCard from '@/components/PostCard.vue'

describe('PostCard.vue', () => {
  it('renders post title', () => {
    const post = {
      title: 'Test Post',
      author: { username: 'testuser' },
      published_date: '2024-01-20T12:00:00Z',
      slug: 'test-post'
    }
    
    const wrapper = mount(PostCard, {
      props: { post }
    })
    
    expect(wrapper.text()).toContain('Test Post')
    expect(wrapper.text()).toContain('testuser')
  })
})