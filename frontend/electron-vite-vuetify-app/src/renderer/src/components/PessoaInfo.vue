<script setup>
import { ref } from 'vue'
import { isEmptyObject } from '../utils/common'
import CardForm from './CardForm.vue'

const props = defineProps(['pessoa', 'configs', 'fixies', 'loadingCardUpdate']);
const emit = defineEmits(['atualizarPessoa', 'removerPessoa']);

const reloadVar = ref(false);

const configs = props.configs;
configs.forEach(configArray => {
    configArray.forEach(celula => {
        const initialValue = props.pessoa[celula.key];
        
        celula.initialValue = initialValue ? initialValue : '';
    });
});

const eventFunctions = {
    editar: () => {
        configs.forEach(configArray => {
            configArray.forEach(celula => {
                if(celula.isEditable){
                    celula.readonly = false;
                }
            });
        });

        setSalvarBtn();

        reload();
    },
    salvar: (body) => {
        const pessoaInfosChange = infosChangesPessoa(body);

        if(!isEmptyObject(pessoaInfosChange)){
            emit('atualizarPessoa', props.pessoa, pessoaInfosChange);
        }

        configs.forEach(configArray => {
            configArray.forEach(celula => {               
                celula.readonly = true;
            });
        });
        
        setEditarBtn();
        
        reload();
    },
    remover: () => emit('removerPessoa', props.pessoa),
};

const customBtns = ref([
    {text: 'Editar', variant: 'flat', icon: 'mdi-pencil', color: 'blue-darken-1', clickEvent: 'editar', needFormData: false},
    {text: 'Remover', variant: 'flat', icon: 'mdi-delete', color: 'red-darken-1', clickEvent: 'remover', needFormData: false},
]);
const editSaveBtn = customBtns.value[0];

function setSalvarBtn(){
    editSaveBtn.text = 'Salvar';
    editSaveBtn.icon = 'mdi-content-save';
    editSaveBtn.color = 'green-darken-1';
    editSaveBtn.clickEvent = 'salvar';
    editSaveBtn.needFormData = true;
}

function setEditarBtn(){
    editSaveBtn.text = 'Editar';
    editSaveBtn.icon = 'mdi-pencil';
    editSaveBtn.color = 'blue-darken-1';
    editSaveBtn.clickEvent = 'editar';
    editSaveBtn.needFormData = false;
}

function btnClicked({event, body}){
    const func = eventFunctions[event];

    if(body){
        func(body);
    }else{
        func();
    }   
}

function infosChangesPessoa(body){
    const pessoa = {};

    for(let key in body){
        if(props.pessoa[key] != body[key]){
            pessoa[key] = body[key];
        }
    }

    return pessoa;
}

function reload(){
    reloadVar.value = !reloadVar.value;
}
</script>

<template>
    <div :key="reloadVar">
        <CardForm 
            :configs="configs"
            :fixies="props.fixies"
            :customBtns="customBtns"
            @clicked="btnClicked"
            :loadingCard="props.loadingCardUpdate"
        />
    </div>
</template>

<style scoped>
</style>
