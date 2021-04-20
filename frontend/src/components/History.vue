<template>
    <b-table :data="data" :columns="columns"></b-table>
</template>

<script>
export default {
    name: 'History',
    data() {
            return {
                data: [
                    { 'name': 'Apple', 'date': '2016-10-15 13:43:27', 'status': 'Up' },
                    { 'name': 'Aeroflot', 'date': '2016-12-15 06:00:53', 'status': 'Up' },
                    { 'name': 'Gazprom', 'date': '2016-04-26 06:26:28', 'status': 'Up' },
                    { 'name': 'Rosneft', 'date': '2016-04-10 10:28:46', 'status': 'Down' },
                    { 'name': 'Lukoil', 'date': '2016-12-06 14:38:38', 'status': 'Down' }
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