<script setup>
  import { ref, computed, watch, toRaw } from 'vue'
  import { fetchGet, fetchPost, fetchPatch, confirmDialog } from '../utils/common';
  import { useAuthStore, usePessoaStore, useSnackbarStore } from '../utils/store';
  import Snackbar from '../components/Snackbar.vue';

  defineOptions({
    inheritAttrs: false
  });

  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore();

  const searchText = ref('');
  let produtos = ref([]);
  let produtosSemIds = ref([]);

  async function requestAllStockRegistres(){ //(url=props.urlGetAllPessoas)
    try{
      const url = "http://127.0.0.1:8000/v1/estoque/get_all_stock_registres/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status === 200){
        produtos.value = await response.json();
        produtosSemIds.value = produtos.value;
        produtosSemIds.value.forEach((item) => {
          delete  item.idProduto;
          delete  item.idEstoque;
        } )
      }else{
        snackbarStore.set(`Falha ao carregar`, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set(`Falha ao carregar`, 'warning');
    }
  }

  function getColorData(data){
    console.log(data);
    const dataInicial = new Date();
    const dataFinal = new Date(data);
     // Data atual

    // Calculando a diferença em milissegundos
    const diferencaEmMilissegundos = dataFinal - dataInicial;

    // Convertendo a diferença de milissegundos para dias
    const umDiaEmMilissegundos = 1000 * 60 * 60 * 24; // 1 dia = 24 horas * 60 minutos * 60 segundos * 1000 milissegundos
    const diferencaEmDias = Math.floor(diferencaEmMilissegundos / umDiaEmMilissegundos);
    let color = undefined;
    console.log(diferencaEmDias);

    if(diferencaEmDias < 0){
      color = "black";
    }else if(diferencaEmDias < 10){
      color = "red";
    }else if(diferencaEmDias < 30){
      color = "orange";
    }else{
      color = "green";
    }

    return color;
  }

  function getColorQuantidade(quantidade){
    let color = undefined;
    
    if(quantidade < 0){
      color = "black";
    }else{
      color = "green";
    }

    return color;
  }

  requestAllStockRegistres();
</script>

<template>
    <Snackbar/>

    <v-app-bar  color="deep-purple" :elevation="2" density="compact">
        <v-btn
            @click=""
            prepend-icon="mdi-plus-circle"
            variant="text"
        >
          Inserir
        </v-btn>
        <v-btn
          @click=""
          prepend-icon="mdi-minus-circle"
          variant="text"
        >
          Retirar
        </v-btn>
        
        <v-btn 
          @click=""
          prepend-icon="mdi-package-variant-closed-plus"
          variant="text"
        >
          Adicionar Produto
        </v-btn>

        <v-btn 
          @click=""
          prepend-icon="mdi-delete"
          variant="text"
        >
          Remover Produto
        </v-btn>

        <v-btn 
          @click=""
          prepend-icon="mdi-pencil"
          variant="text"
        >
          Editar Produto
        </v-btn>

      <template v-slot:append>
        <!-- <v-btn icon="mdi-heart"></v-btn> -->

        <!-- <v-btn icon="mdi-magnify"></v-btn>

        <v-btn icon="mdi-dots-vertical"></v-btn> -->
      </template>
    </v-app-bar>

    <v-toolbar color="grey-lighten-5" class="pa-4">
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
      color="grey-lighten-5"
    >
      <v-data-table-virtual
        :items="produtosSemIds"
        :search="searchText"
        hide-no-data
        hover
        class="elevation-2 rounded"
      >
        <template v-slot:item.dataVencimento="{ value }">
          <v-chip :color="getColorData(value)">
            {{ value }}
          </v-chip>
        </template>

        <template v-slot:item.quantidade="{ value }">
          <v-chip :color="getColorQuantidade(value)">
            {{ value }}
          </v-chip>
        </template>
      </v-data-table-virtual>
    </div>
    
</template>

<style scoped>
</style>