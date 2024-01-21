<script setup>
import { ref } from 'vue'
import { getAuthToken, setMessageSnackbar, fetchDelete} from '../utils/common';
import { useFormStore } from '../utils/store';


const props = defineProps(['title', 'autocompleteItems', 
                        'autocompleteTitle', 'autocompleteValue',
                        'url', 'btnText', 'btnIcon',
                        'successMessage', 'errorMessage']);

const formStore = useFormStore();

const autocomplete = ref('');

const dialogIsVisible = ref(false);
const loading = ref(false);

function openDialog(){
    dialogIsVisible.value = true;
}

function closeDialog(){
    dialogIsVisible.value = false;

    autocomplete.value = '';
}

async function requestDelete(rota=props.url){
    loading.value = true;

    try{
        const url = rota + `${autocomplete.value}/`
        const token = getAuthToken();
        const response = await fetchDelete(url, token);
        const responseJson = await response.json();

        if(response.status === 200){
            const idDeleted = {};

            idDeleted[props.autocompleteValue] = autocomplete.value;

            formStore.send(props.title, idDeleted);

            setMessageSnackbar(props.successMessage, 'success');

            autocomplete.value = '';
        }else{
            setMessageSnackbar(responseJson.message, 'warning');
        }
    }catch(e){
        console.log(e);
        setMessageSnackbar(props.errorMessage, 'warning');
    }        
        
    loading.value = false;
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
        width="512"
    >
        <v-card>
            <v-card-title>
                <span class="text-h5">{{ props.title }}</span>
            </v-card-title>

            <v-divider></v-divider>

            <v-card-text>
                <v-autocomplete
                    v-model="autocomplete"
                    label="Selecione"
                    :items="props.autocompleteItems"
                    :item-title="props.autocompleteTitle"
                    :item-value="props.autocompleteValue"
                ></v-autocomplete>
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
                    color="red-darken-1"
                    variant="flat"
                    :prepend-icon="props.btnIcon"
                    :loading="loading"
                    @click="() => requestDelete()"
                >
                    {{ props.btnText }}
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<style scoped>
</style>
