<script setup>
  import { ref } from 'vue'
  import { useAuthStore } from '../store.js';

  const authStore = useAuthStore();
  const nome = ref(authStore.getNome);
  const cargo = ref(authStore.getCargo);
  
</script>

<template>
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
    </div>
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

</style>
