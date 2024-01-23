<script setup>
  import { ref, computed, watch } from 'vue'
  import { getAuthToken, setMessageSnackbar, fetchGet } from '../utils/common'
  import { useFormStore } from '../utils/store';
  import FormDelete from '../components/FormDelete.vue';

  const emit = defineEmits(['categoriaApagada']);

  function emitCategoriaApagada(){
    emit('categoriaApagada');
  }

  const formStore = useFormStore();
  const recieve = computed(() => formStore.getObj); 
  const categorias = ref(undefined);
  const loading = ref(true);

  async function requestAllCategories(){
    try{
      const url = "http://127.0.0.1:8000/v1/categoria/get_all_categories/";
      const token = getAuthToken();

      const response = await fetchGet(url, token);

        if (response.status != 204){
          const responseJson = await response.json();
          if(response.status === 200){
            categorias.value = responseJson;

            loading.value = false;
          }else{
            setMessageSnackbar(responseJson.message, "warning");
          }
        }
      }catch(e){
        console.log(e);
        setMessageSnackbar("Falha ao carregar categorias", "warning");
      }
    }

  watch(recieve, async (newRecieve, oldRecieve) => {
    if(formStore.getFrom == "Apagar Categoria"){
      const idCategoria = formStore.getObj.idCategoria;

      categorias.value = categorias.value.filter((categoria) => categoria.idCategoria != idCategoria);
    }else if(formStore.getFrom == "Criar Categoria"){
      const categoria = {
        idCategoria: formStore.getObj.uuid,
        nome: formStore.getObj.nome,
        unidadeMedida: formStore.getObj.unidadeMedida,
      }
      categorias.value.push(categoria);
    }
  });
  
  requestAllCategories();
</script>

<template>
  <FormDelete
    title="Apagar Categoria"
    :autocompleteItems="categorias"
    autocompleteTitle="nome"
    autocompleteValue="idCategoria"
    url="http://127.0.0.1:8000/v1/categoria/delete_category/"
    btnText="Apagar"
    btnIcon="mdi-book-minus-outline"
    successMessage="Categoria apagada com sucesso"
    errorMessage="Falha ao apagar categoria"
    @requested="emitCategoriaApagada"
  />
</template>
<style scoped>
</style>
