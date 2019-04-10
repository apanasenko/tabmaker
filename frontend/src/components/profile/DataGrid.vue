<template>
  <div class="stats-container">
    <div class="stats-header">
      <strong class="score">
        {{ overall }}
      </strong>
    <span class="score-description">{{ text }}</span>
    </div>
    <div class="stats-details">
          <div>{{ og }}</div>
          <div>{{ oo }}</div>
          <div>{{ cg }}</div>
          <div>{{ co }}</div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

interface Stats {
  overall: number,
  og: number,
  oo: number,
  cg: number,
  co: number,
}

@Component({})
export default class DataGrid extends Vue {
  name!: 'DataGrid';

  @Prop() stats!: Stats;

  @Prop(String) text!: string;

  get overall() { return this.stats.overall; }

  get og() { return this.stats.og; }

  get oo() { return this.stats.oo; }

  get cg() { return this.stats.cg; }

  get co() { return this.stats.co; }
}
</script>

<style scoped lang="scss">
  strong {
    font-weight: 900;
  }

  .stats-container {
    display: flex;
    flex-flow: column;

    .stats-header {
      display: flex;
      flex-flow: column;
      height: 35px;
    }
  }

  .stats-details {
     align-self: center;
      display: flex;
      flex-flow: row wrap;
      align-content: space-around;
      justify-content: space-between;
      height: 60px;

      div {
        flex: 1 0 50%;
      }
}
</style>
