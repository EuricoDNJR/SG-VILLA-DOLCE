<script setup>

    import { ref, computed } from 'vue';
    import { fetchPost, fetchPatch } from '../utils/common';
    import { useAuthStore, useSnackbarStore, useCaixaStore } from '../utils/store';

    const authStore = useAuthStore();
    const snackbarStore = useSnackbarStore();
    const caixaStore = useCaixaStore();
    const somenteDinheiro = ref('0.00');
    const saldoTotal = ref('0.00');
    
    const caixaStatus = computed(() => caixaStore.getStatus);
    const saldoInicial = ref(caixaStore.getSaldoInicial);
    const observacoes = ref(caixaStore.getObservacoes);
    const caixaAction = computed(() => caixaStore.getAction);
    const caixaIsOpen = computed(() => caixaStatus.value === 'aberto');
    const dataEHoraAbertura = computed(() => caixaStore.getDataAbertura + " " + caixaStore.getHoraAbertura);

    function createCaixaInfo(){
        const caixaInfo = {
            saldoInicial: saldoInicial.value,
            observacoes: observacoes.value,
        };

        return caixaInfo;
    }

    async function requestOpenCaixa(body){
        let responseJson = null;

        try{
            const url = 'http://127.0.0.1:8000/v1/caixa/open_caixa/';
            const token = authStore.getToken;

            const response = await fetchPost(url, body, token);

            if(response.status === 200){
                responseJson = await response.json();
            }else{
                snackbarStore.snackbar("Falha ao abrir caixa", 'red');
            }
        }catch(e){
            console.log(e);
            snackbarStore.snackbar("Falha ao abrir caixa", 'red');
        }

        return responseJson;
    }
    
    async function requestCloseCaixa(){
        try{
            const url = `http://127.0.0.1:8000/v1/caixa/close_caixa/${caixaStore.getId}/`;
            const body = {};
            const token = authStore.getToken;

            const response = await fetchPatch(url, body, token);

            if(response.status === 200){
                const responseJson = await response.json();
            }else{
                snackbarStore.snackbar("Falha ao fechar caixa", 'red');
            }
        }catch(e){
            console.log(e);
            snackbarStore.snackbar("Falha ao fechar caixa", 'red');
        }
    }

    function openCaixa(){
        const caixaInfo = createCaixaInfo();

        requestOpenCaixa(caixaInfo).then((responseJson) => {
            if(responseJson){
                caixaStore.saveOpenCaixa(responseJson);
            }
        })
    }

    function resetCaixaInfo(){
        saldoInicial.value = caixaStore.getSaldoInicialResetValue;
        observacoes.value = caixaStore.getObservacoesResetValue;
    }

    function closeCaixa(){
        requestCloseCaixa();

        caixaStore.resetCaixa();

        resetCaixaInfo();
    }

    function toggleCaixaStatus(){
        if(caixaIsOpen.value){
            if(window.confirm('Fechar o caixa')){
                closeCaixa();
            }
        }else{
            if(window.confirm('Abrir o caixa')){
                openCaixa();
            }
        }
    }

</script>

<template>
   <div class="page-content">
        <section class="main-content">
            <form @submit.prevent="toggleCaixaStatus">
                <div>
                    <h1 :class="{caixaAberto: caixaIsOpen}" id="caixa-status">Caixa {{ caixaStatus }}</h1>
                    
                    <label for="opening-balance">Saldo inicial(dinheiro):</label>
                    <input v-model="saldoInicial" :disabled="caixaIsOpen" type="number" min="0" step=".01" required>
                    
                    <label for="observation">Observação:</label>
                    <textarea v-model="observacoes" :disabled="caixaIsOpen" name="observation" id="observation"></textarea>

                    <div v-show="caixaStatus === 'aberto'">
                        <label for="opening-time">Data/Hora de abertura:</label>
                        <p id="opening-time">{{ dataEHoraAbertura }}</p>
                    </div>
                </div>
                    
                <button id="caixa-btn">{{ caixaAction }} caixa</button>
            </form>

            <div v-show="caixaIsOpen" class="caixa-list">
                <div class="responsive-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Data/Hora</th>
                                <th>Descrição</th>
                                <th>Entrada</th>
                                <th>Saída</th>
                                <th>Pagamento</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>05/12/2023 15:03</td>
                                <td>Saldo inicial</td>
                                <td>R$ 100,00</td>
                                <td>R$ 000,00</td>
                                <td>Dinheiro</td>
                            </tr>
                        </tbody>   
                    </table>
                </div>
                
                <div class="balance-box">
                    <p><b>Somente dinheiro:</b> R$ {{ somenteDinheiro.replace('.', ',') }}</p>
                    <p><b>Saldo final:</b> R$ {{ saldoTotal }}</p>
                </div>
            </div>
        </section>
    </div>
</template>


<style scoped>

/* .page-content {
    display: flex;
    flex-direction: column;
    background: #ffffff;  
  } */

    .main-content {
        display: flex;
        height: 90%;
        margin-bottom: 10px;
    }

    form {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border-right: 1px solid;
        padding-right: 12px;
    }

    form div {
        display: flex;
        flex-direction: column;
    }

    form h1 {
        padding: 12px;
        text-align: center;
        background: #c0161649;
        color: #9a1111;
        border-radius: 5px;
        /* cursor: pointer */
    }

    .caixaAberto{
        background: #16c09849;
        color: #119a7a;
    }

    form label {
        font-weight: bold;
        font-size: 18px;
        margin: 20px 0px 10px 0px;
    }

    form input, form textarea {
        border: solid;
        border-width: 2px;
        border-radius: 5px;
        font-size: 18px;
        padding: 8px;
        outline: none;
    }

    form input {
        height: 40px;
    }

    form textarea {
        resize: none;
        height: 150px;
    }

    form button {
        background: #000;
        color: #ffffff;
        font-size: 18px;
        border-radius: 5px;
        border-style: none;
        cursor: pointer;
        padding: 15px 30px;
        margin-top: 20px;
    }

    form button:hover{
        background-color: #111111;
    }

    form button:active{
        background-color: #1a1a1a;
    }


    .caixa-list {
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 0 12px;
    }

    .responsive-table {
        overflow-x: auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 15px;
        text-align: left;
    }

    thead {
        top: 0;
        position: sticky;
        background-color: #D3D3D3;
    }

    th {
        padding: 12px;
        font-weight: bold;
        font-size: 18px;
    }

    th:first-child {
        border-top-left-radius: 5px;
    }

    td {
        height: 20px;
        padding: 12px;
        border-top: 1px solid;
        border-bottom: 1px solid;
        border-color: #B5B7C0;
        font-size: 18px;
    }

    .balance-box {
        display: flex;
        justify-content: space-around;
        align-items: center;
        height: 55px;
        font-size: 18px;
        background-color: #D3D3D3;
        border-radius: 0 0 5px 5px;
    }

</style>