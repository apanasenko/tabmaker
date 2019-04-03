import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

interface StoreType {
  user: any,
}

export default new Vuex.Store<StoreType>({});
