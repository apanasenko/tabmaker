import { Module, Mutation, VuexModule } from 'vuex-module-decorators';
import store from '@/store';

@Module({
  name: 'user',
  store,
  namespaced: true,
  dynamic: true,
})
export default class UserModule extends VuexModule {
  public user: object | null = null;

  @Mutation receiveUser(user: object) {
    this.user = user;
  }
}
