import { ref } from 'vue'
import { useAuthStore, useSnackbarStore } from '../utils/store';


export function getAuthToken(){
    const authStore = useAuthStore();
    
    return authStore.getToken;
}

export function getCargoUser(){
    const authStore = useAuthStore();
    
    return authStore.getCargo;
}

export function setAuthNomeECargo(nome, cargo){
    const authStore = useAuthStore();
    
    if(nome){
        authStore.setNome(nome);
    }
    if(cargo){
        authStore.setCargo(cargo);
    }
}

export function setMessageSnackbar(msg, messageType){
    const snackbarStore = useSnackbarStore();
    
    snackbarStore.set(msg, messageType);
}

function createFetchOptions(methodName, contentType, token=undefined, body=undefined){
    const options = {
        method: methodName,
        headers: {
            'Content-Type': contentType
        }
    }

    if(token){
        options.headers['jwt-token'] = token;
    }

    if(body){
        options.body = JSON.stringify(body);
    }

    return options;
}

export function fetchGet(url, token=undefined){
    const methodName = 'GET';
    const contentType = 'application/json';

    const options = createFetchOptions(methodName, contentType, token);

    return fetch(url, options);
}

export function fetchPost(url, body, token=undefined){
    const methodName = 'POST';
    const contentType = 'application/json';

    const options = createFetchOptions(methodName, contentType, token, body);

    return fetch(url, options);
}

export function fetchPatch(url, body, token=undefined){
    const methodName = 'PATCH';
    const contentType = 'application/json';

    const options = createFetchOptions(methodName, contentType, token, body);

    return fetch(url, options);
}

export function fetchDelete(url, token=undefined){
    const methodName = 'DELETE';
    const contentType = 'application/json';

    const options = createFetchOptions(methodName, contentType, token);

    return fetch(url, options);
}

async function fetchAllRoles(token){
    const url = "http://127.0.0.1:8000/v1/cargo/get_all_roles/";
    const fetchResponse = await fetchGet(url, token);
    let allRolesJson = null;

    try{
        const responseJson = await fetchResponse.json();

        allRolesJson = responseJson;
    }catch(e){
        console.log(e);
    }

    return allRolesJson;
}

export async function getAllRolesArray(token){
    const cargos = [];

    const fetchResponse = await fetchAllRoles(token)
    
    if(fetchResponse){
        fetchResponse.forEach((cargoObj) => {
            cargos.push(cargoObj.nome);
        });
    }

    return cargos;
}

export function replaceNullToEmptyString(obj){
    const newObj = {...obj};

    for (let chave in newObj) {
      if (newObj[chave] === null) {
        newObj[chave] = "";
      }
    }

    return newObj
}

export function isEmptyObject(obj) {
    return Object.keys(obj).length === 0;
}

export function confirmDialog(msg, callback){
    window.ipcRenderer.confirmDialog(msg).then((isYes) => {
        if(isYes){
            callback();
        }
    });
}

export function exist(value){
    return (value !== undefined) && (value !== null);
}

export function emptyStringToNull(string){
    let newValue = null;

    if(string.length > 0){
        newValue = string;
    }

    return newValue;
}

export function getObjByKeys(obj, keys){
    keys.forEach((key, i) => {
        obj = obj[key];
    });
    
    return obj;
}

export function createCelula({key, title, type, required, initialValue, isEditable, card, readonly, variant}){
    title = (title != undefined) ? title : key;
    type = (type != undefined) ? type : 'text';
    required = (required != undefined) ? required : false;
    initialValue = (initialValue != undefined) ? initialValue : '';
    isEditable = (isEditable != undefined) ? isEditable : true;
    readonly = (readonly != undefined) ? readonly : false;

    return {'key': key, 'title': title, 'type': type, 'required': required, 'initialValue': initialValue, 'isEditable': isEditable, 'card': card, 'readonly': readonly, 'variant': variant};
}

export function createFormFields(configs, fixies=[]){
    const fieldsArray = [];
    const fieldsObj = {};

    configs.forEach((linhaForm, i) => {
        fieldsArray.push([]);
        
        linhaForm.forEach((celulaForm) => {
            const obj = {
                key: celulaForm.key,
                title: celulaForm.title,
                obj: ref(celulaForm.initialValue),
                type: celulaForm.type,
                error: ref(false),
                required: celulaForm.required,
                isEditable: celulaForm.isEditable,
                card: celulaForm.card,
                readonly: celulaForm.readonly,
                variant: celulaForm.variant,
            };

            fieldsObj[celulaForm.title] = obj;
            fieldsArray[i].push(obj);
        });
    });
    
    fixies.forEach((linhaFix, i) => {
        const keysStr = linhaFix[0];
        const newValue = linhaFix[1];

        const keys = keysStr.split('.');
        const key = keys.pop();

        const obj = getObjByKeys(fieldsObj, keys);

        obj[key] = newValue;
    });

    return [fieldsObj, fieldsArray];
}

export function getFormatedDate(date){
    if(date){
        return date.replace(/^(\d{4})-(\d{2})-(\d{2})$/, '$3/$2/$1');
    }
    
    return null;
}

export function getColorQuantidade(quantidade){
  let color = "black";
  
  if(quantidade > 0){
    color = "green";
  }else if(quantidade < 0){
    color = "red";
  }

  return color;
}