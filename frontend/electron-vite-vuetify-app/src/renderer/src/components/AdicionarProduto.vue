<script setup>
  import { ref, reactive } from 'vue';
  import { createCelula, getAuthToken, setMessageSnackbar, fetchPost } from '../utils/common';
  import CardForm from '../components/CardForm.vue';

  const props = defineProps(['categorias']);
  const emit = defineEmits(['produtoAdicionado']);

  const isVisible = reactive({
    dialogAdicionarProduto: false,
  });

  const eventFunctions = {
    fechar: () => isVisible.dialogAdicionarProduto = false,
    adicionar: (body) => emitProdutoAdicionado(body),
  };

  const customBtns = ref([
    {text: 'Fechar', variant: 'text', icon: undefined, color: undefined, clickEvent: 'fechar', needFormData: false, loading: false},
    {text: 'Adicionar', variant: 'flat', icon: 'mdi-package-variant-plus', color: 'blue-darken-1', clickEvent: 'adicionar', needFormData: true, loading: false},
  ]);
  const adicionarBtn = customBtns.value[1];

  async function emitProdutoAdicionado(body){
    adicionarBtn.loading = true;

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

    adicionarBtn.loading = false;
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
          [createCelula({key:'nome', title: 'Nome', required: true}), createCelula({key:'descricao', title: 'Descrição'})],
          [createCelula({key:'categoria', title: 'Categoria', type: 'select', required: true, initialValue: props.categorias.length > 0 ? categorias[0].idCategoria : ''}), createCelula({key:'valorVenda', title: 'Valor de Venda', type: 'number', required: true})],
        ]"
        :fixies="[ 
            ['Categoria.items', props.categorias],
            ['Categoria.itemsTitle', 'nome'],
            ['Categoria.itemsValue', 'idCategoria'],
        ]"
        :customBtns="customBtns"
        @clicked="btnClicked"
      />
  </v-dialog>
</template>

<style scoped>
</style>
