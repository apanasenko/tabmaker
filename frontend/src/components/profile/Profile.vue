<script lang="ts">
import Vue from 'vue';
import axios from 'axios';
import qs from 'query-string';
import Component from 'vue-class-component';
import CubeShadow from '@/components/common/CubeShadow.vue';
import DataGrid from '@/components/profile/DataGrid.vue';
import LineChart from './LineChart.vue';

function posStats(arr: any): any {
  const amount = arr.length;
  const rate = arr.map((el: number[]) => el[0])
    .reduce((a: number, b: number) => a + b, 0) / amount;
  const speaker = arr.map((el: number[]) => el[1])
    .reduce((a: number, b: number) => a + b, 0) / amount;
  return { amount, rate: rate.toFixed(2), speaker: speaker.toFixed(2) };
}

  @Component({
    components: {
      CubeShadow,
      DataGrid,
      LineChart,
    },
  })
export default class Profile extends Vue {
    profile: any = {};

    loaded: boolean = false;

    async fetchProfile() {
      const response = await axios.get(
        '/analytics/api/profile',
        { paramsSerializer: qs.stringify },
      );
      this.profile = response.data;
      this.loaded = true;
    }

    getStatsName(name: string) {
      return {
        overall: posStats(this.profile.analytics.overall)[name],
        og: posStats(this.profile.analytics.og)[name],
        oo: posStats(this.profile.analytics.oo)[name],
        cg: posStats(this.profile.analytics.cg)[name],
        co: posStats(this.profile.analytics.co)[name],
      };
    }

    get dataCollection() {
      return {
        labels: this.profile.analytics.overall.map((x: any) => x[0]),
        datasets: [{
          backgroundColor: 'rgba(0, 0, 120, 0.2)',
          borderWidth: 1,
          borderColor: 'rgba(100, 100, 250, 1)',
          pointBackgroundColor: 'rgba(100, 100, 250, 1)',
          pointRadius: 2,
          data: this.profile.analytics.overall.map((x: any) => x[1]),
        }],
      };
    }

    async created() {
      await this.fetchProfile();
    }
}
</script>

<template>
  <div v-if="!loaded" class="loader">
    <cube-shadow />
    <span>Collecting your data...</span>
  </div>
  <div v-else class="profile-wrapper">
    <div class="overall-statistics">
      <div class="legend-wrapper">
        <div class="header-name">
          {{ profile.first_name }} {{ profile.last_name }}
        </div>
        <div class="legend-wrapper__table">
          <table cellSpacing="15">
            <tbody>
            <tr>
              <td>ОП</td>
              <td>ОО</td>
            </tr>
            <tr>
              <td>ЗП</td>
              <td>ЗО</td>
            </tr>
            </tbody>
          </table>
        </div>
        <div class="general-stats">
          <span>Всего игр отсужено: {{ profile.analytics.judgement }}</span>
        </div>
      </div>
      <data-grid :stats="getStatsName('amount')" text="Всего игр сыграно" />
      <data-grid :stats="getStatsName('rate')" text="Среднее место" />
      <data-grid :stats="getStatsName('speaker')" text="Средний спикерский" />
    </div>
    <div class="chart-wrapper">
      <h2>Спикерские баллы по отборочным играм</h2>
      <line-chart :data="dataCollection" />
    </div>
  </div>
</template>

<style lang="stylus">
  .loader
    margin 0 auto
    width 150px
    display flex
    flex-flow column

  .overall-statistics
    display flex
    justify-content space-around

  .legend-wrapper
    width 270px
    display flex
    flex-flow column

    .legend-wrapper__table
      align-self center

    .header-name
      height 35px
      font-size 28px

  .general-stats
    display flex
    margin-left 40px
  .chart-wrapper
    max-height 300px
</style>
