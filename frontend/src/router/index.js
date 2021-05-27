import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'

Vue.use(VueRouter)

const DEFAULT_TITLE = 'Financial Predictor'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/registration',
    name: 'Registration',
    component: () => import('@/views/Registration.vue'),
    meta: {
      title: DEFAULT_TITLE + ' | Registration'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: DEFAULT_TITLE + ' | Login'
    }
  },
  {
    path: '/quote/:name',
    component: () => import('@/views/Quote.vue'),
    children: [
      {
        path: 'technical',
        name: 'QuoteTechnical',
        component: () => import('@/components/QuoteTechnical.vue'),
        meta: {
          title: DEFAULT_TITLE + ' | Technical information'
        }
      },
      {
        path: '',
        name: 'QuoteForecast',
        component: () => import('@/components/QuoteForecast.vue'),
        meta: {
          title: DEFAULT_TITLE + ' | Forecast'
        }
      },
    ]
  },
  {
    path: '/news/:id',
    name: 'News',
    component: () => import('@/views/NewsItem.vue'),
    meta: {
      title: DEFAULT_TITLE + ' | News'
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: {
      requiredAuth: true,
      title: DEFAULT_TITLE + ' | Profile'
    }
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiredAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})

export default router
