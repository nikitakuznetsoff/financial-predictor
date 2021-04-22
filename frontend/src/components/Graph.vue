<template>
  <div class="graph">
    <b-skeleton size="is-large" v-if="loading" :animated="true"></b-skeleton>
    <section class v-if="!loading">
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
        title: {
          text: 'График',
          align: 'left'
        },
        xaxis: {
          type: 'category',
          
        },
        yaxis: {
          tooltip: {
            enabled: true
          }
        }
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
  },
  watch: {
    $route: 'getCandles',
    startDate: function() {
      this.getCandles();
    },
    interval: function() {
      this.getCandles();
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
      axios.get(API_URL+'/security/'+this.$route.params.name+'/'+startDate+'/'+interval)
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
