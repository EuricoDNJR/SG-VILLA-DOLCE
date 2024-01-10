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
  const produtos = ref([]);
  const produtosSemIds = ref([]);
  const clientes = ref([]);

  async function requestAllStockRegistres(){ //(url=props.urlGetAllPessoas)
    try{
      const url = "http://127.0.0.1:8000/v1/estoque/get_all_stock_registres/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status === 200){
        produtos.value = await response.json();
        produtosSemIds.value = [...toRaw(produtos.value)];
        produtosSemIds.value.forEach((item) => {
          delete  item.idProduto;
          delete  item.idEstoque;
        } )
        console.log(produtos.value);
      }else{
        snackbarStore.set(`Falha ao carregar`, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set(`Falha ao carregar`, 'warning');
    }
  }
  
  async function requestAllClientes(){ //(url=props.urlGetAllPessoas)
    try{
      const url = "http://127.0.0.1:8000/v1/cliente/get_all_clients/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status === 200){
        clientes.value = await response.json();
        clientes.value.forEach((cliente) => {
          cliente.autocomplete = `${cliente.nome}  (Telefone: ${cliente.telefone})`;
        });
      }else{
        snackbarStore.set(`Falha ao carregar`, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set(`Falha ao carregar`, 'warning');
    }
  }

  function getColorData(data){
    const dataInicial = new Date();
    const dataFinal = new Date(data);
     // Data atual

    // Calculando a diferença em milissegundos
    const diferencaEmMilissegundos = dataFinal - dataInicial;

    // Convertendo a diferença de milissegundos para dias
    const umDiaEmMilissegundos = 1000 * 60 * 60 * 24; // 1 dia = 24 horas * 60 minutos * 60 segundos * 1000 milissegundos
    const diferencaEmDias = Math.floor(diferencaEmMilissegundos / umDiaEmMilissegundos);
    let color = undefined;

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
  requestAllClientes();
</script>

<template>
    <Snackbar/>
  
    <v-app-bar  color="deep-purple" :elevation="2" density="compact">
      <template v-slot:prepend>
        <!-- <v-app-bar-nav-icon></v-app-bar-nav-icon> -->
        <v-icon>mdi-menu-right</v-icon>
      </template>

      <!-- <v-app-bar-title>Estoque</v-app-bar-title> -->

      <!-- <v-spacer></v-spacer> -->
      <v-btn
          @click=""
          prepend-icon="mdi-plus-circle"
          stacked
      >
        Inserir
      </v-btn>
      <v-btn
        @click=""
        prepend-icon="mdi-minus-circle"
        stacked
        
      >
        Retirar
      </v-btn>
      
      <v-btn 
        @click=""
        prepend-icon="mdi-package-variant-closed-plus"
        variant="text"
        stacked
      >
        Adicionar Produto
      </v-btn>

      <v-btn 
        @click=""
        prepend-icon="mdi-delete"
        variant="text"
        stacked
      >
        Remover Produto
      </v-btn>

      <v-btn 
        @click=""
        prepend-icon="mdi-pencil"
        variant="text"
        stacked
      >
        Editar Produto
      </v-btn>
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

        <v-col>
          <v-autocomplete
            label="Autocomplete"
            :items="clientes"
            
            item-title="autocomplete"
            item-value="nome"
          ></v-autocomplete>
        </v-col>
      </v-row>
    </v-toolbar>

    <div
      class="pa-4" 
      color="grey-lighten-4"
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