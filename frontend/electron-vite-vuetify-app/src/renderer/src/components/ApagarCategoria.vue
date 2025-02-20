<script setup>
  import { ref, reactive } from 'vue';
  import { createCelula, getAuthToken, setMessageSnackbar, fetchDelete } from '../utils/common';
  import CardForm from '../components/CardForm.vue';

  const props = defineProps(['categorias']);
  const emit = defineEmits(['categoriaApagada']);

  const reloadVar = ref(false);

  const eventFunctions = {
    fechar: () => isVisible.dialogCategoriaApagada = false,
    apagar: (body) => emitCategoriaApagada(body),
  };

  const customBtns = ref([
    {text: 'Fechar', variant: 'text', icon: undefined, color: undefined, clickEvent: 'fechar', needFormData: false, loading: false},
    {text: 'Apagar', variant: 'flat', icon: 'mdi-book-minus-outline', color: 'red-darken-1', clickEvent: 'apagar', needFormData: true, loading: false},
  ]);
  const apagarBtn = customBtns.value[1];

  const isVisible = reactive({
    dialogCategoriaApagada: false,
  });

  async function emitCategoriaApagada(body){
    apagarBtn.loading = true;

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

    apagarBtn.loading = false;
  }

  function reload(){
    reloadVar.value = !reloadVar.value;
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
    
    <div :key="reloadVar">
      <CardForm
        title="Apagar Categoria"
        :configs="[
          [createCelula({key: 'idCategoria', title: 'Categoria', type: 'autocomplete', required: true})],
        ]"
        :fixies="[ 
          ['Categoria.items', props.categorias],
          ['Categoria.itemsTitle', 'nome'],
          ['Categoria.itemsValue', 'idCategoria'],
        ]"
        :customBtns="customBtns"
        @clicked="btnClicked"
      />
    </div>
  </v-dialog>
</template>
<style scoped>
</style>
