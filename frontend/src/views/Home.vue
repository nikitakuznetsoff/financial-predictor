<template>
  <div :style="style">
    <div class="columns pb-6 px-6 is-variable is-6">
      <div class="column is-9">
        <section class="section">
          <p class="title">
            Московская биржа
          </p>
          <section v-if="errored">
            <p>We're sorry, we're not able to retrieve this information at the moment, please try back later</p>
            <p>
              {{ error_text }}
            </p>
          </section>
        </section>

        <div class="tile is-ancestor">
          <a class="tile is-parent is-8" @click="toNewsItem(news[0].id)">
            <article class="tile is-child box">
              <b-skeleton size="is-large" :active="loading"></b-skeleton>
              <b-skeleton size="is-small" :active="loading"></b-skeleton>
              <p class="title is-6" v-if="!loading">{{ news[0].title }}</p>
              <p class="subtitle is-6" v-if="!loading">{{ news[0].published_at }}</p>
            </article>
          </a>

          <a class="tile is-parent" @click="toNewsItem(news[1].id)">
            <article class="tile is-child box">
              <b-skeleton size="is-large" :active="loading"></b-skeleton>
              <b-skeleton size="is-small" :active="loading"></b-skeleton>
              <p class="title is-6" v-if="!loading">{{ news[1].title }}</p>
              <p class="subtitle is-6" v-if="!loading">{{ news[1].published_at }}</p>
            </article>
          </a>
        </div>
          
        <div class="tile is-ancestor">
          <a class="tile is-parent" @click="toNewsItem(news[2].id)">
            <article class="tile is-child box">
              <b-skeleton size="is-large" :active="loading"></b-skeleton>
              <b-skeleton size="is-small" :active="loading"></b-skeleton>
              <p class="title is-6" v-if="!loading">{{ news[2].title }}</p>
              <p class="subtitle is-6" v-if="!loading">{{ news[2].published_at }}</p>
            </article>
          </a>
          <a class="tile is-parent" @click="toNewsItem(news[3].id)">
            <article class="tile is-child box">
              <b-skeleton size="is-large" :active="loading"></b-skeleton>
              <b-skeleton size="is-small" :active="loading"></b-skeleton>
              <p class="title is-6" v-if="!loading">{{ news[3].title }}</p>
              <p class="subtitle is-6" v-if="!loading">{{ news[3].published_at }}</p>
            </article>
          </a>
          <a class="tile is-parent" @click="toNewsItem(news[4].id)">
            <article class="tile is-child box">
              <b-skeleton size="is-large" :active="loading"></b-skeleton>
              <b-skeleton size="is-small" :active="loading"></b-skeleton>
              <p class="title is-6" v-if="!loading">{{ news[4].title }}</p>
              <p class="subtitle is-6" v-if="!loading">{{ news[4].published_at }}</p>
            </article>
          </a>
        </div>
        

        <section class="section">
          <div class="title">
            Investing.com
          </div>
        </section>
        
        <section v-if="isInvestingNewsLoading">
          <div class="tile is-ancestor"
            v-for="v in [0,3,6]"
            v-bind:key="v.id"
          >
            <div class="tile is-parent"
                v-for="v in [0,1,2]"
                v-bind:key="v.id">
              <article 
                class="tile is-child box"
              >
                <b-skeleton size="is-large" :animated="false"></b-skeleton>
                <b-skeleton size="is-small" :animated="false"></b-skeleton>
              </article>
            </div>
          </div>
        </section>
        <section v-else>
          <div class="tile is-ancestor"
            v-for="v in [0,3,6]"
            v-bind:key="v.id"
          >
            <div class="tile is-parent"
                v-for="k in [0,1,2]"
                v-bind:key="k.id">
                
              <div class="tile is-child box" @click="goToAnotherSite(investingNews[v+k].link)">
                <!-- <a v-bind:href="" target="_blank"> -->
                  <strong>{{ investingNews[v+k].title }}</strong>
                <!-- </a> -->
                <p>
                  <span class="tag is-info is-light mr-2">{{ investingNews[v+k].author }}</span>

                  {{ investingNews[v+k].published }}
                </p>
              </div>
            </div>
          </div>

        </section>

       
        <div class="container mt-6">
          <iframe src="https://ru.widgets.investing.com/live-currency-cross-rates?theme=lightTheme&hideTitle=true&roundedCorners=true&pairs=1,9530,1691,2111,2186" 
            width="100%" height="250px" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0">
          </iframe>
        </div>
      </div>
      <div class="column">
        <section class="section">
            <p class="title">
              История поиска
            </p>
        </section>
        <section v-if="isHistoryLoading">
          <div class="box">
            <b-skeleton :animated="false" :count="2"></b-skeleton>
          </div>
        </section>
        <section v-else>
          <div class="box" v-for="sec in history" v-bind:key="sec.id">
            <router-link :to="{ name: 'QuoteForecast', params: { name: sec.secid }}">
              <div class="level mx-4">
                <div class="level-left">
                  <ul>
                    <li>
                      <p class="is-size-4"><strong>{{ sec.secid }}</strong></p>
                    </li>
                    <li>
                      {{ sec.name }}
                    </li>
                  </ul>
                </div>
                <div class="level-right has-text-centered">
                  <ul>
                    <li>
                      <span class="tag is-success is-light is-medium">{{ sec.type }}</span>
                    </li>
                    <li>
                      <span class="tag is-primary is-light is-medium mt-2">{{ sec.currency }}</span>
                    </li>
                  </ul>
                </div>
              </div> 
            </router-link>
            
          </div>
        </section>
        
      </div>
    </div>
    
  </div>
</template>

<script>
import API_URL from '@/common/config'

export default {
  name: 'Home',
  components: {
  },
  methods: {
    toNewsItem: function(id) {
      this.$router.push('/news/'+id)
    },
    getHistoryItems() {
      this.isHistoryLoading = true;
      let c_name = "history";
      let c_start = document.cookie.indexOf(c_name + "=");
      if (c_start != -1) {
        c_start = c_start + c_name.length + 1;
        let c_end = document.cookie.indexOf(";", c_start);
        if (c_end == -1) {
            c_end = document.cookie.length;
        }
        let arr = JSON.parse(document.cookie.substring(c_start, c_end));
        if (arr.length > 0) {
          this.$http.post(API_URL + "/security", {'ids': arr})
          .then(response => {
            this.history = response.data.securities;
            // console.log(this.history);
          })
          .catch(e => {
            console.log(e);
          })
          .finally(() => {
            this.isHistoryLoading = false;
          })
        }
      } else {
        this.history = [];
        this.isHistoryLoading = true;
      }
    },
    getNews() {
      this.loading = true;
      this.$http.get(API_URL + "/news/moex")
      .then(response => {
        this.news = response.data.news
      })
      .catch(e => {
        this.errored = true;
        this.error_text = e;
      })
      .finally(() => (this.loading = false));
    },
    getInvestingNews() {
      this.isInvestingNewsLoading = true;
      this.$http.get(API_URL + "/news/investing")
      .then(response => {
        this.investingNews = response.data.entries;
        console.log(this.investingNews[0])
      })
      .catch(e => {
        console.log(e);
      })
      .finally(() => {
        this.isInvestingNewsLoading = false;
      })
    },
    goToAnotherSite(site) {
      window.open(site);
    }
  },
  data() {
    return {
      news: [],
      loading: true,
      errored: false,
      error_text: null,

      isInvestingNewsLoading: true,
      investingNews: [],

      isHistoryLoading: true,
      history: null,

      style: {
        backgroundColor: '#FAFBFF',
      }
    }
  },
  mounted() {
    this.getNews();
    this.getHistoryItems();
    this.getInvestingNews();
  }
}
</script>
