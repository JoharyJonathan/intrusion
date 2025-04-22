<template>
  <div class="blacklist-table">
    <h2>Liste des IPs bloquées</h2>
    <table>
      <thead>
        <tr>
          <th>Adresse IP</th>
          <th>Heure du blocage</th>
          <th>Raison</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in blacklist" :key="entry.ip">
          <td>{{ entry.ip }}</td>
          <td>{{ entry.timestamp }}</td>
          <td>{{ entry.reason }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      blacklist: []
    };
  },
  mounted() {
    this.fetchBlacklist();
    setInterval(this.fetchBlacklist, 5000);
  },
  methods: {
    async fetchBlacklist() {
      const response = await fetch('http://localhost:5000/blacklist');
      const data = await response.json();
      this.blacklist = data;
    }
  }
};
</script>

<style scoped>
.blacklist-table {
  margin: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}
</style>