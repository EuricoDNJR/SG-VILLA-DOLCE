<script setup>
  import { ref, computed, watch, toRaw } from 'vue'
  import { useAuthStore, usePessoaStore, useSnackbarStore } from '../utils/store';
  import { fetchGet } from '../utils/common';
  import Snackbar from '../components/Snackbar.vue';
  import PessoaInfo from '../components/PessoaInfo.vue';
  import CadastrarPessoa from '../components/CadastrarPessoa.vue';
  
  defineOptions({
    inheritAttrs: false
  });

  const props = defineProps(['tipoPessoa', 
                          'urlGetAllPessoas', 
                          'rotaUpdatePessoa',
                          'rotaDeletePessoa',
                          'urlRegisterPessoa']);

  const authStore = useAuthStore();
  const pessoaStore = usePessoaStore();
  const snackbarStore = useSnackbarStore();
  let pessoas = ref([]);
  let pessoasFiltered = ref([]);
  const searchText = ref('');
  const pessoaWasUpdated = computed(() => pessoaStore.getWasUpdated);
  const pessoaWasDeleted = computed(() => pessoaStore.getWasDeleted);
  const pessoaWasCreated = computed(() => pessoaStore.getWasCreated);
  const pessoaInfoIndex = ref(-1);

  const updatePessoasFiltered = (array) => {
    pessoasFiltered.value = array;
  }

  const requestAllPessoas = async (url=props.urlGetAllPessoas) =>{
    try{
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status === 200){
        pessoas.value = await response.json();
      }else{
        snackbarStore.set(`Falha ao carregar ${props.tipoPessoa.toLowerCase()}`, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set(`Falha ao carregar ${props.tipoPessoa.toLowerCase()}`, 'warning');
    }
  }

  const searchPessoa = () => {
    updatePessoasFiltered(pessoas.value.filter((pessoa) => pessoa.nome.toLowerCase().includes(searchText.value.toLowerCase())));
  }

  function closePessoaInfo(){
    pessoaInfoIndex.value = -1;
  }

  watch(pessoas, async (newPessoas, oldPessoas) => {
    const pessoasOrdemAlfabetica = pessoas.value.sort((pessoaA, pessoaB) => pessoaA.nome.localeCompare(pessoaB.nome));
    
    updatePessoasFiltered(pessoasOrdemAlfabetica);
  });
  
  watch(pessoaWasUpdated, async (newValue, oldValue) => {
    const pessoaUpdate = pessoas.value.find((pessoa) => pessoaStore.getId(pessoa) == pessoaStore.idPessoa);
    const index = pessoas.value.indexOf(pessoaUpdate);
    
    for(let attr in pessoaStore.getInfoChange){
      pessoas.value[index][attr] = pessoaStore.getInfoChange[attr];
    }
  });
  
  watch(pessoaWasDeleted, async (newId, oldId) => {
    pessoas.value = pessoas.value.filter((pessoa) => pessoaStore.getId(pessoa) !== pessoaStore.idPessoa);

    closePessoaInfo();
  });

  watch(pessoaWasCreated, async (newValue, oldValue) => {
    const pessoa = {};
    const newPessoas = [...pessoas.value];

    for(let attr in pessoaStore.getPessoa){
      pessoa[attr] = pessoaStore.getPessoa[attr];
    }

    newPessoas.push(pessoa);

    pessoas.value = newPessoas;

    closePessoaInfo();
  });

  requestAllPessoas();
  
</script>

<template>
    <Snackbar/>
    
    <v-toolbar color="grey-lighten-4" class="pa-4">
      <v-row align="center">
        <v-col>
          <v-toolbar-title class="text-uppercase">
            <span class="font-weight-bold">{{ props.tipoPessoa }}</span>
            <span> ({{ pessoasFiltered.length }})</span>
          </v-toolbar-title>
        </v-col>
        <v-col>
          <v-text-field
            v-model="searchText"
            label="Buscar"
            prepend-inner-icon="mdi-magnify"
            variant="solo"
            hide-details
            @input="searchPessoa"
          ></v-text-field>
        </v-col>
        <v-col cols="auto">
          <CadastrarPessoa
            :tipoPessoa="props.tipoPessoa"
            :urlRegisterPessoa="props.urlRegisterPessoa"
          />
        </v-col>
      </v-row>
    </v-toolbar>
    
    <v-expansion-panels  
        class="pa-4" 
        color="grey-lighten-4"
        v-model="pessoaInfoIndex"
      >
        <v-expansion-panel 
          v-for="(pessoa, i) in pessoasFiltered" :key="i"
        >
          <v-expansion-panel-title expand-icon="mdi-menu-down">
            <v-row>
              <v-col><v-icon>mdi-account</v-icon> {{ pessoa.nome }}</v-col>
              <v-col><v-icon>mdi-cellphone</v-icon> Telefone: {{ pessoa.telefone }}</v-col>
            </v-row>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <PessoaInfo 
              :pessoa="toRaw(pessoa)"
              :tipoPessoa="props.tipoPessoa"
              :rotaUpdatePessoa="props.rotaUpdatePessoa"
              :rotaDeletePessoa="props.rotaDeletePessoa"
            />
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
</template>

<style scoped>
</style>
