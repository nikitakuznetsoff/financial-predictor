<template>
  <div class="quote mx-3">
      <section class="hero">
      <div class="hero-body">
        <p class="title">
          {{ $route.params.name }}
        </p>
        <p class="desciption">
            sample
        </p>
      </div>
    </section>
      <div class="columns">
          <div class="column is-one-quarter">
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
              <b-skeleton></b-skeleton>
            </div>
          </div>
      </div>
  </div>
</template>

<script>
import Graph from '@/components/Graph.vue'

export default {
  name: 'Quote',
  components: {
    Graph
  }
}
</script>
