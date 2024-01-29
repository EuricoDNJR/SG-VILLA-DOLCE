<script setup>
    import { ref, reactive, computed, watch } from 'vue'
    import CardForm from './CardForm.vue'

    const props = defineProps(['title', 'loadingBtn', 'configs', 'fixies']);
    const emit = defineEmits(['cadastrarPessoa']);

    const loadingBtn = computed(() => props.loadingBtn);

    const eventFunctions = {
        fechar: () => isVisible.dialogCadastrarPessoa = false,
        cadastrar: (body) => {
            emit('cadastrarPessoa', body);
        },
    };
    const customBtns = ref([
        {text: 'Fechar', variant: 'text', icon: undefined, color: undefined, clickEvent: 'fechar', needFormData: false, loading: false},
        {text: 'Cadastrar', variant: 'flat', icon: 'mdi-account-plus', color: 'blue-darken-1', clickEvent: 'cadastrar', needFormData: true, loading: false},
    ]);

    const btnCadastrar = customBtns.value[1];

    const isVisible = reactive({
        dialogCadastrarPessoa: false,
    });

    function btnClicked({event, body}){
        const func = eventFunctions[event];

        if(body){
            func(body);
        }else{
            func();
        }   
    }

    function openDialog(){
        isVisible.dialogCadastrarPessoa = true;
    }

    watch(loadingBtn, (newValue, oldValue) => {
        btnCadastrar.loading = newValue;
    });
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
            :customBtns="customBtns"
            @clicked="btnClicked"
        />
    </v-dialog>
</template>

<style scoped>
</style>
