<template>
  <div class="stats-container">
      <span class="score">
        {{ overall }}
      </span>
      <span class="score-description">{{ text }}</span>
    <div class="stats-details">
      <table cellSpacing="15">
        <tbody>
        <tr>
          <td>{{ og }}</td>
          <td>{{ oo }}</td>
        </tr>
        <tr>
          <td>{{ cg }}</td>
          <td>{{ co }}</td>
        </tr>
        </tbody>
      </table>
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

<style scoped lang="stylus">
  .stats-container
    display flex
    flex-flow column
  .stats-details
    align-self center
</style>
