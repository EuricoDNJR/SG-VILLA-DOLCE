<script setup>
  import { ref, reactive, computed } from 'vue'
  import { useAuthStore, useSnackbarStore } from '../utils/store';
  
  const authStore = useAuthStore();
  const snackbarStore = useSnackbarStore();
  const nome = ref(authStore.getNome);
  const cargo = ref(authStore.getCargo);
  const isCurrentPage = reactive({
    dashboard: true,
    caixa: false,
    pedido: false,
    clientes: false,
    funcionarios: false,
    configuracoes: false
  });
  const showSnackbar = computed(() => snackbarStore.showSnackbar);
  const messageSnackbar = computed(() => snackbarStore.message);
  const backgroundColor = computed(() => snackbarStore.backgroundColor);

  function currentPage(currentPageName){
    for (let key in isCurrentPage) {
      isCurrentPage[key] = key === currentPageName;
    }
  }

  function resetUserInfo(){
    authStore.reset();
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
    <div class="aside-in-normal-flow">
      <aside>
          <div class="user-info">
            <img src="" alt="foto do usuário">
            <span class="user" id="user">{{ nome }}</span>
            <span class="position" id="position">{{ cargo }}</span>
          </div>
          <div class="menu">
            <ul>
              <li><router-link class="redirect" :to="{ name: 'dashboard' }" @click="currentPage('dashboard')" :class="{isCurrentPage: isCurrentPage.dashboard}">Dashboard</router-link></li>
              <li><router-link class="redirect" :to="{ name: 'caixa' }" @click="currentPage('caixa')" :class="{isCurrentPage: isCurrentPage.caixa}">Caixa</router-link></li>
              <li><router-link class="redirect" :to="{ name: 'pedido' }" @click="currentPage('pedido')" :class="{isCurrentPage: isCurrentPage.pedido}">Pedido</router-link></li>
              <li><router-link class="redirect" :to="{ name: 'clientes' }" @click="currentPage('clientes')" :class="{isCurrentPage: isCurrentPage.clientes}">Clientes</router-link></li>
              <li><router-link class="redirect" :to="{ name: 'funcionarios' }" @click="currentPage('funcionarios')" :class="{isCurrentPage: isCurrentPage.funcionarios}">Colaboradores</router-link></li>
              <li><router-link class="redirect" :to="{ name: 'dashboard' }" @click="currentPage('configuracoes')" :class="{isCurrentPage: isCurrentPage.configuracoes}">Configurações</router-link></li>
              <li><router-link class="redirect" :to="{ name: 'login' }" @click="resetUserInfo">Sair</router-link></li>
            </ul>
          </div>
      </aside>
    </div>
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
    padding: 40px 40px 0px 40px;
    width: 100%;
  }

  .aside-in-normal-flow{
    position: relative;
    width: 18vw;
    height: 100vh;
    min-width: 240px;
  }
  
  aside {
    position: fixed;
    background-color: #6940AA;
    width: 18vw;
    height: 100vh;
    min-width: 240px;
    padding: 20px 50px;
    z-index: 9999;
  }

  .user-info {
      display: flex;
      flex-direction: column;
      margin-bottom: 40px;
      font-size: 18px;
      border-bottom: 1px solid #ffffff87;
  }

  .user-info img {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 90px;
      height: 90px;
      border-radius: 10px;
      margin-bottom: 15px;
      background-color: gray;
      object-fit: cover;
  }

  .user-info .user {
      font-weight: bold;
      color: #fff;
      margin-bottom: 8px;
      cursor: default;
  }

  .user-info .position {
      color: #ffffff87;
  }

  .menu ul {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 30px;
      list-style: none;
  }

  .redirect {
      text-decoration: none;
      font-size: 22px;
      font-weight: bold;
      color: #ffffff87;
      transition: color 0.5s;
  }

  .redirect:hover {
      color: #ffffff;  
  }

  .isCurrentPage{
    color: #ffffff;  
  }

</style>
