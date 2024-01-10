<script setup>
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router';
  import { useAuthStore, useSnackbarStore, useCaixaStore } from '../utils/store';
  import { fetchGet, replaceNullToEmptyString } from '../utils/common';
  import Snackbar from '../components/Snackbar.vue';

  defineOptions({
    inheritAttrs: false
  });

  // const router = useRouter();
  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore();
  const caixaStore = useCaixaStore();
  // let funcionarios = [];
  // let funcionariosFiltered = [];
  // const loading = ref(true);
  // const searchText = ref('');
  const caixaIsOpen = computed(() => caixaStore.getStatus === 'aberto');
  const pedidosEmAberto = ref([
        { id: 1, nome: 'Pedido 1', data: '01/01/2024', detalhes: 'Detalhes do pedido 1' },
        { id: 2, nome: 'Pedido 2', data: '02/01/2024', detalhes: 'Detalhes do pedido 2' },
        { id: 3, nome: 'Pedido 3', data: '03/01/2024', detalhes: 'Detalhes do pedido 3' },
        // Adicione mais pedidos conforme necessário
      ]);

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
    <v-toolbar color="grey-lighten-4" class="pa-4">
      <v-row align="center">
        <v-col>
          <v-toolbar-title class="text-uppercase">
            <span class="font-weight-bold">Pedidos em Aberto</span>
          </v-toolbar-title>
        </v-col>
      </v-row>
    </v-toolbar>
    
    <v-container>
      <v-row justify="center">
        <v-col
          v-for="pedido in pedidosEmAberto"
          :key="pedido.id"
          cols="12"
          sm="6"
          md="4"
        >
          <v-card
            class="mb-4 border-start-card"
            :title="pedido.nome"
            :subtitle="pedido.data"
            border="start"
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
    </v-container>
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
