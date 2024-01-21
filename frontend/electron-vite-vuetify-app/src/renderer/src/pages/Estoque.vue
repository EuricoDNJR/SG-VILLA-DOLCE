<script setup>
  import { ref, computed, watch, onMounted } from 'vue'
  import { fetchGet, fetchDelete, confirmDialog, getFormatedDate } from '../utils/common';
  import { useAuthStore, useFormStore, useSnackbarStore } from '../utils/store';
  import Snackbar from '../components/Snackbar.vue';
  import InserirEstoque from '../components/InserirEstoque.vue';

  defineOptions({
    inheritAttrs: false
  });

  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore();
  const formStore = useFormStore();

  const recieve = computed(() => formStore.getObj);

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
 
  async function requestAllStockRegistres(){
    try{
      const url = "http://127.0.0.1:8000/v1/estoque/get_all_stock_registres/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){
        entradas.value = responseJson;
      }else if(response.status != 204){
        snackbarStore.set(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set("Falha ao carregar estoque", 'warning');
    }
  }
  
  async function requestDelete(estoque){
    try{
        const url = "http://127.0.0.1:8000/v1/estoque/delete_stock_registre/" + `${estoque.idEstoque}/`;
        const token = authStore.getToken;
        const response = await fetchDelete(url, token);
        const responseJson = await response.json();

        if(response.status === 200){
          entradas.value = entradas.value.filter((stock) => stock.idEstoque != estoque.idEstoque);

          snackbarStore.set("Produto removido com sucesso", 'success');
        }else{
          snackbarStore.set(responseJson.message, 'warning');
        }
    }catch(e){
        console.log(e);
        snackbarStore.set("Erro ao remover produto", 'warning');
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

  onMounted(() => {
    requestAllStockRegistres();;
  });

  watch(recieve, (newRecieve, oldRecive) => {
    if(formStore.getFrom == "Inserir Estoque"){
      const estoque = {
        idEstoque: formStore.getObj.uuid,
        idProduto: formStore.getObj.idProduto,
        nome: formStore.getObj.Nome,
        observacoes: formStore.getObj.observacoes,
        dataEntrada: formStore.getObj.dataEntrada,
        dataVencimento: formStore.getObj.dataVencimento,
        quantidade: formStore.getObj.quantidade
      };

      entradas.value.push(estoque);
    }
  });

</script>

<template>
    <Snackbar/>
  
    <v-app-bar  color="deep-purple" :elevation="2" density="compact">
      <v-app-bar-title>Estoque</v-app-bar-title>

      <template v-slot:prepend>
        <v-icon>mdi-menu-right</v-icon>
      </template>

      <InserirEstoque/>
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
            @input=""
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