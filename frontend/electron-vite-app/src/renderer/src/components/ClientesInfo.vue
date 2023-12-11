<script setup></script>

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
            <p id="name">John Doe</p>
        </div>

        <hr>

        <div class="info-field">    
            <label for="email">E-mail:</label>
            <p id="email">john.doe@example.com</p>
        </div>

        <hr>

        <div class="info-field">
            <label for="phone">Telefone:</label>
            <p id="phone">123-456-7890</p>
        </div>

        <hr>

        <div class="info-field">
            <label for="cpf">CPF:</label>
            <p id="cpf">123.456.789-12</p>
        </div>

        <hr>

        <div class="info-field">
            <label for="date_of_birth">Data de Nascimento:</label>
            <p id="date_of_birth">01/02/2003</p>
        </div>
            
        <hr>

        <div class="info-field">
            <label for="address">Endereço:</label>
            <p id="address">Rua sem saida</p>
        </div>

        <hr>

        <div class="info-field">
            <label for="credit">Saldo:</label>
            <p id="credit">R$ 50,00</p>
        </div>

        <hr>
    </div>

    <div class="card-field">
        <div class="card">
            <div class="card-top-area">
                <p>Villa Dolce Açai</p>
                <!-- <img src="assets/imgs/selo-img.png" alt="card stamp"> -->
            </div>
            <div class="card-main-area">
                <p>Pontos:</p>
                <span>10</span>
            </div>
        </div>
    </div>
    </div>
</template>

<style scoped>
    .page-content {
        width: 82vw;
        background: #ffffff;
        padding: 50px;
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
        margin: 35px 0px 10px 0px;
    }
    /*
    .toolbar button {
        width: 100px;
        height: 40px;
        background: #000;
        color: #ffffff;
        font-size: 20px;
        border-radius: 5px;
        border-style: none;
        cursor: pointer;
    }
    */
    #edit-btn {
        width: 100px;
        height: 40px;
        background: #16c09849;
        font-size: 18px;
        border-radius: 5px;
        border-style: solid;
        border-color: #119a7a;
        cursor: pointer;
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
        width: 100%;
        height: 40%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .card {
        background: linear-gradient(166deg, #6940AA 45%, #ACC0FE 100%);
        width: 500px;
        height: 300px;
        padding: 25px;
        border-radius: 15px;
        color: #ffffff;
        font-size: 25px;
        font-weight: bold;
    }

    .card-top-area {
        display: flex;
        justify-content: space-between;
    }

    .card-main-area {
        display: flex;
    }

    .card-main-area span {
        margin-left: 55px;
        font-size: 140px;
    }

</style>
