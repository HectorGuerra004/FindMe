import { ref } from 'vue'

export const user = ref(
  JSON.parse(localStorage.getItem('user')) || null
)
