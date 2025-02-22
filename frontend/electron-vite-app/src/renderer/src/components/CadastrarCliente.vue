<script setup>
import { ref } from 'vue'
import { useAuthStore, useSnackbarStore } from '../utils/store';
import { fetchPost } from '../utils/common';


const authStore = useAuthStore();
const snackbarStore = useSnackbarStore();
const nome = ref('');
const email = ref('');
const telefone = ref('');
const cpf = ref('');
const dataNascimento = ref('');
const endereco = ref('');

function isValidCliente(cliente){
    return (cliente.nome.length > 0) && (cliente.telefone.length > 0);
}

function emptyStringToNull(string){
    let newValue = null;

    if(string.length > 0){
        newValue = string;
    }

    return newValue;
}

function createCliente(){
    let cliente = {
        nome: nome.value, 
        telefone: telefone.value, 
        email: email.value, 
        cpf: cpf.value, 
        dataNascimento: dataNascimento.value,
        endereco: endereco.value,
        saldo: "0"
    };
    
    if(isValidCliente(cliente)){
        cliente.email = emptyStringToNull(cliente.email);
        cliente.cpf = emptyStringToNull(cliente.cpf);
        cliente.dataNascimento = emptyStringToNull(cliente.dataNascimento);
        cliente.endereco = emptyStringToNull(cliente.endereco);
    }else{
        cliente = null;
    }

    return cliente;
}

async function requestRegisterCliente(){
    const cliente = createCliente();

    if(cliente){
        try{
            const url = "http://127.0.0.1:8000/v1/cliente/create_client/";
            const body = cliente;
            const token = authStore.getToken;

            const response = await fetchPost(url, body, token);

            if(response.status === 201){
                snackbarStore.snackbar("Cliente cadastrado com sucesso", 'green');
            }else{
                snackbarStore.snackbar("Falha ao cadastrar cliente", 'red');
            }
            
        }catch(e){
            console.log(e);
            snackbarStore.snackbar("Falha ao cadastrar cliente", 'red');
        }        
    }else{
        snackbarStore.snackbar("Os campos de nome e telefone são obrigatórios", 'red');
    }
}

</script>

<template>
    <div class="page-content">
        <!-- <a id="id-seta" href="#"><img src="assets/imgs/back-img.svg" alt=""></a> -->

        <div id="cliente-info">
            <div id="info-title">
                <h1>Cadastrar Cliente</h1>
            </div>

            <form id="info-form" @submit.prevent="requestRegisterCliente">
                <div class="info-form">
                    <label class = "text-nome" for="nome">Nome:</label>
                    <input class="label-input" v-model="nome" type="text" id="nome" name="nome" required><br>
                </div>

                <div class="info-form">
                    <label class = "text-nome" for="telefone">Telefone:</label>
                    <input class="label-input" v-model="telefone" type="tel" id="telefone" name="telefone" pattern="[0-9]{11}" placeholder="Apenas números" required><br>
                </div>


                <div class="info-form">
                    <label class = "text-nome" for="email">E-mail:</label>
                    <input class="label-input" v-model="email" type="email" id="email" name="email"><br>
                </div>

                <div class="info-form">
                    <label class = "text-nome" for="cpf">CPF:</label>
                    <input class="label-input" v-model="cpf" type="text" id="cpf" name="cpf" pattern="\d{3}\.\d{3}\.\d{3}-\d{2}" placeholder="000.000.000-00"><br>
                </div>

                <div class="info-form">
                    <label class = "text-nome" for="dataNascimento">Data de Nascimento:</label>
                    <input class="label-input" v-model="dataNascimento" type="date" id="dataNascimento" name="dataNascimento"><br>
                </div>

                <div class="info-form">
                    <label class = "text-nome" for="endereco">Endereço:</label>
                    <textarea class="label-input" v-model="endereco" id="endereco" name="endereco" rows="4"></textarea><br>
                </div>

                <button class="send-btn">Enviar</button>
            </form>
        </div>
    </div>
</template>

<style scoped>
    .page-content {
        display: flex;
        flex-direction: column;
        background: #ffffff;  
    }
    hr {
        height: 2px;
        border-width: 0px;
        background-color: #EEEEEE;
    }

    .info-title h1{
        display: block;
        text-align: center;
        font-size: 2rem;
    }

    .info-form {
        display: inline-block;
        width: 100%;
        text-align: center;
        margin-bottom: 20px;
    }

    .label-input {
        margin-top: 4px;
        font-size: 18px;
        width: 90%; /* Altere o valor conforme necessário para ajustar o tamanho */
        border-radius: 2px; /* Isso arredondará as bordas do input */
        border: 2px solid #000000;   
        padding: 5px;
    }

    #endereco {
        padding: 5px;
        resize: none;
    }

    .text-nome {
        display: inline-block;
        width: 90%;
        text-align: left;
        font-size: 18px;
    }

    #cliente-info {
        margin: auto;
        text-align: center;
        color: white;
        padding: 10px;
        max-width: 500px;
        width: 100%;
        background: linear-gradient(150deg, #6940AA,  #7A62C0, rgb(156, 169, 207) );
        border-radius: 10px;
        margin-bottom: 10px;
    }

    #info-title {
        margin-bottom: 20px;
        color: black;
    }

    .send-btn{
      width: 90%;
      height: 40px;
      background: #000000;
      font-size: 20px;
      border-radius: 5px;
      border-style: none;
      cursor: pointer;
      color: #ffffff;
    }

    .send-btn:hover{
        background-color: #111111;
    }

    .send-btn:active{
        background-color: #1a1a1a;
    }

</style>
