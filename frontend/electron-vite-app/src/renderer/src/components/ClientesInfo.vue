<script setup>

import { reactive, ref } from 'vue'
import { useAuthStore, useClienteStore, useSnackbarStore } from '../utils/store';
import { fetchPatch, fetchDelete, isEmptyObject } from '../utils/common'
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const clienteStore = useClienteStore();
const snackbarStore = useSnackbarStore();
const nome = ref(clienteStore.getNome);
const email = ref(clienteStore.getEmail);
const telefone = ref(clienteStore.getTelefone);
const cpf = ref(clienteStore.getCpf);
const dataNascimento = ref(clienteStore.getDataNascimento);
const endereco = ref(clienteStore.getEndereco);
const saldo = ref(clienteStore.getSaldo);
const pontos = ref(clienteStore.getPontos);
const editSaveBtnText = ref('Editar');
const isEditable = ref(false);

function getClienteInfoChange(){
    let data = {};
    
    if(nome.value != clienteStore.getNome){
        data.nome = nome.value ;
    }
    if(email.value != clienteStore.getEmail){
        data.email = email.value;
    }
    if(telefone.value != clienteStore.getTelefone){
        data.telefone = telefone.value ;
    }
    if(cpf.value != clienteStore.getCpf){
        data.cpf = cpf.value ;
    }
    if(dataNascimento.value != clienteStore.getDataNascimento){
        data.dataNascimento = dataNascimento.value;
    }
    if(endereco.value != clienteStore.getEndereco){
        data.endereco = endereco.value;
    }

    return data;
}

async function updateClienteInfo(){
    const data = getClienteInfoChange();

    if(!isEmptyObject(data)){
        try{
            clienteStore.updateClienteInfo(data);

            const url = `http://127.0.0.1:8000/v1/cliente/update_cliente/${clienteStore.getIdCliente}/`;
            const body = data;
            const token = authStore.getToken;

            const response = await fetchPatch(url, body, token);
            
            if(response.status === 200){
                snackbarStore.snackbar("As informações do cliente foram atualizadas com sucesso", 'green');
            }else{
                snackbarStore.snackbar("Falha ao atualizar informações do cliente", 'red');
            }
        }catch(e){
            console.log(e);
            snackbarStore.snackbar("Falha ao atualizar informações do cliente", 'red');
        }
           
    }
}

function isEditarbtn(){
    return editSaveBtnText.value === "Editar"
}

function setSalvarBtn(){
    isEditable.value = true;
    editSaveBtnText.value = "Salvar";
}

function setEditarBtn(){
    isEditable.value = false;
    editSaveBtnText.value = "Editar";
}   

function ToogleEditableClienteInfo(){
    if(isEditarbtn()){
        setSalvarBtn();
    }else{
        updateClienteInfo();
        
        setEditarBtn();
    }
}

async function deleteCliente(){
    try{
        const url = `http://127.0.0.1:8000/v1/cliente/delete_cliente/${clienteStore.getIdCliente}/`;
        const token = authStore.getToken;
        
        const response = await fetchDelete(url, token);

        if(response.status === 200){
            snackbarStore.snackbar("Cliente deletado com sucesso", 'green');
            router.push("/menu/clientes/");
        }else{
            snackbarStore.snackbar("Falha ao deletar cliente", 'red');
        }
    }catch(e){
        console.log(e);
        snackbarStore.snackbar("Falha ao deletar cliente", 'red');
    }
}

function deleteClienteConfirmation(){
    if(window.confirm('Tem certeza que deseja prosseguir?')){
        deleteCliente();
    }
}

</script>

<template>
   <div class="page-content">
        <!-- <a href="#"><img src="assets/imgs/back-img.svg" alt=""></a> -->

        <div id="cliente-info">
            
            <div class="toolbar">
                <h1>Cliente</h1>

                <div>
                    <button class="edit-btn" @click="ToogleEditableClienteInfo" :class="{saveBtn: isEditable}">{{ editSaveBtnText }}</button>
                    <button class="delete-btn" @click="deleteClienteConfirmation">Apagar</button>
                </div>
            </div>
            
            <hr>

            <div class="info-field">
                <label for="name">Nome:</label>
                <input id="name" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="nome">
            </div>

            <hr>

            <div class="info-field">    
                <label for="email">E-mail:</label>
                <input id="email" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="email">
            </div>

            <hr>

            <div class="info-field">
                <label for="phone">Telefone:</label>
                <input id="phone" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="telefone">
            </div>

            <hr>

            <div class="info-field">
                <label for="cpf">CPF:</label>
                <input id="cpf" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="cpf">
            </div>

            <hr>

            <div class="info-field">
                <label for="date_of_birth">Data de Nascimento:</label>
                <input id="date_of_birth" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="dataNascimento">
            </div>
                
            <hr>

            <div class="info-field">
                <label for="address">Endereço:</label>
                <input id="address" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="endereco">
            </div>

            <hr>

            <div class="info-field">
                <label for="credit">Saldo:</label>
                <p id="credit">R$ {{ saldo.replace('.', ',') }}</p>
            </div>

            <hr>
        </div>

        <div class="card-field">
            <div class="card">
                <div class="card-top-area">
                    <h3 class="card-title">Villa Dolce Açai</h3>
                    <img src="../assets/clientes-info-imgs/selo-img.png" alt="card stamp">
                </div>
                <div class="card-main-area">
                    <p>Pontos:</p>
                    <span>{{ pontos }}</span>
                </div>
            </div>
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

    .toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .edit-btn {
        width: 100px;
        height: 40px;
        background: #16c09849;
        font-size: 18px;
        border-radius: 5px;
        border-style: solid;
        border-color: #119a7a;
        cursor: pointer;
        margin-right: 5px;
        color: #119a7a;
        font-weight: bold;
    }

    .delete-btn {
        width: 100px;
        height: 40px;
        background: #df04044d;
        font-size: 18px;
        border-radius: 5px;
        border-style: solid;
        border-color: #DF0404;
        cursor: pointer;
        color: #DF0404;
        font-weight: bold;
    }

    .saveBtn {
        background-color: #267fec49;
        border-color: #177cbf;
        color: #177cbf;
    }

    .info-field {
        display: flex;
        margin: 10px 0px 10px 0px;
    }

    .info-field label {
        font-weight: bold;
        font-size: 20px;
    }

    .info-field input {
        display: block;
        font-size: 20px;
        margin-left: 10px;
        border: none;
        flex: 1;
    }

    .info-field p {
        font-size: 20px;
        margin-left: 10px;
    }

    .editableItem{
        background-color: rgb(237, 237, 237);
        border: 1px solid black;
    }

    .card-field {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 10px 0px 10px 0px;
    }

    .card {
        background: linear-gradient(264deg, rgba(65, 2, 165, 0.60) 26.97%, rgba(3, 23, 203, 0.60) 100%);
        width: 32vw;
        height: 33vh;
        padding: 15px;
        border-radius: 15px;
        color: #ffffff;
        font-size: 25px;
        font-weight: bold;
        position: relative;
    }

    .card h3{
        font-size: 1.25rem;
    }

    .card img{
        top: 0px;
        right: 0px;
        position: absolute;
        width: 3vw;
        height: auto;
    }

    .card-top-area{
        position: relative;
    }

    .card-main-area{
        position: relative;
        top: 50%;
        transform: translateY(-60%);
        text-align: center;
    }

    .card p{
        display: inline-block;
        position: absolute;
        font-size: 1.2rem;
        top: 0px;
        left: 0px;
    }

    .card span{
        display: inline;
        font-size: 6rem;
        top: 0px;
    }

</style>
