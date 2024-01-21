<script setup>
  import { ref, computed, watch, onMounted } from 'vue'
  import { fetchGet, fetchDelete, confirmDialog, getColorQuantidade } from '../utils/common';
  import { useAuthStore, useFormStore, useSnackbarStore } from '../utils/store';
  import Snackbar from '../components/Snackbar.vue';
  import CriarCategoria from '../components/CriarCategoria.vue';
  import AdicionarProduto from '../components/AdicionarProduto.vue';
  import ApagarCategoria from '../components/ApagarCategoria.vue';

  defineOptions({
    inheritAttrs: false
  });

  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore();
  const formStore = useFormStore();
  const recieve = computed(() => formStore.getObj);

  const headers = [
    { title: 'Nome', key: 'nome', width: '20%' },
    { title: 'Descrição', key: 'descricao', width: '20%'},
    { title: 'Quantidade', key: 'quantidade' },
    { title: 'Categoria', key: 'categoria' },
    { title: 'Valor de Venda', key: 'valorVenda' },
    { title: 'Unidade de Medida', key: 'unidadeMedida' },
    { title: 'Ações', key: 'acoes'},
  ];
  const searchText = ref('');
  const produtos = ref([]);
  const produtosObj = {};

  async function requestAllProducts(){
    try{
      const url = "http://127.0.0.1:8000/v1/produto/get_all_products/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){
        produtos.value = responseJson;

        produtos.value.forEach((produto) => {
          produtosObj[produto.idProduto] = produto;
        });
      }else if(response.status != 204){
        snackbarStore.set(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set("Falha ao carregar produtos", 'warning');
    }
  }

  async function requestDelete(produto){
    try{
        const url = "http://127.0.0.1:8000/v1/produto/delete_product/" + `${produto.idProduto}/`;
        const token = authStore.getToken;
        const response = await fetchDelete(url, token);
        const responseJson = await response.json();

        if(response.status === 200){
          produtos.value = produtos.value.filter((prod) => prod.idProduto != produto.idProduto);

          snackbarStore.set("Produto removido com sucesso", 'success');
        }else{
          snackbarStore.set(responseJson.message, 'warning');
        }
    }catch(e){
        console.log(e);
        snackbarStore.set("Erro ao remover produto", 'warning');
    }        
  }
  
  function deleteConfirmation(produto){
    confirmDialog(`Tem certeza que deseja remover ${produto.nome} do sistema?`, () => requestDelete(produto));
  }

  watch(recieve, async (newRecieve, oldRecieve) => {
    if(formStore.getFrom == "Adicionar Produto"){
      const produto = {
        idProduto: formStore.getObj.uuid,
        nome: formStore.getObj.nome,
        descricao: formStore.getObj.descricao,
        categoria: formStore.getObj.categoria,
        unidadeMedida: formStore.getObj.unidadeMedida,
        valorVenda: formStore.getObj.valorVenda,
        quantidade: formStore.getObj.quantidade
      };

      produtos.value.push(produto);
      produtosObj[produto.idProduto] = produto;
    }
  });
  onMounted(() => {
    requestAllProducts();
  });

</script>

<template>
    <Snackbar/>
  
    <v-app-bar  color="deep-purple" :elevation="2" density="compact">
      <template v-slot:prepend>
        <v-icon>mdi-menu-right</v-icon>
      </template>

      <v-app-bar-title>Produtos</v-app-bar-title>

      <AdicionarProduto/>

      <CriarCategoria/>
     
      <ApagarCategoria/>
  </v-app-bar>

    <v-toolbar color="grey-lighten-4" class="pa-4">
      <v-row align="center">
        <v-col>
          <v-text-field
            v-model="searchText"
            label="Produto"
            prepend-inner-icon="mdi-magnify"
            variant="solo"
            hide-details
          ></v-text-field>
        </v-col>
      </v-row>
    </v-toolbar>

    <div
      class="pa-4" 
      color="grey-lighten-4"
    >
      <v-data-table-virtual
        :headers="headers"
        :items="produtos"
        :search="searchText"
        hide-no-data
        hover
        class="elevation-2 rounded"
        multi-line
      >
        <template v-slot:item.quantidade="{ value }">
          <v-chip :color="getColorQuantidade(value)">
            {{ value.replace('.', ',') }}
          </v-chip>
        </template>

        <template v-slot:item.valorVenda="{ value }">
          R$ {{ value.replace('.', ',') }}
        </template>

        <template v-slot:item.acoes="{ item }">
          <!-- <v-btn
            size="small"
            class="d-print-inline"
            color="primary"
            variant="text"
            @click="console.log(item);"
            icon="mdi-pencil"
          ></v-btn> -->

          <v-btn
            size="small"
            class="d-print-inline"
            color="primary"
            variant="text"
            @click="() => deleteConfirmation(item)"
            icon="mdi-delete"
          ></v-btn>
        </template>
      </v-data-table-virtual>
    </div>
    
</template>

<style scoped>
</style>