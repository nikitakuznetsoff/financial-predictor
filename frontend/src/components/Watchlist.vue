<template>
  <div class="watchlist">
    <div class="container">
      <div class="columns is-centered mt-3">
        <div class="column">
          <div class="card mx-2">
            <div class="card-content">
              <div class="level">
                <div class="level-left mr-3">
                  <ul>
                    <li><p>Сегодня</p></li>
                    <li class="is-size-4">+50%</li>
                  </ul>
                </div>
                <b-icon
                  icon="arrow-up-circle"
                  size="is-medium"
                  type="is-success">
                </b-icon>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="card">
            <div class="card-content">
              <div class="level">
                <div class="level-left mr-3">
                  <ul>
                    <li><p>Неделя</p></li>
                    <li class="is-size-4">+50%</li>
                  </ul>
                </div>
                <b-icon
                  icon="arrow-down-circle"
                  size="is-medium"
                  type="is-danger">
                </b-icon>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="card">
            <div class="card-content">
              <div class="level">
                <div class="level-left mr-3">
                  <ul>
                    <li><p>Месяц</p></li>
                    <li class="is-size-4">+50%</li>
                  </ul>
                </div>
                <b-icon
                  icon="arrow-down-circle"
                  size="is-medium"
                  type="is-danger">
                </b-icon>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="card">
            <div class="card-content">
              <div class="level">
                <div class="level-left mr-3">
                  <ul>
                    <li><p>Год</p></li>
                    <li class="is-size-4">+50%</li>
                  </ul>
                </div>
                <b-icon
                  icon="arrow-down-circle"
                  size="is-medium"
                  type="is-danger">
                </b-icon>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  

    <div class="container mb-6">
      <section class="section">
        <h1 class="title is-4">
          Список отслеживания
        </h1>
      </section>
      
      <div class="box">
        <b-table
          :data="instrumentsData"
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
  </div>
</template>

<script>
export default {
  name: 'Watchlist',
  props: {
    userID: Number
  },
  data() {
    return {
      qwe: 0,
      instrumentsData: [
        {
          id: 'AFLT',
          name: 'Aeroflot',
          price: 123,
          day: 1.2,
          week: 1.2,
          month: -1.2,
          year: 1.2,
          type: 'Акции',
          currency: 'SUR'
        },
        {
          id: 'AAPL',
          name: 'Apple',
          price: 123,
          day: 1.2,
          week: 1.2,
          month: 1.2,
          year: 1.2,
          type: 'Акции',
          currency: 'USD'
        },
        {
          id: 'GAZP',
          name: 'Gazprom',
          price: 123,
          day: 1.2,
          week: 1.2,
          month: 1.2,
          year: 1.2,
          type: 'Акции',
          currency: 'SUR'
        } 
      ],
    }
  }
}
</script>