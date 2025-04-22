<template>
  <div class="stats-container">
    <h2 class="stats-title">Network Security Dashboard</h2>
    
    <div class="charts-grid">
      <!-- Graphique principal -->
      <div class="chart-card">
        <h3>Traffic Analysis</h3>
        <div class="chart-wrapper">
          <canvas ref="trafficChart"></canvas>
        </div>
      </div>

      <!-- Graphique secondaire -->
      <div class="chart-card">
        <h3>Threat Overview</h3>
        <div class="chart-wrapper">
          <canvas ref="threatChart"></canvas>
        </div>
      </div>

      <!-- Liste des IP bloquées -->
      <div class="chart-card blocked-ips">
        <h3>Blocked IPs (Total: {{ blockedIpsCount }})</h3>
        <ul v-if="recentAttacks.length">
          <li v-for="attack in recentAttacks" :key="attack.ip" class="attack-item">
            <span class="ip-address">{{ attack.ip }}</span>
            <span class="attack-time">{{ formatDate(attack.time) }}</span>
            <span class="attack-reason">{{ attack.reason }}</span>
          </li>
        </ul>
        <p v-else class="no-data">No blocked IPs detected</p>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  data() {
    return {
      trafficChart: null,
      threatChart: null,
      blockedIpsCount: 0,
      recentAttacks: [],
      refreshInterval: null
    };
  },
  mounted() {
    this.fetchData();
    this.refreshInterval = setInterval(this.fetchData, 5000); // Rafraîchir toutes les 5s
  },
  beforeUnmount() {
    clearInterval(this.refreshInterval);
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('http://localhost:5000/stats');
        if (!response.ok) throw new Error('Failed to load stats');
        const data = await response.json();

        this.blockedIpsCount = data.blocked_ips;
        this.recentAttacks = data.recent_attacks;

        this.updateCharts(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    updateCharts(data) {
      // Détruire les anciens graphiques s'ils existent
      if (this.trafficChart) this.trafficChart.destroy();
      if (this.threatChart) this.threatChart.destroy();

      // Graphique de trafic (doughnut)
      this.trafficChart = new Chart(this.$refs.trafficChart, {
        type: 'doughnut',
        data: {
          labels: ['Normal Traffic', 'Malicious Traffic'],
          datasets: [{
            data: [
              data.total_requests - data.malicious_requests, 
              data.malicious_requests
            ],
            backgroundColor: ['#4bc0c0', '#ff6384'],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'bottom' },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.label}: ${context.raw} (${context.raw/data.total_requests*100}%)`;
                }
              }
            }
          }
        }
      });

      // Graphique de menaces (bar)
      this.threatChart = new Chart(this.$refs.threatChart, {
        type: 'bar',
        data: {
          labels: ['Total Requests', 'Malicious', 'Blocked IPs'],
          datasets: [{
            label: 'Network Stats',
            data: [
              data.total_requests, 
              data.malicious_requests, 
              data.blocked_ips
            ],
            backgroundColor: [
              '#36a2eb',
              '#ff6384',
              '#ff9f40'
            ]
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: true }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    },
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleString();
    }
  }
};
</script>

<style scoped>
.stats-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.stats-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.chart-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.chart-wrapper {
  position: relative;
  height: 300px;
  width: 100%;
}

.blocked-ips {
  max-height: 400px;
  overflow-y: auto;
}

.attack-item {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
  display: grid;
  grid-template-columns: 1fr 1fr 2fr;
  gap: 10px;
  font-size: 0.9em;
}

.ip-address {
  font-family: monospace;
  color: #e74c3c;
  font-weight: bold;
}

.attack-time {
  color: #7f8c8d;
}

.attack-reason {
  color: #34495e;
}

.no-data {
  color: #7f8c8d;
  text-align: center;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .attack-item {
    grid-template-columns: 1fr;
  }
}
</style>