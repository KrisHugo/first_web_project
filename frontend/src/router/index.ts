import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/userStore.js'

// 1. 定义路由组件 (懒加载)
const Layout = () => import(/* webpackChunkName: "user" */ '@/layouts/MainLayout.vue')
const HomeView = () => import(/* webpackChunkName: "user" */ '@/views/HomeView.vue')
const LoginView = () => import(/* webpackChunkName: "user" */ '@/views/LoginView.vue')
const ProfileView = () => import(/* webpackChunkName: "user" */ '@/views/ProfileView.vue')
const NotFound = () => import(/* webpackChunkName: "user" */ '@/views/NotFound.vue')
// const UserProfile = () => import(/* webpackChunkName: "user" */ '@/views/UserProfile.vue')
// const UserSettings = () => import(/* webpackChunkName: "user" */ '@/views/UserSettings.vue')

// 2. 定义路由规则
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: Layout,
    meta: { requiresAuth: true }, // 需要登录
    children: [
      {
        path: '',
        name: 'home',
        component: HomeView,
        meta: { title: '首页' }
      },
      {
        path: 'profile',
        name: 'profile',
        component: ProfileView,
        meta: { 
          title: '个人资料',
          keepAlive: true // 缓存页面
        }
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { 
      title: '登录',
      guestOnly: true // 仅未登录可访问
    }
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound
  }
]

// 3. 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

// 4. 全局前置守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} | 我的应用`
  }

  // 检查登录状态
  if (to.meta.requiresAuth) {
    if (userStore.isLoggedIn) {
      next()
    } else {
      next({ name: 'login', query: { redirect: to.fullPath } })
    }
  } 
  // 检查仅游客访问
  else if (to.meta.guestOnly && userStore.isLoggedIn) {
    next(from.query.redirect ? { path: from.query.redirect as string } : { name: 'home' })
  } 
  else {
    next()
  }
})

export default router