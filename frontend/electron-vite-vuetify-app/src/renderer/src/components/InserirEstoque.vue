<script setup>
    import { createCelula } from '../utils/common';
    import { getAuthToken, setMessageSnackbar, fetchGet } from '../utils/common'
    import FormPost from '../components/FormPost.vue';

    const produtos = [];

    async function requestAllProducts(){
      try{
        const url = "http://127.0.0.1:8000/v1/produto/get_all_products/";
        const token = getAuthToken();

        const response = await fetchGet(url, token);

        if(response.status === 200){
          const responseJson = await response.json();
          responseJson.forEach((produtoObj) => {
            produtos.push(produtoObj.nome);
          });
        }else{
          setMessageSnackbar("Falha ao carregar produtos", "warning");
        }
      }catch(e){
        console.log(e);
        setMessageSnackbar("Falha ao carregar produtos", "warning");
      }
    }

    requestAllProducts();
</script>
<!-- "idProduto": "168d9d25-6ce7-4904-8f42-cbdeee98163d",
            "quantidade": 5,
            "dataEntrada": "2023-10-01",
            "dataVencimento": "2024-06-01",
            "observacoes": "Mercadoria adquirida por meio de brinde" -->
<template>
  <FormPost
    title="Inserir Estoque"
    url="http://127.0.0.1:8000/v1/estoque/create_stock_registre/"
    :configs="[
        [createCelula('idProduto', 'Produto', 'select', true), createCelula('quantidade', 'Quantidade', 'number', true)],
        [createCelula('dataEntrada', 'Data de Entrada', 'date', true), createCelula('dataVencimento', 'Data de Vencimento', 'date')],
        [createCelula('observacoes', 'Observações', 'text')],
    ]"
    :fixies="[
        ['Produto.items', produtos],
        ['Produto.obj.value', 'Açaí'],
    ]"
    btnText="Inserir"
    btnIcon="mdi-plus-circle"
    successMessage="Estoque inserido com sucesso"
    errorMessage="Falha ao inserir estoque"
  />
</template>
<style scoped>
</style>
