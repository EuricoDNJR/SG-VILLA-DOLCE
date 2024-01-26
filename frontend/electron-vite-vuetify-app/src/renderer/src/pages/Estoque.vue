<script setup>
  import { ref, onMounted } from 'vue'
  import { fetchGet, fetchDelete, getAuthToken, setMessageSnackbar, confirmDialog, getFormatedDate } from '../utils/common';
  import Snackbar from '../components/Snackbar.vue';
  import InserirEstoque from '../components/InserirEstoque.vue';

  defineOptions({
    inheritAttrs: false
  });

  const searchText = ref('');
  const headers = [
    { title: 'Nome', key: 'nome' },
    { title: 'Quantidade', key: 'quantidade' },
    { title: 'Data de Entrada', key: 'dataEntrada' },
    { title: 'Data de Vencimento', key: 'dataVencimento' },
    { title: 'Observações', key: 'observacoes' },
    { title: 'Ações', key: 'acoes'},
  ];
  const entradas = ref([]);
  const produtos = ref([]);
 
  async function requestAllStockRegistres(){
    try{
      const url = "http://127.0.0.1:8000/v1/estoque/get_all_stock_registres/"
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          entradas.value = responseJson;
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar estoque", 'warning');
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
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar produtos", 'warning');
    }
  }
  
  async function requestDelete(estoque){
    try{
        const url = "http://127.0.0.1:8000/v1/estoque/delete_stock_registre/" + `${estoque.idEstoque}/`;
        const token = getAuthToken();

        const response = await fetchDelete(url, token);
        const responseJson = await response.json();

        if(response.status === 200){
          entradas.value = entradas.value.filter((stock) => stock.idEstoque != estoque.idEstoque);

          setMessageSnackbar("Produto removido com sucesso", 'success');
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
    }catch(e){
        console.log(e);
        setMessageSnackbar("Erro ao remover produto", 'warning');
    }        
  }
  
  function deleteConfirmation(estoque){
    confirmDialog(`Tem certeza que deseja remover esse estoque do produto ${estoque.nome} do sistema?`, () => requestDelete(estoque));
  }

  function getColorDate(date){
    let color = "white";

    if(date){
      const dataInicial = new Date();
      const dataFinal = new Date(date);
      const diferencaEmMilissegundos = dataFinal - dataInicial;
      const umDiaEmMilissegundos = 1000 * 60 * 60 * 24; // 1 dia = 24 horas * 60 minutos * 60
      const diferencaEmDias = Math.floor(diferencaEmMilissegundos / umDiaEmMilissegundos);

      if(diferencaEmDias < 0){
        color = "black";
      }else if(diferencaEmDias < 10){
        color = "red";
      }else if(diferencaEmDias < 20){
        color = "orange";
      }else{
        color = "green";
      }
    }
  
    return color;
  }

  function inserirEstoque(obj){
    const estoque = {
      idEstoque: obj.uuid,
      idProduto: obj.idProduto,
      nome: obj.Nome,
      observacoes: obj.observacoes,
      dataEntrada: obj.dataEntrada,
      dataVencimento: obj.dataVencimento,
      quantidade: obj.quantidade
    };

    entradas.value.push(estoque);
  }

  onMounted(() => {
    requestAllProducts();
    requestAllStockRegistres();
  });
</script>

<template>
    <Snackbar/>
  
    <v-app-bar  color="deep-purple" :elevation="2" density="compact">
      <v-app-bar-title>Estoque</v-app-bar-title>

      <template v-slot:prepend>
        <v-icon>mdi-menu-right</v-icon>
      </template>

      <InserirEstoque
        :produtos="produtos"
        @estoqueInserido="inserirEstoque"
      />
    </v-app-bar>

    <v-toolbar color="grey-lighten-4" class="pa-4">
      <v-text-field
        v-model="searchText"
        label="Produto"
        prepend-inner-icon="mdi-magnify"
        variant="solo"
        hide-details
        @input=""
      ></v-text-field>
    </v-toolbar>

    <div
      class="pa-4" 
      color="grey-lighten-4"
    >
      <v-data-table-virtual
        :headers="headers"
        :items="entradas"
        :search="searchText"
        hide-no-data
        hover
        class="elevation-2 rounded"
      >
        <template v-slot:item.dataEntrada="{ value }">
          {{ getFormatedDate(value) }}
        </template>

        <template v-slot:item.dataVencimento="{ value }">
          <v-chip :color="getColorDate(value)">
            {{ getFormatedDate(value) }}
          </v-chip>
        </template>

        <template v-slot:item.quantidade="{ value }">
          {{ value.replace(".", ",") }}
        </template>

        <template v-slot:item.acoes="{ item }">
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