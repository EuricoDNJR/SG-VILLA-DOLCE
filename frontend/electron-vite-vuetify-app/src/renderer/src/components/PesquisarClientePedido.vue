<script setup>
  import { ref, watch } from 'vue'
  import { fetchGet } from '../utils/common';
  import { useAuthStore, useSnackbarStore } from '../utils/store';

  const props = defineProps(['telefoneCliente', 'readonly'])
  const emit = defineEmits(['clienteAtualizado']);

  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore()

  const clientes = ref([{nome:'', telefone:''}]);
  const cliente = ref(clientes.value[0]);
  
  async function requestAllClientes(){
    try{
      const url = "http://127.0.0.1:8000/v1/cliente/get_all_clients/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){
        clientes.value = responseJson;

        cliente.value = clientes.value.find((cliente) => cliente.telefone == props.telefoneCliente);
      }else{
        snackbarStore.set(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set(`Falha ao carregar`, 'warning');
    }
  }

  function itemProps(item){
    return {
      title: item.nome,
      subtitle: `Telefone: ${item.telefone}`,
    };
  }

  watch(cliente, async (newValue, oldValue) => {
    emit('clienteAtualizado', cliente.value);
  });

  requestAllClientes();
</script>

<template>
  <v-autocomplete
    v-model="cliente"
    label="Cliente"
    :items="clientes"
    :item-props="itemProps"
    :hint="`Telefone: ${cliente.telefone}`"
    return-object
    persistent-hint
    variant="outlined"
    hide-details="auto"
    :readonly="props.readonly"
  ></v-autocomplete>
</template>

<style scoped>
</style>