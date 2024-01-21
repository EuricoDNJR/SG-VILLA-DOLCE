<script setup>
    import { ref   } from 'vue'
    import { createCelula } from '../utils/common';
    import { getAuthToken, setMessageSnackbar, fetchGet } from '../utils/common'
    import FormPost from '../components/FormPost.vue';

    const loading = ref(true);
    let produtos = undefined;

    async function requestAllProducts(){
      try{
        const url = "http://127.0.0.1:8000/v1/produto/get_all_products/";
        const token = getAuthToken();

        const response = await fetchGet(url, token);
        const responseJson = await response.json();

        if(response.status === 200){
          produtos = responseJson;

          loading.value = false;
        }else if(response.status != 204){
          setMessageSnackbar(responseJson.message, "warning");
        }
      }catch(e){
        console.log(e);
        setMessageSnackbar("Erro ao carregar produtos", "warning");
      }
    }

    requestAllProducts();
</script>

<template>
  <FormPost v-if="!loading"
    title="Inserir Estoque"
    url="http://127.0.0.1:8000/v1/estoque/create_stock_registre/"
    :configs="[
        [createCelula('idProduto', 'Produto', 'select', true), createCelula('quantidade', 'Quantidade', 'number', true)],
        [createCelula('dataEntrada', 'Data de Entrada', 'date', true), createCelula('dataVencimento', 'Data de Vencimento', 'date')],
        [createCelula('observacoes', 'Observações', 'text')],
    ]"
    :fixies="[
        ['Produto.items', produtos],
        ['Produto.itemsTitle', 'nome'],
        ['Produto.itemsValue', 'idProduto'],
        ['Produto.obj.value', produtos[0].idProduto],
    ]"
    btnText="Inserir"
    btnIcon="mdi-plus-minus-box"
    successMessage="Estoque inserido com sucesso"
    errorMessage="Falha ao inserir estoque"
  />
</template>
<style scoped>
</style>
