<script setup>
import { ref } from 'vue'
import { useAuthStore, usePessoaStore, useSnackbarStore } from '../utils/store';
import { fetchPost } from '../utils/common';

const authStore = useAuthStore();
const pessoaStore = usePessoaStore();
const snackbarStore = useSnackbarStore();
const dialogIsVisible = ref(false);
const nome = ref('');
const email = ref('');
const telefone = ref('');
const cpf = ref('');
const dataNascimento = ref('');
const endereco = ref('');
const nomeError = ref(false);
const telefoneError = ref(false);

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
        saldo: 0
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
        nomeError.value = false;
        telefoneError.value = false;

        try{
            const url = "http://127.0.0.1:8000/v1/cliente/create_client/";
            const body = cliente;
            const token = authStore.getToken;

            const response = await fetchPost(url, body, token);

            if(response.status === 201){
                pessoaStore.create(cliente);
                snackbarStore.set("Cliente cadastrado com sucesso", 'success');
            }else{
                snackbarStore.set("Falha ao cadastrar cliente", 'warning');
            }
            
        }catch(e){
            console.log(e);
            snackbarStore.set("Falha ao cadastrar cliente", 'warning');
        }        
    }else{
        nomeError.value = true;
        telefoneError.value = true;
    }
}

function closeDialog(){
    dialogIsVisible.value = false;
    nome.value  = '';
    email.value  = '';
    telefone.value  = '';
    cpf.value  = '';
    dataNascimento.value  = '';
    endereco.value = '';
}

</script>

<template>
    <v-dialog 
        v-model="dialogIsVisible"
        persistent
        width="1024"
    >
        <template v-slot:activator="{ props }">
            <v-btn
                v-bind="props"
                color="blue"
                variant="flat"
                icon="mdi-plus"
            >
                <v-icon> mdi-plus</v-icon> 
                <v-tooltip 
                    activator="parent"
                    location="bottom">
                Cadastrar Cliente
                </v-tooltip>
            </v-btn>
        </template>

        <v-card>
            <v-card-title>
                <span class="text-h5">Cadastrar Cliente</span>
            </v-card-title>

            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col>
                            <v-text-field
                                v-model="nome"
                                label="Nome*"
                                hide-details="auto"
                                :rules="[value => !!value || 'Campo obrigatório.']"
                                :error="nomeError"
                                :messages="['Campo obrigatório.']" 
                                required
                            ></v-text-field>
                        </v-col>
                        <v-col>
                            <v-text-field
                                v-model="telefone"
                                label="Telefone*"
                                hide-details="auto"
                                :rules="[value => !!value || 'Campo obrigatório.']"
                                :error="telefoneError"
                                :messages="['Campo obrigatório.']" 
                                required
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col>
                            <v-text-field
                                v-model="email"
                                label="E-mail"
                                hide-details="auto"
                            ></v-text-field>
                        </v-col>
                        <v-col>
                            <v-text-field
                                v-model="cpf"
                                label="CPF"
                                hide-details="auto"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col>
                            <v-text-field
                                v-model="dataNascimento"
                                label="Data de Nascimento"
                                type="date"
                                hide-details="auto"
                            ></v-text-field>
                        </v-col>
                    
                        <v-col>
                            <v-text-field
                                v-model="endereco"
                                label="Endereço"
                                hide-details="auto"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                </v-container>
                <small>*Indica campo obrigatório</small>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn   
                    variant="text"
                    @click="closeDialog"
                >
                    Fechar
                </v-btn>
                <v-btn
                    color="blue-darken-1"
                    variant="flat"
                    @click="requestRegisterCliente"
                >
                    Cadastrar
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<style scoped>
</style>
