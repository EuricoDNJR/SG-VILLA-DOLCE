async function loadData(){
    dados = await window.ipcRenderer.getUserDataCookie();
    
    const options = {
        method: 'GET',
        headers: {
            'jwt-token': dados.token,
            'Content-Type': 'application/json'
        }
    };

    const response = await fetch("http://127.0.0.1:8000/v1/cliente/get_all_clients/", options);

    if(response.status !== 204){
        const responseJson = await response.json();
    }
}

loadData();