<script setup>
import { ref, reactive } from 'vue'
import CardForm from './CardForm.vue'

const props = defineProps(['title', 'loadingBtn', 'configs', 'fixies']);
const emit = defineEmits(['cadastrarPessoa']);

const isVisible = reactive({
    dialogCadastrarPessoa: false,
});

function emitCadastrarPessoa(body){
    emit('cadastrarPessoa', body);
}

function openDialog(){
    isVisible.dialogCadastrarPessoa = true;
}

</script>

<template>
    <v-btn
        v-bind="props"
        color="blue-darken-1"
        variant="flat"
        icon="mdi-plus"
        @click="openDialog"
    >
        <v-icon> mdi-account-plus</v-icon> 
        <v-tooltip 
            activator="parent"
            location="bottom"
        >
            {{ props.title }}
        </v-tooltip>
    </v-btn>
    
    <v-dialog 
        v-model="isVisible.dialogCadastrarPessoa"
        persistent
        width="1024"
    >
        <CardForm
            :title="props.title"
            :configs="props.configs"
            :fixies="props.fixies"
            btnText="Cadastrar"
            btnIcon="mdi-account-plus"
            btnColor="blue-darken-1"
            :loading="props.loadingBtn"
            @submit="emitCadastrarPessoa"
            @close="isVisible.dialogCadastrarPessoa = false"
        />
    </v-dialog>
</template>

<style scoped>
</style>
