<script setup>

import { ref, reactive, computed, toRaw, watch } from 'vue'
import { useAuthStore, usePessoaStore, useSnackbarStore, useCargosStore } from '../utils/store';
import { fetchPatch, fetchDelete, isEmptyObject, confirmDialog, exist, getId } from '../utils/common'


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
    return this._attrs;
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
const cargoStore = useCargosStore();

const props = defineProps(['pessoa',
                        'tipoPessoa',
                        'rotaUpdatePessoa',
                        'rotaDeletePessoa']);

savePersonInStore(props.pessoa);

const idPessoa = createIdComputed();
const atributosGerais = ref(getAtributosGerais());
const atributosEspecificos = ref(getAtributosEspecificos());
const pessoaInfoChange = new PessoaInfoChange({});
const pageWasClosed = ref(false);
const editSaveBtn = new EditSaveBtn({
    text: "Editar",
    color: "blue",
    icon: "mdi-pencil",
});
const isEditable = ref(false);


function getIdPessoa(pessoa){
    return getId(props.tipoPessoa, pessoa);
}

function createIdComputed(){
    let id = undefined;

    if(props.tipoPessoa === "Clientes"){
        id = computed(() => pessoaStore.getPessoa.idCliente);
    }else if(props.tipoPessoa === "Colaboradores"){
        id = computed(() => pessoaStore.getPessoa.idUsuario);
    }

    return id;
}

function getAtributosGerais(){
    const atributosGerais = [];

    const nome = createComputedWithGetSet("nome");
    const telefone = createComputedWithGetSet("telefone");
    const email = createComputedWithGetSet("email");
    const cpf = createComputedWithGetSet("cpf");
    const dataNascimento = createComputedWithGetSet("dataNascimento");
    const endereco = createComputedWithGetSet("endereco");

    atributosGerais.push([{
            title: "Nome",
            value: nome,
            type: "text",
        },
        {
            title: "Telefone",
            value: telefone,
            type: "text",
        }
    ]);

    atributosGerais.push([{
            title: "Email",
            value: email,
            type: "text",
        },
        {
            title: "CPF",
            value: cpf,
            type: "text",
        }
    ]);

    atributosGerais.push([{
            title: "Data de Nascimento",
            value: dataNascimento,
            type: "date",
        },
        {
            title: "Endereço",
            value: endereco,
            type: "text",
        }
    ]);

    return atributosGerais;
}

function getAtributosEspecificos(){
    const atributosEspecificos = [];

    if(props.tipoPessoa === "Clientes"){
        const saldo = computed(() => pessoaStore.getPessoa.saldo);

        atributosEspecificos.push({
            color: "green",
            icon: "mdi-currency-brl",
            title: "Saldo",
            value: saldo.value.replace('.', ','),
            isEditable: false,
            isSelect: false,
        });

        atributosEspecificos.push({
            color: "purple",
            icon: "mdi-star",
            title: "Pontos",
            value: saldoToPontos(Number(saldo.value)),
            isEditable: false,
            isSelect: false,
        });
    }else if(props.tipoPessoa === "Colaboradores"){
        const cargo = createComputedWithGetSet("cargo");

        atributosEspecificos.push({
            color: "black",
            icon: "mdi-shield-crown",
            title: "Cargo",
            value: cargo,
            isEditable: true,
            isSelect: true,
            items: cargoStore.getCargos,
        });
    }

    return atributosEspecificos;
}

function savePersonInStore(pessoa){
    let isNewPessoa = undefined;

    try{
      isNewPessoa = getIdPessoa(pessoaStore.getPessoa) != getIdPessoa(pessoa);
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
            let value = pessoaInfoChange.attrs[attr];

            if(pageWasClosed.value){
                value = pessoaStore.getOldPessoa[attr]
            }else if(!exist(value)){
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

async function ToogleEditablePessoaInfo(){
    if(editSaveBtn.isSalvarBtn()){
        isEditable.value = false;

        await updatePessoaInfo();

        pessoaInfoChange.reset();
    }else{
        isEditable.value = true;
    }

    editSaveBtn.toogle();
}

async function updatePessoaInfo(id=idPessoa.value, rota=props.rotaUpdatePessoa){
    const infoChange = toRaw(pessoaInfoChange.attrs);

    if(!isEmptyObject(infoChange)){
        try{
            const url = rota + `${id}/`;
            const body = infoChange;
            const token = authStore.getToken;   

            const response = await fetchPatch(url, body, token);
            
            if(response.status === 200){
                pessoaStore.update(infoChange);
                snackbarStore.set(`As informações do ${pessoaStore.getPessoa.nome} foram atualizadas com sucesso`, "success");
            }else{
                snackbarStore.set(`Falha ao atualizar informações do ${pessoaStore.getPessoa.nome}`, "warning");
            }
        }catch(e){
            console.log(e);
            snackbarStore.set(`Falha ao atualizar informações do ${pessoaStore.getPessoa.nome}`, "warning");
        }
    }
}

async function deletePessoa(id=idPessoa.value, rota=props.rotaDeletePessoa){
    try{
        const url = rota + `${id}/`;
        const token = authStore.getToken;
        
        const response = await fetchDelete(url, token);

        if(response.status === 200){
            pessoaStore.delete(id);
            
            snackbarStore.set(`${pessoaStore.getPessoa.nome} foi removido do sistema com sucesso`, "success");
        }else{
            snackbarStore.set(`Falha ao remover ${pessoaStore.getPessoa.nome} do sistema`, "warning");
        }
    }catch(e){
        console.log(e);
        snackbarStore.set(`Falha ao remover ${pessoaStore.getPessoa.nome} do sistema`, "warning");
    }
}

function deletePessoaConfirmation(){
    confirmDialog(`Tem certeza que deseja remover ${pessoaStore.getPessoa.nome} do sistema?`, deletePessoa);
}

function saldoToPontos(saldo){
    return Math.floor(saldo/15);
}

watch(idPessoa, (newId, oldId) => {
    pageWasClosed.value = true;
});

</script>

<template>
    <form @submit.prevent="">
        
        <v-row v-for="(atributos, i) in atributosGerais" :key="i">
            <v-col v-for="(atributo, j) in atributos" :key="j">
                <v-text-field
                    variant="underlined"
                    v-model="atributo.value"
                    :label="atributo.title"
                    :type="atributo.type"
                    hide-details="auto"
                    :readonly="!isEditable"
                ></v-text-field>
            </v-col>
        </v-row>
        
        <v-row class="mb-4"> 
            <v-col v-for="(atributo, i) in atributosEspecificos" :key="i">
                <div v-if="isEditable && atributo.isEditable">
                    <v-select v-if="atributo.isSelect"
                        v-model="atributo.value"
                        :label="atributo.title"
                        :items="atributo.items"
                        variant="underlined"
                    ></v-select>

                    <v-text-field v-else
                        v-model="atributo.value"
                        :label="atributo.title"
                        hide-details="auto"
                        variant="underlined"
                    ></v-text-field>
                </div>

                <v-card variant="tonal" :color="atributo.color" v-else>
                    <v-card-title>
                        {{ atributo.title }}
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="auto">
                                <v-icon >{{ atributo.icon }}</v-icon>
                            </v-col>
                            <v-col>
                                <h2>{{ atributo.value }}</h2>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-btn
            class="me-4"
            :color="editSaveBtn.btn.color"
            @click="ToogleEditablePessoaInfo"
            :prepend-icon="editSaveBtn.btn.icon"
        >
            {{ editSaveBtn.btn.text }}
        </v-btn>

        <v-btn
            color="red"
            @click="deletePessoaConfirmation"
            prepend-icon="mdi-delete"
        >
            Remover
        </v-btn> 
    </form>
</template>

<style scoped>
</style>
