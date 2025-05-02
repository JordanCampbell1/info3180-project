import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'

// Lazy-loaded views (optimal for performance)
const AboutView = () => import('../views/AboutView.vue')

/* Middleware: Auth Guard
function requireAuth(to, from, next) {
  const token = localStorage.getItem('token')
  if (!token) {
    next('/login')  // Redirect to login if no token exists
  } else {
    next()
  }
}*/

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      //beforeEnter: requireAuth
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/profile',
      name: 'my-profile',
      component: () => import('../views/MyProfileView.vue') // Add this line
    },
    {
      path: '/profiles/:id',
      name: 'ProfileDetails',
      component: () => import('@/views/ProfileDetails.vue') // or wherever the component is
    },
    {
      path: '/match-report/:profileId',
      name: 'Match Report',
      component: () => import('@/views/MatchReport.vue') // or wherever the component is
    },
    {
      path: '/profiles/new',
      name: 'CreateProfile',
      component: () => import('@/views/CreateProfile.vue') // or wherever the component is
    },
    {
      path: '/profiles/favourites',
      name: 'Favourites',
      component: () => import('@/views/Favourites.vue') // or wherever the component is
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFound.vue')
    },
    
    
  ]
})

export default router
