<script setup>
  import { ref, computed } from 'vue'
  import scrollIntoView from 'scroll-into-view-if-needed'
  import PessoaInfo from '../components/PessoaInfo.vue';
  import CadastrarPessoa from '../components/CadastrarPessoa.vue';
  
  defineOptions({
    inheritAttrs: false
  });

  const props = defineProps(['title', 'pessoas', 'registerTitle', 'loadingBtnRegister', 
                'configsRegister', 'fixiesRegister', 'loadingCardUpdate', 'reloadPessoaInfo', 'configsPessoaInfo', 'fixiesPessoaInfo']);
  const emit = defineEmits(['cadastrarPessoa', 'removerPessoa', 'atualizarPessoa']);

  const pessoasFiltered = computed(() => props.pessoas.filter((pessoa) => {
      const searchByName = pessoa.nome.toLowerCase().includes(searchText.value.toLowerCase());const searchByPhone = pessoa.telefone.toLowerCase().includes(searchText.value.toLowerCase());
      
      return searchByName || searchByPhone;
    }
  ));
  
  const searchText = ref('');
  const pessoaInfoIndex = ref(-1);


  function emitCadastrarPessoa(body){
    emit('cadastrarPessoa', body);
  }

  function emitAtualizarPessoa(pessoa, infosChange){
    emit('atualizarPessoa', pessoa, infosChange);
  }

  function emitRemoverPessoa(pessoa){
    emit('removerPessoa', pessoa);

    closePessoaInfo();
  }

  function closePessoaInfo(){
    pessoaInfoIndex.value = -1;
  }

  function scrollTo(id){
    const node = document.getElementById(id);

    setTimeout(() => {
      scrollIntoView(node, {
        scrollMode: 'if-needed',
        behavior: 'smooth',
        block: 'center',
        
      })
    }, 140); 
  }
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
            :configs="props.configsRegister"
            :fixies="props.fixiesRegister"
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
          v-for="(pessoa, i) in pessoasFiltered" :key="i" :id="i" @click="() => scrollTo(i)"
        >
          <v-expansion-panel-title expand-icon="mdi-menu-down">
            <v-row>
              <v-col><v-icon>mdi-account</v-icon> {{ pessoa.nome }}</v-col>
              <v-col><v-icon>mdi-cellphone</v-icon> Telefone: {{ pessoa.telefone }}</v-col>
            </v-row>
          </v-expansion-panel-title>

          <v-expansion-panel-text>
            <div :key="props.reloadPessoaInfo">
              <PessoaInfo
                :pessoa="pessoa"
                :configs="props.configsPessoaInfo"
                :fixies="props.fixiesPessoaInfo"
                @atualizarPessoa="emitAtualizarPessoa"
                @removerPessoa="emitRemoverPessoa"
                :loadingCardUpdate="props.loadingCardUpdate"
              />
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>
    </v-expansion-panels>
</template>

<style scoped>
</style>
