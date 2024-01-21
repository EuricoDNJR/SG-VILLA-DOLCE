<script setup>
  import { ref, computed, reactive, watchEffect, watch } from 'vue'
  import { fetchGet, getColorQuantidade } from '../utils/common';
  import { useAuthStore, useSnackbarStore, usePedidoStore } from '../utils/store';
  
  const props = defineProps(['produtoRemovido']);
  const emit = defineEmits(['produtoAdicionado']);

  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore();

  const produtoWasRemoved = computed(() => props.produtoRemovido.wasRemoved);

  const produtos = ref([]);
  const produto = reactive({
    quantidade: 0,
    valorVendaUnidade: 0,
    valorTotalProduto: computed(() => (produto.quantidade * produto.valorVendaUnidade).toFixed(2)),
    product: undefined,
  });

  const dialogIsVisible = reactive({
    adicionarProduto: false,
  });

  const searchText = ref('');
  const headers = [
    { title: 'Nome', key: 'nome', width:"40%" },
    { title: 'Quantidade', key: 'quantidade' },
    { title: 'Observações', key: 'observacoes' },
    { title: 'Ações', key: 'acoes'},
  ];


  async function requestAllProducts(){
    try{
      const url = "http://127.0.0.1:8000/v1/produto/get_all_products/"
      const token = authStore.getToken;
  
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){
        produtos.value = responseJson;
      }else{
        snackbarStore.set(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set(`Falha ao carregar`, 'warning');
    }
  }

  function selectProduto(product){
    produto.product = product;
    produto.valorVendaUnidade = Number(product.valorVenda);
  }

  function adicionarProduto(){
    if(produto.quantidade > 0){
      produto.product.quantidade = (produto.product.quantidade - produto.quantidade).toFixed(3);

      const product = {...produto.product};
      delete product.valorVenda;

      product.valorVendaUnd = produto.valorVendaUnidade.toFixed(2);
      product.quantidade = produto.quantidade.toFixed(3);
      product.desconto = "0.00";
      
      emit('produtoAdicionado', product);

      closeDialog();
    }else{
      snackbarStore.set("Quantidade inválida", 'warning');
    }
  }

  function openDialog(){
    dialogIsVisible.adicionarProduto = true;
  }

  function closeDialog(){
    dialogIsVisible.adicionarProduto = false;
    produto.quantidade = 0;
  }

  watch(produtoWasRemoved, async (newValue, oldValue) => {
     const produtoToUpdate = produtos.value.find((produto) => produto.idProduto == props.produtoRemovido.idProduto);

    if(produtoToUpdate){
      produtoToUpdate.quantidade = (Number(produtoToUpdate.quantidade) + Number(props.produtoRemovido.quantidade)).toFixed(3); 
    }
  });

  requestAllProducts();
</script>

<template>
  <v-dialog 
  v-model="dialogIsVisible.adicionarProduto"
  persistent
  width="512"
>
    <v-card>
      <v-card-title>
        <span class="text-h5">Adicionar Produto ao Pedido</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col>
              <v-text-field
                v-model.number="produto.quantidade"
                label="Quantidade"
                type="number"
                hide-details="auto"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model.number="produto.valorVendaUnidade"
                label="Valor da Unidade"
                type="number"
                hide-details="auto"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                v-model="produto.valorTotalProduto"
                label="Valor Total"
                type="number"
                hide-details="auto"
                :readonly="true"
                density="comfortable"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn   
            variant="text"
            @click="closeDialog"
          >
            Fechar
          </v-btn>
          <v-btn
            color="blue-darken-1"
            variant="flat"
            prepend-icon="mdi-plus"
            @click="adicionarProduto"
          >
            Adicionar
          </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-toolbar color="grey-lighten-4">
      <v-row align="center">
        <v-col>
          <v-text-field
            v-model="searchText"
            label="Produto"
            prepend-inner-icon="mdi-magnify"
            variant="solo"
            hide-details
          ></v-text-field>
        </v-col>
      </v-row>
  </v-toolbar>

  <v-data-table-virtual
    :headers="headers"
    :items="produtos"
    :search="searchText"
    hide-no-data
    hover
    class="elevation-2 rounded"
  >
    <template v-slot:item.quantidade="{ value }">
      <v-chip :color="getColorQuantidade(value)">
        {{ value.replace(".", ",") }}
      </v-chip>
    </template>

    <template v-slot:item.acoes="{ item }">
      <v-btn
          color="primary"
          variant="text"
          icon="mdi-plus"
          @click="() => {
            selectProduto(item);
            openDialog()
          }"
      ></v-btn>
    </template>
  </v-data-table-virtual>
</template>

<style scoped>
</style>