<template>
  <div class="quote mx-3 mb-3">
      <section class="hero">
        <div class="hero-body">
          <section v-if="loading">
            <p class="title">
              <b-skeleton size="is-large" :active="loading"></b-skeleton>
            </p>
            <p class="subtitle">
              <b-skeleton size="is-small" :active="loading"></b-skeleton>
            </p>
          </section>
          <section v-else>
            <p class="title">
              <section v-if="quote_is_empty">
                unknown quote
              </section>
              <section v-else>
                {{ quote.LATNAME.value }}
              </section>
            </p>
            <p class="subtitle" v-if="!quote_is_empty">
              {{ $route.params.name }}
            </p>
          </section>
          <!-- <p class="desciption">
              Group Name: {{ quote.GROUPNAME.value }}
          </p> -->
        </div>
      </section>
            <b-tabs position="is-centered" 
              type="is-toggle"
            
              class="block"
              animated="False"
              size="is-small"
              v-model="period"
            >
              <b-tab-item label="1 день" @click="changeIntervalStatus"></b-tab-item>
              <b-tab-item label="1 неделя" @click="changeIntervalStatus"></b-tab-item>
              <b-tab-item label="1 месяц" @click="changeIntervalStatus"></b-tab-item>
              <b-tab-item label="3 месяца" @click="changeIntervalStatus"></b-tab-item>
              <b-tab-item label="6 месяцев" @click="changeIntervalStatus"></b-tab-item>
              <b-tab-item label="1 год" @click="changeIntervalStatus"></b-tab-item>
              <b-tab-item label="Макс" @click="changeIntervalStatus"></b-tab-item>
          </b-tabs>

          <div class="columns">
            <div class="column is-2">
               <b-menu>
                <b-menu-list label="Меню">
                  <b-menu-item icon="information-outline" label="Информация"></b-menu-item>
                  
                  <b-menu-item icon="av-timer" :active="true" expanded>
                    <template #label="props">
                      Интервалы
                      <b-icon class="is-pulled-right" :icon="props.expanded ? 'menu-down' : 'menu-up'"></b-icon>
                    </template>
                    <b-menu-item icon="arrow-right" 
                      label="1 мин" 
                      @click="interval = 1"
                      :disabled="isIntervalAvailable(1)"
                    ></b-menu-item>
                    <b-menu-item icon="arrow-right" 
                      label="10 мин" 
                      @click="interval = 10"
                      :disabled="isIntervalAvailable(10)"
                    ></b-menu-item>
                    <b-menu-item icon="arrow-right" 
                      label="1 час" 
                      @click="interval = 60"
                      :disabled="isIntervalAvailable(60)" 
                    ></b-menu-item>
                    <b-menu-item icon="arrow-right" 
                      label="1 день" 
                      @click="interval = 24"
                      :disabled="isIntervalAvailable(24)" 
                    ></b-menu-item>
                    <b-menu-item icon="arrow-right" 
                      label="1 неделя" 
                      @click="interval = 7"
                      :disabled="isIntervalAvailable(7)" 
                    ></b-menu-item>
                    <b-menu-item icon="arrow-right" 
                      label="1 месяц" 
                      @click="interval = 31"
                      :disabled="isIntervalAvailable(31)" 
                    ></b-menu-item>
                    <b-menu-item icon="arrow-right" 
                      label="3 месяца" 
                      @click="interval = 4" 
                      :disabled="isIntervalAvailable(4)"
                    ></b-menu-item>
                  </b-menu-item>
                </b-menu-list>

                <b-menu-list label="Алгоритмы" icon="chart-areaspline">
                  <b-menu-item label="ARIMA" icon="vector-line" @click="selectedAlgo = 'ARIMA'"></b-menu-item>
                  <b-menu-item label="SARIMA" icon="vector-line" @click="selectedAlgo = 'SARIMA'"></b-menu-item>
                  <b-menu-item label="Прочее" icon="vector-line" @click="selectedAlgo = 'OTHER'"></b-menu-item>
                </b-menu-list>
              </b-menu> 
            </div>

            <div class="column">
              <Graph :tabIndex="period" 
                :interval="interval"
                :algo="selectedAlgo"
              ></Graph>
            </div>
        
          <div class="column is-2">
            <b-skeleton size="is-large" :active="loading"></b-skeleton>
            <div class="card" v-if="!loading">
              <div class="card-content is-size-7">
                <b-table :data="quote" :columns="columns">
                </b-table>
              </div>
            </div>
          </div>
        </div>
  </div>
</template>

<script>
import axios from 'axios'
import API_URL from '../common/config'
import Graph from '@/components/Graph.vue'

export default {
  name: 'Quote',
  components: {
    Graph
  },
  data() {
    return {
      quote: null,
      loading: true,
      quote_is_empty: false,
      errored: false,
      error_text: null,

      period: 0,
      interval: 1,
      selectedAlgo: 'ARIMA',

      is_1_min: null,
      is_10_min: null, 
      is_1_hour: null,
      is_1_day: null,
      is_1_week: null,
      is_1_month: null,
      is_3_month: null,

      columns: [
        {
          'field': 'title',
          'label': 'Title'
        },
        {
          'field': 'value',
          'label': 'Name'
        },
      ],
    }
  },
  created() {
    this.fetchData()
  },
  watch: {
    $route: 'fetchData'
  },
  methods: {
    fetchData() {
      this.quote = this.error_text = null;
      this.quote_is_empty = this.error = false;
      this.loading = true;

      axios.get(API_URL + '/security/' + this.$route.params.name)
      .then(response => {
        if (response.status != 200) {
          this.quote_is_empty = true;
        } else {
          this.quote = response.data.security;  
        }
      })
      .catch(e => {
        console.log(e);
        this.errored = true;
        this.error_text = e;
      })
      .finally(() => {
        this.loading = false
      });
    },
    isIntervalAvailable(interval) {
      let intervals = [1, 10, 60, 24, 7, 31, 4];
      let interval_slice = null;
      // console.log(this.period);
      // console.log(this.interval);
      switch(this.period) {
        case 0:
          interval_slice = intervals.slice(0, 3);
          break;
        case 1:
          interval_slice = intervals.slice(2, 4)
          break;
        case 2:
          interval_slice = intervals.slice(2, 6)
          break;
        case 3:
          interval_slice = intervals.slice(3, 7)
          break;
        case 4:
          interval_slice = intervals.slice(3, 7)
          break;
        case 5:
          interval_slice = intervals.slice(3, 7)
          break;
        case 6:
          interval_slice = intervals.slice(5, 7)
          break;
      }
      if (interval_slice.includes(interval)) {
        return null
      } else {
        return 'disabled'
      }
    },
    changeIntervalStatus() {
      // let intervals = [1, 10, 60, 24, 7, 31, 4];
      // let interval_slice = null;
      // console.log(this.period);
      // console.log(this.interval);
      switch(this.period) {
        case 0:
          this.is_1_min = this.is_10_min = null;
          this.is_1_hour = this.is_1_day = this.is_1_week = this.is_1_month = this.is_3_month = '';
          // interval_slice = intervals.slice(0, 3);
          break;
        case 1:
          this.is_1_hour = this.is_1_day = null;
          this.is_1_min = this.is_10_min = this.is_1_week = this.is_1_month = this.is_3_month = '';
          // interval_slice = intervals.slice(2, 4)
          break;
        case 2:
          this.is_1_day = this.is_1_week = this.is_1_month = null;
          this.is_1_min = this.is_10_min = this.is_1_hour = this.is_3_month = '';
          // interval_slice = intervals.slice(3, 6)
          break;
        case 3:
          this.is_1_week = this.is_1_month = this.is_3_month = null;
          this.is_1_min = this.is_10_min = this.is_1_hour = '';
          // interval_slice = intervals.slice(4, 7)
          break;
        case 4:
          this.is_1_week = this.is_1_month = this.is_3_month = null;
          this.is_1_min = this.is_10_min = this.is_1_hour = '';
          // interval_slice = intervals.slice(4, 7)
          break;
        case 5:
          this.is_1_week = this.is_1_month = this.is_3_month = null;
          this.is_1_min = this.is_10_min = this.is_1_hour = '';
          // interval_slice = intervals.slice(4, 7)
          break;
        case 6:
          this.is_1_month = this.is_3_month = null;
          this.is_1_min = this.is_10_min = this.is_1_hour = this.is_1_week = '';
          // interval_slice = intervals.slice(5, 7)
          break;
      }
    }
  },
}
</script>
