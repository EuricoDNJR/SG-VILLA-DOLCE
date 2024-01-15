<script setup>
  import { ref, computed, watch, onMounted, reactive } from 'vue'
  import { fetchGet, fetchDelete, confirmDialog, getFormatedDate } from '../utils/common';
  import { useAuthStore, useSnackbarStore, usePedidoStore } from '../utils/store';
  import Snackbar from '../components/Snackbar.vue';
  
  defineOptions({
    inheritAttrs: false
  });

  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore()
  const pedidoStore = usePedidoStore();  
  
  const dialogIsVisible = ref(false);

  const searchText = ref('');
  const headers = [
    { title: 'Nome', key: 'nome', width:"40%" },
    { title: 'Quantidade', key: 'quantidade' },
    { title: 'Observações', key: 'observacoes' },
    { title: 'Ações', key: 'acoes'},
  ];
  // "idProduto": "4718af40-ee5d-486f-8a8a-d1ffe3604a2a",
  //     "quantidade": 0.450,
  //     "valorVendaUnd": 40.00,
  //     "desconto": 15.00
  const idCliente = undefined;
  const Pagamento = reactive({
    valorTotal: 0,
  });
  const idCaixa = undefined;
  const idProdutos = ref([]);
  const status = "Pendente";
  const desconto = reactive({
    qtd: 0,
    value: false,
  });

  const produtos = ref([]);

  const produto = ref(undefined);
  const quantidade = ref(0);
  const valorVendaUnidade = ref(undefined);
  const valorTotalProduto = computed(() => (valorVendaUnidade.value * quantidade.value).toFixed(2));
  
  const pedido = ref([]);
  const clientes = ref([]);
  const telefoneVisitante = "00000000000";
  const cliente = ref(undefined);
  const loading = ref(true);

  async function requestAllProducts(){
    try{
      const url = "http://127.0.0.1:8000/v1/produto/get_all_products/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status === 200){
        produtos.value = await response.json();
      }else{
        snackbarStore.set(`Falha ao carregar`, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set(`Falha ao carregar`, 'warning');
    }
  }
  
  async function requestAllClientes(){
    try{
      const url = "http://127.0.0.1:8000/v1/cliente/get_all_clients/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status === 200){
        clientes.value = await response.json();

        cliente.value = clientes.value.find((client) => client.telefone == telefoneVisitante);
      }else{
        snackbarStore.set(`Falha ao carregar`, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set(`Falha ao carregar`, 'warning');
    }
  }
  
  function getColorQuantidade(quantidade){
    let color = "black";
    
    if(quantidade > 0){
      color = "green";
    }else if(quantidade < 0){
      color = "red";
    }

    return color;
  }

  function addProdutoInPedido(){
    loading.value = true;

    Pagamento.valorTotal += quantidade.value * valorVendaUnidade.value;
    console.log(produto.value);
    produto.value.quantidade -= quantidade.value
    const product = {...produto.value};
    product.quantidade = quantidade.value;
    product.valorVenda = valorVendaUnidade.value;
    product.id = pedido.value.length;
    console.log(product);
    pedido.value.push(product);

    dialogIsVisible.value = false;
    
    loading.value = false;
  }

  function removeProdutoInPedido(product){
    loading.value = true;
    const produtoToUpdate = produtos.value.find((prod) => prod.idProduto == product.idProduto);
    console.log(produtoToUpdate);
    Pagamento.valorTotal -= product.quantidade * product.valorVenda;
    produtoToUpdate.quantidade = Number(produtoToUpdate.quantidade) + Number(product.quantidade);

    pedido.value = pedido.value.filter((prod) => prod.id != product.id);

    loading.value = false;
  }

  function selectProduto(product){
    valorVendaUnidade.value = product.valorVenda;
    produto.value = product;
  }

  function openDialog(){
    dialogIsVisible.value = true;
  }

  function closeDialog(){
    dialogIsVisible.value = false;
  }

  watch(cliente, (newCliente, oldCliente) => {
    desconto.qtd = Math.floor(Number(cliente.value.saldo)/15);
  });

  onMounted(() => {
    requestAllProducts();
    requestAllClientes()
  });

</script>

<template>
    <Snackbar/>

  <v-navigation-drawer
    permanent
    location="right"
  >
    <template v-slot:prepend>
      <div class="pa-2">
        <v-autocomplete
          v-model="cliente"
          label="Cliente"
          :items="clientes"
          :item-title="(item)=>`${item.nome} (Tel: ${item.telefone})`"
          return-object
          variant="outlined"
          hide-details="auto"
        ></v-autocomplete>
      </div>
    </template>

    <v-dialog 
        v-model="dialogIsVisible"
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
                          v-model="quantidade"
                          label="Quantidade"
                          type="number"
                          hide-details="auto"
                      ></v-text-field>
                    </v-col>
                    <v-col>
                      <v-text-field
                          v-model="valorVendaUnidade"
                          label="Valor da Unidade"
                          type="number"
                          hide-details="auto"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <v-text-field
                        v-model="valorTotalProduto"
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
                      @click="() => addProdutoInPedido()"
                  >
                      Adicionar
                  </v-btn>
              </v-card-actions>
          </v-card>
    </v-dialog>

    <div class="pa-2">
      <v-list lines="one">
        <v-row v-for="(produto, i) in pedido"
            :key="i"
            v-if="!loading">
          <v-list-item
            :title="produto.nome"
            :subtitle="`${String(produto.quantidade).replace('.', ',')} x ${produto.valorVenda}`"
          ></v-list-item>
  
          <v-spacer></v-spacer>
  
          <v-btn
            icon="mdi-delete"
            color="primary"
            variant="text"
            @click="() => removeProdutoInPedido(produto)"
          ></v-btn>
        </v-row>
      </v-list>
    </div>

    <template v-slot:append>
      <v-row class="pa-2 mt-2">
        <v-chip color="grey-darken-4" variant="text">
          <h2>Total:</h2>
        </v-chip>

        <v-spacer></v-spacer>

        <v-chip color="green-darken-1" variant="text">
          <h2>R$ {{ Pagamento.valorTotal.toFixed(2).replace('.', ',') }}</h2>
        </v-chip>
      </v-row>
      <!-- grey-darken-1 -->
      <v-btn
        block
        color="deep-purple"
        prepend-icon="mdi-sale"
        @click=""
        :disabled="desconto.qtd <= 0"
      >
        Aplicar Desconto ({{ desconto.qtd }})
      </v-btn>

      <v-btn
        block
        color="green"
        prepend-icon="mdi-receipt-text-plus"
        @click=""
        >
        Criar
      </v-btn>
    </template>
  </v-navigation-drawer>
  
  <div
    color="grey-lighten-4"
    class="pa-3"
  >

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
          {{ String(value).replace(".", ",") }}
        </v-chip>
      </template>

      <template v-slot:item.acoes="{ item }">
        <v-btn
            color="primary"
            variant="text"
            icon="mdi-plus"
            @click="() => {
              openDialog()
              selectProduto(item);
            }"
        ></v-btn>
      </template>
    </v-data-table-virtual>
  </div>
</template>

<style scoped>
</style>