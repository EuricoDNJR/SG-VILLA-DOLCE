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

    const response = await fetch("http://127.0.0.1:8000/v1/usuario/login/", options);
    const responseJson = await response.json();

    if(!response.ok){
        printErrorMessage(responseJson.message);
    }else{
        document.location.href = `http://127.0.0.1:5500/frontend/dashboard/dashboard.html?nome=${responseJson.nome}&cargo=${responseJson.cargo}`;

        // SAVE TOKEN IN COOKIES
        // responseJson.token
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

function showHidePassword(event){
    const btn = event.target;
    const inputPassword = document.getElementById("password");

    if(btn.textContent === "Mostrar"){
        inputPassword.type = "text";
        btn.textContent = "Ocultar";
    }else{
        inputPassword.type = "password";
        btn.textContent = "Mostrar";
    }
}

// EVENTS LISTENERS
const btnSubmitForm = document.getElementById("btn");
const btnShowHidePassword = document.getElementById("show-hide-password");

btnSubmitForm.addEventListener("click", handleLogin);
btnShowHidePassword.addEventListener("click", showHidePassword);

