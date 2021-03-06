import {
  Action, Module, Mutation, VuexModule,
} from 'vuex-module-decorators';
import Store from '../store';

@Module({
  dynamic: true,
  store: Store,
  name: 'user',
  namespaced: true,
})
export default class UserModule extends VuexModule {
  public user: object = {};

  @Mutation receiveUser(user: object) {
    this.user = user;
  }
}
