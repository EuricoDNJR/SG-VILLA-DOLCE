<script setup>
import { ref } from 'vue'
import { useAuthStore, usePessoaStore, useSnackbarStore, useCargosStore } from '../utils/store';
import { fetchPost } from '../utils/common';


const props = defineProps(['tipoPessoa',
                        'urlRegisterPessoa']);

const authStore = useAuthStore();
const pessoaStore = usePessoaStore();
const snackbarStore = useSnackbarStore();
const cargoStore = useCargosStore();
const cargos = cargoStore.getCargos;
const dialogIsVisible = ref(false);

const nome = ref('');
const senha = ref('');
const telefone = ref('');
const email = ref('');
const cpf = ref('');
const dataNascimento = ref('');
const endereco = ref('');
const cargo = ref(cargos[0]);

const nomeError = ref(false);
const senhaError = ref(false);
const telefoneError = ref(false);
const emailError = ref(false);
const cpfError = ref(false);
const dataNascimentoError = ref(false);
const enderecoError = ref(false);

const atributos = ref(getAtributos());

const loading = ref(false);

const tooltipText = getTooltipText();

function getAtributos(){
    const atributos = [];

    if(props.tipoPessoa === "Clientes"){
        atributos.push([{
                title: "Nome",
                value: nome,
                type: "text",
                error: nomeError
            },
            {
                title: "Telefone",
                value: telefone,
                type: "text",
                error: telefoneError
            }
        ]);

        atributos.push([{
                title: "Email",
                value: email,
                type: "text",
                error: emailError
            },
            {
                title: "CPF",
                value: cpf,
                type: "text",
                error: cpfError
            }
        ]);

        atributos.push([{
                title: "Data de Nascimento",
                value: dataNascimento,
                type: "date",
                error: dataNascimentoError
            },
            {
                title: "Endereço",
                value: endereco,
                type: "text",
                error: enderecoError
            }
        ]);
    }else if(props.tipoPessoa === "Colaboradores"){
        atributos.push([{
                title: "Nome",
                value: nome,
                type: "text",
                error: nomeError
            },
            {
                title: "senha",
                value: senha,
                type: "text",
                error: senhaError
            }
        ]);

        atributos.push([{
                title: "Telefone",
                value: telefone,
                type: "text",
                error: telefoneError
                
            },
            {
                title: "Email",
                value: email,
                type: "text",
                error: emailError
            }
        ]);

        atributos.push([{
                title: "CPF",
                value: cpf,
                type: "text",
                error: cpfError
            },
            {
                title: "Data de Nascimento",
                value: dataNascimento,
                type: "date",
                error: dataNascimentoError
            },
        ]);

        atributos.push([{
                title: "Endereço",
                value: endereco,
                type: "text",
                error: enderecoError
            },
            {
                title: "Cargo",
                value: cargo,
                type: "select",
                items: cargoStore.getCargos,
            }
        ]);
    }

    return atributos;
}

function getTooltipText(){
    let tooltipText = undefined;

    if(props.tipoPessoa === "Clientes"){
        tooltipText = "Cliente";
    }else if(props.tipoPessoa === "Colaboradores"){
        tooltipText = "Colaborador";
    }

    return tooltipText
}

function isValidPessoa(pessoa){
    let isValid = undefined

    if(props.tipoPessoa === "Clientes"){
        nomeError.value = (pessoa.nome.length <= 0);
        telefoneError.value = (pessoa.telefone.length <= 0);

        isValid = !(nomeError.value || telefoneError.value);
    }else if(props.tipoPessoa === "Colaboradores"){
        nomeError.value = (pessoa.nome.length <= 0);
        senhaError.value = (pessoa.senha.length <= 0);
        telefoneError.value = (pessoa.telefone.length <= 0);
        emailError.value = (pessoa.email.length <= 0);
        cpfError.value = (pessoa.cpf.length <= 0);
        dataNascimentoError.value = (pessoa.dataNascimento.length <= 0);
        enderecoError.value = (pessoa.endereco.length <= 0);

        isValid = !(nomeError.value || 
                    senhaError.value ||
                    telefoneError.value ||
                    emailError.value ||
                    cpfError.value  ||
                    dataNascimentoError.value ||
                    enderecoError.value);
    }
    
    return isValid;
}

function emptyStringToNull(string){
    let newValue = null;

    if(string.length > 0){
        newValue = string;
    }

    return newValue;
}

function createPessoa(){
    let pessoa = undefined;

    if(props.tipoPessoa === "Clientes"){
        pessoa = {
            nome: nome.value, 
            telefone: telefone.value, 
            email: email.value, 
            cpf: cpf.value, 
            dataNascimento: dataNascimento.value,
            endereco: endereco.value,
            saldo: 0,
        };
    }else if(props.tipoPessoa === "Colaboradores"){
        pessoa = {
            nome: nome.value, 
            senha: senha.value,
            telefone: telefone.value, 
            email: email.value, 
            cpf: cpf.value, 
            dataNascimento: dataNascimento.value,
            endereco: endereco.value,
            cargo: cargo.value,
        };
    }

    
    if(isValidPessoa(pessoa)){
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

    const pessoa = createPessoa();

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

function closeDialog(){
    dialogIsVisible.value = false;
    nome.value  = '';
    email.value  = '';
    telefone.value  = '';
    cpf.value  = '';
    dataNascimento.value  = '';
    endereco.value = '';
    senha.value = '';
    cargo.value = cargos[0];
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
                <v-icon> mdi-account-plus</v-icon> 
                <v-tooltip 
                    activator="parent"
                    location="bottom">
                Cadastrar {{ tooltipText }}
                </v-tooltip>
            </v-btn>
        </template>

        <v-card>
            <v-card-title>
                <span class="text-h5">Cadastrar {{ tooltipText }}</span>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <v-container>
                    <v-row v-for="(atributosPar, i) in atributos" :key="i">
                        <v-col v-for="(atributo, i) in atributosPar" :key="i">
                            <v-text-field v-if="atributo.type !== 'select'"
                                v-model="atributo.value"
                                :label="atributo.title"
                                :type="atributo.type"
                                :rules="[value => !!value || 'Campo obrigatório.']"
                                :error-messages="atributo.error ? ['Campo obrigatório.'] : []"
                                hide-details="auto"
                                required
                            ></v-text-field>
                            <v-select v-else
                                v-model="atributo.value"
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
