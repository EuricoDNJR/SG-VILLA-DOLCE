<script setup>
    import { reactive, ref } from 'vue'
    import { useAuthStore, useFuncionarioStore } from '../store.js';
    import { useRouter } from 'vue-router';

    const authStore = useAuthStore();
    const router = useRouter();
    const funcionarioStore = useFuncionarioStore();
    const nome = ref(funcionarioStore.getNome);
    const email = ref(funcionarioStore.getEmail);
    const telefone = ref(funcionarioStore.getTelefone);
    const cpf = ref(funcionarioStore.getCpf);
    const dataNascimento = ref(funcionarioStore.getDataNascimento);
    const endereco = ref(funcionarioStore.getEndereco);
    const cargo = ref(funcionarioStore.getCargo);
    const editSaveBtnText = ref('Editar');
    const isEditable = ref(false);

    async function updateFuncionarioInfo(rotaAPI){
        const data = getFuncionarioInfoChange(funcionarioStore);

        if(!isEmpty(data)){
            funcionarioStore.updateFuncionarioInfo(data);
            const validatedData = onlyValidateData(data);

            const options = {
                method: 'PATCH',
                headers: {
                    'jwt-token': authStore.getToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(validatedData)
            };

            const response = await fetch(`http://127.0.0.1:8000/v1/${rotaAPI}/`, options);
        }
    }

    function ToogleEditableInfo(){
        if(editSaveBtnText.value === "Editar"){
            isEditable.value = true;
            editSaveBtnText.value = "Salvar";
        }else{
            updateFuncionarioInfo(`usuario/update_user/${funcionarioStore.getIdUsuario}`);
            
            isEditable.value = false;
            editSaveBtnText.value = "Editar";
        }
    }

    async function deleteRequest(rotaAPI, rotaPAGE){
        const options = {
            method: 'DELETE',
            headers: {
                'jwt-token': authStore.getToken,
                'Content-Type': 'application/json'
            }
        };

        const response = await fetch(`http://127.0.0.1:8000/v1/${rotaAPI}/`, options);

        if(response.status === 200){
            router.push(rotaPAGE);
        }
        
    }

    function deleteFuncionarioConfirmation(){
        if(window.confirm('Tem certeza que deseja prosseguir?')){
            deleteRequest(`usuario/delete_user/${funcionarioStore.getIdUsuario}`, 
                              "/menu/funcionarios/");
        }
    }

    function getFuncionarioInfoChange(store){
        let data = {};
        
        if(nome.value != store.getNome){
            data.nome = nome.value ;
        }
        if(email.value != store.getEmail){
            data.email = email.value;
        }
        if(telefone.value != store.getTelefone){
            data.telefone = telefone.value ;
        }
        if(cpf.value != store.getCpf){
            data.cpf = cpf.value ;
        }
        if(dataNascimento.value != store.getDataNascimento){
            data.dataNascimento = dataNascimento.value;
        }
        if(endereco.value != store.getEndereco){
            data.endereco = endereco.value;
        }
        if(cargo.value != store.getCargo){
            data.cargo = cargo.value;
        }

        return data;
    }

    function onlyValidateData(data){
        return data;
    }

    function isEmpty(obj) {
        return Object.keys(obj).length === 0;
    }

   
</script>

<template>
   <div class="page-content">
        <!-- <a href="#"><img src="assets/imgs/back-img.svg" alt=""></a> -->

        <div id="cliente-info">
            
            <div class="toolbar">
                <h1>Colaborador</h1>

                <div>
                    <button class="edit-btn" @click="ToogleEditableInfo" :class="{saveBtn: isEditable}">{{ editSaveBtnText }}</button>
                    <button class="delete-btn" @click="deleteFuncionarioConfirmation">Apagar</button>
                </div>
            </div>
            
            <hr>

            <div class="info-field">
                <label for="name">Nome:</label>
                <input id="name" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="nome">
            </div>

            <hr>

            <div class="info-field">    
                <label for="email">E-mail:</label>
                <input id="email" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="email">
            </div>

            <hr>

            <div class="info-field">
                <label for="phone">Telefone:</label>
                <input id="phone" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="telefone">
            </div>

            <hr>

            <div class="info-field">
                <label for="cpf">CPF:</label>
                <input id="cpf" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="cpf">
            </div>

            <hr>

            <div class="info-field">
                <label for="date_of_birth">Data de Nascimento:</label>
                <input id="date_of_birth" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="dataNascimento">
            </div>
                
            <hr>

            <div class="info-field">
                <label for="address">Endereço:</label>
                <input id="address" :class="{ editableItem: isEditable }" :readonly="!isEditable" v-model="endereco">
            </div>

            <hr>

            <div class="info-field">
                <label for="cargo">Cargo:</label>
                
                <p id="cargo">{{ cargo }}</p>
            </div>

            <hr>
        </div>
        
    </div>
</template>

<style scoped>
    .page-content {
        display: flex;
        flex-direction: column;
        background: #ffffff;  
    }
    hr {
        height: 2px;
        border-width: 0px;
        background-color: #EEEEEE;
    }

    .toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .edit-btn {
        width: 100px;
        height: 40px;
        background: #16c09849;
        font-size: 18px;
        border-radius: 5px;
        border-style: solid;
        border-color: #119a7a;
        cursor: pointer;
        margin-right: 5px;
        color: #119a7a;
        font-weight: bold;
    }

    .delete-btn {
        width: 100px;
        height: 40px;
        background: #df04044d;
        font-size: 18px;
        border-radius: 5px;
        border-style: solid;
        border-color: #DF0404;
        cursor: pointer;
        color: #DF0404;
        font-weight: bold;
    }

    .saveBtn {
        background-color: #267fec49;
        border-color: #177cbf;
        color: #177cbf;
    }

    .info-field {
        display: flex;
        margin: 10px 0px 10px 0px;
    }

    .info-field label {
        font-weight: bold;
        font-size: 20px;
    }

    .info-field input {
        display: block;
        font-size: 20px;
        margin-left: 10px;
        border: none;
        flex: 1;
    }

    .info-field p {
        font-size: 20px;
        margin-left: 10px;
    }

    .editableItem{
        background-color: rgb(237, 237, 237);
        border: 1px solid black;
    }
</style>
