<script setup>

import { ref } from 'vue'
import { useClienteStore } from '../store.js';

const clienteStore = useClienteStore();
const nome = ref(clienteStore.getNome);
const email = ref(clienteStore.getEmail);
const telefone = ref(clienteStore.getTelefone);
const cpf = ref(clienteStore.getCpf);
const data_nascimento = ref(clienteStore.getDataNascimento);
const endereco = ref(clienteStore.getEndereco);
const saldo = ref(clienteStore.getSaldo);
const pontos = ref(clienteStore.getPontos);

</script>

<template>
   <div class="page-content">

    <!-- <a href="#"><img src="assets/imgs/back-img.svg" alt=""></a> -->

    <div id="cliente-info">
        
        <div class="toolbar">
            <h1>Cliente</h1>

            <div>
                <button id="edit-btn"><a href="#">Editar</a></button>
                <button id="delete-btn"><a href="#">Apagar</a></button>
            </div>
        </div>
        
        <hr>

        <div class="info-field">
            <label for="name">Nome:</label>
            <p id="name">{{ nome }}</p>
        </div>

        <hr>

        <div class="info-field">    
            <label for="email">E-mail:</label>
            <p id="email">{{ email }}</p>
        </div>

        <hr>

        <div class="info-field">
            <label for="phone">Telefone:</label>
            <p id="phone">{{ telefone }}</p>
        </div>

        <hr>

        <div class="info-field">
            <label for="cpf">CPF:</label>
            <p id="cpf">{{ cpf }}</p>
        </div>

        <hr>

        <div class="info-field">
            <label for="date_of_birth">Data de Nascimento:</label>
            <p id="date_of_birth">{{ data_nascimento }}</p>
        </div>
            
        <hr>

        <div class="info-field">
            <label for="address">Endereço:</label>
            <p id="address">{{ endereco }}</p>
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

    #edit-btn {
        width: 100px;
        height: 40px;
        background: #16c09849;
        font-size: 18px;
        border-radius: 5px;
        border-style: solid;
        border-color: #119a7a;
        cursor: pointer;
        margin-right: 5px;
    }

    #delete-btn {
        width: 100px;
        height: 40px;
        background: #df04044d;
        font-size: 18px;
        border-radius: 5px;
        border-style: solid;
        border-color: #DF0404;
        cursor: pointer;
    }

    #edit-btn a {
        text-decoration: none;
        color: #119a7a;
        font-weight: bold;
    }

    #delete-btn a {
        text-decoration: none;
        color: #DF0404;
        font-weight: bold;
    }

    .info-field {
        display: flex;
        margin: 10px 0px 10px 0px;
    }

    .info-field label {
        font-weight: bold;
        font-size: 20px;
    }

    .info-field p {
        font-size: 20px;
        margin-left: 10px;
    }

    .card-field {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
    }

    .card {
        /* background: linear-gradient(166deg, #6940AA 45%, #ACC0FE 100%); */
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


/* 
    .card-top-area {
        display: flex;
        justify-content: space-between;
    }

    .card-main-area {
        display: flex;
        text-align: center;
    }

    .card-main-area span {
        margin-left: 55px;
        font-size: 110px;
    } */

</style>
