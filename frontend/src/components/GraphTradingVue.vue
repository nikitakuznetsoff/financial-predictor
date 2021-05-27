<template>
  <div class="graph-trading-vue">
    <b-skeleton 
      size="is-large" 
      v-if="loading" 
      :animated="true"
      :height="600"
    ></b-skeleton>
    <section class v-if="!loading">
        <trading-vue 
          :data="graph" 
          :titleTxt="this.$route.params.name"
          :width="this.width"
          :overlays="overlays"
          :height="600"
          :chart-config=" { DEFAULT_LEN: 110 } "
          :color-back="'#fff'"
          :color-grid="'#eee'"
          :color-text="'#333'">
        </trading-vue>
    </section>
    
  </div>
</template>

<script>
import axios from 'axios'
import API_URL from '../common/config'
import TradingVue from 'trading-vue-js'

export default {
  name: 'Graph',
  components: {
    TradingVue
  },
  props: {
    interval: Number,
    tabIndex: Number,
    algo: String,
    width: Number
  },
  data() {
    return {
      candles: null,
      candles_is_empty: false,
      loading: true,
      errored: false,
      error_text: null,

      time_gap: 1000 * 60 * 60 * 3,

      graph: {
          chart: {
          type: "Candles",
          data: [],
          indexBased: true,
        },
        onchart: [
          {
            name: 'Predictions',
            type: 'Splitters',
            data: [
              [Date.now() + 1000 * 60 * 60 * 3, "Pritet", 1, "#34a853", 0.75],
            ],
            settings: {
              font: '10x Arial'
            }
          },
        ],
        offchart: [

        ]
      },
      intervals: {
        'day': 1000 * 60 * 60 * 24,
        'week': 1000 * 60 * 60 * 24 * 7,
        'month': 1000 * 60 * 60 * 24 * 30,
        'year': 1000 * 60 * 60 * 24 * 30 * 12,
      },
    }
  },
  computed: {
    startDate: function() {
      return new Date(this.getStartDate(this.tabIndex));
    }
  },
  created() {
    // this.getCandles();
    // this.getPrediction();
  },
  watch: {
    $route: 'getCandles',
    startDate: function() {
      this.graph.onchart = [];
      this.graph.offchart = [];
      this.getCandles();
      // this.getPrediction();
    },
    interval: function() {
      this.graph.onchart = [];
      this.graph.offchart = [];
      this.getCandles();
      // this.getPrediction();
    },
    algo: function() {
      this.getPrediction();
    }
  },
  methods: {
    getCandles() {
      this.graph.onchart = [];
      this.graph.offchart = [];
      this.$parent.loading = true;
      this.candles = this.error_text = null;
      this.errored = this.candles_is_empty = false;
      this.loading = true;
      let month = this.startDate.getMonth() + 1;
      var startDate = this.startDate.getFullYear()+'-'+month+'-'+this.startDate.getDate();
      var interval = this.interval;

      // response structure http://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/57/securities/AFLT/candles.json?from=2021-04-13&interval=10
      axios.get(API_URL+'/security/'+this.$route.params.name+'/candles?from='+startDate+'&interval='+interval)
      .then(response => {
        if (response.status != 200) {
          this.candles_is_empty = true;
        } else {
          this.candles = { ohlcv: response.data.candles };
          this.graph.chart.data = response.data.candles;
        }
      })
      .catch(e => {
        this.errored = true;
        this.error_text = e;
      })
      .finally(() => {
        this.loading = false;
        this.$parent.loading = false;
      })
    },
    getPrediction() {
      this.loading = true;
      this.$parent.loading = true;
      let curr_algo = this.algo;
      let body = {
        candles: this.graph.chart.data,
        algo: curr_algo,
        count: 25
      }
      axios.post(API_URL+'/tasks', body)
      .then(resp => {
        let predictions = resp.data.prediction.values;
        let last_timestamp = this.graph.chart.data[this.graph.chart.data.length-1][0];
        let curr_interval = this.interval;
        let time_interval = this.getTimeFromInterval(curr_interval);
        let points = []
        for (let i = 0; i < predictions.length; i++) {
          let point_with_data = [last_timestamp + time_interval * (i+1), predictions[i]]
          points.push(point_with_data)
        }
        let spline = {
            name: curr_algo,
            type: 'Spline',
            data: points,
            settings: {
              lineWidth: 4
            }
          }
        console.log(points)
        // let point = null;
        // if (info < this.graph.chart.data[this.graph.chart.data.length-1][1]) {
        //   point = [Date.now() + this.time_gap, 0,  info, curr_algo];
        // } else {
        //   point = [Date.now() + this.time_gap, 1,  info, curr_algo];
        // }
        this.graph.onchart.push(spline)
      })
      .catch(err => {
        console.log(err);
      })
      .finally(() => {
        this.loading = false;
        this.$parent.loading = false;
      })
    },
    getStartDate(value) {
      switch (value) {
        case 0:
          return Date.now() - this.intervals['day'];
        case 1:
          return Date.now() - this.intervals['week'];
        case 2:
          return Date.now() - this.intervals['month'];
        case 3:
          return Date.now() - this.intervals['month'] * 3;
        case 4:
          return Date.now() - this.intervals['month'] * 6;
        case 5:
          return Date.now() - this.intervals['year'];
        case 6:
          return Date.now();
      }
    },
    // Get time in milliseconds from moex interval value
    getTimeFromInterval(interval) {
      switch (interval) {
        case 1:
          return 1000 * 60
        case 10:
          return 1000 * 60 * 10
        case 60:
          return 1000 * 60 * 60
        case 24:
          return 1000 * 60 * 60 * 24
        case 7:
         return 1000 * 60 * 60 * 24 * 7
        case 31:
          return 1000 * 60 * 60 * 24 * 31
        case 4:
          return 1000 * 60 * 60 * 24 * 31 * 3
      }
      return -1
    }
  }
}
</script>
