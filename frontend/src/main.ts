import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import ElementUI from 'element-ui';
import axios from 'axios';
import Cookies from 'js-cookie';
import {getModule} from 'vuex-module-decorators';
import User from '@/store/user';

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

Vue.config.productionTip = false;
Vue.config.devtools = true;
Vue.use(ElementUI);
const userState = getModule(User);
// @ts-ignore
userState.receiveUser(window.userData);

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
