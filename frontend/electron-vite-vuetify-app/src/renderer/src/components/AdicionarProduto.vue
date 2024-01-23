<script setup>
  import { ref, computed, watch } from 'vue'
    import { createCelula } from '../utils/common';
    import { getAuthToken, setMessageSnackbar, fetchGet } from '../utils/common'
    import { useFormStore } from '../utils/store';
    import FormPost from '../components/FormPost.vue';

    const formStore = useFormStore();
    const recieve = computed(() => formStore.getObj); 
    const categorias = ref([]);
    const reloadVar = ref(false);

    async function requestAllCategories(){
      try{
        const url = "http://127.0.0.1:8000/v1/categoria/get_all_categories/";
        const token = getAuthToken();

        const response = await fetchGet(url, token);
        if (response.status != 204){
          const responseJson = await response.json();
          if(response.status === 200){
            categorias.value = responseJson;
          }else{
            setMessageSnackbar(responseJson.message, "warning");
          }
        }
      }catch(e){
        console.log(e);
        setMessageSnackbar("Falha ao carregar categorias", "warning");
      }
    }

    function reload(){
      reloadVar.value = !reloadVar.value;
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

        reload();
    });

    requestAllCategories();
</script>

<template>
  <div :key="reloadVar">
    <FormPost 
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
          ['Categoria.obj.value', categorias[0] ? categorias[0].idCategoria : ''],
      ]"
      btnText="Adicionar"
      btnIcon="mdi-package-variant-plus"
      successMessage="Produto adicionado com sucesso"
      errorMessage="Falha ao adicionar produto"
    />
  </div>
</template>
<style scoped>
</style>
