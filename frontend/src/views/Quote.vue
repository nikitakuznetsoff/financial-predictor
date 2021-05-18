<template>
    <div class="quote" id="quote">
        <section class="hero mb-5 is-primary">
            <div class="hero-body mx-6">
                <section v-if="loading">
                  <li>
                    <ul>
                      <p class="title"> 
                        <b-skeleton 
                          size="is-large" 
                          :active="loading"
                          :width="200"
                        ></b-skeleton>
                      </p>
                    </ul>
                    <ul>
                      <p class="subtitle">
                        <b-skeleton 
                          size="is-small" 
                          :active="loading"
                          :width="200">
                        </b-skeleton>
                      </p>
                    </ul>
                  </li> 
                </section>
                
                <section v-else>
                  <nav class="level">
                    <div class="level-left">
                      <ul>
                        <li>
                          <p class="title">
                            <section v-if="quote_is_empty">
                              unknown quote
                            </section>
                            <section v-else>
                              {{ quote.LATNAME.value }}
                            </section>
                          </p>
                        </li>
                        <li>
                          <p class="subtitle" v-if="!quote_is_empty">
                            {{ $route.params.name }}
                          </p>
                        </li>
                      </ul>
                    </div>

                    <div class="level-right">
                      <div class="button is-primary is-light is-medium">
                        Отслеживать
                      </div>
                    </div>
                  </nav>
                </section>
            </div>
        </section>
        
        <router-view></router-view>
        
    </div>
</template>

<script>
import axios from 'axios'
import API_URL from '@/common/config'

export default {
  name: 'Quote',
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
