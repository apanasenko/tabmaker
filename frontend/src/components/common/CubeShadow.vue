<template>
  <div v-bind:style="styles" class="spinner spinner--cube-shadow"></div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

function getRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i += 1) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

@Component({})
export default class CubeShadow extends Vue {
  name!: 'CubeShadow';

  @Prop({ default: '150px' }) size!: string;

  @Prop({ default: getRandomColor() }) background!: string;

  @Prop({ default: '1.8s' }) duration!: string;

  get styles() {
    return {
      width: this.size,
      height: this.size,
      backgroundColor: this.background,
      animationDuration: this.duration,
    };
  }
}
</script>

<style lang="scss" scoped>
  .spinner {
    animation: cube-shadow-spinner 1.8s cubic-bezier(0.75, 0, 0.5, 1) infinite;
  }

  @keyframes cube-shadow-spinner {
    50% {
      border-radius: 50%;
      transform: scale(0.5) rotate(360deg);
    }
    100% {
      transform: scale(1) rotate(720deg);
    }
  }
</style>
