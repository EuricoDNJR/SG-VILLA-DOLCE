<script setup>
import { ref, toRaw } from 'vue'
import { createFormFields, emptyStringToNull } from '../utils/common';
import { useAuthStore, useSnackbarStore, useFormStore } from '../utils/store';
import { fetchPost } from '../utils/common';


const props = defineProps(['title', 'url', 'configs', 
                        'fixies', 'btnText', 'btnIcon',
                        'successMessage', 'errorMessage']);

const authStore = useAuthStore();
const snackbarStore = useSnackbarStore();
const formStore = useFormStore();

let [fieldsObj, formFields] = createFormFields(
    props.configs,
    props.fixies,
);
formFields = ref(formFields);

const dialogIsVisible = ref(false);
const loading = ref(false);


function isValid(){
    let isValidReturn = true;

    for(let title in fieldsObj){
        if(fieldsObj[title].required){
            fieldsObj[title].error.value = (fieldsObj[title].obj.value.length <= 0);
        }
        if(fieldsObj[title].error.value){
            isValidReturn = false;
        }
    }

    return isValidReturn;
}

function create(){
    const something = {};

    for(let title in fieldsObj){
        something[fieldsObj[title].key] = fieldsObj[title].obj.value.trim();
    }
    
    return something;
}

function get(){
    let something = null;

    if(isValid()){
        something = create();

        for(let key in something){
            something[key] = emptyStringToNull(something[key]);
        }
    }

    return something;
}

async function requestPost(url=props.url){
    loading.value = true;

    const body = get();
    console.log(formFields.value);
    if(body){
        try{
            const token = authStore.getToken;
            
            const response = await fetchPost(url, body, token);

            if(response.status === 201){
                const responseJson = await response.json();

                Object.assign(body, responseJson);
                
                formStore.send(props.title, body);
                
                snackbarStore.set(props.successMessage, 'success');
            }else{
                snackbarStore.set(props.errorMessage, 'warning');
            }
            
        }catch(e){
            console.log(e);
            snackbarStore.set(props.errorMessage, 'warning');
        }        
    }

    loading.value = false;
}
function openDialog(){
    dialogIsVisible.value = true;
}

function closeDialog(){
    dialogIsVisible.value = false;

    for(let title in fieldsObj){
        if(fieldsObj[title].type != "select"){
            fieldsObj[title].obj.value = "";
        }
            
        fieldsObj[title].error.value = false;
    }
}
</script>

<template>
    <v-btn
        variant="text"
        :prepend-icon="props.btnIcon"
        stacked
        @click="openDialog"
    >
        {{ props.title }}
    </v-btn>
    <v-dialog 
        v-model="dialogIsVisible"
        persistent
        width="1024"
    >
        <v-card>
            <v-card-title>
                <span class="text-h5">{{ props.title }}</span>
            </v-card-title>

            <v-divider></v-divider>

            <v-card-text>
                <v-container>
                    <v-row v-for="(formLine, i) in formFields" :key="i">
                        <v-col v-for="(field, j) in formLine" :key="i">
                            <v-text-field v-if="field.type !== 'select'"
                                v-model="field.obj"
                                :label="field.title"
                                :type="field.type"
                                :error-messages="field.error ? ['Campo obrigatório.'] : []"
                                hide-details="auto"
                            ></v-text-field>
                            <v-select v-else
                                v-model="field.obj"
                                :label="field.title"
                                :items="field.items"
                                :item-title="field.itemsTitle"
                                :item-value="field.itemsValue"
                                :error-messages="field.error ? ['Campo obrigatório.'] : []"
                                hide-details="auto"
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
                    :prepend-icon="props.btnIcon"
                    :loading="loading"
                    @click="() => requestPost()"
                >
                    {{ props.btnText }}
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<style scoped>
</style>
