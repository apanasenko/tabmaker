<script lang="ts">
import Vue from 'vue';
import axios from 'axios';
import qs from 'query-string';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import CubeShadow from '@/components/common/CubeShadow.vue';


@Component({ components: { CubeShadow } })
export default class MotionAnalysis extends Vue {
    motion: object = {};

    loaded: boolean = false;

    @Prop(Number) motionId!: number;

    async fetchMotionAnalysis() {
      const response = await axios.get(
        `/analytics/api/motion/${this.motionId}/`,
        { paramsSerializer: qs.stringify },
      );
      this.motion = response.data;
      this.loaded = true;
    }

    async created() {
      await this.fetchMotionAnalysis();
    }
}
</script>

<template>
 <div v-if="!loaded" class="loader">
    <cube-shadow />
    <span>Collecting your data...</span>
  </div>
  <div v-else>
    <h1>{{ motion.motion }}</h1>
    <p>{{ motion.infoslide }}</p>
    <p> Правительство: {{ motion.analysis.government_score }}</p>
    <p> Оппозиция: {{ motion.analysis.opposition_score }}</p>
  </div>
</template>

<style lang="stylus">
  .loader
    margin 0 auto
    width 150px
    display flex
    flex-flow column
</style>
