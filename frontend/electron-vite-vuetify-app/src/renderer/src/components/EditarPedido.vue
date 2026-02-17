<script setup>
  import { ref, computed, watch, onMounted, reactive, toRaw,  onBeforeUnmount } from 'vue'
  import { fetchGet, fetchPost, fetchPatch, confirmDialog, getFormatedDate } from '../utils/common';
  import { useAuthStore, useSnackbarStore } from '../utils/store';
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
          const mergedProdutos = [];
          const mergedMap = new Map();

          responseJson.idProdutos.forEach((produtoRaw) => {
            const produto = { ...produtoRaw };
            const key = `${produto.idProduto}::${Number(produto.valorVendaUnd || 0).toFixed(2)}`;
            const existing = mergedMap.get(key);

            if (existing) {
              existing.quantidade = (
                Number(existing.quantidade || 0) + Number(produto.quantidade || 0)
              ).toFixed(3);
              existing.desconto = (
                Number(existing.desconto || 0) + Number(produto.desconto || 0)
              ).toFixed(2);
            } else {
              mergedMap.set(key, produto);
              mergedProdutos.push(produto);
            }
          });

          pedido.value = mergedProdutos;
          pedido.value.forEach((produto) => {
            produto.id = -1;
            produto._pendingQuantidade = 0;
            produto._pendingDesconto = 0;
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
      await requestAddInOrder();
      
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
        snackbarStore.set("Falha ao finalizar pedido", 'warning');
      }

    loading.finalizarBtn = false;
  }

  async function requestAddInOrder(idPedido=props.pedido.idPedido){
    try{
      const url = `http://127.0.0.1:8000/v1/pedido/add_in_order/${idPedido}/`;
      const body = {
          idProdutos: pedido.value
            .filter((produto) => Number(produto._pendingQuantidade || 0) > 0)
            .map((produto) => {
              return {
                idProduto: produto.idProduto,
                quantidade: Number(produto._pendingQuantidade).toFixed(3),
                valorVendaUnd: produto.valorVendaUnd,
                desconto: Number(produto._pendingDesconto || 0).toFixed(2)
              };
            }),
      };
      const token = authStore.getToken;
      
      if(body.idProdutos.length > 0){
        const response = await fetchPatch(url, body, token);
        const responseJson = await response.json();

        if(response.status === 200){
          pedido.value.forEach((produto) => {
            if (Number(produto._pendingQuantidade || 0) > 0) {
              produto.id = -1;
              produto._pendingQuantidade = 0;
              produto._pendingDesconto = 0;
            }
          });

          emit('adicionadoAoPedido', Pagamento.valorTotal);

          snackbarStore.set(responseJson.message, 'success');
        }else{
          snackbarStore.set(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      snackbarStore.set("Falha ao adicionar produto ao pedido", 'warning');
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
    const existingProduto = pedido.value.find(
      (item) =>
        item.idProduto == produto.idProduto &&
        Number(item.valorVendaUnd || 0) === Number(produto.valorVendaUnd || 0)
    );

    if (existingProduto) {
      const quantidadeAtual = Number(existingProduto.quantidade || 0);
      const quantidadeNova = Number(produto.quantidade || 0);
      const descontoAtual = Number(existingProduto.desconto || 0);
      const descontoNovo = Number(produto.desconto || 0);
      const pendingQuantidadeAtual = Number(existingProduto._pendingQuantidade || 0);
      const pendingDescontoAtual = Number(existingProduto._pendingDesconto || 0);

      existingProduto.quantidade = (quantidadeAtual + quantidadeNova).toFixed(3);
      existingProduto.desconto = (descontoAtual + descontoNovo).toFixed(2);
      existingProduto._pendingQuantidade = (pendingQuantidadeAtual + quantidadeNova).toFixed(3);
      existingProduto._pendingDesconto = (pendingDescontoAtual + descontoNovo).toFixed(2);

      return;
    }

    produto._pendingQuantidade = Number(produto.quantidade || 0).toFixed(3);
    produto._pendingDesconto = Number(produto.desconto || 0).toFixed(2);
    produto.id = pedido.value.length;
    pedido.value.push(produto);
  }

  function toMoney(value){
    return Number(value || 0).toFixed(2).replace('.', ',');
  }

  async function printComanda(layout = 'a4'){
    let html = "";
    const fallbackPrint = (html) =>
      new Promise((resolve) => {
        const frame = document.createElement("iframe");
        frame.style.position = "fixed";
        frame.style.right = "0";
        frame.style.bottom = "0";
        frame.style.width = "0";
        frame.style.height = "0";
        frame.style.border = "0";
        frame.srcdoc = html;
        frame.onload = () => {
          setTimeout(() => {
            try {
              frame.contentWindow.focus();
              frame.contentWindow.print();
            } finally {
              setTimeout(() => {
                frame.remove();
                resolve();
              }, 300);
            }
          }, 100);
        };
        document.body.appendChild(frame);
      });

    try {
      const isThermal = layout === 'thermal';
      const now = new Date();
      const emitidoEm = `${String(now.getDate()).padStart(2, "0")}/${String(now.getMonth() + 1).padStart(2, "0")}/${now.getFullYear()}`;
      const itensHtml = pedido.value.map((produto, idx) => {
        const quantidade = String(produto.quantidade || 0).replace('.', ',');
        const unitario = toMoney(produto.valorVendaUnd);
        const desconto = toMoney(produto.desconto);
        const totalItem = toMoney(
          Number(produto.quantidade || 0) * Number(produto.valorVendaUnd || 0) - Number(produto.desconto || 0)
        );
        if (isThermal) {
          return `
            <div class="item">
              <div class="item-line"><strong>${idx + 1}. ${produto.nome || ""}</strong></div>
              <div class="item-line">${quantidade} x ${unitario} - desc ${desconto}</div>
              <div class="item-line">Total item: R$ ${totalItem}</div>
            </div>
          `;
        }
        return `
          <tr>
            <td>${produto.nome || ""}</td>
            <td>${quantidade}</td>
            <td>R$ ${unitario}</td>
            <td>R$ ${desconto}</td>
            <td>R$ ${totalItem}</td>
          </tr>
        `;
      }).join('');

      html = `
        <html>
          <head>
            <meta charset="utf-8" />
            <title>Comanda Pedido ${props.pedido.idPedido}</title>
            <style>
              body { font-family: Arial, sans-serif; color: #222; padding: ${isThermal ? "8px" : "16px"}; width: ${isThermal ? "72mm" : "auto"}; }
              .screen-actions { margin-bottom: 10px; display: flex; gap: 8px; align-items: center; }
              .screen-btn { border: 1px solid #666; background: #f8f8f8; padding: 6px 10px; cursor: pointer; border-radius: 4px; font-size: 12px; }
            h1 { margin: 0 0 8px 0; font-size: 20px; }
            .info { margin: 2px 0; font-size: 13px; }
            .muted { color: #666; font-size: 12px; margin-bottom: 10px; }
              table { width: 100%; border-collapse: collapse; margin-top: 10px; }
              th, td { border: 1px solid #ddd; padding: 6px; font-size: 12px; text-align: left; }
              th { background: #f3f3f3; }
              .total { margin-top: 10px; font-size: 16px; font-weight: bold; text-align: right; }
              .item { margin: 8px 0; border-bottom: 1px dashed #bbb; padding-bottom: 6px; }
              .item-line { font-size: 12px; line-height: 1.3; }
              @media print {
                body { margin: 0; width: ${isThermal ? "72mm" : "auto"}; }
                .screen-actions { display: none; }
              }
            </style>
          </head>
          <body>
            <div class="screen-actions">
              <button class="screen-btn" onclick="window.print()">Imprimir Agora</button>
              <span class="muted">Atalho: Ctrl+P</span>
            </div>
            <h1>Comanda do Pedido</h1>
            <div class="muted">Emitido em: ${emitidoEm}</div>
            <div class="info"><strong>Pedido:</strong> ${props.pedido.idPedido}</div>
            <div class="info"><strong>Cliente:</strong> ${props.pedido.nomeCliente || ""}</div>
            <div class="info"><strong>Telefone:</strong> ${props.pedido.telefoneCliente || ""}</div>
            ${isThermal
              ? `<div>${itensHtml}</div>`
              : `<table>
                  <thead>
                    <tr>
                      <th>Produto</th>
                      <th>Qtd</th>
                      <th>Unitario</th>
                      <th>Desconto</th>
                      <th>Total</th>
                    </tr>
                  </thead>
                  <tbody>${itensHtml}</tbody>
                </table>`
            }
            <div class="total">Total: R$ ${toMoney(Pagamento.valorTotal)}</div>
          </body>
        </html>
      `;

      snackbarStore.set("Preparando impressao...", 'info');

      if (window.ipcRenderer?.printHtml) {
        const result = await window.ipcRenderer.printHtml({
          html,
          layout,
        });

        if (!result?.ok) {
          throw new Error(result?.message || "Falha ao imprimir");
        }
      } else {
        await fallbackPrint();
      }

      snackbarStore.set("Comanda aberta. Se preciso, clique em 'Imprimir Agora'.", 'success');
    } catch (error) {
      try {
        const safeHtml = html || `<html><body><h3>Erro ao montar comanda.</h3></body></html>`;
        await fallbackPrint(safeHtml);
        snackbarStore.set("Comando de impressao enviado (fallback)", 'success');
      } catch (_) {
        snackbarStore.set(String(error) || "Falha ao imprimir", 'warning');
      }
    }
  }

  function printComandaA4(){
    printComanda('a4');
  }

  function printComandaThermal(){
    printComanda('thermal');
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
        variant="tonal"
        prepend-icon="mdi-content-save-check"
        color="blue-darken-1"
        @click="() => requestAddInOrder()"
      >
        Salvar Alterações
      </v-btn>

      <v-btn
        class="ma-1"
        variant="tonal"
        prepend-icon="mdi-printer"
        color="grey-darken-2"
        @click.stop.prevent="printComandaA4"
      >
        Imprimir Comanda
      </v-btn>

      <v-btn
        class="ma-1"
        variant="tonal"
        prepend-icon="mdi-receipt-text"
        color="brown-darken-1"
        @click.stop.prevent="printComandaThermal"
      >
        Imprimir Térmica
      </v-btn>

      <v-btn
        variant="tonal"
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
