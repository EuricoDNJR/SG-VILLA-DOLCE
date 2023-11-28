function getDadosLoginForm(){
    const cellphone = document.getElementById("cellphone");
    const password = document.getElementById("password");

    return {
        telefone: cellphone.value,
        senha: password.value
    };
}

function formatDadosLogin(data){
    const formatedData = {...data};

    formatedData.telefone = data.telefone.replace(/\D/g, '');

    return formatedData;
}

function resetErrorMessage(){
    const errorMessageElement = document.getElementById("error-message");

    errorMessageElement.style.display = "none";
}

function printErrorMessage(message){
    const errorMessageElement = document.getElementById("error-message");

    errorMessageElement.textContent = "*" + message;
    errorMessageElement.style.display = "block";
}

async function requestLogin(data){   
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

        printErrorMessage(responseJson.message);
    }else{
        // window.location.href = "http://127.0.0.1:5500/SG-VILLA-DOLCE/frontend/dashboard/dashboard.html";
        // REDIRECIONAR PARA PÁGINA DASHBOARD
        // PRECISO DE ALGUNS DADOS DO USUÁRIO -> NOME, CARGO e IMAGEM
    }
}

function handleLogin(event){
    event.preventDefault();
    resetErrorMessage();

    data = getDadosLoginForm();

    formatedData = formatDadosLogin(data);

    if(formatedData.telefone === "" || formatedData.senha === ""){
        printErrorMessage("Preencha os campos de telefone e senha");
    }else{
        requestLogin(formatedData);
    }
}

// EVENTS LISTENERS
const btn = document.getElementById("btn");

btn.addEventListener("click", handleLogin);
