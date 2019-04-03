import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from './components/MainPage.vue';
import Profile from './components/profile/Profile.vue'

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'index',
      component: HelloWorld,
    },
    {
      path: '/profile',
      name: 'profile-analytics',
      component: Profile,
    },
  ],
});
