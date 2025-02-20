<script setup>
  import { ref, onMounted } from 'vue'
  import { fetchGet, getAuthToken, setMessageSnackbar, getFormatedDate } from '../utils/common';
  import ListaProdutos from '../components/ListaProdutos.vue';

  const pedidosFechados = ref([]);
  const expanded = ref([]);
  const searchText = ref('');
  const headers = [
    { title: 'Colaborador', key: 'nomeUsuario' },
    { title: 'Cliente', key: 'nomeCliente' },
    { title: 'Telefone do Cliente', key: 'telefoneCliente' },
    { title: 'Valor Total', key: 'valorTotal' },
    { title: 'Status', key: 'status' },
    { title: 'Tipo de Pagamento', key: 'tipoPagamento' },
    { title: 'Valor Recebido', key: 'valorRecebimento'},
    { title: 'Valor Devolvido (troco)', key: 'valorDevolvido'}
  ];
  
  async function requestPedidosFechados(){
    try{
      const url = 'http://127.0.0.1:8000/v1/pedido/get_all_paid_and_canceled_orders/';
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status == 200){
          pedidosFechados.value = responseJson;
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar pedidos fechados", 'warning');
    }
  }

  function getColorStatus(status){
    let color = 'white';
    
    if(status == 'Pago'){
      color = 'green';
    }else if(status == 'Pendente'){
      color = 'yellow';
    }else if(status == 'Cancelado'){
      color = 'red';
    }

    return color;
  }

  onMounted(() => requestPedidosFechados());
</script>

<template>
    <v-toolbar color="grey-lighten-4" class="pa-4">
      <v-text-field
        v-model="searchText"
        label="Pesquisar"
        prepend-inner-icon="mdi-magnify"
        variant="solo"
        hide-details
      ></v-text-field>
    </v-toolbar>

    <div
      class="pa-4" 
      color="grey-lighten-4"
    >
      <v-data-table
        v-model:expanded="expanded"
        :headers="headers"
        :items="pedidosFechados"
        item-value="idPedido"
        :search="searchText"
        items-per-page-text="Itens por página"
        :items-per-page-options="[
          { value: 10, title: '10' },
          { value: 25, title: '25' },
          { value: 50, title: '50' },
          { value: 100, title: '100' },
          { value: pedidosFechados.length, title: 'Todos' }
        ]"
        hide-no-data
        hover
        class="elevation-2 rounded"
        show-expand
      >
        <template v-slot:expanded-row="{ columns, item }">
          <tr>
            <td :colspan="columns.length">
              <ListaProdutos
                :idPedido="item.idPedido"
              /> 
            </td>
          </tr>
        </template>

        <template v-slot:item.status="{ value }">
          <v-chip :color="getColorStatus(value)">
            {{ value }}
          </v-chip>
        </template>

        <template v-slot:item.valorTotal="{ value }">
          {{ value.replace(".", ",") }}
        </template>

        <template v-slot:item.valorRecebimento="{ value }">
          {{ value.replace(".", ",") }}
        </template>

        <template v-slot:item.valorDevolvido="{ value }">
          {{ value.replace(".", ",") }}
        </template>
      </v-data-table>
    </div>
</template>

<style scoped>
</style>
