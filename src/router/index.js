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
      name: 'Home',
      component: HomeView,
      //beforeEnter: requireAuth
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/about',
      name: 'About',
      component: AboutView
    },
    {
      path: '/users/:userid',
      name: 'My Profile',
      component: () => import('../views/MyProfileView.vue') // Add this line
    },
    {
      path: '/profiles/:id',
      name: 'Profile Details',
      component: () => import('@/views/ProfileDetails.vue') // or wherever the component is
    },
    {
      path: '/match-report/:profileId',
      name: 'Match Report',
      component: () => import('@/views/MatchReport.vue') // or wherever the component is
    },
    {
      path: '/profiles/new',
      name: 'Create Profile',
      component: () => import('@/views/CreateProfile.vue') // or wherever the component is
    },
    {
      path: '/profiles/favourites',
      name: 'Favourites',
      component: () => import('@/views/Favourites.vue') // or wherever the component is
    },
    {
      path: '/logout',
      name: 'Log Out', 
      component: () => import('@/views/LogOutView.vue') // or wherever the component is
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'Not Found',
      component: () => import('@/views/NotFound.vue')
    },
    
    
    
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const publicPages = ['/login', '/register']
  const authRequired = !publicPages.includes(to.path)

  if (authRequired && !token) {
    return next('/login')
  }

  if ((to.path === '/login' || to.path === '/register') && token) {
    return next('/')
  }

  next()
})


export default router
