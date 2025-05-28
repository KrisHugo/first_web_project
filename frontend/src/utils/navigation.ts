import router from '@/router/index.js'

export const navigateTo = (name: string, params?: any) => {
  if (params) {
    router.push({ name, params })
  } else {
    router.push({ name })
  }
}

export const replaceTo = (name: string) => {
  router.replace({ name })
}