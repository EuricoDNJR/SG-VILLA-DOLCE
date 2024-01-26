<script setup>
  import { ref, computed, reactive } from 'vue'
  import PessoaInfo from '../components/PessoaInfo.vue';
  import CadastrarPessoa from '../components/CadastrarPessoa.vue';
  
  defineOptions({
    inheritAttrs: false
  });

  const props = defineProps(['title', 'pessoas', 'registerTitle', 'loadingBtnRegister', 'configs', 'fixies']);
  const emit = defineEmits(['cadastrarPessoa', 'removerPessoa']);

  const pessoasFiltered = computed(() => props.pessoas.filter((pessoa) => {
      const searchByName = pessoa.nome.toLowerCase().includes(searchText.value.toLowerCase());const searchByPhone = pessoa.telefone.toLowerCase().includes(searchText.value.toLowerCase());
      
      return searchByName || searchByPhone;
    }
  ));
  
  const searchText = ref('');
  const pessoaInfoIndex = ref(-1);

  const reload = reactive({
    pessoaInfo: false,
  });

  function emitCadastrarPessoa(body){
    emit('cadastrarPessoa', body);
  }

  function emitAtualizarPessoa(){
    reload.pessoaInfo = !reload.pessoaInfo;
  }

  function emitRemoverPessoa(pessoa){
    emit('removerPessoa', pessoa);

    closePessoaInfo();
  }

  function closePessoaInfo(){
    pessoaInfoIndex.value = -1;
  }

  // watch(pessoas, async (newPessoas, oldPessoas) => {
  //   const pessoasOrdemAlfabetica = pessoas.value.sort((pessoaA, pessoaB) => pessoaA.nome.localeCompare(pessoaB.nome));
    
  //   updatePessoasFiltered(pessoasOrdemAlfabetica);
  // });
  
  // watch(pessoaWasUpdated, async (newValue, oldValue) => {
  //   const pessoaUpdate = pessoas.value.find((pessoa) => pessoaStore.getId(pessoa) == pessoaStore.idPessoa);
  //   const index = pessoas.value.indexOf(pessoaUpdate);
    
  //   for(let attr in pessoaStore.getInfoChange){
  //     pessoas.value[index][attr] = pessoaStore.getInfoChange[attr];
  //   }
  // });
  
  // watch(pessoaWasDeleted, async (newId, oldId) => {
  //   pessoas.value = pessoas.value.filter((pessoa) => pessoaStore.getId(pessoa) !== pessoaStore.idPessoa);

  //   closePessoaInfo();
  // });

  // watch(pessoaWasCreated, async (newValue, oldValue) => {
  //   const pessoa = {};
  //   const newPessoas = [...pessoas.value];

  //   for(let attr in pessoaStore.getPessoa){
  //     pessoa[attr] = pessoaStore.getPessoa[attr];
  //   }

  //   newPessoas.push(pessoa);

  //   pessoas.value = newPessoas;

  //   closePessoaInfo();
  // });
</script>

<template>  
    <v-toolbar color="grey-lighten-4" class="pa-4">
      <v-row align="center">
        <v-col>
          <v-toolbar-title class="text-uppercase">
            <span class="font-weight-bold">{{ props.title }}</span>
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
          ></v-text-field>
        </v-col>

        <v-col cols="auto">
          <CadastrarPessoa
            :title="props.registerTitle"
            :loadingBtn = "props.loadingBtnRegister"
            :configs="props.configs"
            :fixies="props.fixies"
            @cadastrarPessoa="emitCadastrarPessoa"
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
            <div :key="reload.pessoaInfo">
              <PessoaInfo
                :pessoa="pessoa"
                @atualizarPessoa="emitAtualizarPessoa"
                @removerPessoa="emitRemoverPessoa"
              />
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>
    </v-expansion-panels>
</template>

<style scoped>
</style>
