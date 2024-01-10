<script setup>
  import Snackbar from '../components/Snackbar.vue';
  import Pessoas from '../components/Pessoas.vue';
  
  defineOptions({
    inheritAttrs: false
  });
</script>

<template>
    <Snackbar/>

    <Pessoas 
      tipoPessoa="Clientes"
      urlGetAllPessoas="http://127.0.0.1:8000/v1/cliente/get_all_clients/"
      rotaUpdatePessoa="http://127.0.0.1:8000/v1/cliente/update_cliente/"
      rotaDeletePessoa="http://127.0.0.1:8000/v1/cliente/delete_cliente/"
      urlRegisterPessoa="http://127.0.0.1:8000/v1/cliente/create_client/"
    />
</template>

<style scoped>
</style>
