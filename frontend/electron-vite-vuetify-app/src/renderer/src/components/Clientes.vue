<script setup>
  import { ref, reactive, computed, watch, toRaw } from 'vue'
  import { useAuthStore, usePessoaStore, useSnackbarStore } from '../utils/store';
  import { fetchGet } from '../utils/common';
  import ClientesInfo from './ClientesInfo.vue';
  import CadastrarCliente from './CadastrarCliente.vue';
  
  defineOptions({
    inheritAttrs: false
  });

  const authStore = useAuthStore();
  const pessoaStore = usePessoaStore();
  const snackbarStore = useSnackbarStore();
  let clientes = ref([]);
  let clientesFiltered = ref([]);
  const quantidadeDeClientes = ref(0);
  const searchText = ref('');
  const pessoaWasUpdated = computed(() => pessoaStore.getWasUpdated);
  const clienteIdDeleted = computed(() => pessoaStore.getIdDeleted);
  const pessoaWasCreated = computed(() => pessoaStore.getWasCreated);
  const snackbarIsVisible = ref(false);
  const snackbarText = computed(() => snackbarStore.getText);
  const snackbarMessageType = computed(() => snackbarStore.getMessageType);
  const snackbarWasActivated = computed(() => snackbarStore.getWasActivated);
  
  const updateQuantidadeDeClientes = (qtd) => {
    quantidadeDeClientes.value = qtd;
  }
  
  const updateClientesFiltered = (array) => {
    clientesFiltered.value = array;
  }

  const requestAllClientes = async () =>{
    try{
      const url = "http://127.0.0.1:8000/v1/cliente/get_all_clients/";
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status === 200){
        clientes.value = await response.json();
      }else{
        snackbarStore.set("Falha ao carregar clientes", 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set("Falha ao carregar clientes", 'warning');
    }
  }

  const searchCliente = () => {
    updateClientesFiltered(clientes.value.filter((cliente) => cliente.nome.toLowerCase().includes(searchText.value.toLowerCase())));
  }

  watch(clientes, async (newClientes, oldClientes) => {
    const clientesOrdemAlfabetica = clientes.value.sort((clienteA, clienteB) => clienteA.nome.localeCompare(clienteB.nome));

    updateClientesFiltered(clientesOrdemAlfabetica);
  });

  watch(clientesFiltered, async (newClientesFiltered, oldClientesFiltered) => {
    updateQuantidadeDeClientes(clientesFiltered.value.length);
  });
  
  watch(pessoaWasUpdated, async (newValue, oldValue) => {
    const clienteUpdate = clientes.value.find((cliente) => cliente.idCliente == pessoaStore.getPessoa.idCliente);
    const index = clientes.value.indexOf(clienteUpdate);
    
    for(let attr in pessoaStore.getInfoChange){
      clientes.value[index][attr] = pessoaStore.getInfoChange[attr];
    }
  });

  watch(clienteIdDeleted, async (newId, oldId) => {
      clientes.value = clientes.value.filter((cliente) => cliente.idCliente !== newId);
  });

  watch(snackbarWasActivated, async (newValue, oldValue) => {
    snackbarIsVisible.value = false;
    
    setTimeout(() => {
        snackbarIsVisible.value = true;
    }, 200);
  });

  watch(pessoaWasCreated, async (newValue, oldValue) => {
    const pessoa = {};
    const newClientes = [...clientes.value];

    for(let attr in pessoaStore.getPessoa){
      pessoa[attr] = pessoaStore.getPessoa[attr];
    }

    newClientes.push(pessoa);

    clientes.value = newClientes;
  });

  function closeSnackbar(){
    snackbarIsVisible.value = false;
  }

  requestAllClientes();
  
</script>

<template class="background-grey-lighten-5">
    <v-snackbar
      v-model="snackbarIsVisible"
      :timeout="5000"
      location="top"
      elevation="21"
      >
          <v-alert
          :text="snackbarText"
          :type="snackbarMessageType"
          variant="tonal"
          density="compact"
          ></v-alert>

      <template v-slot:actions>
          <v-btn
          color="blue"
          variant="text"
          @click="closeSnackbar"
          >
          Fechar
          </v-btn>
      </template>
    </v-snackbar>
    
    <v-toolbar color="grey-lighten-5" class="pa-4">
      <v-row align="center">
        <v-col>
          <v-toolbar-title class="text-uppercase">
            <span class="font-weight-bold">clientes</span>
            <span> ({{ quantidadeDeClientes }})</span>
          </v-toolbar-title>
        </v-col>
        <v-col>
          <v-text-field
            v-model="searchText"
            label="Buscar"
            prepend-inner-icon="mdi-magnify"
            variant="solo"
            hide-details
            @input="searchCliente"
          ></v-text-field>
        </v-col>
        <v-col cols="auto">
          <CadastrarCliente/>
        </v-col>
      </v-row>
    </v-toolbar>
    
    <v-expansion-panels  
        class="pa-4 background-grey-lighten-5" 
        color="grey-lighten-5"
      >
        <v-expansion-panel 
          v-for="(cliente, i) in clientesFiltered" :key="i"
        >
          <v-expansion-panel-title expand-icon="mdi-menu-down">
            <v-row>
              <v-col><v-icon>mdi-account</v-icon> {{ cliente.nome }}</v-col>
              <v-col><v-icon>mdi-cellphone</v-icon> Telefone: {{ cliente.telefone }}</v-col>
            </v-row>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <ClientesInfo :pessoa="toRaw(cliente)"/>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
</template>

<style scoped>
</style>
