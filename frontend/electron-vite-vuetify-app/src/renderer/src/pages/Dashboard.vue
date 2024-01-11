
<script setup>
  import { onMounted } from 'vue';
  import { Chart, registerables } from 'chart.js';

  Chart.register(...registerables);

  const plugin = {
    id: 'customCanvasBackgroundColor',
    beforeDraw: (chart, args, options) => {
      const {ctx} = chart;
      ctx.save();
      ctx.globalCompositeOperation = 'destination-over';
      ctx.fillStyle = options.color || '#99ffff';
      ctx.fillRect(0, 0, chart.width, chart.height);
      ctx.restore();
    }
  };

  function pie(){
    const data = {
      labels: ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple'],
      datasets: [{
        data: [20, 20, 15, 25, 15, 30], // Substitua esses valores pelos seus próprios dados
        backgroundColor: [
          'rgba(25, 118, 210, 0.7)',
          'rgba(139, 195, 74, 0.7)',
          'rgba(255, 193, 7, 0.7)',
          'rgba(248, 121, 121, 0.7)',
          'rgba(103, 58, 183, 0.7)',
          'rgba(255, 165, 0, 0.7)',
        ],
      }]
  };

    // Opções do gráfico
    const options = {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Categorias mais vendidas'
        },
        customCanvasBackgroundColor: {
          color: 'white',
        },
      },
    };

    // Criar o gráfico
    const ctx = document.getElementById('myPieChart').getContext('2d');
    const myPieChart = new Chart(ctx, {
      type: 'pie',
      data: data,
      options: options,
      plugins: [plugin],
    });
  }
  

  onMounted(() => {
    pie();
    const ctx = document.getElementById('chartCanvas').getContext('2d');

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
        datasets: [
          {
            
            label: 'Vendas Semestrais',
            data: [20, 65, 60, 100, 75],
            lineTension: 0.2,
            borderColor: '#1976D2',
            backgroundColor: 'rgba(25, 118, 210, 0.3)', // Preenchimento de fundo
            borderWidth: 2,
            pointRadius: 4,
            pointBackgroundColor: '#1976D2',
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'category',
            labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
            grid: {
              display: false
            }
          },
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
          },
          title: {
            display: true,
            text: 'Vendas'
          },
          customCanvasBackgroundColor: {
            color: 'white',
          }
        },
      },
      plugins: [plugin],
    });
  });

  
  </script>

<template>
  <div
    class="pa-4" 
    color="grey-lighten-4"
  >
    <canvas  
      id="chartCanvas"
      width="400"
      height="400"
      class="elevation-2 rounded"></canvas>
  </div>

  <v-container
    class="pa-4" 
    color="grey-lighten-4"
  >
    <v-row>
      <v-col>
        <canvas  
          id="myPieChart"
          width="50"
          height="50"
          class="elevation-2 rounded"></canvas>
      </v-col>

      <v-col>
        <v-card
          class="elevation-2 rounded"
          title="Clientes que mais compraram"
        >
          <v-list>
            <v-list-item
              color="primary"
              rounded="xl"
            >
            

            <!-- <v-list-item
              v-for="(item, i) in items"
              :key="i"
              :value="item"
              color="primary"
              rounded="xl"
            >
              <template v-slot:prepend>
                <v-icon :icon="item.icon"></v-icon>
              </template> -->

              
              <v-card v-for="(j, i) in [1, 2, 3, 4, 5]" :key="i">
                <v-card-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-account" color="primary"></v-icon>
                  </template>

                  <v-card-title>
                    João
                    <v-chip color="green">
                      R$ 1500,30
                    </v-chip> 
                  </v-card-title>

                  <v-card-subtitle>
                    8 pedidos no semestre
                  </v-card-subtitle>
                </v-card-item>
              </v-card>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <v-col>
        <v-card
          class="elevation-2 rounded"
          title="Produtos mais vendidos"
        >
          <v-list>
            <v-list-item
              color="primary"
              rounded="xl"
            >
            

            <!-- <v-list-item
              v-for="(item, i) in items"
              :key="i"
              :value="item"
              color="primary"
              rounded="xl"
            >
              <template v-slot:prepend>
                <v-icon :icon="item.icon"></v-icon>
              </template> -->

              
              <v-card v-for="(j, i) in [1, 2, 3, 4, 5]" :key="i">
                <v-card-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-tag" color="primary"></v-icon>
                  </template>

                  <v-card-title>
                    Açaí
                    <v-chip color="green">
                      R$ 1500,30
                    </v-chip> 
                  </v-card-title>

                  <v-card-subtitle>
                    8 vendas no semestre
                  </v-card-subtitle>
                </v-card-item>
              </v-card>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
/* Adicione estilos específicos, se necessário */
</style>