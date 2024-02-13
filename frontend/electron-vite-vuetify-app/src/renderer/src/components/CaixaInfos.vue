<script setup>
  import { ref, computed, watch, onMounted, reactive, toRaw,  onBeforeUnmount } from 'vue'
  import { fetchGet, fetchPost, fetchPatch, confirmDialog, getFormatedDate } from '../utils/common';
  import { useAuthStore, useSnackbarStore } from '../utils/store';
  import SelecionarProdutoPedido from '../components/SelecionarProdutoPedido.vue';
  import PesquisarClientePedido from '../components/PesquisarClientePedido.vue';
  import DescontoPedido from '../components/DescontoPedido.vue';

  const props = defineProps(['caixa']);
  const emit = defineEmits(['voltar']);

  const formasPagamento = ref(["Dinheiro", "Pix"]);

  console.log(props.caixa);

  // const authStore = useAuthStore();
  // const snackbarStore = useSnackbarStore()
  
  // const produtoRemovido = reactive({
  //   wasRemoved: false,
  //   idProduto: undefined,
  //   quantidade: undefined,
  // });

  // const pedido = ref([]);
  // const Pagamento = reactive({
  //   valorTotal: computed(() => {
  //     return pedido.value.reduce((somatorio, produto) => {
  //       return somatorio + Number(produto.quantidade) * Number(produto.valorVendaUnd) - Number(produto.desconto);
  //     }, 0);
  //   }),
  //   valorTotalComputed: computed(() => Pagamento.valorTotal.toFixed(2)),
  //   valorRecebimento: 0,
  //   valorDevolvido: computed(() => ((Pagamento.valorRecebimento - Pagamento.valorTotal) > 0 ? Pagamento.valorRecebimento - Pagamento.valorTotal : 0).toFixed(2)),
  //   tiposPagamento: [],
  //   pagamentoSelecionado: undefined,
  // });
  // const cliente = reactive({
  //   saldo: 0,
  // });
  // const dialogIsVisible = reactive({
  //   finalizarPedido: false,
  //   desconto: false,
  // });
  // const loading = reactive({
  //   finalizarBtn: false,
  //   descontoPedido: true,
  // });


  // async function requestAllPaymentTypes(){
  //   try{
  //     const url = "http://127.0.0.1:8000/v1/tipo_pagamento/get_all_payment_types/"
  //     const token = authStore.getToken;
      
  //     const response = await fetchGet(url, token);
  //     const responseJson = await response.json();

  //     if(response.status === 200){
  //       Pagamento.tiposPagamento = responseJson;

  //       Pagamento.pagamentoSelecionado = Pagamento.tiposPagamento[0];
  //     }else{
  //       snackbarStore.set(responseJson.message, 'warning');
  //     }
  //   }catch(e){
  //     console.log(e);
  //     snackbarStore.set("Falha ao carregar tipos de pagamento", 'warning');
  //   }
  // }
  
  // async function requestOrder(idPedido=props.pedido.idPedido){
  //   try{
  //     const url = `http://127.0.0.1:8000/v1/pedido/get_order/${idPedido}/`
  //     const token = authStore.getToken;
      
  //     const response = await fetchGet(url, token);
  //     const responseJson = await response.json();

  //     if(response.status === 200){  
  //       if(responseJson.idProdutos){
  //         pedido.value = responseJson.idProdutos;
  //         pedido.value.forEach((produto) => {
  //           produto.id = -1;
  //         });
  //       }
        
  //       cliente.saldo = Number(responseJson.saldoCliente);

  //       loading.descontoPedido = false;
  //     }else{
  //       snackbarStore.set(responseJson.message, 'warning');
  //     }
  //   }catch(e){
  //     console.log(e);
  //     snackbarStore.set("Falha ao carregar pedido", 'warning');
  //   }
  // }

  // async function requestFinishOrder(idPedido=props.pedido.idPedido){
  //   loading.finalizarBtn = true;

  //   try{
  //     await requestAddInOrder();
      
  //     const url = `http://127.0.0.1:8000/v1/pedido/finish_order/${idPedido}/`;
  //     const body = {
  //       valorRecebimento: Pagamento.valorRecebimento,
  //       valorDevolvido: Pagamento.valorDevolvido,
  //       tipoPagamento: Pagamento.pagamentoSelecionado.nome,
  //     };
  //     const token = authStore.getToken;

  //     const response = await fetchPatch(url, body, token);
  //     const responseJson = await response.json();

  //     if(response.status === 200){       
  //       emit('pedidoFinished', idPedido);

  //       snackbarStore.set(responseJson.message, 'success');
  //     }else{
  //       snackbarStore.set(responseJson.message, 'warning');
  //     }
  //   }catch(e){
  //       console.log(e);
  //       snackbarStore.set("Falha ao finalizar pedido", 'warning');
  //     }

  //   loading.finalizarBtn = false;
  // }

  // async function requestAddInOrder(idPedido=props.pedido.idPedido){
  //   try{
  //     const url = `http://127.0.0.1:8000/v1/pedido/add_in_order/${idPedido}/`;
  //     const body = {
  //         idProdutos: pedido.value.filter(
  //           (produto) => produto.id != -1
  //         ).map(
  //           (produto) => {
  //             return {
  //               idProduto: produto.idProduto,
  //               quantidade: produto.quantidade,
  //               valorVendaUnd: produto.valorVendaUnd,
  //               desconto: produto.desconto
  //             };
  //           }
  //         ),
  //     };
  //     const token = authStore.getToken;
      
  //     if(body.idProdutos.length > 0){
  //       const response = await fetchPatch(url, body, token);
  //       const responseJson = await response.json();

  //       if(response.status === 200){
  //         pedido.value.forEach(
  //           (produto) => produto.id = -1
  //         )

  //         emit('adicionadoAoPedido', Pagamento.valorTotal);

  //         snackbarStore.set(responseJson.message, 'success');
  //       }else{
  //         snackbarStore.set(responseJson.message, 'warning');
  //       }
  //     }
  //   }catch(e){
  //     console.log(e);
  //     snackbarStore.set("Falha ao adicionar produto ao pedido", 'warning');
  //   }
  // }

  // function removeProdutoInPedido(product){   
  //   pedido.value = pedido.value.filter((produto) => produto.id != product.id);
    
  //   produtoRemovido.idProduto = product.idProduto;
  //   produtoRemovido.quantidade = product.quantidade;
  //   produtoRemovido.wasRemoved = !produtoRemovido.wasRemoved;
  // }
  
  // function closeDialog(nome){
  //   dialogIsVisible[nome] = false;

  //   if(nome == "finalizarPedido"){
  //     Pagamento.valorRecebimento = 0;
  //   }
  // }

  // function adicionarProduto(produto){
  //   produto.id = pedido.value.length;

  //   pedido.value.push(produto);
  // }

  // requestOrder();
  // requestAllPaymentTypes();
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
              <v-row v-for="(v, i) in formasPagamento" dense>
                <v-col>
                  <span class="text-grey-darken-1">{{v}}</span>
                </v-col>
                <v-col>
                  <span class="text-green">R$ 2000,30</span>
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
                  <span class="text-green">R$ 2000,30</span>
                </v-col>
              </v-row>

              <v-row dense>
                <v-col>
                  <span class="text-grey-darken-1">Saídas</span>
                </v-col>
                <v-col>
                  <span class="text-red">R$ 2000,30</span>
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
                  <span class="text-green font-weight-bold">R$ 0,00</span>
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
                  <span>10 pedidos</span>
                </v-col>
              </v-row>

              <v-row dense>
                <v-col>
                  <span class="text-grey-darken-1">Cancelado</span>
                </v-col>
                <v-col>
                  <span>2 pedidos</span>
                </v-col>
              </v-row>

              <v-row dense>
                <v-col>
                  <span class="text-grey-darken-1">Ticker Médio</span>
                </v-col>
                <v-col>
                  <span class="text-green">R$ 200,03</span>
                </v-col>
              </v-row>

              <v-row dense>
                <v-col>
                  <span class="text-grey-darken-1">Média de produto</span>
                </v-col>
                <v-col>
                  <span>10,3</span>
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