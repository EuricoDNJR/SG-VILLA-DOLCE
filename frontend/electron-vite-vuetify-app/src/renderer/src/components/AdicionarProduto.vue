<script setup>
  import { ref, computed, watch } from 'vue'
    import { createCelula } from '../utils/common';
    import { getAuthToken, setMessageSnackbar, fetchGet } from '../utils/common'
    import { useFormStore } from '../utils/store';
    import FormPost from '../components/FormPost.vue';

    const formStore = useFormStore();
    const recieve = computed(() => formStore.getObj); 
    let categorias = undefined;
    const loading = ref(true);

    async function requestAllCategories(){
      try{
        const url = "http://127.0.0.1:8000/v1/categoria/get_all_categories/";
        const token = getAuthToken();

        const response = await fetchGet(url, token);
        if (response.status != 204){
          const responseJson = await response.json();
          if(response.status === 200){
            categorias = responseJson;

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

    function reload(callback){
      loading.value = true;

      setTimeout(() => {
        callback();

        loading.value = false;
      }, 0);
    }

    watch(recieve, async (newRecieve, oldRecieve) => {
      reload(() => {
        if(formStore.getFrom == "Apagar Categoria"){
          const idCategoria = formStore.getObj.idCategoria;

          categorias = categorias.filter((categoria) => categoria.idCategoria != idCategoria);

        }else if(formStore.getFrom == "Criar Categoria"){
          const categoria = {
            idCategoria: formStore.getObj.uuid,
            nome: formStore.getObj.nome,
            unidadeMedida: formStore.getObj.unidadeMedida,
          }
          categorias.push(categoria);
        }
      });
    });

    requestAllCategories();
</script>

<template>
  <FormPost v-if="!loading"
    title="Adicionar Produto"
    url="http://127.0.0.1:8000/v1/produto/create_product/"
    :configs="[
        [createCelula('nome', 'Nome', 'text', true), createCelula('descricao', 'Descrição', 'text')],
        [createCelula('categoria', 'Categoria', 'select', true), createCelula('valorVenda', 'Valor de Venda', 'number', true)],
    ]"
    :fixies="[
        ['Categoria.items', categorias],
        ['Categoria.itemsTitle', 'nome'],
        ['Categoria.itemsValue', 'idCategoria'],
        ['Categoria.obj.value', categorias[0].idCategoria],
    ]"
    btnText="Adicionar"
    btnIcon="mdi-package-variant-plus"
    successMessage="Produto adicionado com sucesso"
    errorMessage="Falha ao adicionar produto"
  />
</template>
<style scoped>
</style>
