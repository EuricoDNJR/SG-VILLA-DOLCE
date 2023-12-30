<script setup></script>

<template>
   <div class="page-content">
        <section class="main-content">
            <div class="toolbar">

                <h1>Selecionar produtos</h1>

                <div>
                <div class="search-container">
                    <form action="#" method="get">
                    <input type="text" class="search-box" name="search" placeholder="Buscar">
                    <button type="submit" class="search-btn"><img src="../assets/search-imgs/magnifying-glass-solid.svg"
                        alt="search icone"></button>
                    </form>
                </div>
                </div>
            </div>

            <div class=clients-list>
                <table>
                <thead>
                    <tr>
                    <th>Nome</th>
                    <th>Quantidade</th>
                    <th>Preço R$</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>Açai</td>
                    <td>3Kg</td>
                    <td>45,00 </td>
                    </tr>
                    <tr>
                    <td>Açai</td>
                    <td>3Kg</td>
                    <td>45,00 </td>
                    </tr>
                    <tr>
                    <td>Açai</td>
                    <td>3Kg</td>
                    <td>45,00 </td>
                    </tr>
                    <tr>
                    <td>Açai</td>
                    <td>3Kg</td>
                    <td>45,00 </td>
                    </tr>
                    <tr>
                    <td>Açai</td>
                    <td>3Kg</td>
                    <td>45,00 </td>
                    </tr>
                    <tr>
                    <td>Açai</td>
                    <td>3Kg</td>
                    <td>45,00 </td>
                    </tr>
                    <tr>
                    <td>Açai</td>
                    <td>3Kg</td>
                    <td>45,00 </td>
                    </tr>
                </tbody>
                </table>
            </div>

            <div class=add-container>
                <label for="quant">Quantidade</label>
                <input type="number" name="qaunt" id="quant-input">
                <button id="quant-add-btn">add</button>
            </div>

            <div class="clients-func">
                <h1>Cliente</h1>

                <button id="select-client-btn" type="button">Selecionar</button>
                <button id="register-client-btn" type="button">Cadastrar</button>

            </div>

            <dialog id="modal-select-client">

                <div class="toolbar">

                <h1>Clientes</h1>

                <div>
                    <div class="search-container">
                    <form action="#" method="get">
                        <input type="text" class="search-box" name="search" placeholder="Buscar">
                        <button type="submit" class="search-btn"><img src="../assets/search-imgs/magnifying-glass-solid.svg"
                            alt="search icone"></button>
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
                    <tr>
                        <td>Mateus Assis</td>
                        <td>(225) 555-0118</td>
                        <td>mateus.assis@example.com</td>
                        <td>
                        <button class="select-client-modal-btn">selecionar</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Filipe Mateus</td>
                        <td>(225) 555-0118</td>
                        <td>filipe.mateus@example.com</td>
                        <td>
                        <button class="select-client-modal-btn">selecionar</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Lucas Lopes</td>
                        <td>(225) 555-0118</td>
                        <td>lucas.lopes@example.com</td>
                        <td>
                        <button class="select-client-modal-btn">selecionar</button>
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>
                <button id="close-modal-btn" type="button">Fechar</button>
            </dialog>

            <div>
                <h1>Forma de pagamento</h1>

                <form action="" name="form-payment-option">
                <div class="payment-option">
                    <input type="radio" name="forma-pagamento" id="pix" value="pix">
                    <label for="pix">Pix</label>
                    <input type="radio" name="forma-pagamento" id="dinheiro" value="dinheiro">
                    <label for="dinheiro">Dinheiro</label>
                    <input type="radio" name="forma-pagamento" id="cartao-credito" value="cartao-credito">
                    <label for="cartao-credito">Cartão de crédito</label>
                    <input type="radio" name="forma-pagamento" id="cartao-debito" value="cartao-debito">
                    <label for="cartao-debito">Cartão de débito</label>
                </div>

                <div>
                    <span id="total-order-value">R$ 35,64</span>
                    <button id="finish-order" type="button">Finalizar pedido</button>
                </div>
                </form>
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


    hr {
        height: 2px;
        border-width: 0px;
        background-color: #EEEEEE;
    }

    .clients-list {
        height: 29vh;
        overflow-x: auto;
    }

    .clients-list table {
        border-collapse: collapse;
        width: 100%;
        color: #333;
        font-size: 15px;
        text-align: left;
    }

    .clients-list thead {
        top: 0;
        position: sticky;
        background-color: #ffffff;
    }

    .clients-list th {
        padding: 12px 12px 12px 0px;
        color: #B5B7C0;
        font-weight: bold;
    }

    .clients-list td {
        padding: 12px 12px 12px 0px;
        border-top: 1px solid;
        border-bottom: 1px solid;
        border-color: #B5B7C0;
        font-size: 18px;
    }

    .clients-list th:first-child, td:first-child {
        width: 80%;
    }

    .clients-list th:nth-child(2), .clients-list td:nth-child(2),
    .clients-list th:nth-child(3), .clients-list td:nth-child(3) {
    text-align: center;
    }

    .add-container {
        margin: 10px 0px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 18px;
    }

    .add-container label {
        font-size: 20px;
        font-weight: bold;
        margin-right: 5px;
    }

    .add-container input {
        border: solid;
        border-width: 2px;
        border-radius: 5px;
        font-size: 18px;
        padding: 2px;
        height: 35px;
    }

    .add-container button {
        width: 40px;
        height: 35px;
        margin-left: 5px;
        background: #000;
        font-size: 15px;
        color: #ffffff;
        border-radius: 5px;
        border-style: none;
        cursor: pointer
    }

</style>
