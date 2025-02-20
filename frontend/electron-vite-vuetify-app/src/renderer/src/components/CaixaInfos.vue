<script setup>
  import { ref, computed, watch, onMounted, reactive } from 'vue'
  import { fetchGet, getAuthToken, setMessageSnackbar, confirmDialog, getFormatedDate } from '../utils/common';

  const props = defineProps(['caixa']);
  const emit = defineEmits(['voltar']);

  const formasPagamento = ref([]);
  const entradas = ref(0);
  const saidas = ref(0);
  const qtdPedidos = ref(0);
  const qtdPedidosCancelados = ref(0);
  const mediaProdutos = ref(0);


  async function requestSumTypePayment(idCaixa=props.caixa.idCaixa){
    try{
      const url = `http://127.0.0.1:8000/v1/caixa/get_sum_type_payment/${idCaixa}`
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){
        formasPagamento.value = responseJson;
      }else{
        setMessageSnackbar(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar tipos de pagamento", 'warning');
    }
  }

  async function requestInputsAndOutputs(idCaixa=props.caixa.idCaixa){
    try{
      const url = `http://127.0.0.1:8000/v1/caixa/get_inputs_outputs/${idCaixa}`
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){
        entradas.value = responseJson.entradas;
        saidas.value = responseJson.saidas;
      }else{
        setMessageSnackbar(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar tipos de pagamento", 'warning');
    }
  }

  async function requestQuantOrdersStats(idCaixa=props.caixa.idCaixa){
    try{
      const url = `http://127.0.0.1:8000/v1/caixa/get_quant_orders_stats/${idCaixa}`
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){
        qtdPedidos.value = responseJson.nao_cancelados;
        qtdPedidosCancelados.value = responseJson.cancelados;
      }else{
        setMessageSnackbar(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar tipos de pagamento", 'warning');
    }
  }

  async function requestAverageProductsPerOrder(idCaixa=props.caixa.idCaixa){
    try{
      const url = `http://127.0.0.1:8000/v1/caixa/average_products_per_order/${idCaixa}`
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){
        mediaProdutos.value = responseJson;
      }else{
        setMessageSnackbar(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar tipos de pagamento", 'warning');
    }
  }

  onMounted(() => {
    requestSumTypePayment();
    requestInputsAndOutputs();
    requestQuantOrdersStats();
    requestAverageProductsPerOrder();
  });
</script>

<template>
  <div class="d-flex justify-space-between align-center">
      <v-btn
        variant="text"
        icon="mdi-arrow-left"
        @click="emit('voltar')"
      >
        <v-icon>mdi-arrow-left</v-icon>
        <v-tooltip 
          activator="parent"
          location="bottom"
        >
          Voltar
        </v-tooltip >
      </v-btn>
  </div>

  <div class="pa-4">
    <v-card class="mb-1">
      <v-card-item>
        <v-row class="d-flex align-center">
          <v-col>
            <p class="text-grey text-caption">Saldo Inicial</p>
            <p class="text-green font-weight-bold">R$ {{ props.caixa.saldoInicial.replace('.', ',')}}</p>
          </v-col>
          
          <v-divider vertical></v-divider>

          <v-col>
            <p class="text-grey text-caption">Saldo Final</p>
            <p class="text-green font-weight-bold">R$ {{ props.caixa.saldoFinal.replace('.', ',')}}</p>
          </v-col>

          <v-divider vertical></v-divider>

          <v-col>
            <v-chip 
              :color="props.caixa.aberto ? 'blue' : 'grey'"
              variant="flat"
            >
              Status: {{props.caixa.aberto ? 'Aberto' : 'Fechado'}}
            </v-chip>
          </v-col>
        </v-row>
      </v-card-item>
    </v-card>

    <v-card color="grey-lighten-4">
      <v-card-item>
        <v-row class="d-flex align-center">
          <v-col>
            <p class="text-grey text-caption">Abertura</p>
            <p>{{getFormatedDate(props.caixa.dataAbertura)}} <v-icon color="primary">mdi-account</v-icon>{{props.caixa.nomeUsuarioAbertura}}</p>
          </v-col>

          <v-divider vertical></v-divider>

          <v-col>
            <p class="text-grey text-caption">Fechamento</p>
            <p v-if="props.caixa.aberto">Indefinido</p>
            <p v-else>{{getFormatedDate(props.caixa.dataFechamento)}} <v-icon color="primary">mdi-account</v-icon>{{props.caixa.nomeUsuarioFechamento}}</p>
            
          </v-col>
        </v-row>
      </v-card-item>
    </v-card>
    
    <v-row class="mt-4">
      <v-col>
        <v-card class="h-100">
          <v-card-title class="font-weight-bold">Caixa</v-card-title>
          
          <v-divider></v-divider>

          <v-card-item>
            <div id="FormasDePagamento">
              <v-row v-for="(value, key) in formasPagamento" dense>
                <v-col>
                  <span class="text-grey-darken-1">{{key}}</span>
                </v-col>
                <v-col>
                  <span class="text-green">R$ {{value.replace('.', ',')}}</span>
                </v-col>
              </v-row>
            </div>

            <v-divider class="mt-2 mb-2"></v-divider>

            <div id="EntradasESaidas">
              <v-row dense>
                <v-col>
                  <span class="text-grey-darken-1">Entradas</span>
                </v-col>
                <v-col>
                  <span class="text-green">R$ {{entradas}}</span>
                </v-col>
              </v-row>

              <v-row dense>
                <v-col>
                  <span class="text-grey-darken-1">Saídas</span>
                </v-col>
                <v-col>
                  <span class="text-red">R$ {{saidas}}</span>
                </v-col>
              </v-row>
            </div>

            <v-divider class="mt-2 mb-2"></v-divider>

            <div id="Total">
              <v-row dense>
                <v-col>
                  <span class="font-weight-bold">Total</span>
                </v-col>
                <v-col>
                  <span class="text-green font-weight-bold">R$ {{ props.caixa.saldoFinal.replace('.', ',')}}</span>
                </v-col>
              </v-row>
            </div>
          </v-card-item>
        </v-card>
      </v-col>

      <v-col>
        <v-card class="h-100">
          <v-card-title class="font-weight-bold">Estatísticas</v-card-title>
          
          <v-divider></v-divider>

          <v-card-item>
             <v-row dense>
                <v-col>
                  <span class="text-grey-darken-1">Pedidos</span>
                </v-col>
                <v-col>
                  <span>{{ qtdPedidos }} pedido(s)</span>
                </v-col>
              </v-row>

              <v-row dense>
                <v-col>
                  <span class="text-grey-darken-1">Cancelado</span>
                </v-col>
                <v-col>
                  <span>{{ qtdPedidosCancelados }} pedido(s)</span>
                </v-col>
              </v-row>

              <v-row dense>
                <v-col>
                  <span class="text-grey-darken-1">Ticker Médio</span>
                </v-col>
                <v-col>
                  <span class="text-green">R$ {{(Number(props.caixa.saldoFinal) / qtdPedidos).toFixed(2).replace('.', ',')}}</span>
                </v-col>
              </v-row>

              <v-row dense>
                <v-col>
                  <span class="text-grey-darken-1">Média de produto</span>
                </v-col>
                <v-col>
                  <span>{{mediaProdutos.toFixed(1).replace('.', ',')}}</span>
                </v-col>
              </v-row>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </div>
  <!-- <v-row class="d-flex align-center">
              <v-col>
                <p class="text-grey text-caption">Saldo Final</p>
                <p class="text-green font-weight-bold">R$ {{ props.caixa.saldoFinal.replace('.', ',')}}</p>
              </v-col>

              

              <v-col>
                <v-chip 
                  :color="props.caixa.aberto ? 'blue' : 'grey'"
                  variant="flat"
                >
                  Status: {{props.caixa.aberto ? 'Aberto' : 'Fechado'}}
                </v-chip>
              </v-col>
            </v-row> -->
</template>

<style scoped>
</style>