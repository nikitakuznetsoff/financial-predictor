<template>
  <div class="watchlist">
      <div class="columns is-centered mt-3">
        <div class="column">
          <div class="card">
            <div class="card-content">
              <b-skeleton 
                size="is-large" 
                v-if="loading"
              ></b-skeleton>
              <section v-if="!loading">
                <div class="level" v-if="general.day > 0">
                  <div class="level-left mr-3" >
                    <ul>
                      <li>
                        Сегодня
                        <b-tooltip 
                          multilined
                          type="is-light"
                          label="Процентное изменение цены акций вашего списка наблюдения, 
                          вычисленное как среднее арифметическое.">
                            <b-icon
                              icon="information-outline"
                              size="is-small">
                            </b-icon>
                        </b-tooltip>
                      </li>
                      <li class="is-size-4">+{{ general.day }}%</li>
                    </ul>
                  </div>
                  <b-icon
                    icon="arrow-up-circle"
                    size="is-medium"
                    type="is-success">
                  </b-icon>
                </div>
                <div class="level" v-else>
                  <div class="level-left mr-3" >
                    <ul>
                      <li>
                        Сегодня
                        <b-tooltip 
                          multilined
                          type="is-light"
                          label="Процентное изменение цены акций вашего списка наблюдения, 
                          вычисленное как среднее арифметическое.">
                            <b-icon
                              icon="information-outline"
                              size="is-small">
                            </b-icon>
                        </b-tooltip>
                        
                        </li>
                      <li class="is-size-4">{{ general.day }}%</li>
                    </ul>
                  </div>
                  <b-icon
                    icon="arrow-down-circle"
                    size="is-medium"
                    type="is-danger">
                  </b-icon>
                </div>
              </section>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="card">
            <div class="card-content">
              <b-skeleton 
                size="is-large" 
                v-if="loading"
              ></b-skeleton>
              <section v-if="!loading">
                <div class="level" v-if="general.week > 0">
                  <div class="level-left mr-3" >
                    <ul>
                      <li><p>Неделя</p></li>
                      <li class="is-size-4">+{{ general.week }}%</li>
                    </ul>
                  </div>
                  <b-icon
                    icon="arrow-up-circle"
                    size="is-medium"
                    type="is-success">
                  </b-icon>
                </div>
                <div class="level" v-else>
                  <div class="level-left mr-3" >
                    <ul>
                      <li><p>Неделя</p></li>
                      <li class="is-size-4">{{ general.week }}%</li>
                    </ul>
                  </div>
                  <b-icon
                    icon="arrow-down-circle"
                    size="is-medium"
                    type="is-danger">
                  </b-icon>
                </div>
              </section>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="card">
            <div class="card-content">
              <b-skeleton 
                size="is-large" 
                v-if="loading"
              ></b-skeleton>
              <section v-if="!loading">
                <div class="level" v-if="general.month > 0">
                  <div class="level-left mr-3" >
                    <ul>
                      <li><p>Месяц</p></li>
                      <li class="is-size-4">+{{ general.month }}%</li>
                    </ul>
                  </div>
                  <b-icon
                    icon="arrow-up-circle"
                    size="is-medium"
                    type="is-success">
                  </b-icon>
                </div>
                <div class="level" v-else>
                  <div class="level-left mr-3" >
                    <ul>
                      <li><p>Месяц</p></li>
                      <li class="is-size-4">{{ general.month }}%</li>
                    </ul>
                  </div>
                  <b-icon
                    icon="arrow-down-circle"
                    size="is-medium"
                    type="is-danger">
                  </b-icon>
                </div>
              </section>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="card mx-2">
            <div class="card-content">
              <b-skeleton 
                size="is-large" 
                v-if="loading"
              ></b-skeleton>
              <section v-if="!loading">
                <div class="level" v-if="general.year > 0">
                  <div class="level-left mr-3" >
                    <ul>
                      <li><p>Год</p></li>
                      <li class="is-size-4">+{{ general.year }}%</li>
                    </ul>
                  </div>
                  <b-icon
                    icon="arrow-up-circle"
                    size="is-medium"
                    type="is-success">
                  </b-icon>
                </div>
                <div class="level" v-else>
                  <div class="level-left mr-3" >
                    <ul>
                      <li><p>Год</p></li>
                      <li class="is-size-4">{{ general.year }}%</li>
                    </ul>
                  </div>
                  <b-icon
                    icon="arrow-down-circle"
                    size="is-medium"
                    type="is-danger">
                  </b-icon>
                </div>
              </section>
            </div>
          </div>
        </div>
      </div>

      <section class="section">
        <h1 class="title is-4">
          Список отслеживания
        </h1>
      </section>
      
      <div class="box">
        <b-skeleton 
          size="is-large" 
          v-if="loading"
        ></b-skeleton>
        
        <b-table
          :data="securities"
          v-if="!loading"
        >
          <b-table-column field="id" label="Код" sortable v-slot="props">
            <router-link :to="{ name: 'QuoteForecast', params: { name: props.row.id }}">{{ props.row.id }}</router-link>
          </b-table-column>

          <b-table-column field="name" label="Название" sortable v-slot="props">
          {{ props.row.name }}
          </b-table-column>

          <b-table-column field="price" label="Цена" sortable centered v-slot="props">
          {{ props.row.price }}
          </b-table-column>

          <b-table-column field="currency" label="Валюта" sortable centered v-slot="props">
            {{ props.row.currency }}
          </b-table-column>

          <b-table-column field="day" label="1 день %" sortable centered  v-slot="props">
            <section v-if="props.row.day > 0">
              <p class="has-text-success">+{{ props.row.day }}%</p>
            </section>
            <section v-else>
              <p class="has-text-danger">{{ props.row.day }}%</p>
            </section>
          </b-table-column>

          <b-table-column field="week" label="1 неделя %" sortable centered v-slot="props">
            <section v-if="props.row.week > 0">
              <p class="has-text-success">+{{ props.row.week }}%</p>
            </section>
            <section v-else>
              <p class="has-text-danger">{{ props.row.week }}%</p>
            </section>
          </b-table-column>

          <b-table-column field="month" label="1 месяц %" sortable centered v-slot="props">
            <section v-if="props.row.month > 0">
              <p class="has-text-success">+{{ props.row.month }}%</p>
            </section>
            <section v-else>
              <p class="has-text-danger">{{ props.row.month }}%</p>
            </section>
          </b-table-column>

          <b-table-column field="year" label="1 год %" sortable centered v-slot="props">
            <section v-if="props.row.year > 0">
              <p class="has-text-success">+{{ props.row.year }}%</p>
            </section>
            <section v-else>
              <p class="has-text-danger">{{ props.row.year }}%</p>
            </section>
          </b-table-column>

          <b-table-column field="type" label="Тип бумаги" sortable centered v-slot="props">
            {{ props.row.type }}
          </b-table-column>
        </b-table>
      </div>
  </div>
</template>

<script>
import API_URL from '@/common/config'

export default {
  name: 'Watchlist',
  data() {
    return {
      loading: true,
      securities: null,
      general: null
    }
  },
  methods: {
    getSubscriptionsInfo() {
      this.loading = true;
      this.$http.get(API_URL+'/security/subscriptions')
      .then(resp => {
        this.securities = resp.data.subscriptions.securities;
        this.general = resp.data.subscriptions.general;
        // console.log(this.data);
      })
      .catch(e => {
        console.log(e);
      })
      .finally(() => {
        this.loading = false;
      })
    }
  },
  created() {
    this.getSubscriptionsInfo();
  }
}
</script>