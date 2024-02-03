<script setup>
  import { onMounted, reactive } from 'vue';
  import { fetchGet, getAuthToken, setMessageSnackbar } from '../utils/common';
  import { Chart, registerables } from 'chart.js';
  import 'chartjs-adapter-date-fns';
  import Snackbar from '../components/Snackbar.vue';

  defineOptions({
    inheritAttrs: false
  });

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

  const isVisible = reactive({
    pieChart: false,
    lineChart: false,
  });
    
  async function requestBestSellingCategories(){
    let bestSellingCategories = undefined;

    try{
      const url = "http://127.0.0.1:8000/v1/dashboard/best-selling-categories/"
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          bestSellingCategories = responseJson;
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar categorias mais vendidas", 'warning');
    }

    return bestSellingCategories;
  } 

  function createChart({id, type, data, options}){
    const ctx = document.getElementById(id).getContext('2d');

    new Chart(ctx, {
      type: type,
      data: data,
      options: options,
      plugins: [plugin],
    });
  }

  async function createPieChart(){
    const bestSellingCategories = await requestBestSellingCategories();

    if(bestSellingCategories){
      const data = {
        labels: [],
        datasets: [{
          data: [],
        }]
      };
      bestSellingCategories.forEach((sellingCategorie) => {
        data.labels.push(sellingCategorie.categoria);
        data.datasets[0].data.push(Number(sellingCategorie.total_vendido));
      });

      const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Categorias mais vendidas no semestre',
            font: {
              size: 18
            },
          },
          customCanvasBackgroundColor: {
            color: 'white',
          },
          tooltip: {
            callbacks: {
              label: function(context){
                return `R$ ${context.parsed.toFixed(2).replace('.', ',')}`;
              },
            }
          },
        },
        devicePixelRatio: 4,
      };

      createChart({
        id: 'myPieChart', 
        type: 'pie', 
        data: data, 
        options: options,
      });

      isVisible.pieChart = true;
    }
  }
  
  async function createLineChart(){
    const bestSellingCategories = await requestBestSellingCategories();

    if(bestSellingCategories){
      const data = {
        labels: [],
        datasets: [{
          label: 'Vendas Semestrais',
          data: [],
          lineTension: 0.2,
          borderColor: '#1976D2',
          backgroundColor: 'rgba(25, 118, 210, 0.3)', // Preenchimento de fundo
          borderWidth: 1,
          pointRadius: 3,
          pointBackgroundColor: '#1976D2',
          fill: true,
        }]
      };
      
      const hoje = new Date;
      bestSellingCategories.forEach((sellingCategorie) => {
        // data.labels.push(sellingCategorie.categoria);
        data.labels.push(hoje.setDate(hoje.getDate() - 50));
        data.datasets[0].data.push(Number(sellingCategorie.total_vendido));
      });

      const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'month',
            },
            grid: {
              display: false,
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
            text: 'Vendas',
            font: {
              size: 18
            },
          },
          customCanvasBackgroundColor: {
            color: 'white',
          },
          tooltip: {
            callbacks: {
              label: function(context){
                return `R$ ${context.parsed.y.toFixed(2).replace('.', ',')}`;
              },
              title: function(context){
                const datetime = context[0].label;

                let [mes, dia, ano, hora] = datetime.split(' ');

                return `${dia} de ${mes} de ${ano}`.replaceAll(',', '');
              }
            }
          }
        },
        devicePixelRatio: 4,
      };

      createChart({
        id: 'myLineChart', 
        type: 'line', 
        data: data, 
        options: options,
      });

      isVisible.lineChart = true;
    }
  }

  onMounted(() => {
    createLineChart();

    createPieChart();
  });
</script>

<template>
  <Snackbar/>

  <div id="line-chart"
    class="pa-4" 
    color="grey-lighten-4"
    v-show="isVisible.lineChart"
  >
    <canvas  
      id="myLineChart"
      width="400"
      height="400"
      class="elevation-2 rounded"></canvas>
  </div>

  <div id="clientes-mais-compraram-e-produtos-mais-vendidos"
    class="pa-4" 
    color="grey-lighten-4"
  >
    <v-row>
      <v-col>
        <v-card
          class="elevation-2 rounded"
        >
          <v-card-title><strong>Clientes que mais compraram</strong></v-card-title>
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
        >
          <v-card-title><strong>Produtos mais vendidos</strong> </v-card-title>
        
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
  </div>

  <div id="pie-chart"
    class="pa-4" 
    color="grey-lighten-4"
    style="height: 450px;"
    v-show="isVisible.pieChart"
  >
    <canvas  
      id="myPieChart"
      width="50"
      height="50"
      class="elevation-2 rounded"></canvas>
  </div> 
</template>

<style scoped>
</style>