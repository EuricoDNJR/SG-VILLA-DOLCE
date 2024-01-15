<script setup>
  import { ref, computed } from 'vue'
  import { useAuthStore, useSnackbarStore, useCaixaStore } from '../utils/store';
  import { fetchGet, replaceNullToEmptyString } from '../utils/common';
  import Snackbar from '../components/Snackbar.vue';

  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore();
  const caixaStore = useCaixaStore();
  const pedidosEmAberto = ref([
        { id: 1, nome: 'Pedido 1', data: '01/01/2024', detalhes: 'Detalhes do pedido 1' },
        { id: 2, nome: 'Pedido 2', data: '02/01/2024', detalhes: 'Detalhes do pedido 2' },
        { id: 3, nome: 'Pedido 3', data: '03/01/2024', detalhes: 'Detalhes do pedido 3' },
        { id: 4, nome: 'Pedido 4', data: '04/01/2024', detalhes: 'Detalhes do pedido 4' },
        // Adicione mais pedidos conforme necessário
      ]);

  function calculatedRows(){
    const pedidosMatrix = [];

    let j = -1;
    for(let i=0; i < pedidosEmAberto.value.length; i++){
      if(i/3 === 0){
        pedidosMatrix.push([]);
        j++;
      }
      pedidosMatrix[j].push(pedidosEmAberto.value[i]);
    }

    return pedidosMatrix;
  }
  async function requestPedidosEmAberto(){
    try{
      const url = "http://127.0.0.1:8000/v1/pedido/get_all_orders/";
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status === 200){
        pedidosEmAberto.value = await response.json();;
      }
    }catch(e){
      console.log(e);
      snackbarStore.set("Falha ao carregar pedidos", "warning");
    }
  }

  requestPedidosEmAberto();
</script>

<template>
  <div class="pa-4">
    <v-row v-for="(rowPedidos, rowIndex) in calculatedRows()" :key="rowIndex">
      <v-col
        v-for="pedido in rowPedidos"
        :key="pedido.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card
          class="mb-4 border-start-card"
          :title="pedido.nome"
          :subtitle="pedido.data"
          hover
        >
          <template v-slot:prepend>
            <v-avatar color="blue-darken-2">
              <v-icon icon="mdi-label"></v-icon>
            </v-avatar>
          </template>  

          <template v-slot:append>
            <v-chip color="green">
              <h3>R$ 120,32</h3>
            </v-chip>
          </template> 
          
          <v-card-text>
            <v-timeline density="compact" align="start">
              
              <v-timeline-item
                dot-color="blue-darken-2"
                size="x-small"
              >
                {{ pedido.detalhes }}
              </v-timeline-item>
            </v-timeline>

            <v-timeline density="compact" align="start">
              
              <v-timeline-item
                dot-color="blue-darken-2"
                size="x-small"
              >
                {{ pedido.detalhes }}
              </v-timeline-item>
            </v-timeline>

            <v-timeline density="compact" align="start">
              
              <v-timeline-item
                dot-color="grey-darken-3"
                size="x-small"
              >
                <v-icon>mdi-dots-horizontal</v-icon>
              </v-timeline-item>
            </v-timeline>
            <!-- <v-timeline density="compact" align="start">
              pedido.detalhes 
              <v-timeline-item
                v-for="message in messages"
                :key="message.time"
                :dot-color="message.color"
                size="x-small"
              >
                <div class="mb-4">
                  <div class="font-weight-normal">
                    <strong>{{ message.from }}</strong> @{{ message.time }}
                  </div>
                  <div>{{ message.message }}</div>
                </div>
              </v-timeline-item>
            </v-timeline> -->
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped>
.border-start-card {
  border-left: 4px solid #1976D2; /* Cor e largura da borda */
}
</style>
