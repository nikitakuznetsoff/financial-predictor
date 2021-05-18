<template>
  <div :style="style">
    <div class="columns pb-6 px-6">
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
        </section>

        <section class="section">
          <div class="title">
            Intesting.com
          </div>

          <div class="tile is-ancestor">
            <a class="tile is-parent">
              <article class="tile is-child box">
                <b-skeleton size="is-large"></b-skeleton>
                <b-skeleton size="is-small"></b-skeleton>
              </article>
            </a>
            <a class="tile is-parent">
              <article class="tile is-child box">
                <b-skeleton size="is-large"></b-skeleton>
                <b-skeleton size="is-small"></b-skeleton>
              </article>
            </a>
            <a class="tile is-parent">
              <article class="tile is-child box">
                <b-skeleton size="is-large"></b-skeleton>
                <b-skeleton size="is-small"></b-skeleton>
              </article>
            </a>
          </div>

          <div class="tile is-ancestor">
            <a class="tile is-parent">
              <article class="tile is-child box">
                <b-skeleton size="is-large"></b-skeleton>
                <b-skeleton size="is-small"></b-skeleton>
              </article>
            </a>
            <a class="tile is-parent">
              <article class="tile is-child box">
                <b-skeleton size="is-large"></b-skeleton>
                <b-skeleton size="is-small"></b-skeleton>
              </article>
            </a>
            <a class="tile is-parent">
              <article class="tile is-child box">
                <b-skeleton size="is-large"></b-skeleton>
                <b-skeleton size="is-small"></b-skeleton>
              </article>
            </a>
          </div>

        </section>
      </div>
      <div class="column">
        <section class="section">
            <p class="title">
              История поиска
            </p>
        </section>
        <History></History>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import API_URL from '@/common/config'
import History from '@/components/History.vue'

export default {
  name: 'Home',
  components: {
    History
  },
  methods: {
    toNewsItem: function(id) {
      this.$router.push('/news/'+id)
    }
  },
  data() {
    return {
      news: [],
      loading: true,
      errored: false,
      error_text: null,
      style: {
        backgroundColor: '#FAFBFF',
      }
    }
  },
  mounted() {
    axios.get(API_URL + "/news/moex")
    .then(response => {
      this.news = response.data.news
    })
    .catch(e => {
      console.log(e);
      this.errored = true;
      this.error_text = e;
    })
    .finally(() => (this.loading = false));
  }
}
</script>
