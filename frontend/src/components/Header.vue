<template>
  <b-navbar :spaced="true" :shadow="true">
    <template #brand>
      <b-navbar-item tag="router-link" :to="{ path: '/' }">
        <b-icon
          icon="finance">
        </b-icon>
         <p class="mx-1">Financial Predictor</p>
      </b-navbar-item>
    </template>
    <template #start>
      <div class="mx-3">
        <form v-on:submit.prevent="onSubmit">
          <b-input placeholder="Поиск"
              type="text"
              icon="magnify"
              icon-clickable
              v-model="search"
              @focus="focusedInput()"
              @blur="dropdownMenuStatus = false; isLoading=true"
          >
          </b-input>
        </form> 
        <div class="box" :style="dropdownMenuStyle">
          <div class="content">
            <section v-if="isLoading">
              <div class="m-6">
              <b-loading 
                :is-full-page="false" 
                v-model="isLoading" 
                :can-cancel="true"
              ></b-loading>
            </div>
            </section>
            <section v-else>
              <b-table
                :data="findedInstruments"
                narrowed
              >
                <b-table-column field="id" v-slot="props">
                  {{ props.row.id }}
                </b-table-column>
                <b-table-column field="name" v-slot="props">
                  {{ props.row.name }}
                </b-table-column>
                <b-table-column field="type" v-slot="props">
                  {{ props.row.type }}
                </b-table-column>

              </b-table>
            </section>
          </div>
        </div>
      </div>
    </template>

    <template #end>
      <b-navbar-item tag="div">
        <div class="buttons">
          <section v-if="$store.getters.isLoggedIn">
            <router-link 
              class="button is-primary is-light" 
              :to="{ path: '/profile' }"
              >
              <b-icon
                icon="home-account">
              </b-icon>
              <p>Профиль</p>
            </router-link>
            <a class="button" @click="logout">
              <b-icon
                icon="logout-variant">
              </b-icon>
              <p>Выйти</p>
            </a>
          </section>
            <section v-else>
              <router-link 
                class="button is-primary" 
                :to="{ path: '/registration' }"
              >
                <b-icon
                  icon="account-plus">
                </b-icon>
                <strong>Регистрация</strong>
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
                    role="button"
                  >
                    <b-icon
                      icon="login-variant">
                    </b-icon>
                    <span>Войти</span>
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
            </section>
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
      search: '',
      authStatus: '',
      dropdownMenuStatus: false,
      isLoading: true,
      knownInstruments: [
        {
          id: 'AFLT',
          name: 'Aeroflot',
          type: 'Акции'
        },
        {
          id: 'GAZP',
          name: 'Gazprom',
          type: 'Акции'
        },
        {
          id: 'AAPL',
          name: 'Apple',
          type: 'Акции'
        }
      ],
      findedInstruments: null,
      columns: [
        { field: 'id' },
        { field: 'name' },
        { field: 'type' }
      ]
    } 
  },
  computed: {
    dropdownMenuStyle: function() {
      if (this.dropdownMenuStatus == true) {
        return "display: flex; position: absolute; min-width: 250px; min-height: 25px"
      } else {
        return "display: none"
      }
    }
  }, 
  methods: {
    focusedInput() {
      this.dropdownMenuStatus = true;
      if (this.search != '') {
        this.changedSearch();
      } else {
        this.isLoading=true;
      }
    },
    changedSearch() {
      this.findedInstruments = this.knownInstruments;
      this.isLoading = false;
    },
    onSubmit() {
      this.$router.push({ name: 'QuoteForecast', params: { name: this.search }})
    },
    changedAuthStatus() {
      self.authStatus = this.$store.authStatus;
    },
    logout() {
      this.$store.dispatch('logout')
      .then(() => {
          this.$router.push('/')
      })
    }
  },
  created() {
    this.changedAuthStatus();
  },
  watch: {
    $store: 'changedAuthStatus',
    search: 'changedSearch'
  }
}
</script>