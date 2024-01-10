<script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { useRouter } from 'vue-router';
  import { useAuthStore, useClienteStore, useSnackbarStore } from '../utils/store';
  import { fetchGet, replaceNullToEmptyString } from '../utils/common';

  const router = useRouter();
  const authStore = useAuthStore();
  const clienteStore = useClienteStore();
  const snackbarStore = useSnackbarStore();
  let clientes = [];
  let clientesFiltered = [];
  const loading = ref(true);
  const searchText = ref('');

  const redirectToClienteInfo = () => {
    router.push("/menu/ver-cliente/");
  }

  const redirectToCadastrarCliente = () => {
    router.push("/menu/cadastrar-cliente/");
  }

  const handleClienteInfoAndRedirect = (cliente) => {
    replaceNullToEmptyString(cliente);

    clienteStore.saveClienteInfo({...cliente, pontos: Math.floor(cliente.saldo/15)});

    redirectToClienteInfo();
  }

  const requestAllClientes = async () =>{
    try{
      const url = "http://127.0.0.1:8000/v1/cliente/get_all_clients/";
      const token = authStore.getToken;
      
      const response = await fetchGet(url, token);

      if(response.status === 200){
        clientes = await response.json();

        // ORDEM ALFABÉTICA POR NOME
        clientes = clientes.sort((clienteA, clienteB) => clienteA.nome.localeCompare(clienteB.nome));
        clientesFiltered = [...clientes];
      }else{
        snackbarStore.snackbar("Falha ao carregar clientes", 'red');
      }
    }catch(e){
      console.log(e);
      snackbarStore.snackbar("Falha ao carregar clientes", 'red');
    }
   
    loading.value = false;
  }

  const searchCliente = () => {
    // Recarregando tabela para atualizar os clientes
    loading.value = true;

    clientesFiltered = clientes.filter((cliente) => cliente.nome.toLowerCase().includes(searchText.value.toLowerCase()));
  
    loading.value = false;
  }

  requestAllClientes();
  
</script>

<template>
  <div class="page-content">

<section class="main-content">
  <div class="toolbar">

    <h1>Clientes</h1>

    <div>
      <div class="search-container">
        <form action="#" method="get">
          <input type="text" class="search-box" @input="searchCliente" v-model="searchText" name="search" placeholder="Buscar">
          <img class=search-btn-img src="../assets/search-imgs/magnifying-glass-solid.svg" alt="search icone">
        </form>
      </div>

      <button class="register-btn" @click="redirectToCadastrarCliente">Cadastrar cliente</button>
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
        <tr v-for="(cliente, index) in clientesFiltered" :key="index">
          <td>{{ cliente.nome }}</td>
          <td>{{ cliente.telefone }}</td>
          <td>{{ cliente.email }}</td>
          <td>             
            <button class="view-profile-btn" @click="handleClienteInfoAndRedirect(cliente)">Ver</button>          
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class=loader-container v-else></div>
  
</section>

</div>
</template>

<style scoped>
  .page-content {
    display: flex;
    flex-direction: column;
    background: #ffffff;  
  }

  .toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
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
      justify-content: space-between;
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

  .search-btn-img {
      width: 20px;
      height: 20px;
  }

  /* .search-btn:hover{
    background-color: rgb(231, 231, 231);
  } */

  .register-btn {
      width: 180px;
      height: 40px;
      margin-left: 20px;
      background: #000;
      font-size: 20px;
      border-radius: 5px;
      border-style: none;
      cursor: pointer;
      color: #ffffff;
  }

  .register-btn:hover{
      background-color: #111111;
  }

  .register-btn:active{
      background-color: #1a1a1a;
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
      font-weight: bold;
      color: hsl(263, 45%, 46%);
  }

</style>
