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
      tipoPessoa="Colaboradores"
      urlGetAllPessoas="http://127.0.0.1:8000/v1/usuario/get_all_users/"
      rotaUpdatePessoa="http://127.0.0.1:8000/v1/usuario/update_user/"
      rotaDeletePessoa="http://127.0.0.1:8000/v1/usuario/delete_user/"
      urlRegisterPessoa="http://127.0.0.1:8000/v1/usuario/create_user/"
      tooltipText="Colaborador"
    />
</template>

<style scoped>
</style>