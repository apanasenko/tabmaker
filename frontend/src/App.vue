<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import User from './store/user';

const userState = getModule(User);

@Component
export default class App extends Vue {
  public get user(): object|null {
    return userState.user;
  }

  async created() {
    if (!this.user) {
      window.location.assign(`/profile/login?next=/analytics${this.$route.path}`);
    }
  }
}
</script>

<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style lang="stylus">
  #app
    font-family 'Avenir', Helvetica, Arial, sans-serif
    -webkit-font-smoothing antialiased
    -moz-osx-font-smoothing grayscale
    text-align center
    color #2c3e50
    width 900px
    margin 50px auto

  #nav
    padding 30px

    a
      font-weight bold
      color #2c3e50

      &.router-link-exact-active
        color #42b983
</style>
