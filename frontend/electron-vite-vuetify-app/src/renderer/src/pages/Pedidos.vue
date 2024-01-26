<script setup>
  import { ref, computed } from 'vue'
  import { useCaixaStore } from '../utils/store';
  import Snackbar from '../components/Snackbar.vue';
  import CriarPedido from '../components/CriarPedido.vue';
  import PedidosEmAberto from '../components/PedidosEmAberto.vue';

  defineOptions({
    inheritAttrs: false
  });

  const caixaStore = useCaixaStore();
  
  const caixaIsOpen = computed(() => caixaStore.getStatus === 'aberto');
  const isCriarPedido = ref(false);

  function toPedidosEmAberto(){
    isCriarPedido.value = false;
  }
  
  function toCriarPedido(){
    isCriarPedido.value = true;
  }
</script>

<template>
  <Snackbar/>       
  
  <div v-if="caixaIsOpen" class="open-caixa">
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
        >
            Pedidos em Aberto
        </v-btn>

        <v-btn
            variant="text"
            prepend-icon="mdi-receipt-text-plus"
            stacked
            @click="toCriarPedido"
        >
            Criar Pedido
        </v-btn>
    </v-app-bar>

    <div v-if="isCriarPedido">
      <CriarPedido
        @pedidoCriado="toPedidosEmAberto"
      />
    </div>
    <div v-else>
      <PedidosEmAberto/>
    </div>
  </div>
  <div v-else class="close-caixa">
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
</template>

<style scoped>
</style>
