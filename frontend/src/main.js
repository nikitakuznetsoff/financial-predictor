import Vue from 'vue'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import VueApexCharts from 'vue-apexcharts'
import Vuex from 'vuex'
import Axios from 'axios'

import App from './App.vue'
import router from './router'
// import store from './store'

Vue.prototype.$http = Axios
Vue.prototype.$http.defaults.headers.common['Authorization'] = 'the best token'

Vue.use(Buefy)
Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
