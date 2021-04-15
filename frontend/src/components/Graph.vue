<template>
  <div class="graph">
    <b-skeleton size="is-large" v-if="loading"></b-skeleton>
    <section class v-if="!loading">
      <!-- {{ candles }} -->
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
          height: 350
        },
        title: {
          text: 'Chart',
          align: 'left'
        },
        xaxis: {
          type: 'datetime'
        },
        yaxis: {
          tooltip: {
            enabled: true
          }
        }
      },
    }
  },
  created() {
    this.getCandles();
  },
  watch: {
    $route: 'getCandles'
  },
  methods: {
    getCandles() {
      this.candles = this.error_text = null;
      this.errored = this.candles_is_empty = false;
      this.loading = true;
      var start_date = '2021-04-13';
      var interval = 10;

      // response structure http://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/57/securities/AFLT/candles.json?from=2021-04-13&interval=10
      axios.get(API_URL+'/security/'+this.$route.params.name+'/'+start_date+'/'+interval)
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
    }
  }
}
</script>
