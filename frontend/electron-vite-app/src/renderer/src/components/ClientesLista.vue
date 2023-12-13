<script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { useAuthStore } from '../store.js';

  const authStore = useAuthStore();
  let clientes = [];
  const loading = ref(true);

  const requestAllClientes = async () =>{
    const options = {
        method: 'GET',
        headers: {
            'jwt-token': authStore.getToken,
            'Content-Type': 'application/json'
        }
    };
    console.log(authStore.getToken);

    const response = await fetch("http://127.0.0.1:8000/v1/cliente/get_all_clients/", options);

    if(response.ok && response.status !== 204){
      clientes = await response.json();

      // ORDEM ALFABÉTICA POR NOME
      clientes = clientes.sort((clienteA, clienteB) => clienteA.nome.localeCompare(clienteB.nome));
    }
   
    loading.value = false;
  }

  requestAllClientes();
    // 
</script>

<template>
  <div class="page-content">

<section class="main-content">
  <div class="toolbar">

    <h1>Clientes</h1>

    <div>
      <div class="search-container">
        <form action="#" method="get">
          <input type="text" class="search-box" name="search" placeholder="Buscar">
          <button type="submit" class="search-btn"><!--<img src="assets/cliente-lista-imgs/magnifying-glass-solid.svg"
              alt="search icone">--></button>
        </form>
      </div>

      <button class="register-btn"><a href="#">Cadastrar cliente</a></button>
    </div>
  </div>

  <div v-if="!loading">
    <table>
      <thead>
        <tr>
          <th>Nome</th>
          <th>Telefone</th>
          <th>Email</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(cliente, index) in clientes" :key="index">
          <td>{{ cliente.nome }}</td>
          <td>{{ cliente.telefone }}</td>
          <td>{{ cliente.email }}</td>
          <td>             
            <button class="view-profile-btn"><router-link class="router-link" :to="{ name: 'Ver Cliente' }">Ver</router-link></button>           
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class=loader-container v-else>
    <p id="loader"></p>
  </div>
  
</section>

</div>
</template>

<style scoped>
  /* @keyframes spin {
      0% {
          transform: rotate(0deg);
      }
      100% {
          transform: rotate(360deg);
      }
  } */

  .page-content {
    display: flex;
    flex-direction: column;
    background: #ffffff;  
  }

  .toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      /* margin: 20px 0px 10px 0px; */
  }

  .toolbar h1 {
      font-size: 2rem;
  }

  .toolbar > div {
      display: flex;
  }

  .search-container form {
      width: 300px;
      height: 40px;
      padding: 4px;
      border: solid;
      border-width: 2px;
      border-radius: 5px;
      display: flex;
      align-items: center;
      background-color: #F9FBFF;
  }

  .search-box {
      width: 250px;
      height: 27px;
      font-size: 20px;
      background-color: transparent;
      border: none;
      outline: none;
  }

  .search-btn {
      width: 40px;
      height: 30px;
      cursor: pointer;
      border: none;
      background-color: transparent;
  }

  .search-btn img {
      width: 20px;
      height: 20px;
  }

  .register-btn {
      width: 180px;
      height: 40px;
      margin-left: 20px;
      background: #000;
      font-size: 20px;
      border-radius: 5px;
      border-style: none;
      cursor: pointer;
  }

  .register-btn a {
      text-decoration: none;
      color: #ffffff;
  }

  /* 
  hr {
      height: 2px;
      border-width: 0px;
      background-color: #EEEEEE;
  } */

  .clients-list {
      height: 80vh;
      overflow-x: auto;
  }

  table {
      border-collapse: collapse;
      width: 100%;
      color: #333;
      font-size: 15px;
      text-align: left;
  }

  thead {
      top: 0;
      position: sticky;
      background-color: #ffffff;
  }

  th {
      padding: 12px 12px 12px 0px;
      color: #7d7f88;
      font-weight: bold;
  }

  td {
      padding: 12px 12px 12px 0px;
      border-top: 1px solid;
      border-bottom: 1px solid;
      border-color: #B5B7C0;
      font-size: 18px;
  }


  tr td:last-child {
      text-align: right;
  }

  .view-profile-btn {
      width: 90px;
      height: 30px;
      background: #6940aa7e;
      font-size: 18px;
      border-radius: 5px;
      border-style: solid;
      border-color: #6940AA;
      cursor: pointer;
  }

  .view-profile-btn a {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      text-decoration: none;
      font-weight: bold;
      color: hsl(263, 45%, 46%);
  }

  .loader-container{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 70vh;
  }

  #loader{
      border: 4px solid rgba(0, 0, 0, 0.1);
      border-top: 4px solid #333;
      border-radius: 50%;
      width: 250px;
      height: 250px;
      animation: spin 1s linear infinite; /* Aplica a animação */
  }


</style>
