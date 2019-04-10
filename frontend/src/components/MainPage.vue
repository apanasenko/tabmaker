<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component export default class MainPage extends Vue {}
</script>

<template>
  <div>
    <h1>Портал аналитики</h1>
    <router-link :to="{name:'profile-analytics'}">Аналитика профиля</router-link>
  </div>
</template>

<style scoped lang="scss">
  h3 {
    margin: 40px 0 0;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
</style>
