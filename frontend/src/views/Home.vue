<template>
  <div class="news mx-3">
    <div class="columns">
      <div class="column is-1"/>
      <div class="column is-7">
        <section class="hero">
          <div class="hero-body">
            <p class="title">
              News
            </p>
          </div>
        </section>
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
      </div>
      <div class="column">
        <section class="hero">
          <div class="hero-body">
            <p class="title">
              History
            </p>
          </div>
        </section>
      </div>
      <div class="column is-1"/>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import API_URL from '../common/config'

export default {
  name: 'Hone',
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
      error_text: null
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
