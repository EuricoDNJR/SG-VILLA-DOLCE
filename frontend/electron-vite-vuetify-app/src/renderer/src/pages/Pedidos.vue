<script setup>
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router';
  import { useAuthStore, useSnackbarStore, useCaixaStore } from '../utils/store';
  import { fetchGet, replaceNullToEmptyString } from '../utils/common';
  import Snackbar from '../components/Snackbar.vue';
  import CriarPedido from '../components/CriarPedido.vue';
  import PedidosEmAberto from '../components/PedidosEmAberto.vue';


  defineOptions({
    inheritAttrs: false
  });

  // const router = useRouter();
  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore();
  const caixaStore = useCaixaStore();
  const isCriarPedido = ref(false);
  // let funcionarios = [];
  // let funcionariosFiltered = [];
  // const loading = ref(true);

  const caixaIsOpen = computed(() => caixaStore.getStatus === 'aberto');
  const pedidosEmAberto = ref([
        { id: 1, nome: 'Pedido 1', data: '01/01/2024', detalhes: 'Detalhes do pedido 1' },
        { id: 2, nome: 'Pedido 2', data: '02/01/2024', detalhes: 'Detalhes do pedido 2' },
        { id: 3, nome: 'Pedido 3', data: '03/01/2024', detalhes: 'Detalhes do pedido 3' },
        // Adicione mais pedidos conforme necessário
      ]);

  function toPedidosEmAberto(){
    isCriarPedido.value = false;
  }
  
  function toCriarPedido(){
    isCriarPedido.value = true;
  }
  // const searchPedidos = () => {
  //   // Recarregando a tabela para atualizar 
  //   loading.value = true;

  //   funcionariosFiltered = funcionarios.filter((funcionario) => funcionario.nome.toLowerCase().includes(searchText.value.toLowerCase()));
   
  //   loading.value = false;
  // }

  // const redirectToCriarPedido = () => {
  //   router.push("/menu/criar-pedido/");
  // }

  // const redirectToPedidoInfo = () => {
  //   router.push("/menu/ver-funcionario/");
  // }

  // const handlePedidoInfoAndRedirect = (funcionario) => {
  //   replaceNullToEmptyString(funcionario);

  //   funcionarioStore.saveFuncionarioInfo({...funcionario});

  //   redirectToPedidoInfo();
  // }

  // const requestAllPedidos = async () =>{
  //   try{
  //     const url = "http://127.0.0.1:8000/v1/pedido/get_all_orders/";
  //     const token = authStore.getToken;
      
  //     const response = await fetchGet(url, token);

  //     if(response.status === 200){
  //       funcionarios = await response.json();

  //       funcionariosFiltered = [...funcionarios];
  //       console.log(funcionariosFiltered);
  //     }else{
  //       snackbarStore.set("Falha ao carregar pedidos", "warning");
  //     }
  //   }catch(e){
  //     console.log(e);
  //     snackbarStore.set("Falha ao carregar pedidos", "warning");
  //   }
   
  //   loading.value = false;
  // }

  // requestAllPedidos();
  
</script>

<template>
  <Snackbar/>       
  
  <div v-if="caixaIsOpen" class="page-content">
    <v-app-bar  color="deep-purple" :elevation="2" density="compact">
        <v-app-bar-title>Pedidos</v-app-bar-title>

        <template v-slot:prepend>
          <v-icon>mdi-menu-right</v-icon>
        </template>

        <v-btn
            variant="text"
            prepend-icon="mdi-view-list"
            stacked
            @click="toPedidosEmAberto"
        >
            Pedidos em Aberto
        </v-btn>

        <v-btn
            variant="text"
            prepend-icon="mdi-receipt-text-plus"
            stacked
            @click="toCriarPedido"
        >
            Criar Pedido
        </v-btn>
    </v-app-bar>

    <div v-if="isCriarPedido">
      <CriarPedido/>
    </div>

    <div v-else>
      <PedidosEmAberto/>
    </div>
  </div>
  <div v-else class="close-caixa">
    <v-container fluid fill-height>
        <v-row align="center" justify="center">
          <v-col cols="12" md="6">
            <v-card
              class="text-center"
              color="red-darken-2"
              dark
            >
              <v-card-text class="display-2">
                <h2>Caixa Fechado</h2>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
  </div>
</template>

<style scoped>
.border-start-card {
  border-left: 4px solid #1976D2; /* Cor e largura da borda */
}
</style>
