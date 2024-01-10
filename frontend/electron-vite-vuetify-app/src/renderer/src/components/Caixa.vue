<script setup>

    import { ref, computed, watch } from 'vue';
    import { fetchGet, fetchPost, fetchPatch, confirmDialog } from '../utils/common';
    import { useAuthStore, useSnackbarStore, useCaixaStore } from '../utils/store';
    import Snackbar from './Snackbar.vue';

    const authStore = useAuthStore();
    const snackbarStore = useSnackbarStore();
    const caixaStore = useCaixaStore();
    // const somenteDinheiro = ref(0);
    // const saldoTotal = ref(0);
    
    const isVisible = ref(false);
    const loading = ref(false);
    
    const caixaStatus = computed(() => caixaStore.getStatus);
    const saldoInicial = ref(0);
    // const caixaAction = computed(() => caixaStore.getAction);
    const caixaIsOpen = computed(() => caixaStore.getStatus === 'aberto');
    // const dataEHoraAbertura = computed(() => caixaStore.getDataAbertura + " " + caixaStore.getHoraAbertura);
    // let pedidos = undefined;

  
    function createCaixaInfo(){
        const caixaInfo = {
            saldoInicial: saldoInicial.value,
            observacoes: "",
        };
        
        return caixaInfo;
    }

    async function requestOpenCaixa(body){
        let responseJson = null;

        loading.value = true;

        try{
            const url = 'http://127.0.0.1:8000/v1/caixa/open_caixa/';
            const token = authStore.getToken;

            const response = await fetchPost(url, body, token);

            if(response.status === 200){
                responseJson = await response.json();
                snackbarStore.set("Caixa aberto com sucesso", 'success');
            }else{
                snackbarStore.set("Falha ao abrir caixa", 'warning');
            }
        }catch(e){
            console.log(e);
            snackbarStore.set("Falha ao abrir caixa", 'warning');
        }

        loading.value = false;

        return responseJson;
    }

    async function openCaixa(){
        const caixaInfo = createCaixaInfo();

        const responseJson = await requestOpenCaixa(caixaInfo);
        console.log(responseJson);
        caixaStore.saveOpenCaixa(responseJson);

        console.log("Caixa ID: " + caixaStore.getId + "         Caixa.vue in openCaixa function");

        isVisible.value = false;
    }
    
    async function requestCloseCaixa(id=caixaStore.getId){
        let responseJson = null;

        loading.value = true;

        try{
            const url = `http://127.0.0.1:8000/v1/caixa/close_caixa/${id}/`;
            const body = {};
            const token = authStore.getToken;

            const response = await fetchPatch(url, body, token);

            if(response.status === 200){
                responseJson = await response.json();
                snackbarStore.set("Caixa fechado com sucesso", 'success');
            }else{
                snackbarStore.set("Falha ao fechar caixa", 'warning');
            }
        }catch(e){
            console.log(e);
            snackbarStore.set("Falha ao fechar caixa", 'warning');
        }

        loading.value = false;

        return responseJson;
    }


    // function resetCaixaInfo({saldoInicialR, observacoesR}){
    //     saldoInicial.value = saldoInicialR;
    //     observacoes.value = observacoesR;
    // }

    async function closeCaixa(){
        const responseJson = await requestCloseCaixa();

        const resettedCaixa = caixaStore.resetCaixa();
        
        // resetCaixaInfo(resettedCaixa);

        isVisible.value = false;
    }
    
    async function requestAllCaixas(){
        let responseJson = null;
        
        try{
            const url = "http://127.0.0.1:8000/v1/caixa/get_all_caixa/";
            const token = authStore.getToken;
            
            const response = await fetchGet(url, token);

            if(response.status === 200){
                responseJson = await response.json();
            }else{
                snackbarStore.set("Falha ao carregar caixas", 'warning');
            }
        }catch(e){
            console.log(e);
            snackbarStore.set("Falha ao carregar caixas", 'warning');
        }

        return responseJson;
    }

    async function getCaixaAberto(){
        const caixas = await requestAllCaixas();
        const caixa = caixas.find((caixa) => caixa.aberto);
        console.log(caixas.filter((caixa) => caixa.aberto));
        if(caixa){
            caixaStore.saveOpenCaixa(caixa);
        }
    }
    // async function requestAllPedidos(){
    //     let responseJson = null;
        
    //     try{
    //         const url = "http://127.0.0.1:8000/v1/pedido/get_all_orders/";
    //         const token = authStore.getToken;
            
    //         const response = await fetchGet(url, token);

    //         if(response.status === 200){
    //             responseJson = await response.json();
    //         }else{
    //             snackbarStore.snackbar("Falha ao carregar pedidos", 'red');
    //         }
    //     }catch(e){
    //         console.log(e);
    //         snackbarStore.snackbar("Falha ao carregar pedidos", 'red');
    //     }

    //     return responseJson;
    // }

    // function updateSaldoFinal(){
    //     saldoTotal.value = saldoInicial.value;
    //     somenteDinheiro.value = saldoInicial.value; 

    //     pedidos.forEach((element) => {
    //         saldoTotal.value += Number(element.valorTotal);
                
    //         if(element.tipoPagamento === "Dinheiro"){
    //             somenteDinheiro.value += Number(element.valorTotal);
    //         }
    //     });
    // }

    // async function pedidosFechadosCaixa(idCaixa){
    //     if(caixaIsOpen.value){
    //         const allPedidos = await requestAllPedidos();
    //         console.log(allPedidos);
    //         pedidos = allPedidos.filter((pedido) => pedido.idCaixa === caixaStore.getId && pedido.status === "Pago");

    //         updateSaldoFinal();
            
    //         loading.value = false;
    //     }
    // }   

    function setVisible(){
        isVisible.value = true;
    }

    // pedidosFechadosCaixa(caixaStore.getId);
    getCaixaAberto();

</script>

<template>
    <Snackbar/>
    
    <v-list-item v-if="!caixaIsOpen"
        title="Abrir Caixa"
        append-icon="mdi-lock-open-variant"
        @click="setVisible"
    >
        <v-dialog 
            v-model="isVisible"
            width="300"
        >
            <v-card>
                <v-card-title>
                    <span class="text-h5">Abertura de Caixa</span>
                </v-card-title>

                <v-card-text>
                    <v-text-field
                        v-model="saldoInicial"
                        type="number"
                        label="Saldo Inicial"
                        hide-details="auto"
                        :rules="[value => !!value || 'Campo obrigatório.', value => value >= 0 || 'O valor deve ser maior ou igual a 0.']"
                        prepend-inner-icon="mdi-currency-brl"
                        required
                    ></v-text-field>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                        color="deep-purple"
                        variant="flat"
                        @click="openCaixa"
                        :loading="loading"
                    >
                        Abrir
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-list-item>

    <v-list-item v-else
        title="Fechar Caixa"
        append-icon="mdi-lock"
        @click="setVisible"
    >
        <v-dialog 
            v-model="isVisible"
            width="300"
        >
            <v-card>
                <v-card-title>
                    <span class="text-h5">Fechamento de Caixa</span>
                </v-card-title>

                <!-- <v-card-text>
                    <v-text-field
                        v-model="saldoInicial"
                        type="number"
                        label="Saldo Inicial"
                        hide-details="auto"
                        :rules="[value => !!value || 'Campo obrigatório.']"
                        prepend-inner-icon="mdi-currency-brl"
                        required
                    ></v-text-field>
                </v-card-text> -->

                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                        color="deep-purple"
                        variant="flat"
                        @click="closeCaixa"
                        :loading="loading"
                    >
                        Fechar
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-list-item>

    <!-- <v-list-item
        title="Histórico"
        append-icon="mdi-history"
        @click="setVisible"
    >
    </v-list-item> -->
</template>

<style scoped>
</style>