<script setup>
  import { ref, computed, watch, onMounted, reactive, toRaw } from 'vue'
  import { fetchGet, fetchPost, confirmDialog, getFormatedDate } from '../utils/common';
  import { useAuthStore, useSnackbarStore, useCaixaStore } from '../utils/store';
  import SelecionarProdutoPedido from '../components/SelecionarProdutoPedido.vue';
  import PesquisarClientePedido from '../components/PesquisarClientePedido.vue';
  import DescontoPedido from '../components/DescontoPedido.vue';

  const emit = defineEmits(['pedidoCriado']);

  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore()
  const caixaStore = useCaixaStore();  

  const telefoneVisitante = "00000000000";

  const produtoRemovido = reactive({
    wasRemoved: false,
    idProduto: undefined,
    quantidade: undefined,
  });

  const Pagamento = reactive({
    valorTotal: computed(() => {
      return pedido.value.reduce((somatorio, produto) => {
        return somatorio + Number(produto.quantidade) * Number(produto.valorVendaUnd) - Number(produto.desconto);
      }, 0);
    })
  });

  const pedido = ref([]);

  let clienteSelecionado = undefined;

  const loadingCriarPedido = ref(false);
  

  function createOrder(){
    const idProdutos = [];
    
    pedido.value.forEach((product) => {
      idProdutos.push({
        idProduto: product.idProduto,
        quantidade: product.quantidade,
        valorVendaUnd: product.valorVendaUnd,
        desconto: product.desconto,
      });
    });

    const order = {
      "idCliente": clienteSelecionado.idCliente,
      "Pagamento": {},
      "idCaixa": caixaStore.getId,
      "idProdutos": idProdutos,
      "status": "Pendente",
    }

    return order;
  }

  async function requestCreateOrder(){
      loadingCriarPedido.value = true;

      try{
        const url = "http://127.0.0.1:8000/v1/pedido/create_order/";
        const body = createOrder();
        const token = authStore.getToken;

        const response = await fetchPost(url, body, token);
        const responseJson = await response.json();
        
        if(response.status === 201){
          emit('pedidoCriado');
          
          snackbarStore.set(responseJson.message, "success");
        }else{
          snackbarStore.set(responseJson.message, "warning");
        }
      }catch(e){
        console.log(e);
        snackbarStore.set("Falha ao criar pedido", "warning");
      }

      loadingCriarPedido.value = false;
  }

  function removeProdutoInPedido(product){
    pedido.value = pedido.value.filter((produto) => produto.id != product.id);

    produtoRemovido.idProduto = product.idProduto;
    produtoRemovido.quantidade = product.quantidade;
    produtoRemovido.wasRemoved = !produtoRemovido.wasRemoved;
  }

  function atualizaCliente(cliente){
    clienteSelecionado = cliente;

    pedido.value.forEach((produto) => {
      produto.desconto = "0.00";
    });
  }

  function adicionarProduto(produto){
    produto.id = pedido.value.length;

    pedido.value.push(produto);
  };
</script>

<template>
  <div class="pa-2">
    <SelecionarProdutoPedido
      :produtoRemovido="produtoRemovido"
      @produtoAdicionado="adicionarProduto"
    />
  </div>

  <v-navigation-drawer
    permanent
    location="right"
  >
    <template v-slot:prepend>
      <PesquisarClientePedido 
        class="pa-2"
        :telefoneCliente="telefoneVisitante"
        :readonly="false" 
        @clienteAtualizado="atualizaCliente"
      />
    </template>

    <div class="pa-2">
      <v-list lines="one">
        <v-row v-for="(produto, i) in pedido" :key="i">
          <v-list-item
            :title="produto.nome"
            :subtitle="`${produto.quantidade.replace('.', ',')} x ${produto.valorVendaUnd} - ${produto.desconto.replace('.', ',')}`"
          ></v-list-item>
  
          <v-spacer></v-spacer>
  
          <v-btn
            icon="mdi-delete"
            color="primary"
            variant="text"
            @click="() => removeProdutoInPedido(produto)"
          ></v-btn>
        </v-row>
      </v-list>
    </div>

    <template v-slot:append>
      <v-row class="pa-2 mt-2">
        <v-chip color="grey-darken-4" variant="text">
          <h2>Total:</h2>
        </v-chip>

        <v-spacer></v-spacer>

        <v-chip color="green-darken-1" variant="text">
          <h2>R$ {{ Pagamento.valorTotal.toFixed(2).replace('.', ',') }}</h2>
        </v-chip>
      </v-row>

      <DescontoPedido v-if="pedido.length > 0"
        :pedido="pedido"
        :saldoCliente="clienteSelecionado.saldo"
      />

      <v-btn
        block
        color="green"
        prepend-icon="mdi-receipt-text-plus"
        @click="requestCreateOrder"
        :loading="loadingCriarPedido"
      >
        Criar
      </v-btn>
    </template>
  </v-navigation-drawer>
</template>

<style scoped>
</style>