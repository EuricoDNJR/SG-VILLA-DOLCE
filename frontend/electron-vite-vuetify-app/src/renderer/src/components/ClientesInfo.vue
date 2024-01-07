<script setup>

import { ref, reactive, computed, toRaw } from 'vue'
import { useAuthStore, usePessoaStore, useSnackbarStore } from '../utils/store';
import { fetchPatch, fetchDelete, isEmptyObject, confirmDialog } from '../utils/common'

class EditSaveBtn {
  constructor(btn) {
    this._btn = reactive(btn);
  }

  get btn() {
    return this._btn;
  }

  set btn(obj) {
    for(let key in obj){
        this._btn[key] = obj[key];
    }
  }

  isEditarBtn() {
    return this.btn.text === "Editar";
  }

  isSalvarBtn(){
    return this.btn.text === "Salvar";
  }

  setSalvarBtn(){
    this.btn = {
        text: "Salvar",
        color: "green",
        icon: "mdi-content-save",
    };
  }

  setEditarBtn(){
    this.btn = {
        text: "Editar",
        color: "blue",
        icon: "mdi-pencil",
    };
  }

  toogle(){
    if(this.isEditarBtn()){
        this.setSalvarBtn();
    }else{
        this.setEditarBtn();
    }
  }
}

class PessoaInfoChange {
  constructor(attrs) {
    this._attrs = reactive(attrs);
  }

  get attrs() {
    return toRaw(this._attrs);
  }

  set attrs(obj) {
    this._attrs = reactive(obj);
  }

  setAttr(attr, valor){
    this._attrs[attr] = valor;
  }

  reset(){
    for (const key of Object.keys(this._attrs)) {
        delete this._attrs[key];
    }
  } 
}

const authStore = useAuthStore();
const pessoaStore = usePessoaStore();
const snackbarStore = useSnackbarStore();

const props = defineProps(['pessoa']);

savePersonInStore(props.pessoa);

console.log("Cliente ID: " + pessoaStore.getPessoa.idCliente + "           ClientesInfo.vue");

const idCliente = computed(() => pessoaStore.getPessoa.idCliente);
const nome = createComputedWithGetSet("nome");
const telefone = createComputedWithGetSet("telefone");
const email = createComputedWithGetSet("email");
const cpf = createComputedWithGetSet("cpf");
const dataNascimento = createComputedWithGetSet("dataNascimento");
const endereco = createComputedWithGetSet("endereco");
const saldo = computed(() => pessoaStore.getPessoa.saldo);
const pessoaInfoChange = new PessoaInfoChange({});

const editSaveBtn = new EditSaveBtn({
    text: "Editar",
    color: "blue",
    icon: "mdi-pencil",
});
const isEditable = ref(false);

function savePersonInStore(pessoa){
    let isNewPessoa = undefined;

    try{
      isNewPessoa = pessoaStore.getPessoa.idCliente != pessoa.idCliente;
    }catch{
      isNewPessoa = true
    }

    if(isNewPessoa){
      pessoaStore.setPessoa(pessoa);
    }
}

function createComputedWithGetSet(attr){
    const varComputed = computed({
        get() {
            let value = null;

            value = pessoaInfoChange.attrs[attr];

            if(!value){
                value = pessoaStore.getPessoa[attr];
            }
            
            return value;
        },
        set(newValue) {
            pessoaInfoChange.setAttr(attr, newValue);
        }
    });

    return varComputed;
}

function ToogleEditableClienteInfo(){
    if(editSaveBtn.isSalvarBtn()){
        isEditable.value = false;

        updateClienteInfo();

        pessoaInfoChange.reset();
    }else{
        isEditable.value = true;
    }

    editSaveBtn.toogle();
}

async function updateClienteInfo(id=idCliente.value){
    const infoChange = {...pessoaInfoChange.attrs};

    if(!isEmptyObject(infoChange)){
        try{
            const url = `http://127.0.0.1:8000/v1/cliente/update_cliente/${id}/`;
            const body = infoChange;
            const token = authStore.getToken;   

            const response = await fetchPatch(url, body, token);
            
            if(response.status === 200){
                console.log(infoChange);
                pessoaStore.update(infoChange);
                snackbarStore.set("As informações do cliente foram atualizadas com sucesso", "success");
            }else{
                snackbarStore.set("Falha ao atualizar informações do cliente", "error");
            }
        }catch(e){
            console.log(e);
            snackbarStore.set("Falha ao atualizar informações do cliente", "error");
        }
    }
}

async function deleteCliente(id=idCliente.value){
    try{
        const url = `http://127.0.0.1:8000/v1/cliente/delete_cliente/${id}/`;
        const token = authStore.getToken;
        
        const response = await fetchDelete(url, token);

        if(response.status === 200){
            pessoaStore.delete(id);
            
            snackbarStore.set("O cliente foi removido do sistema com sucesso", "success");
        }else{
            snackbarStore.set("Falha ao remover cliente do sistema", "warning");
        }
    }catch(e){
        console.log(e);
        snackbarStore.set("Falha ao remover cliente do sistema", "warning");
    }
}

function deleteClienteConfirmation(){
    confirmDialog("Tem certeza que deseja remover esse cliente do sistema?", deleteCliente);
}

function saldoToPontos(saldo){
    return Math.floor(saldo/15);
}

</script>

<template>
    <form @submit.prevent="">
        <v-row>
            <v-col>
                <v-text-field
                    variant="underlined"
                    v-model="nome"
                    label="Nome"
                    hide-details="auto"
                    :readonly="!isEditable"
                ></v-text-field>
            </v-col>
            <v-col>
                <v-text-field
                    variant="underlined"
                    v-model="telefone"
                    label="Número de Telefone"
                    hide-details="auto"
                    :readonly="!isEditable"
                ></v-text-field>
            </v-col>
        </v-row>

        <v-row>
            <v-col>
                <v-text-field
                    variant="underlined"
                    v-model="email"
                    label="E-mail"
                    hide-details="auto"
                    :readonly="!isEditable"
                ></v-text-field>
            </v-col>
            <v-col>
                <v-text-field
                    variant="underlined"
                    v-model="cpf"
                    label="CPF"
                    hide-details="auto"
                    :readonly="!isEditable"
                ></v-text-field>
            </v-col>
        </v-row>

        <v-row>
            <v-col>
                <v-text-field
                    variant="underlined"
                    v-model="dataNascimento"
                    label="Data de Nascimento"
                    hide-details="auto"
                    :readonly="!isEditable"
                ></v-text-field>
            </v-col>
            <v-col>
                <v-text-field
                    variant="underlined"
                    v-model="endereco"
                    label="Endereço"
                    hide-details="auto"
                    :readonly="!isEditable"
                ></v-text-field>
            </v-col>
        </v-row>
        
        <v-row class="mb-4"> 
            <v-col>
                <v-card variant="tonal" color="green">
                    <v-card-title>
                        Saldo
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="auto">
                                <v-icon >mdi-currency-brl</v-icon>
                            </v-col>
                            <v-col>
                                <h2>{{ saldo.replace('.', ',') }}</h2>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col>
                <v-card variant="tonal" color="purple">
                    <v-card-title>
                        Pontos
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="auto">
                                <v-icon>mdi-star</v-icon>
                            </v-col>
                            <v-col>
                                <h2>{{ saldoToPontos(Number(saldo)) }}</h2>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-btn
            class="me-4"
            :color="editSaveBtn.btn.color"
            @click="ToogleEditableClienteInfo"
            :prepend-icon="editSaveBtn.btn.icon"
        >
            {{ editSaveBtn.btn.text }}
        </v-btn>

        <v-btn
            color="red"
            @click="deleteClienteConfirmation"
            prepend-icon="mdi-delete"
        >
            Remover
        </v-btn> 
    </form>
</template>

<style scoped>
</style>
