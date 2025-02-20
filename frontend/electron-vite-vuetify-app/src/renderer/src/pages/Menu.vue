<script setup>
  import { reactive, computed } from 'vue'
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '../utils/store';
  import Caixa from '../components/Caixa.vue';
  import Configuracoes from '../components/Configuracoes.vue';

  defineOptions({
    inheritAttrs: false
  });

  const router = useRouter();
  const authStore = useAuthStore();
  const nome = computed(() => authStore.getNome);
  const cargo = computed(() => authStore.getCargo);

  const isVisible = reactive({
    configuracoes: false,
  });

  function resetUserInfo(){
    authStore.reset();

    router.push('/');
  }
</script>

<template>
  <main>
    <v-navigation-drawer
      color="deep-purple"
      permanent
    >
      <v-list>
        <v-list-item :title="nome" :subtitle="cargo"></v-list-item>

        <v-divider></v-divider>
        
        <v-list-item 
          prepend-icon="mdi-view-dashboard" 
          link title="Dashboard" 
          to="/menu/dashboard/">
        </v-list-item>

        <v-list-group
          value="Caixa"
          prepend-icon="mdi-cash-register"
        >
            <template v-slot:activator="{ props }">
              <v-list-item
                v-bind="props"
                title="Caixa"
              ></v-list-item>
            </template>

            <Caixa/>

            <v-list-item 
              append-icon="mdi-history" 
              link title="Histórico" 
              to="/menu/historico-caixas/">
            </v-list-item>
        </v-list-group>

        <v-list-item 
          prepend-icon="mdi-receipt" 
          link title="Pedidos" 
          to="/menu/pedidos/">
        </v-list-item>

        <v-list-item 
          prepend-icon="mdi-package-variant-closed" 
          link title="Estoque" 
          to="/menu/estoque/">
        </v-list-item>

        <v-list-item 
          prepend-icon="mdi-package-variant" 
          link title="Produtos" 
          to="/menu/produtos/">
        </v-list-item>

        <v-list-item 
          prepend-icon="mdi-account-multiple" 
          link title="Clientes" 
          to="/menu/clientes/">
        </v-list-item>

        <v-list-item 
          prepend-icon="mdi-account-group" 
          link title="Colaboradores" 
          to="/menu/colaboradores/">
        </v-list-item>
        
        <v-list-item
          prepend-icon="mdi-cog" 
          link title="Configurações" 
          @click="isVisible.configuracoes = true"
        >
          <Configuracoes
            :isVisible="isVisible.configuracoes"
            @close="isVisible.configuracoes = false"
          />
        </v-list-item>
      </v-list>

      <template v-slot:append>
          <div class="pa-2">
            <v-btn block
              color="grey-darken-4" 
              @click="resetUserInfo"
              prepend-icon="mdi-logout"
            >
              Sair
            </v-btn>
          </div>
      </template>
    </v-navigation-drawer>

    <div class="router-view-div">
      <router-view class="router-view"/>
    </div>
  </main>
</template>

<style scoped>
  main {
    display: flex;
  }
  .router-view-div{
    /* padding: 20px 10px 10px 10px; */
    width: 100%;
  }
</style>
