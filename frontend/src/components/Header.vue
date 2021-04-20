<template>
    <b-navbar>
        <template #brand>
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
                <img
                    src="https://raw.githubusercontent.com/buefy/buefy/dev/static/img/buefy-logo.png"
                    alt="Lightweight UI components for Vue.js based on Bulma"
                >
            </b-navbar-item>
        </template>
        <template #start>
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
                Home
            </b-navbar-item>
            <!-- <b-navbar-dropdown label="Docs">
                <b-navbar-item tag="router-link" :to="{ path: '/about' }">
                    About
                </b-navbar-item>
            </b-navbar-dropdown> -->

            <form v-on:submit.prevent="onSubmit">
              <b-navbar-item>
                <b-input placeholder="Search for instruments"
                    type="text"
                    icon="magnify"
                    icon-clickable
                    @icon-click="searchIconClick"
                    v-model="search">
                </b-input>
              </b-navbar-item>
            </form>
            
        </template>

        <template #end>
            <b-navbar-item tag="div">
                <div class="buttons">
                    <router-link class="button is-primary" :to="{ path: '/registration' }">
                        <strong>Sign up</strong>
                    </router-link>
                    <b-dropdown
                        position="is-bottom-left"
                        append-to-body
                        aria-role="menu"
                        trap-focus
                    >
                        <template #trigger>
                            <a
                                class="button"
                                role="button">
                                <span>Login</span>
                                <b-icon icon="menu-down"></b-icon>
                            </a>
                        </template>


                        <b-dropdown-item
                            aria-role="menu-item"
                            :focusable="false"
                            custom
                            paddingless>
                            <Login />
                        </b-dropdown-item>
                    </b-dropdown>
                </div>
            </b-navbar-item>
        </template>
    </b-navbar>
</template>

<script>
import Login from '@/components/Login.vue'

export default {
  name: 'Header',
  components: {
      Login
  },
  data: function () {
      return {
          search: ""
      } 
  },
  methods: {
      onSubmit: function() {
          this.$router.push('/quote/' + this.search)
      }
  }
}
</script>
