<template>
    <!-- <div ref="graphlLight"></div> -->
    <div></div>
</template>

<script>

import { createChart } from 'lightweight-charts';
// import Graph from './Graph.vue';

// var chartElement = document.createElement('qwe');
// var elem = document.getElementById("app");
// console.log(elem);

export default {
    name: 'GraphLight',
    data() {
        return {
            series: [
                { time: '2019-04-11', value: 80.01 },
                { time: '2019-04-12', value: 96.63 },
                { time: '2019-04-13', value: 76.64 },
                { time: '2019-04-14', value: 81.89 },
                { time: '2019-04-15', value: 74.43 },
                { time: '2019-04-16', value: 80.01 },
                { time: '2019-04-17', value: 96.63 },
                { time: '2019-04-18', value: 76.64 },
                { time: '2019-04-19', value: 81.89 },
                { time: '2019-04-20', value: 74.43 },
            ]
        }
    },
    methods: {
        // init() {
        //     const chart = createChart(this.$refs.graphLight, { width: 400, height: 300 });
        //     const lineSeries = chart.addLineSeries();
        //     lineSeries.setData([
        //         { time: '2019-04-11', value: 80.01 },
        //         { time: '2019-04-12', value: 96.63 },
        //         { time: '2019-04-13', value: 76.64 },
        //         { time: '2019-04-14', value: 81.89 },
        //         { time: '2019-04-15', value: 74.43 },
        //         { time: '2019-04-16', value: 80.01 },
        //         { time: '2019-04-17', value: 96.63 },
        //         { time: '2019-04-18', value: 76.64 },
        //         { time: '2019-04-19', value: 81.89 },
        //         { time: '2019-04-20', value: 74.43 },
        //     ]);
        // }
    },
    mounted() {
        // var elem = document.getElementById("app");
        // console.log(this.$parent);
        // const chart = createChart(this.$parent, { width: 400, height: 300 });
        // const lineSeries = chart.addLineSeries();
        // lineSeries.setData([
        //     { time: '2019-04-11', value: 80.01 },
        //     { time: '2019-04-12', value: 96.63 },
        //     { time: '2019-04-13', value: 76.64 },
        //     { time: '2019-04-14', value: 81.89 },
        //     { time: '2019-04-15', value: 74.43 },
        //     { time: '2019-04-16', value: 80.01 },
        //     { time: '2019-04-17', value: 96.63 },
        //     { time: '2019-04-18', value: 76.64 },
        //     { time: '2019-04-19', value: 81.89 },
        //     { time: '2019-04-20', value: 74.43 },
        // ]);
    }
}

</script>