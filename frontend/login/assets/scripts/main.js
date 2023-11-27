const btn = document.getElementById("btn");
btn.addEventListener("click", requestLogin);

function trataDadosLogin(){
    const cellphone = document.getElementById("cellphone");
    const password = document.getElementById("password");
    
    // TRATAR DADOS AQUI 

    return {
        "telefone": cellphone.value,
        "senha": password.value,
    };
}

function requestLogin(){
    const data = trataDadosLogin();

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),  
    };

    fetch("http://127.0.0.1:8000/v1/usuario/login/", options).then(
        (response) => {
            if(!response.ok){
                // APRESENTAR NA TELA A FALHA NO LOGIN
                if(response.status == 404){
                    // USUÁRIO NÃO ENCONTRADO
                    throw new Error(`${response.status} ${response.statusText}`);
                }else if(response.status == 401){
                    // USUÁRIO NÃO AUTORIZADO
                    throw new Error(`${response.status} ${response.statusText}`);
                }else{
                    // FALHA NO LOGIN
                    throw new Error(`${response.status} ${response.statusText}`);
                }
            }else{
                // USUÁRIO AUTORIZADO
                // REDIRECIONAR PARA PÁGINA DASHBOARD
                // PRECISO DE ALGUNS DADOS DO USUÁRIO -> NOME, CARGO e IMAGEM
            }
        })
}
