<script setup>
  import { reactive } from 'vue';
  import { createCelula, getAuthToken, setMessageSnackbar, fetchPost } from '../utils/common';
  import CardForm from '../components/CardForm.vue';

  const props = defineProps(['categorias']);
  const emit = defineEmits(['produtoAdicionado']);

  const isVisible = reactive({
    dialogAdicionarProduto: false,
  });
  const loadingBtn = reactive({
    adicionarProduto: false,
  });

  async function emitProdutoAdicionado(body){
    loadingBtn.adicionarProduto = true;

    try{
      const url = "http://127.0.0.1:8000/v1/produto/create_product/";
      const token = getAuthToken();
      
      const response = await fetchPost(url, body, token);
      const responseJson = await response.json();

      if(response.status === 201){
        Object.assign(body, responseJson);
        
        emit('produtoAdicionado', body);
        
        setMessageSnackbar("Produto adicionado com sucesso", 'success');
      }else{
        setMessageSnackbar(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao adicionar produto", 'warning');
    }        

    loadingBtn.adicionarProduto = false;
  }
</script>

<template>
  <v-dialog
    v-model="isVisible.dialogAdicionarProduto"
    persistent
    width="512"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        stacked
        variant="text"
        prepend-icon="mdi-book-plus-outline"
        v-bind="props"
      >
        Adicionar Produto
      </v-btn>
    </template>

    <CardForm
      title="Adicionar Produto"
      :configs="[
          [createCelula('nome', 'Nome', 'text', true), createCelula('descricao', 'Descrição', 'text')],
          [createCelula('categoria', 'Categoria', 'select', true), createCelula('valorVenda', 'Valor de Venda', 'number', true)],
      ]"
      :fixies="[ 
          ['Categoria.items', props.categorias],
          ['Categoria.itemsTitle', 'nome'],
          ['Categoria.itemsValue', 'idCategoria'],
          ['Categoria.obj.value', props.categorias.length > 0 ? categorias[0].idCategoria : ''],
      ]"
      btnText="Adicionar"
      btnIcon="mdi-package-variant-plus"
      btnColor="blue-darken-1"
      :loading="loadingBtn.adicionarProduto"
      @submit="emitProdutoAdicionado"
      @close="isVisible.dialogAdicionarProduto = false"
    />
  </v-dialog>
</template>

<style scoped>
</style>
