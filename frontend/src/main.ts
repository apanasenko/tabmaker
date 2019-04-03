import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import ElementUI from 'element-ui';
import axios from 'axios';
import Cookies from "js-cookie";

Vue.config.productionTip = false;
Vue.config.devtools = true;
Vue.use(ElementUI);

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');


axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
