<script setup>
  import { ref, reactive } from 'vue';
  import { createCelula, getAuthToken, setMessageSnackbar, fetchDelete } from '../utils/common';
  import CardForm from '../components/CardForm.vue';

  const props = defineProps(['categorias']);
  const emit = defineEmits(['categoriaApagada']);

  const reloadVar = ref(false);

  const isVisible = reactive({
    dialogCategoriaApagada: false,
  });
  const loadingBtn = reactive({
    categoriaApagada: false,
  });

  async function emitCategoriaApagada(body){
    loadingBtn.categoriaApagada = true;

    try{
      const url = `http://127.0.0.1:8000/v1/categoria/delete_category/${body.idCategoria}/`;
      const token = getAuthToken();
      
      const response = await fetchDelete(url, token);
      const responseJson = await response.json();

      if(response.status === 200){     
        emit('categoriaApagada', body);
        
        reload();

        setMessageSnackbar("Categoria apagada com sucesso", 'success');
      }else{
        setMessageSnackbar(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao apagar categoria", 'warning');
    }        

    loadingBtn.categoriaApagada = false;
  }

  function reload(){
    reloadVar.value = !reloadVar.value;
  }
</script>

<template>
  <v-dialog
    v-model="isVisible.dialogCategoriaApagada"
    persistent
    width="384"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        stacked
        variant="text"
        prepend-icon="mdi-book-minus-outline"
        v-bind="props"
      >
        Apagar Categoria
      </v-btn>
    </template>
    
    <CardForm :key="reloadVar"
      title="Apagar Categoria"
      :configs="[
          [createCelula('idCategoria', 'Categoria', 'autocomplete', true)],
      ]"
      :fixies="[ 
          ['Categoria.items', props.categorias],
          ['Categoria.itemsTitle', 'nome'],
          ['Categoria.itemsValue', 'idCategoria'],
          ['Categoria.obj.value', ''],
      ]"
      btnText="Apagar"
      btnIcon="mdi-book-minus-outline"
      btnColor="red-darken-1"
      :loading="loadingBtn.categoriaApagada"
      @submit="emitCategoriaApagada"
      @close="isVisible.dialogCategoriaApagada = false"
    />
  </v-dialog>
</template>
<style scoped>
</style>
