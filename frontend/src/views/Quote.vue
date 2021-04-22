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
              animated="false"
              size="is-small"
              v-model="period"
            >
              <b-tab-item label="1 день"></b-tab-item>
              <b-tab-item label="1 неделя"></b-tab-item>
              <b-tab-item label="1 месяц"></b-tab-item>
              <b-tab-item label="3 месяца"></b-tab-item>
              <b-tab-item label="6 месяцев"></b-tab-item>
              <b-tab-item label="1 год"></b-tab-item>
              <b-tab-item label="Макс"></b-tab-item>
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
                    <b-menu-item icon="arrow-right" label="1 мин" @click="interval = 1"></b-menu-item>
                    <b-menu-item icon="arrow-right" label="4 мин" @click="interval = 4"></b-menu-item>
                    <b-menu-item icon="arrow-right" label="7 мин" @click="interval = 7"></b-menu-item>
                    <b-menu-item icon="arrow-right" label="10 мин" @click="interval = 10"></b-menu-item>
                    <b-menu-item icon="arrow-right" label="24 мин" @click="interval = 24"></b-menu-item>
                    <b-menu-item icon="arrow-right" label="31 мин" @click="interval = 31"></b-menu-item>
                    <b-menu-item icon="arrow-right" label="1 час" @click="interval = 60"></b-menu-item>
                  </b-menu-item>
                </b-menu-list>

                <b-menu-list label="Алгоритмы" icon="chart-areaspline">
                  <b-menu-item label="ARIMA" icon="vector-line"></b-menu-item>
                    <b-menu-item label="SARIMA" icon="vector-line"></b-menu-item>
                    <b-menu-item label="Прочее" icon="vector-line"></b-menu-item>

                </b-menu-list>
                <!-- <b-menu-list label="Actions">
                  <b-menu-item label="Logout"></b-menu-item>
                </b-menu-list> -->
              </b-menu> 
            </div>

            <div class="column">
              <Graph :tabIndex="period" :interval="interval"></Graph>
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
      interval: 0,
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
  }
}
</script>
