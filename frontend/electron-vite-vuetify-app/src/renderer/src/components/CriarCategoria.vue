<script setup>
  import { reactive } from 'vue';
  import { createCelula, getAuthToken, setMessageSnackbar, fetchPost } from '../utils/common';
  import CardForm from '../components/CardForm.vue';

  const emit = defineEmits(['categoriaCriada']);

  const isVisible = reactive({
    dialogCriarCategoria: false,
  });
  const loadingBtn = reactive({
    criarCategoria: false,
  });

  async function emitCategoriaCriada(body){
    loadingBtn.criarCategoria = true;

    try{
      const url = "http://127.0.0.1:8000/v1/categoria/create_category/";
      const token = getAuthToken();
      
      const response = await fetchPost(url, body, token);
      const responseJson = await response.json();

      if(response.status === 201){
        Object.assign(body, responseJson);
        
        emit('categoriaCriada', body);
        
        setMessageSnackbar("Categoria criada com sucesso", 'success');
      }else{
        setMessageSnackbar(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao criar categoria", 'warning');
    }        

    loadingBtn.criarCategoria = false;
  }
</script>

<template>
  <v-dialog
    v-model="isVisible.dialogCriarCategoria"
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
        Criar Categoria
      </v-btn>
    </template>

    <CardForm
      title="Criar Categoria"
      :configs="[
          [createCelula('nome', 'Nome', 'text', true), createCelula('unidadeMedida', 'Unidade de Medida', 'select', true)],
      ]"
      :fixies="[
          ['Unidade de Medida.items', ['UND', 'KG']],
          ['Unidade de Medida.obj.value', 'UND'],
      ]"
      btnText="Criar"
      btnIcon="mdi-book-plus-outline"
      btnColor="blue-darken-1"
      :loading="loadingBtn.criarCategoria"
      @submit="emitCategoriaCriada"
      @close="isVisible.dialogCriarCategoria = false"
    />
  </v-dialog>
</template>

<style scoped>
</style>
