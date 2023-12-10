<script setup>
  import { ref, reactive } from 'vue'
  import { useAuthStore } from '../store.js';

  const authStore = useAuthStore();
  let clientes = [];

  async function requestAllClientes(){
    const options = {
        method: 'GET',
        headers: {
            'jwt-token': authStore.getToken,
            'Content-Type': 'application/json'
        }
    };

    const response = await fetch("http://127.0.0.1:8000/v1/cliente/get_all_clients/", options);

    if(response.status !== 204){
        responseJson = await response.json();
        // {
        //             "idCliente": str(cliente.idCliente),
        //             "email": cliente.email if cliente.email is not None else None,
        //             "nome": cliente.nome,
        //             "dataNascimento": str(cliente.dataNascimento) if cliente.dataNascimento is not None else None,
        //             "cpf": cliente.cpf if cliente.cpf is not None else None,
        //             "endereco": cliente.endereco if cliente.endereco is not None else None,
        //             "telefone": cliente.telefone if cliente.telefone is not None else None,
        //             "saldo": str(cliente.saldo) if cliente.saldo is not None else None
        //         }
        console.log(responseJson)
    }
    
    // clientes = items.sort((a, b) => a.nome.localeCompare(b.nome));
  }
  // function geraItems(){
  //   const items = [];

  //   for(let i=0; i<30; i++){
  //     items.push({
  //       nome: `nome ${i}`,
  //       telefone: `${i}`.repeat(8),
  //       email: `nome-${i}@email.com`
  //     })
  //   }

  //   return items.sort((a, b) => a.nome.localeCompare(b.nome));
  // }
</script>

<template>
  <div class="page-content">

<!-- <a href="#"><img src="assets/cliente-lista-imgs/back-img.svg" alt=""></a> -->

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

  <div class=clients-list>
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
        <tr v-for="(cliente, index) in clientes">
          <td>{{ cliente.nome }}</td>
          <td>{{ cliente.telefone }}</td>
          <td>{{ cliente.email }}</td>
          <td>
            <button class="view-profile-btn"><a href="#">ver</a></button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
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
    margin: 20px 0px 10px 0px;
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
    text-decoration: none;
    font-weight: bold;
    color: #6940AA;
    margin: 15px 0px 15px 0px;
}
</style>
