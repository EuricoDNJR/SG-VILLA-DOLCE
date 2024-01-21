<script setup>
  import { ref, computed, watch, onMounted } from 'vue'
  import { useAuthStore, useSnackbarStore, useCaixaStore, usePedidoStore } from '../utils/store';
  import { fetchGet, fetchPatch, confirmDialog } from '../utils/common';
  import EditarPedido from '../components/EditarPedido.vue';

  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore();
  const caixaStore = useCaixaStore();
  
  const pedidosEmAberto = ref([]);
  const calculatedRows = computed(() => {
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
  });

  const isEditarPedido = ref(false);

  let pedido = undefined;

  
  async function requestPedidosEmAberto(idCaixa=caixaStore.getId){
    try{
      const url = `http://127.0.0.1:8000/v1/caixa/get_pedidos_caixa/${idCaixa}`;
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){
        pedidosEmAberto.value = responseJson.filter((pedido) => pedido.status == "Pendente");
      }
    }catch(e){
      console.log(e);
      snackbarStore.set("Falha ao carregar pedidos", "warning");
    }
  }

  async function requestCancelarPedido(idPedido=pedido.idPedido){
    try{
      const url = `http://127.0.0.1:8000/v1/pedido/cancel_order/${idPedido}/`
      const body = {};
      const token = authStore.getToken;

      const response = await fetchPatch(url, body, token);
      const responseJson = await response.json();

      if(response.status === 200){
        pedidosEmAberto.value = pedidosEmAberto.value.filter((pedido) => pedido.idPedido != idPedido);

        snackbarStore.set("Pedido cancelado com sucesso", 'success');

        toPedidosEmAberto();
      }else{
        snackbarStore.set(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set("Erro ao cancelar pedido", 'warning');
    }       
  }

  function toEditarPedido(order){
    pedido = order;

    isEditarPedido.value = true; 
  }

  function toPedidosEmAberto(){
    isEditarPedido.value = false; 
  }

  function cancelarPedidoConfirmation(){
    confirmDialog(`Tem certeza que deseja cancelar o pedido?`, requestCancelarPedido);
  }

  function finishPedido(idPedidoFinished){
    isEditarPedido.value = false;

    pedidosEmAberto.value = pedidosEmAberto.value.filter((pedido) => pedido.idPedido != idPedidoFinished);
  }

  function atualizarPedido(valorTotal){ 
    pedido.valorTotal = valorTotal.toFixed(2);
  }

  onMounted(() => requestPedidosEmAberto());
</script>

<template>
  <div v-if="isEditarPedido" class="pa-2">    
    <EditarPedido 
      :pedido="pedido"
      @voltar="toPedidosEmAberto"
      @cancelarPedido="cancelarPedidoConfirmation"
      @pedidoFinished="finishPedido"
      @adicionadoAoPedido="atualizarPedido"
    />
  </div>
  <div class="pa-4" v-else>
    <v-row v-for="(rowPedidos, rowIndex) in calculatedRows" :key="rowIndex">
      <v-col
        v-for="pedido in rowPedidos"
        :key="pedido.idPedido"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card
          class="mb-4 border-start-card"
          :title="pedido.nomeCliente"
          :subtitle="pedido.telefoneCliente"
          @click="() => toEditarPedido(pedido)"
        >
          <template v-slot:prepend>
            <v-avatar color="blue-darken-2">
              <v-icon icon="mdi-label"></v-icon>
            </v-avatar>
          </template>  

          <template v-slot:append>
            <v-chip color="green">
              <h3>R$ {{ pedido.valorTotal.replace(".", ",") }}</h3>
            </v-chip>
          </template> 
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
