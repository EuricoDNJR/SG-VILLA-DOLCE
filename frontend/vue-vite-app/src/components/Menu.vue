<script setup>
  import { ref } from 'vue'
  import { useAuthStore } from '../store.js';

  const count = ref(0);
  const authStore = useAuthStore();
  const textRouterLink = ref("To componentA");

  textRouterLink.value = authStore.getNome;
  
</script>

<template>
  <main>
    <aside>
        <div class="user-info">
          <img src="" alt="foto do usuário">
          <span class="user" id="user">Dua Lipa</span>
          <span class="position" id="position">Gerente</span>
        </div>
        <div class="menu">
          <ul>
            <li><router-link class="router-link" :to="{ name: 'Dashboard' }">Dashboard</router-link></li>
            <li><router-link class="router-link" :to="{ name: 'Dashboard' }">Caixa</router-link></li>
            <li><router-link class="router-link" :to="{ name: 'Dashboard' }">Pedido</router-link></li>
            <li><router-link class="router-link" :to="{ name: 'Clientes Lista' }">Clientes</router-link></li>
            <li><router-link class="router-link" :to="{ name: 'Dashboard' }">Funcionários</router-link></li>
            <li><router-link class="router-link" :to="{ name: 'Dashboard' }">Configurações</router-link></li>
            <li><router-link class="router-link" :to="{ name: 'Dashboard' }">Sair</router-link></li>
          </ul>
        </div>
    </aside>

    <router-view/>
  </main>
</template>

<style scoped>
  main {
      display: flex;
  }

  aside {
      background-color: #6940AA;
      width: 18vw;
      height: 100%;
      padding: 20px 50px;
  }

  .user-info {
      display: flex;
      flex-direction: column;
      margin-bottom: 60px;
  }

  .user-info img {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 120px;
      height: 120px;
      border-radius: 10px;
      margin-bottom: 15px;
      background-color: gray;
      object-fit: cover;
  }

  .user-info .user {
      font-size: 22px;
      font-weight: bold;
      color: #fff;
      margin-bottom: 8px;
      cursor: default;
  }

  .user-info .position {
      font-size: 20px;
      color: #ffffff87;
  }

  .menu ul li {
      list-style: none;
      /*font-size: 30px;
      margin: 30px 0px 30px 0px;*/
      margin-bottom: 40px;
      /*font-weight: bold;
      color: #fff;*/
  }

  .menu a {
      text-decoration: none;
      font-size: 22px;
      font-weight: bold;
      color: #ffffff87;
      transition: color 0.5s;   
  }

  .menu a:hover {
      color: #ffffff;
      
  }

  .page-content {
      width: 82vw;
      background: #ffffff;
  }

</style>
