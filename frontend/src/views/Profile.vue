<template>
  <div class="profile">
    <section class="hero is-primary">
        <div class="hero-body mx-6">
          <ul>
            <li>
              <b-skeleton 
                size="is-large" 
                v-if="loading"
                :width="200"
              ></b-skeleton>
              <p class="title" v-if="!loading">{{ user.username }}</p>
            </li>
            <li class="mt-2">
              <b-skeleton 
                size="is-medium" 
                v-if="loading"
                :width="200"
              ></b-skeleton>
              <p 
                class="is-size-6"
                v-if="!loading"
              >
                <b-icon
                  icon="calendar"
                  size="is-small">
                </b-icon>
                Зарегистрировался  <span class="tag is-primary is-light mx-2 is-size-7">{{ regTime }} дня назад</span>
              </p>
            </li>
          </ul>
            
        </div>  
    </section>

    <b-tabs type="is-boxed is-centered mt-3">
      <b-tab-item label="Отслеживаемые" icon="account-details">
        <div class="container mb-6">
          <section v-if="loading">
            <b-skeleton 
              size="is-medium" 
              v-if="!loading"
            ></b-skeleton>
          </section>
          <section v-else>
            <section v-if="user.subscriptions == null">
              <div class="has-text-centered mt-6 mb-6">
                <b-icon
                  icon="message-bulleted-off"
                  size="is-medium">
                </b-icon>
                <p>У пользователя нет отслеживаемых инструментов</p>
              </div>
            </section>
            <section v-else>
              <Watchlist></Watchlist>
            </section>
          </section>
        </div>
      </b-tab-item>
        <b-tab-item label="Настройки" icon="cog">
          <div class="columns is-centered">
            <div class="column is-half">
                <section class="section">
                    <h1 class="title is-4 has-text-centered">  
                        Пользовательские настройки
                    </h1>
                    <div class="notification is-primary is-light">
                      <div class="level">
                        <div class="level-left">
                          <b-icon
                            icon="account"
                            size="is-medium">
                          </b-icon>
                          <ul class="mx-6" v-if="!loading">
                            <li><strong>Имя пользователя</strong></li>
                            <li>{{ user.username }}</li>
                          </ul>
                        </div>
                        <div class="button is-primary">Изменить имя пользователя</div>
                      </div>
                    </div>

                    <div class="notification is-primary is-light">
                      <div class="level">
                        <div class="level-left">
                          <b-icon
                            icon="email"
                            size="is-medium">
                          </b-icon>
                          <ul class="mx-6" v-if="!loading">
                            <li><strong>Электронная почта</strong></li>
                            <li>{{ user.email }}</li>
                          </ul>
                        </div>
                        <div class="button is-primary">Изменить email</div>
                      </div>
                    </div>

                    <div class="notification is-primary is-light">
                      <div class="level">
                        <div class="level-left">
                          <b-icon
                            icon="lock"
                            size="is-medium">
                          </b-icon>
                          <ul class="mx-6">
                            <li><strong>Пароль</strong></li>
                            <li>Изменить ваш пароль</li>
                          </ul>
                        </div>
                        <div class="button is-primary">Изменить пароль</div>
                      </div>
                    </div>

                    <div class="notification is-danger is-light">
                      <div class="level">
                        <div class="level-left">
                          <b-icon
                            icon="delete"
                            size="is-medium">
                          </b-icon>
                          <ul class="mx-6">
                            <li><strong>Удаление профиля</strong></li>
                          </ul>
                        </div>
                        <div class="button is-danger">Удалить профиль</div>
                      </div>
                    </div>   
                </section>
              </div>
          </div>
        </b-tab-item>
    </b-tabs>
  </div>
</template>

<script>
import API_URL from '@/common/config'
import Watchlist from '@/components/Watchlist.vue'

export default {
  name: 'Profile',
  components: {
    Watchlist
  },
  data() {
    return {
      loading: true,
      user: null,
    }
  },
  computed: {
    regTime: function() {
      let now = new Date();
      let date = new Date(this.user.registration);
      let gap = now - date;
      return Math.floor(gap / 1000 / 60 / 60 / 24)
    }
  },
  methods: {
    getProfileInfo() {
      this.$http.get(API_URL+'/users')
      .then(resp => {
        this.user = resp.data.user;
      })
      .catch(err => {
        console.log(err);
        if (err.response.status == 401) {
          this.$store.dispatch('logout')
          .then(() => this.$router.push('/'));
        } else {
          this.$buefy.toast.open({
            type: 'is-danger',
            message: err.response.data
          });
        }
      })
      .finally(() => {
        this.loading = false;
      })
    }
  },
  created() {
    this.getProfileInfo()
  }
}
</script>