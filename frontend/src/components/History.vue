<template>
  <div class="history">
    <!-- <b-table :data="data" :columns="columns" class="box"></b-table> -->
    <div class="box">
        <!-- <div class="level mx-5">
          <p>Aeroflot</p>
          <p>ALFT</p>
          <p>Акции</p>
        </div> -->
       <b-skeleton :animated="false" :count="2"></b-skeleton>
    </div>
    <div class="box">
       <b-skeleton :animated="false" :count="2"></b-skeleton>
    </div>
    <div class="box">
       <b-skeleton :animated="false" :count="2"></b-skeleton>
    </div>
  </div>
    
</template>

<script>
export default {
  name: 'History',
  data() {
    return {
      data: [
        { 'name': 'Apple', 'date': '2021-04-15 13:43:27', 'status': 'Up' },
        { 'name': 'Aeroflot', 'date': '2021-04-15 06:00:53', 'status': 'Up' },
        { 'name': 'Gazprom', 'date': '2021-04-06 06:26:28', 'status': 'Up' },
        { 'name': 'Rosneft', 'date': '2021-04-06 10:28:46', 'status': 'Down' },
        { 'name': 'Lukoil', 'date': '2021-04-06 14:38:38', 'status': 'Down' }
      ],
      columns: [
        {
          field: 'name',
          label: 'Name',
        },
        {
          field: 'date',
          label: 'Date',
          centered: true
        },
        {
          field: 'status',
          label: 'Status',
        }
      ]
    }
  }
}
</script>