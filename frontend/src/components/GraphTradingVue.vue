<template>
  <div class="graph ml-3">
    <b-skeleton 
      size="is-large" 
      v-if="loading" 
      :animated="true"
      :height="500"
    ></b-skeleton>
    <section class v-if="!loading">
        <trading-vue 
          :data="candles" 
          :titleTxt="this.$route.params.name"
          :indexBased="true"
          :width="1300"
          :height="600"
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
    algo: String
  },
  data() {
    return {
      candles: null,
      candles_is_empty: false,
      loading: true,
      errored: false,
      error_text: null,

      chart: {
        type: "Candles",
        data: [],
        indexBased: true
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
      return new Date(this.getInterval(this.tabIndex));
    }
  },
  created() {
    // this.getCandles();
    // this.getPrediction();
  },
  watch: {
    $route: 'getCandles',
    startDate: function() {
      this.getCandles();
      this.getPrediction();
    },
    interval: function() {
      this.getCandles();
      this.getPrediction();
    },
    algo: function() {
      this.candles[0]['data'].pop();
      this.chartOptions.annotations.points.pop();
      this.chartOptions.annotations.xaxis.pop();
      this.getPrediction();
    }
  },
  methods: {
    getCandles() {
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
          this.chart.data = response.data.candles;
        }
      })
      .catch(e => {
        console.log(e);
        this.errored = true;
        this.error_text = e;
      })
      .finally(() => {
        this.loading = false;
      })
    },
    getPrediction() {
      this.loading = true;
      let algo = this.algo;
      axios.post(API_URL+'/tasks/'+algo, this.candles[0])
      .then(resp => {
        console.log(resp);
        let info = resp.data;
        // let point = {
        //   x: '2021-04-26 18:00:00',
        //   y: 50
        // }
        let candle = {
          x: info['date'],
          y: [info['prediction'], info['prediction'], info['prediction'], info['prediction']]
        }
        this.candles[0]['data'].push(candle);
        let p = {
              x: info['date'],
              y: info['prediction'],
              borderColor: '#FF4560',
              marker: {
                size: 8,
              },
              label: {
                borderColor: '#FF4560',
                text: 'Прогноз',
                orientation: 'vertical',
              }
            }

        let xas = {
              x: info['date'],
              borderColor: '#FF6B6B',
              // label: {
              //   borderColor: '#FF6B6B',
              //   style: {
              //     fontSize: '13px',
              //     color: '#fff',
              //     background: '#FF6B6B'
              //   },
              //   orientation: 'vertical',
              //   // offsetY: 7,
              //   text: 'Это прогноз стоимости мудила'
              // }
            }
        this.chartOptions.annotations.points.push(p);
        this.chartOptions.annotations.xaxis.push(xas);
      })
      .catch(err => {
        console.log(err);
      })
      .finally(() => {
        this.loading = false;
      })
    },
    getInterval(value) {
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
  }
}
</script>
