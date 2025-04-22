<template>
  <div id="app">
    <h1>Surveillance du réseau</h1>
    <StatsCharts />
    <BlacklistTable />
  </div>
</template>

<script>
import StatsCharts from '@/components/StatsCharts.vue';
import BlacklistTable from '@/components/BlacklistTable.vue';

export default {
  components: {
    StatsCharts,
    BlacklistTable
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 20px;
}
</style>