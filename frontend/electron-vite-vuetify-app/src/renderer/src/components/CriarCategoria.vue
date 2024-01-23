<script setup>
  import { createCelula } from '../utils/common';
  import FormPost from '../components/FormPost.vue';

  const emit = defineEmits(['categoriaCriada']);

  function emitCategoriaCriada(){
    emit('categoriaCriada');
  }
</script>

<template>
  <FormPost
    title="Criar Categoria"
    url="http://127.0.0.1:8000/v1/categoria/create_category/"
    :configs="[
        [createCelula('nome', 'Nome', 'text', true), createCelula('unidadeMedida', 'Unidade de Medida', 'select', true)],
    ]"
    :fixies="[
        ['Unidade de Medida.items', ['UND', 'KG']],
        ['Unidade de Medida.obj.value', 'UND'],
    ]"
    btnText="Criar"
    btnIcon="mdi-book-plus-outline"
    successMessage="Categoria criada com sucesso"
    errorMessage="Falha ao criar categoria"
    @postRequested="emitCategoriaCriada"
  />
</template>

<style scoped>
</style>
