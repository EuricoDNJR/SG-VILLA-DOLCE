<script setup>
  import { ref, onMounted } from 'vue'
  import { fetchGet, fetchDelete, getAuthToken, setMessageSnackbar, confirmDialog, getColorQuantidade } from '../utils/common';
  import Snackbar from '../components/Snackbar.vue';
  import CriarCategoria from '../components/CriarCategoria.vue';
  import ApagarCategoria from '../components/ApagarCategoria.vue';
  import AdicionarProduto from '../components/AdicionarProduto.vue';

  defineOptions({
    inheritAttrs: false
  });

  const headers = [
    { title: 'Nome', key: 'nome', width: '20%' },
    { title: 'Descrição', key: 'descricao', width: '20%'},
    { title: 'Quantidade', key: 'quantidade' },
    { title: 'Categoria', key: 'categoria' },
    { title: 'Valor de Venda', key: 'valorVenda' },
    { title: 'Unidade de Medida', key: 'unidadeMedida' },
    { title: 'Ações', key: 'acoes'},
  ];

  const categorias = ref([]);
  const produtos = ref([]);
  const produtosObj = {};
  const searchText = ref('');

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

  async function requestAllProducts(){
    try{
      const url = "http://127.0.0.1:8000/v1/produto/get_all_products/"
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);
      
      if (response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          produtos.value = responseJson;

          produtos.value.forEach((produto) => {
            produtosObj[produto.idProduto] = produto;
          });
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar produtos", 'warning');
    }
  }

  async function requestDelete(produto){
    try{
        const url = "http://127.0.0.1:8000/v1/produto/delete_product/" + `${produto.idProduto}/`;
        const token = getAuthToken();
        const response = await fetchDelete(url, token);
        const responseJson = await response.json();

        if(response.status === 200){
          produtos.value = produtos.value.filter((prod) => prod.idProduto != produto.idProduto);

          setMessageSnackbar("Produto removido com sucesso", 'success');
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
    }catch(e){
        console.log(e);
        setMessageSnackbar("Erro ao remover produto", 'warning');
    }        
  }
  
  function deleteConfirmation(produto){
    confirmDialog(`Tem certeza que deseja remover ${produto.nome} do sistema?`, () => requestDelete(produto));
  }

  function adicionarProduto(obj){
    const produto = {
        idProduto: obj.uuid,
        nome: obj.nome,
        descricao: obj.descricao,
        categoria: obj.categoria,
        unidadeMedida: obj.unidadeMedida,
        valorVenda: obj.valorVenda,
        quantidade: obj.quantidade
      };

      produtos.value.push(produto);
      produtosObj[produto.idProduto] = produto;
  }

  function criarCategoria(obj){
    const categoria = {
      idCategoria: obj.uuid,
      nome: obj.nome,
      unidadeMedida: obj.unidadeMedida,
    };

    categorias.value.push(categoria);
  }

  function apagarCategoria(obj){
    console.log(obj);
    const idCategoria = obj.idCategoria;

    categorias.value = categorias.value.filter((categoria) => categoria.idCategoria != idCategoria);
  }

  onMounted(() => {
    requestAllCategories();
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
      <AdicionarProduto 
        :categorias="categorias"
        @produtoAdicionado="adicionarProduto"
      />

      <CriarCategoria
        @categoriaCriada="criarCategoria"
      />

      <ApagarCategoria
        :categorias="categorias"
        @categoriaApagada="apagarCategoria"
      />
    </v-app-bar>

    <v-toolbar color="grey-lighten-4" class="pa-4">
      <v-text-field
        v-model="searchText"
        label="Produto"
        prepend-inner-icon="mdi-magnify"
        variant="solo"
        hide-details
      ></v-text-field>
    </v-toolbar>

    <div id="tabela"
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
            {{ Number(value).toFixed(3).replace('.', ',') }}
          </v-chip>
        </template>

        <template v-slot:item.valorVenda="{ value }">
          R$ {{ Number(value).toFixed(2).replace('.', ',') }}
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