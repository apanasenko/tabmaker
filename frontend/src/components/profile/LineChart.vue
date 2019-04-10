<script>
import { Line } from 'vue-chartjs';

export default {
  extends: Line,
  props: {
    data: { type: Object, required: true },
    options: { type: Object },
    height: { default: 100 },
  },
  data() {
    return {
      defaults: {
        responsive: true,
        legend: {
          display: false,
        },
        scales: { xAxes: [{ display: false }] },
        layout: { padding: 5 },
      },
    };
  },
  mounted() {
    this.renderChart(this.data, { ...this.defaults, ...this.options });
  },
};
</script>
