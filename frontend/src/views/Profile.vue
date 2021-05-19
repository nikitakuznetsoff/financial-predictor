<template>
  <div class="profile">
    <section class="hero is-primary">
        <div class="hero-body mx-6">
          <ul>
            <li>
              <p class="title">Имя пользователя</p>
            </li>
            <li class="mt-2">
              <p class="is-size-6">
                <b-icon
                  icon="calendar"
                  size="is-small">
                </b-icon>
                Зарегистрировался  <span class="tag is-primary is-light mx-2 is-size-7">2 дня назад</span>
              </p>
            </li>
          </ul>
            
        </div>  
    </section>

    <b-tabs type="is-boxed is-centered mt-3">
        <b-tab-item label="Отслеживаемые" icon="account-details">
          <!-- <div class="has-text-centered mt-6 mb-6">
            <b-icon
              icon="message-bulleted-off"
              size="is-medium">
            </b-icon>
            <p>У пользователя нет отслеживаемых инструментов</p>
          </div> -->
          <Watchlist :userID="id"></Watchlist>
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
                          <ul class="mx-6">
                            <li><strong>Имя пользователя</strong></li>
                            <li>{{ email }}</li>
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
                          <ul class="mx-6">
                            <li><strong>Электронная почта</strong></li>
                            <li>{{ email }}</li>
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
      email: null,
      id: null
    }
  },
  methods: {
    getProfileInfo() {
      this.$http.get(API_URL+'/users')
      .then(resp => {
        this.email = resp.data.email;
        this.id = resp.data.id;
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