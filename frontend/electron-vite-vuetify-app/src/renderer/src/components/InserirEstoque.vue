<script setup>
  import { reactive } from 'vue';
  import { createCelula, getAuthToken, setMessageSnackbar, fetchPost } from '../utils/common';
  import CardForm from '../components/CardForm.vue';

  const props = defineProps(['produtos']);
  const emit = defineEmits(['estoqueInserido']);

  const isVisible = reactive({
    dialogInserirEstoque: false,
  });
  const loadingBtn = reactive({
    inserirEstoque: false,
  });

  async function emitEstoqueInserido(body){
    loadingBtn.inserirEstoque = true;

    try{
      const url = "http://127.0.0.1:8000/v1/estoque/create_stock_registre/";
      const token = getAuthToken();
      
      const response = await fetchPost(url, body, token);
      const responseJson = await response.json();

      if(response.status === 201){
        Object.assign(body, responseJson);
        
        emit('estoqueInserido', body);
        
        setMessageSnackbar("Estoque inserido com sucesso", 'success');
      }else{
        setMessageSnackbar(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao inserir estoque", 'warning');
    }        

    loadingBtn.inserirEstoque = false;
  }
</script>

<template>
  <v-dialog
    v-model="isVisible.dialogInserirEstoque"
    persistent
    width="512"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        stacked
        variant="text"
        prepend-icon="mdi-plus-minus-box"
        v-bind="props"
      >
        Inserir Estoque
      </v-btn>
    </template>

    <CardForm
      title="Inserir Estoque"
      :configs="[
          [createCelula('idProduto', 'Produto', 'select', true), createCelula('quantidade', 'Quantidade', 'number', true)],
          [createCelula('dataEntrada', 'Data de Entrada', 'date', true), createCelula('dataVencimento', 'Data de Vencimento', 'date')],
          [createCelula('observacoes', 'Observações', 'text')],
      ]"
      :fixies="[
          ['Produto.items', props.produtos],
          ['Produto.itemsTitle', 'nome'],
          ['Produto.itemsValue', 'idProduto'],
          ['Produto.obj.value', props.produtos.length > 0 ? props.produtos[0].idProduto : ''],
      ]"
      btnText="Inserir"
      btnIcon="mdi-plus-minus-box"
      btnColor="blue-darken-1"
      :loading="loadingBtn.inserirEstoque"
      @submit="emitEstoqueInserido"
      @close="isVisible.dialogInserirEstoque = false"
    />
  </v-dialog>
</template>

<style scoped>
</style>
