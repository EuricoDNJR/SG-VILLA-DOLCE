<script setup>
import { ref, toRaw } from 'vue'
import { useAuthStore, usePessoaStore, useSnackbarStore, useCargosStore } from '../utils/store';
import { fetchPost } from '../utils/common';
import { isValidCliente, createCliente, createAtributosCliente } from '../utils/cliente';
import { isValidColaborador, createColaborador, createAtributosColaborador } from '../utils/colaborador';


const props = defineProps(['tipoPessoa',
                        'urlRegisterPessoa',
                        'tooltipText']);

const authStore = useAuthStore();
const pessoaStore = usePessoaStore();
const snackbarStore = useSnackbarStore();
const cargoStore = useCargosStore();
const cargos = cargoStore.getCargos;

const dialogIsVisible = ref(false);

const isValidPessoa = {Clientes: isValidCliente, Colaboradores: isValidColaborador};
const createPessoa = {Clientes: createCliente, Colaboradores: createColaborador};
const createAtributos = {Clientes: createAtributosCliente, Colaboradores: createAtributosColaborador};

const atributos = ref(createAtributos[props.tipoPessoa]());

const loading = ref(false);


function emptyStringToNull(string){
    let newValue = null;

    if(string.length > 0){
        newValue = string;
    }

    return newValue;
}

function getPessoa(){
    let pessoa = createPessoa[props.tipoPessoa](toRaw(atributos.value));

    if(isValidPessoa[props.tipoPessoa](toRaw(atributos.value), pessoa)){
        pessoa.email = emptyStringToNull(pessoa.email);
        pessoa.cpf = emptyStringToNull(pessoa.cpf);
        pessoa.dataNascimento = emptyStringToNull(pessoa.dataNascimento);
        pessoa.endereco = emptyStringToNull(pessoa.endereco);
    }else{
        pessoa = null;
    }

    return pessoa;
}

async function requestRegisterPessoa(url=props.urlRegisterPessoa){
    loading.value = true;

    const pessoa = getPessoa();

    if(pessoa){
        try{
            const body = pessoa;
            const token = authStore.getToken;

            const response = await fetchPost(url, body, token);

            if(response.status === 201){
                const responseJson = await response.json();
                
                if(props.tipoPessoa === "Clientes"){
                    pessoa.idCliente = responseJson.uuid;
                }else if(props.tipoPessoa === "Colaboradores"){
                    pessoa.idUsuario = responseJson.uuid;
                }
                
                pessoaStore.create(pessoa);

                snackbarStore.set("Cadastro realizado com sucesso", 'success');
            }else{
                snackbarStore.set("Falha no cadastro", 'warning');
            }
            
        }catch(e){
            console.log(e);
            snackbarStore.set("Falha no cadastro", 'warning');
        }        
    }

    loading.value = false;
}

function openDialog(){
    dialogIsVisible.value = true;
}

function closeDialog(){
    dialogIsVisible.value = false;
    atributos.value = createAtributos[props.tipoPessoa]();
}

</script>

<template>
    <v-btn
        v-bind="props"
        color="blue"
        variant="flat"
        icon="mdi-plus"
        @click="openDialog"
    >
        <v-icon> mdi-account-plus</v-icon> 
        <v-tooltip 
            activator="parent"
            location="bottom">
        Cadastrar {{ props.tooltipText }}
        </v-tooltip>
    </v-btn>
    <v-dialog 
        v-model="dialogIsVisible"
        persistent
        width="1024"
    >
       <v-card>
            <v-card-title>
                <span class="text-h5">Cadastrar {{ props.tooltipText }}</span>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <v-container>
                    <v-row v-for="(atributosPar, i) in atributos" :key="i">
                        <v-col v-for="(atributo, i) in atributosPar" :key="i">
                            <v-text-field v-if="atributo.type !== 'select'"
                                v-model="atributo.obj"
                                :label="atributo.title"
                                :type="atributo.type"
                                :rules="[value => !!value || 'Campo obrigatório.']"
                                :error-messages="atributo.error ? ['Campo obrigatório.'] : []"
                                hide-details="auto"
                                required
                            ></v-text-field>
                            <v-select v-else
                                v-model="atributo.obj"
                                :label="atributo.title"
                                :items="atributo.items"
                            >   
                            </v-select>
                        </v-col>
                    </v-row>
                </v-container>
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
                    prepend-icon="mdi-account-plus"
                    @click="() => requestRegisterPessoa()"
                    :loading="loading"
                >
                    Cadastrar
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<style scoped>
</style>
