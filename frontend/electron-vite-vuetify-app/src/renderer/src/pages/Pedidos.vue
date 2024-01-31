<script setup>
  import { ref, computed, reactive } from 'vue'
  import { useCaixaStore } from '../utils/store';
  import Snackbar from '../components/Snackbar.vue';
  import CriarPedido from '../components/CriarPedido.vue';
  import PedidosEmAberto from '../components/PedidosEmAberto.vue';
  import PedidosFechados from '../components/PedidosFechados.vue';

  defineOptions({
    inheritAttrs: false
  });

  const caixaStore = useCaixaStore();
  
  const caixaIsOpen = computed(() => caixaStore.getStatus === 'aberto');
  const whichPage = reactive({
    name: 'pedidos abertos',
  });

  function toPedidosEmAberto(){
    whichPage.name = 'pedidos abertos';
  }
  
  function toPedidosFechados(){
    whichPage.name = 'pedidos fechados';
  }

  function toCriarPedido(){
    whichPage.name = 'criar pedido';
  }
</script>

<template>
  <Snackbar/>    
  
  <div v-if="!caixaIsOpen" class="close-caixa">
    <v-container fluid fill-height>
        <v-row align="center" justify="center">
          <v-col cols="12" md="6">
            <v-card
              class="text-center"
              color="red-darken-2"
              dark
            >
              <v-card-text class="display-2">
                <h2>Caixa Fechado</h2>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
  </div>
  
  <v-app-bar  color="deep-purple" :elevation="2" density="compact">
        <v-app-bar-title>Pedidos</v-app-bar-title>

        <template v-slot:prepend>
          <v-icon>mdi-menu-right</v-icon>
        </template>

        <v-btn
            variant="text"
            prepend-icon="mdi-view-list"
            stacked
            @click="toPedidosEmAberto"
            v-show="caixaIsOpen"
        >
            Pedidos em Aberto
        </v-btn>

        <v-btn
            variant="text"
            prepend-icon="mdi-view-list-outline"
            stacked
            @click="toPedidosFechados"
        >
            Pedidos Fechados
        </v-btn>

        <v-btn
            variant="text"
            prepend-icon="mdi-receipt-text-plus"
            stacked
            @click="toCriarPedido"
            v-show="caixaIsOpen"
        >
            Criar Pedido
        </v-btn>
  </v-app-bar>
  <div v-if="whichPage.name == 'pedidos fechados'">
    <PedidosFechados/>
  </div>
  <div v-if="whichPage.name == 'criar pedido'">
    <CriarPedido
      @pedidoCriado="toPedidosEmAberto"
    />
  </div>
  <div v-if="whichPage.name == 'pedidos abertos'">
    <PedidosEmAberto/>
  </div>

</template>

<style scoped>
</style>
