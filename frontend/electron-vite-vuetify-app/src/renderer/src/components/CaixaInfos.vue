<script setup>
  import { ref, computed, watch, onMounted, reactive, toRaw,  onBeforeUnmount } from 'vue'
  import { fetchGet, fetchPost, fetchPatch, confirmDialog, getFormatedDate } from '../utils/common';
  import { useAuthStore, useSnackbarStore } from '../utils/store';
  import SelecionarProdutoPedido from '../components/SelecionarProdutoPedido.vue';
  import PesquisarClientePedido from '../components/PesquisarClientePedido.vue';
  import DescontoPedido from '../components/DescontoPedido.vue';

  const props = defineProps(['caixa']);
  const emit = defineEmits([
    'voltar',
  ]);

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
</template>

<style scoped>
</style>