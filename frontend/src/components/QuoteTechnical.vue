<template>
    <div class="quote-technical">
        <div class="tabs is-centered">
            <ul class="px-6">
            <li><router-link :to="{ name: 'QuoteForecast' }">Обзор</router-link></li>
            <li class="is-active"><a>Техническая информация</a></li>
            </ul>
        </div>

        <div class="container box mb-6">
            <div class="card-content">
                <section v-if="loading">
                    <b-skeleton size="is-large" :active="loading"></b-skeleton>
                </section>
                <section v-else>
                    <b-table :data="quote" :columns="columns">
                    </b-table>
                </section>
            </div>
          </div>
    </div>
</template>

<script>
import axios from 'axios'
import API_URL from '@/common/config'

export default {
  name: 'QuoteTechnical',
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
  },
}
</script>