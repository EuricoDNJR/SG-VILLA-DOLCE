<script setup>
  import { onMounted, ref } from 'vue'
  import { fetchGet, getAuthToken, setMessageSnackbar } from '../utils/common';

  const props = defineProps(['idPedido']);

  const produtos = ref([]);

  async function requestPedidoById(id=props.idPedido){
    let pedido = undefined;

    try{
      const url = `http://127.0.0.1:8000/v1/pedido/get_order/${id}`;
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status == 200){
          pedido = responseJson;
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar pedido", 'warning');
    }

    return pedido;
  }

  async function getProdutosPedido(){
    const pedido = await requestPedidoById();
    
    produtos.value = pedido.idProdutos;
    console.log(pedido.idProdutos);
  }

  onMounted(() => getProdutosPedido());
</script>

<template>
  <v-list> 
    <v-list-subheader>PRODUTOS</v-list-subheader>

    <v-list-item
      v-for="(produto, i) in produtos" :key="i"
    >
      <v-card
        class="pa-1"
        variant="tonal"
      >
        <v-card-title>{{ produto.nome }}</v-card-title>
        <v-card-subtitle>{{produto.quantidade.replace('.', ',')}} x {{produto.valorVendaUnd.replace('.', ',')}} = <v-chip color="green" variant="elevated">R$ {{produto.valorTotal.replace('.', ',')}}</v-chip></v-card-subtitle>
      </v-card>   
    </v-list-item>
  </v-list>
</template>

<style scoped>
</style>
