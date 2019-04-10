import Vue from 'vue';
import Router from 'vue-router';
import MainPage from './components/MainPage.vue';
import Profile from './components/profile/Profile.vue';
import Motion from './components/motion-analysis/Motion.vue';
import { mapProps } from '@/utils/routers';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'index',
      component: MainPage,
    },
    {
      path: '/profile',
      name: 'profile-analytics',
      component: Profile,
    },
    {
      path: '/motion/:motionId/',
      name: 'motion-analytics',
      component: Motion,
      props: mapProps({ motionId: Number }),
    },
  ],
});
