<script setup>
  import { ref, reactive, computed } from 'vue'
  import { useRouter } from 'vue-router';
  import { useAuthStore, useSnackbarStore } from '../utils/store';


  const router = useRouter();
  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore();
  const nome = ref(authStore.getNome);
  const cargo = ref(authStore.getCargo);

  const showSnackbar = computed(() => snackbarStore.showSnackbar);
  const messageSnackbar = computed(() => snackbarStore.message);
  const backgroundColor = computed(() => snackbarStore.backgroundColor);

  function resetUserInfo(){
    authStore.reset();

    router.push('/');
  }

  function closeSnackbar(){
    snackbarStore.closeSnackbar();
  }
</script>

<template>
  <div v-show="showSnackbar" class="snackbar" :style="{backgroundColor: backgroundColor}">
    {{ messageSnackbar }}
    <button @click="closeSnackbar" class="close-btn">FECHAR</button>
  </div>
  <main>
    <v-navigation-drawer
    color="deep-purple">
      <v-list-item :title="nome" :subtitle="cargo"></v-list-item>

      <v-divider></v-divider>

      <v-list-item 
        prepend-icon="mdi-view-dashboard" 
        link title="Dashboard" 
        to="/menu/dashboard/">
      </v-list-item>

      <v-list-item 
        prepend-icon="mdi-cash-register" 
        link title="Caixa" 
        to="/menu/caixa/">
      </v-list-item>

      <v-list-item 
        prepend-icon="mdi-receipt" 
        link title="Pedidos" 
        to="/menu/pedidos/">
      </v-list-item>

      <v-list-item 
        prepend-icon="mdi-account-multiple" 
        link title="Clientes" 
        to="/menu/clientes/">
      </v-list-item>

      <v-list-item 
        prepend-icon="mdi-account-group" 
        link title="Colaboradores" 
        to="/menu/funcionarios/">
      </v-list-item>

      <v-list-item 
        prepend-icon="mdi-cog" 
        link title="Configurações" 
        to="/menu/dashboard/">
      </v-list-item>

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
  @keyframes slideDown {
    from {
      transform: translate(-50%, -100%);
    }
    to {
      transform: translate(-50%, 10px);
    }
  }
  .snackbar{
    position: fixed;
    display: flex;
    justify-content: center;
    align-items: center;
    max-width: 45vw;
    padding: 10px;
    border-radius: 5px;
    left: 50%;
    gap: 45px;
    color: white;
    animation: slideDown 0.3s ease forwards;
    text-align: center;
    font-weight: bold;
  }

  .close-btn{
    background-color: transparent;
    border: none;
    font-weight: bold;
    padding: 10px;
    color: rgb(28, 28, 28);
  }

  .close-btn:hover{
    background-color: rgba(255, 255, 255, 0.1);
  }

  .close-btn:active{
    background-color: rgba(255, 255, 255, 0.15);
  }

  main {
      display: flex;
  }

  .router-view-div{
    /* padding: 20px 10px 10px 10px; */
    width: 100%;
  }
</style>
