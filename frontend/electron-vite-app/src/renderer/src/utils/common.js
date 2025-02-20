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
    for (let chave in obj) {
      if (obj[chave] === null) {
        obj[chave] = "";
      }
    }
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
  