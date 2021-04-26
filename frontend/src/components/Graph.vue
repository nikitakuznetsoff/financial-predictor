<template>
  <div class="graph">
    <b-skeleton size="is-large" v-if="loading" :animated="true"></b-skeleton>
    <section class v-if="!loading">
        <!-- start date: {{ startDate }} -->
        <apexchart type="candlestick" :options="chartOptions" :series="candles"></apexchart>
    </section>
    
  </div>
</template>

<script>
import axios from 'axios'
import API_URL from '../common/config'

export default {
  name: 'Graph',
  components: {

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

      chartOptions: {
        chart: {
          type: 'candlestick',
        },
        animations: {
          enabled: true,
          speed: 2000,
        },
        annotations: {
          xaxis: [
            {
              x: '2021-04-23 23:00:00',
              borderColor: '#FF6B6B',
              label: {
                borderColor: '#FF6B6B',
                style: {
                  fontSize: '13px',
                  color: '#fff',
                  background: '#FF6B6B'
                },
                orientation: 'vertical',
                // offsetY: 7,
                text: 'Это прогноз стоимости мудила'
              }
            }
          ],
          points: [
            {
              x: '2021-04-23 23:00:00',
              y: 65,
              borderColor: '#FF4560',
              marker: {
                size: 8,
              },
              label: {
                borderColor: '#FF4560',
                text: 'Прогноз стоимости',
                orientation: 'vertical',
              }
            }
          ]
        },
        xaxis: {
          type: 'category',
          
        },
        yaxis: {
          tooltip: {
            enabled: true
          }
        },
      },
      annotations: {
          xaxis: [
            {
              x: new Date('2021-04-24').getTime(),
              borderColor: '#775DD0',
              label: {
                style: {
                  color: '#fff',
                },
                text: 'X-axis annotation - 22 Nov'
              }
            }
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
      return new Date(this.getInterval(this.tabIndex));
    }
  },
  created() {
    this.getCandles();
    this.getPrediction();
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
          this.candles = [ response.data ];
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
      let algo = this.algo;
      // let candles = this.candles.data;
      axios.post(API_URL+'/tasks/'+algo, this.candles[0])
      .then(resp => {
        console.log(resp);
      })
      .catch(err => {
        console.log(err);
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
