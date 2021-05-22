<template>
    <div class="quote" id="quote">
        <section class="hero mb-5 is-primary">
            <div class="hero-body mx-6">
                <section v-if="loading">
                  <ul>
                    <li>
                      <p class="title"> 
                        <b-skeleton 
                          size="is-large" 
                          :animated="false"
                          :width="200"
                        ></b-skeleton>
                      </p>
                    </li>
                    <li>
                      <p class="subtitle">
                        <b-skeleton 
                          size="is-small" 
                          :animated="false"
                          :width="200">
                        </b-skeleton>
                      </p>
                    </li>
                  </ul> 
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
                              {{ quote.name }}
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
                      <section v-if="subscriptionLoading">
                        <b-skeleton 
                          size="is-large" 
                          :animated="false"
                          :width="150"
                          :height="50"
                        ></b-skeleton>
                      </section>
                      <section v-else>
                        <div
                          v-if="isSubscribed" 
                          class="button is-primary is-light is-medium"
                          @click="unsubscribe"
                        >
                          Отписаться
                        </div>
                        <div
                          v-else
                          class="button is-primary is-light is-medium" 
                          @click="subscribe"
                        >
                          Подписаться
                        </div>
                      </section>
                    </div>
                  </nav>

                </section>
            </div>
        </section>
        
        <router-view></router-view>
        
    </div>
</template>

<script>
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

      subscriptionLoading: true,
      subscriptions: null,
      isSubscribed: false,

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
    this.fetchData();
    this.getSubscriptions();
  },
  watch: {
    $route: [
      'fetchData',
      'getSubscriptions'
    ]
  },
  methods: {
    fetchData() {
      this.quote = this.error_text = null;
      this.quote_is_empty = this.error = false;
      this.loading = true;

      this.$http.get(API_URL + '/security/' + this.$route.params.name)
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
    getSubscriptions() {
      this.isSubscribed = false;
      this.subscriptionLoading = true;
      this.$http.get(API_URL + '/users/subscriptions')
      .then(response => {
        if (response.status == 200) {
          this.subscriptions = response.data.subscriptions;
          if (this.subscriptions.includes(this.quote.secid)) {
            this.isSubscribed = true;
          } else {
            this.isSubscribed = false;
          }
        }
      })
      .catch((e) => {
        console.log(e);
      })
      .finally(() => {
        this.subscriptionLoading = false;
      })
    },
    subscribe() {
      this.$http.post(API_URL + '/users/subscribe', {'secid': this.quote.secid})
      .then(() => {
        console.log('Subscription successful');
        this.subscriptions.push(this.quote.secid);
        this.isSubscribed = true;
      })
      .catch((e) => {
        console.log(e);
      })
    },
    unsubscribe() {
      this.$http.post(API_URL + '/users/unsubscribe', {'secid': this.quote.secid})
      .then(() => {
        console.log('Unsubscription successful');
        this.getSubscriptions();
      })
      .catch((e) => {
        console.log(e);
      })
    }
  },
}
</script>
