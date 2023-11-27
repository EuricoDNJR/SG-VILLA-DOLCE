const btn = document.getElementById("btn");
btn.addEventListener("click", callRequestLogin);

function trataDadosLogin(){
    const cellphone = document.getElementById("cellphone");
    const password = document.getElementById("password");

    // TRATAR DADOS AQUI

    return {
        telefone: cellphone.value,
        senha: password.value
    };
}

async function requestLogin(){   
    const data = trataDadosLogin();

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    };

    response = await fetch("http://127.0.0.1:8000/v1/usuario/login/", options);

    if(!response.ok){
        const responseJson = await response.json();

        const errorMessageElement = document.getElementById("error-message");

        errorMessageElement.textContent = responseJson.message;
        errorMessageElement.style.display = "block";
    }else{
        // USUÁRIO AUTORIZADO
        // REDIRECIONAR PARA PÁGINA DASHBOARD
        // PRECISO DE ALGUNS DADOS DO USUÁRIO -> NOME, CARGO e IMAGEM
    }
}

function callRequestLogin(event){
    event.preventDefault();
    
    requestLogin();
}