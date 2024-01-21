<script setup>
  import { ref, computed, watch, onMounted, reactive, toRaw,  onBeforeUnmount } from 'vue'
  import { fetchGet, fetchPost, fetchPatch, confirmDialog, getFormatedDate } from '../utils/common';
  import { useAuthStore, useSnackbarStore, useCaixaStore, usePedidoStore } from '../utils/store';
  import SelecionarProdutoPedido from '../components/SelecionarProdutoPedido.vue';
  import PesquisarClientePedido from '../components/PesquisarClientePedido.vue';
  import DescontoPedido from '../components/DescontoPedido.vue';

  const props = defineProps(['pedido']);
  const emit = defineEmits([
    'pedidoFinished', 
    'voltar',
    'cancelarPedido',
    'adicionadoAoPedido'
  ]);

  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore()
  
  const produtoRemovido = reactive({
    wasRemoved: false,
    idProduto: undefined,
    quantidade: undefined,
  });

  const pedido = ref([]);
  const Pagamento = reactive({
    valorTotal: computed(() => {
      return pedido.value.reduce((somatorio, produto) => {
        return somatorio + Number(produto.quantidade) * Number(produto.valorVendaUnd) - Number(produto.desconto);
      }, 0);
    }),
    valorTotalComputed: computed(() => Pagamento.valorTotal.toFixed(2)),
    valorRecebimento: 0,
    valorDevolvido: computed(() => ((Pagamento.valorRecebimento - Pagamento.valorTotal) > 0 ? Pagamento.valorRecebimento - Pagamento.valorTotal : 0).toFixed(2)),
    tiposPagamento: [],
    pagamentoSelecionado: undefined,
  });
  const cliente = reactive({
    saldo: 0,
  });
  const dialogIsVisible = reactive({
    finalizarPedido: false,
    desconto: false,
  });
  const loading = reactive({
    finalizarBtn: false,
    descontoPedido: true,
  });


  async function requestAllPaymentTypes(){
    try{
      const url = "http://127.0.0.1:8000/v1/tipo_pagamento/get_all_payment_types/"
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){
        Pagamento.tiposPagamento = responseJson;

        Pagamento.pagamentoSelecionado = Pagamento.tiposPagamento[0];
      }else{
        snackbarStore.set(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set("Falha ao carregar tipos de pagamento", 'warning');
    }
  }
  
  async function requestOrder(idPedido=props.pedido.idPedido){
    try{
      const url = `http://127.0.0.1:8000/v1/pedido/get_order/${idPedido}/`
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);
      const responseJson = await response.json();

      if(response.status === 200){  
        if(responseJson.idProdutos){
          pedido.value = responseJson.idProdutos;
          pedido.value.forEach((produto) => {
            produto.id = -1;
          });
        }
        
        cliente.saldo = Number(responseJson.saldoCliente);

        loading.descontoPedido = false;
      }else{
        snackbarStore.set(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set("Falha ao carregar pedido", 'warning');
    }
  }

  async function requestFinishOrder(idPedido=props.pedido.idPedido){
    loading.finalizarBtn = true;

    try{
      requestAddInOrder();
      
      const url = `http://127.0.0.1:8000/v1/pedido/finish_order/${idPedido}/`;
      const body = {
        valorRecebimento: Pagamento.valorRecebimento,
        valorDevolvido: Pagamento.valorDevolvido,
        tipoPagamento: Pagamento.pagamentoSelecionado.nome,
      };
      const token = authStore.getToken;

      const response = await fetchPatch(url, body, token);
      const responseJson = await response.json();

      if(response.status === 200){       
        emit('pedidoFinished', idPedido);

        snackbarStore.set(responseJson.message, 'success');
      }else{
        snackbarStore.set(responseJson.message, 'warning');
      }
    }catch(e){
      console.log(e);
      snackbarStore.set(`Falha ao carregar`, 'warning');
    }

    loading.finalizarBtn = false;
  }

  async function requestAddInOrder(idPedido=props.pedido.idPedido){
    try{
      const url = `http://127.0.0.1:8000/v1/pedido/add_in_order/${idPedido}/`;
      const body = {
          idProdutos: pedido.value.filter(
            (produto) => produto.id != -1
          ).map(
            (produto) => {
              return {
                idProduto: produto.idProduto,
                quantidade: produto.quantidade,
                valorVendaUnd: produto.valorVendaUnd,
                desconto: produto.desconto
              };
            }
          ),
          valorTotal: Pagamento.valorTotalComputed,
          desconto: true,
      };
      const token = authStore.getToken;
      
      if(body.idProdutos.length > 0){
        const response = await fetchPatch(url, body, token);
        const responseJson = await response.json();

        if(response.status === 200){
          pedido.value.forEach(
            (produto) => produto.id = -1
          )

          emit('adicionadoAoPedido', Pagamento.valorTotal);

          snackbarStore.set(responseJson.message, 'success');
        }else{
          snackbarStore.set(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      snackbarStore.set(`Falha ao adicionar produto ao pedido`, 'warning');
    }
  }

  function removeProdutoInPedido(product){   
    pedido.value = pedido.value.filter((produto) => produto.id != product.id);
    
    produtoRemovido.idProduto = product.idProduto;
    produtoRemovido.quantidade = product.quantidade;
    produtoRemovido.wasRemoved = !produtoRemovido.wasRemoved;
  }
  
  function closeDialog(nome){
    dialogIsVisible[nome] = false;

    if(nome == "finalizarPedido"){
      Pagamento.valorRecebimento = 0;
    }
  }

  function adicionarProduto(produto){
    produto.id = pedido.value.length;

    pedido.value.push(produto);
  }

  requestOrder();
  requestAllPaymentTypes();
</script>

<template>
  <div class="d-flex justify-space-between align-center">
      <v-btn
        variant="text"
        icon="mdi-arrow-left"
        @click="emit('voltar')"
      >
        <v-icon>mdi-arrow-left</v-icon>
        <v-tooltip 
          activator="parent"
          location="bottom"
        >
          Voltar
        </v-tooltip >
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn
        class="ma-1"
        variant="flat"
        prepend-icon="mdi-content-save-check"
        color="blue-darken-1"
        @click="() => requestAddInOrder()"
      >
        Salvar Alterações
      </v-btn>

      <v-btn
        variant="flat"
        prepend-icon="mdi-cancel"
        color="red-darken-1"
        @click="emit('cancelarPedido')"
      >
        Cancelar Pedido
      </v-btn>
    </div>

  <SelecionarProdutoPedido
    :produtoRemovido="produtoRemovido"
    @produtoAdicionado="adicionarProduto"
  />

  <v-navigation-drawer
    permanent
    location="right"
  >
    <template v-slot:prepend>
      <PesquisarClientePedido 
        :telefoneCliente="props.pedido.telefoneCliente"
        :readonly="true" 
        class="pa-2"
      />
    </template>

    <div class="pa-2" id="lista-produtos-do-pedido">
      <v-list lines="one">
        <v-row v-for="(produto, i) in pedido" :key="i">
          <v-list-item
            :title="produto.nome"
            :subtitle="`${produto.quantidade.replace('.', ',')} x ${produto.valorVendaUnd} - ${produto.desconto.replace('.', ',')}`"
          ></v-list-item>
  
          <v-spacer></v-spacer>
  
          <v-btn v-if="produto.id != -1"
            icon="mdi-delete"
            color="primary"
            variant="text"
            @click="() => removeProdutoInPedido(produto)"
          ></v-btn>
        </v-row>
      </v-list>
    </div>

    <template v-slot:append>
      <v-row class="pa-2 mt-2" id="valor-total-pedido">
        <v-chip color="grey-darken-4" variant="text">
          <h2>Total:</h2>
        </v-chip>

        <v-spacer></v-spacer>

        <v-chip color="green-darken-1" variant="text">
          <h2>R$ {{ Pagamento.valorTotal.toFixed(2).replace('.', ',') }}</h2>
        </v-chip>
      </v-row>
     
      <DescontoPedido v-if="!loading.descontoPedido && pedido.length > 0"
        :pedido="pedido"
        :saldoCliente="cliente.saldo"
      />

      <v-dialog id=finalizar 
          v-model="dialogIsVisible.finalizarPedido"
          persistent
          width="512"
        >
          <template v-slot:activator="{ props }">
            <v-btn
              block
              color="green-darken-1"
              prepend-icon="mdi-checkbox-marked-circle"
              v-bind="props"
            >
              Finalizar
            </v-btn>
          </template>

          <v-card>
              <v-card-title>
                  <span class="text-h5">Finalizar Pedido</span>
              </v-card-title>

              <v-divider></v-divider>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-text-field
                        v-model.number="Pagamento.valorRecebimento"
                        label="Valor Recebido"
                        type="number"
                        hide-details="auto"
                        density="comfortable"
                        step="0.01"
                      ></v-text-field>
                    </v-col>
                    <v-col>
                      <v-text-field
                        v-model.number="Pagamento.valorTotalComputed"
                        label="Valor Total"
                        type="number"
                        hide-details="auto"
                        :readonly="true"
                        density="comfortable"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <v-text-field
                        v-model.number="Pagamento.valorDevolvido"
                        label="Valor Devolvido (Troco)"
                        type="number"
                        hide-details="auto"
                        :readonly="true"
                        density="comfortable"
                      ></v-text-field>
                    </v-col>

                    <v-col>
                      <v-select
                        v-model="Pagamento.pagamentoSelecionado"
                        label="Tipo Pagamento"
                        hide-details="auto"
                        density="comfortable"
                        :items="Pagamento.tiposPagamento"
                        item-title="nome"
                        return-object
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                  <v-spacer></v-spacer>

                  <v-btn   
                    variant="text"
                    @click="() => closeDialog('finalizarPedido')"
                  >
                    Fechar
                  </v-btn>

                  <v-btn
                    color="green-darken-1"
                    variant="flat"
                    prepend-icon="mdi-checkbox-marked-circle"
                    @click="() => requestFinishOrder()"
                    :loading="loading.finalizarBtn"
                  >
                    Finalizar
                  </v-btn>
              </v-card-actions>
          </v-card>
      </v-dialog>
    </template>
  </v-navigation-drawer>
</template>

<style scoped>
</style>