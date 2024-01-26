<script setup>
import { ref } from 'vue'
import { createFormFields, emptyStringToNull } from '../utils/common';


const props = defineProps(['title', 'configs', 'fixies', 
                        'customBtns', 'loading', 'key']);
const emit = defineEmits(['clicked']);

let [fieldsObj, formFields] = createFormFields(
    props.configs,
    props.fixies,
);
formFields = ref(formFields);


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

function submitForm(){
    const body = get();

    if(body){
        emit('submit', body);
    }
}

function closeCard(){
    emit('close');
}

function emitClicked(eventClick){
    emit('clicked', eventClick);
}

</script>

<template>
    <v-card 
        :key="props.key"
        class="elevation-0"    
    >
        <div v-if="props.title">
            <v-card-title>
                <span class="text-h5">{{ props.title }}</span>
            </v-card-title>

            <v-divider></v-divider>
        </div>

        <v-card-text>
            <v-row v-for="(formLine, i) in formFields" :key="i">
                <v-col v-for="(field, j) in formLine" :key="i">
                    <v-text-field v-if="['text', 'number', 'date'].includes(field.type)"
                        v-model="field.obj"
                        :label="field.title"
                        :type="field.type"
                        :error-messages="field.error ? ['Campo obrigatório.'] : []"
                        hide-details="auto"
                    ></v-text-field>
                    <v-select v-if="field.type == 'select'"
                        v-model="field.obj"
                        :label="field.title"
                        :items="field.items"
                        :item-title="field.itemsTitle"
                        :item-value="field.itemsValue"
                        :error-messages="field.error ? ['Campo obrigatório.'] : []"
                        hide-details="auto"
                    ></v-select>
                    <v-autocomplete v-if="field.type == 'autocomplete'"
                        v-model="field.obj"
                        :label="field.title"
                        :items="field.items"
                        :item-title="field.itemsTitle"
                        :item-value="field.itemsValue"
                        :error-messages="field.error ? ['Campo obrigatório.'] : []"
                        hide-details="auto"
                    ></v-autocomplete>
                </v-col>
            </v-row>
        </v-card-text>

        <v-card-actions v-if="props.customBtns">      
            <v-spacer></v-spacer>
                  
            <v-btn v-for="(btn, i) in props.customBtns" :key="i"  
                :color="btn.color"
                :variant="btn.variant"
                :prepend-icon="btn.icon"
                @click="() => emitClicked(btn.clickEvent)"
            >
                {{ btn.text }}
            </v-btn>    
        </v-card-actions>

        <v-card-actions v-else>
            <v-spacer></v-spacer>
            
            <v-btn   
                variant="text"
                @click="closeCard"
            >
                Fechar
            </v-btn>
            
            <v-btn
                :color="props.btnColor"
                variant="flat"
                :prepend-icon="props.btnIcon"
                :loading="props.loading"
                @click="submitForm"
            >
                {{ props.btnText }}
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<style scoped>
</style>
