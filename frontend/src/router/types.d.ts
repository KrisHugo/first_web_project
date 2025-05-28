import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    // 页面标题
    title?: string
    // 是否需要认证
    requiresAuth?: boolean
    // 仅未登录可访问
    guestOnly?: boolean
    // 是否缓存页面
    keepAlive?: boolean
    // 权限码
    permissions?: string[]
  }
}