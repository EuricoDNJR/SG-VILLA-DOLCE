<script setup>
  import { ref, reactive } from 'vue';
  import { createCelula, getAuthToken, setMessageSnackbar, fetchPost } from '../utils/common';
  import CardForm from '../components/CardForm.vue';

  const props = defineProps(['produtos']);
  const emit = defineEmits(['estoqueInserido']);

  const isVisible = reactive({
    dialogInserirEstoque: false,
  });

  const eventFunctions = {
    fechar: () => isVisible.dialogInserirEstoque = false,
    inserir: (body) => emitEstoqueInserido(body),
  };

  const customBtns = ref([
    {text: 'Fechar', variant: 'text', icon: undefined, color: undefined, clickEvent: 'fechar', needFormData: false, loading: false},
    {text: 'Inserir', variant: 'flat', icon: 'mdi-plus-minus-box', color: 'blue-darken-1', clickEvent: 'inserir', needFormData: true, loading: false},
  ]);
  const inserirBtn = customBtns.value[1];

  async function emitEstoqueInserido(body){
    inserirBtn.loading = true;

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

    inserirBtn.loading = false;
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
          [createCelula({key: 'idProduto', title: 'Produto', type: 'select', required: true, initialValue: props.produtos.length > 0 ? props.produtos[0].idProduto : ''}), createCelula({key: 'quantidade', title: 'Quantidade', type: 'number', required: true})],
          [createCelula({key: 'dataEntrada', title: 'Data de Entrada', type: 'date', required: true}), createCelula({key: 'dataVencimento', title: 'Data de Vencimento', type: 'date'})],
          [createCelula({key: 'observacoes', title: 'Observações'})],
        ]"
        :fixies="[
            ['Produto.items', props.produtos],
            ['Produto.itemsTitle', 'nome'],
            ['Produto.itemsValue', 'idProduto'],
        ]"
        :customBtns="customBtns"
        @clicked="btnClicked"
      />
  </v-dialog>
</template>

<style scoped>
</style>
