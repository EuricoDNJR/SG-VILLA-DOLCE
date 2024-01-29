<script setup>
  import { ref, reactive } from 'vue';
  import { createCelula, getAuthToken, setMessageSnackbar, fetchPost } from '../utils/common';
  import CardForm from '../components/CardForm.vue';

  const emit = defineEmits(['categoriaCriada']);

  const isVisible = reactive({
    dialogCriarCategoria: false,
  });

  const eventFunctions = {
    fechar: () => isVisible.dialogCriarCategoria = false,
    criar: (body) => emitCategoriaCriada(body),
  };

  const customBtns = ref([
    {text: 'Fechar', variant: 'text', icon: undefined, color: undefined, clickEvent: 'fechar', needFormData: false, loading: false},
    {text: 'Criar', variant: 'flat', icon: 'mdi-book-plus-outline', color: 'blue-darken-1', clickEvent: 'criar', needFormData: true, loading: false},
  ]);
  const criarBtn = customBtns.value[1];

  async function emitCategoriaCriada(body){
    criarBtn.loading = true;

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

    criarBtn.loading = false;
  }

  function btnClicked({event, body}){
    const func = eventFunctions[event];

    if(body){
        func(body);
    }else{
        func();
    }   
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
          [createCelula({key: 'nome', title: 'Nome', required: true}), createCelula({key: 'unidadeMedida', title: 'Unidade de Medida', type: 'select', required: true, initialValue: 'UND'})],
        ]"
        :fixies="[
          ['Unidade de Medida.items', ['UND', 'KG']],
        ]"
        :customBtns="customBtns"
        @clicked="btnClicked"
      />
  </v-dialog>
</template>

<style scoped>
</style>
