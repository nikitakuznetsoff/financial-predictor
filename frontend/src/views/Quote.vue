<template>
  <div class="quote mx-3 mb-3">
      <section class="hero">
      <div class="hero-body">
        <p class="title">
          <b-skeleton size="is-large" :active="loading"></b-skeleton>
          <section v-if="!loading">
            <section v-if="quote_is_empty">
              unknown quote
            </section>
            <section v-else>
              {{ quote.LATNAME.value }}
            </section>
          </section>
        </p>
        <!-- <p class="desciption">
            Group Name: {{ quote.GROUPNAME.value }}
        </p> -->
      </div>
    </section>
      <div class="columns">
          <div class="column is-one-fifth">
            <b-menu>
              <b-menu-list label="Menu">
                <b-menu-item icon="information-outline" label="Info"></b-menu-item>
                <b-menu-item icon="account" label="My Account">
                  <b-menu-item label="Account data"></b-menu-item>
                  <b-menu-item label="Addresses"></b-menu-item>
                </b-menu-item>
              </b-menu-list>
              <b-menu-list>
                <b-menu-item label="Expo" icon="link" tag="router-link" target="_blank" to="/expo"></b-menu-item>
              </b-menu-list>
            </b-menu>    
          </div>
          <div class="column">
            <div class="container">
              <Graph></Graph>
            </div>
          </div>
          <div class="column is-one-quarter">
            <b-skeleton size="is-large" :active="loading"></b-skeleton>
            <div class="card" v-if="!loading">
              <div class="card-content">
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
      columns: [
        {
          'field': 'title',
          'label': 'Title'
        },
        {
          'field': 'value',
          'label': 'Name'
        },
      ]
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
    }
  }
}
</script>
