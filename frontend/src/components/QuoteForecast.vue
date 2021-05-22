<template>
  <div class="quote-forecast">
      <div class="tabs is-centered">
        <ul class="px-6">
          <li class="is-active"><a>Обзор</a></li>
          <li><router-link :to="{ name: 'QuoteTechnical' }">Техническая информация</router-link></li>
        </ul>
      </div>

      <b-tabs position="is-centered" 
          type="is-toggle"
          class="block"
          :animated="false"
          size="is-small"
          v-model="period"
        >
          <b-tab-item label="1 день"></b-tab-item>
          <b-tab-item label="1 неделя"></b-tab-item>
          <b-tab-item label="1 месяц"></b-tab-item>
          <b-tab-item label="3 месяца"></b-tab-item>
          <b-tab-item label="6 месяцев"></b-tab-item>
          <b-tab-item label="1 год"></b-tab-item>
          <!-- <b-tab-item label="Макс"></b-tab-item> -->
      </b-tabs>

      <div class="columns px-6 pb-3">
        <div class="column is-2">
          <b-menu>
            <b-menu-list label="Интервалы" icon="av-timer">
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
            </b-menu-list>

            <b-menu-list label="Алгоритмы" icon="chart-areaspline" > 
              <b-menu-item label="MA" 
                icon="vector-line" 
                @click="selectedAlgo = 'ma'"></b-menu-item>
              <b-menu-item label="ARMA" 
                icon="vector-line" 
                @click="selectedAlgo = 'arma'"></b-menu-item>
              <b-menu-item label="ARIMA" 
                icon="vector-line" 
                @click="selectedAlgo = 'arima'"></b-menu-item>
              <b-menu-item label="SARIMA" 
                icon="vector-line" 
                @click="selectedAlgo = 'sarima'"></b-menu-item>

            </b-menu-list>
          </b-menu> 
        </div>

        <div class="column" ref="graphColumn">
          <!-- <Graph 
            :tabIndex="period" 
            :interval="interval"
            :algo="selectedAlgo"
          ></Graph> -->
          <GraphTradingVue 
            :tabIndex="period" 
            :interval="interval"
            :algo="selectedAlgo"
            :width="this.width"
          ></GraphTradingVue>
        </div>
    </div>

    <section class="hero is-light">
      <div class="hero-body mx-6">
        <div class="title">
          {{ this.$route.params.name }} Новости
        </div>

        <b-carousel-list 
          v-model="currentNews" 
          :data="news" 
          :items-to-show="4"
          >
          <template #item="list">
            <div class="card mx-4">
              <div class="card-content">
                <div class="content">
                  <p>
                    <strong>
                      {{ list.title }}
                    </strong>
                    <br>
                    {{ list.message }}
                  </p>
                </div>
              </div>
            </div>
          </template>
        </b-carousel-list>

      </div>
    </section>

    <!-- <section class="section mx-6">
      <h1 class="title">
        Идеи
      </h1>
    </section> -->

  </div>
</template>

<script>
// import Graph from '@/components/Graph.vue'
import GraphTradingVue from '@/components/GraphTradingVue.vue'

export default {
  name: 'Quote',
  components: {
    // Graph,
    GraphTradingVue
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
      width: 0,

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

      currentNews: 0,
      news: [
        {
          'title': 'Заголовок1',
          'message': 'Текст'
        },
        {
          'title': 'Заголовок2',
          'message': 'Текст'
        },
        {
          'title': 'Заголовок3',
          'message': 'Текст'
        },
        {
          'title': 'Заголовок4',
          'message': 'Текст'
        },
        {
          'title': 'Заголовок5',
          'message': 'Текст'
        },
        {
          'title': 'Заголовок6',
          'message': 'Текст'
        },
      ]
    }
  },
  methods: {
    isIntervalAvailable(interval) {
      let intervals = [1, 10, 60, 24, 7, 31, 4];
      let interval_slice = null;
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
  },
  mounted() {
    this.width = this.$refs.graphColumn.offsetWidth;
  }
}
</script>
