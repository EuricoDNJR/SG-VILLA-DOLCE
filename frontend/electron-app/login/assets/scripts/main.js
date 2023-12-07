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
    const MessageElement = document.getElementById("message");

    MessageElement.style.display = "none";
}

function printMessage(message, backgroundColor){
    const MessageElement = document.getElementById("message");

    MessageElement.textContent = message;
    MessageElement.style.backgroundColor = backgroundColor;
    MessageElement.style.display = "block";
}

function printErrorMessage(message){
    printMessage("*" + message, "#ff3333");
}

function printLoginSuccessfulMessage(){
    printMessage("Login efetuado com sucesso", "#33ff66");
}

async function requestLogin(data){   
    // document.body.style.cursor = "progress";
    const loaderElement = document.getElementById("loader");
    loaderElement.style.display = "block";

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    };

    const response = await fetch("http://127.0.0.1:8000/v1/usuario/login/", options);
    const responseJson = await response.json();

    loaderElement.style.display = "none";

    if(!response.ok){
        printErrorMessage(responseJson.message);

        return null;
    }else{
        printLoginSuccessfulMessage();
        
        const userData = {
            token: responseJson.token,
            nome: responseJson.nome,
            cargo: responseJson.cargo
        };

        return userData;
        // document.body.style.cursor = "default";
    }
}

async function handleLogin(event){
    resetErrorMessage();

    data = getDadosLoginForm();

    formatedData = formatDadosLogin(data);

    if(formatedData.telefone === "" || formatedData.senha === ""){
        printErrorMessage("Preencha os campos de telefone e senha");
    }else{
        userData = await requestLogin(formatedData);

        // const userData = {
        //     token: "gd4fsd-0e9-af",
        //     nome: "Eurico Delmondes do Nascimento Junior",
        //     cargo: "Dev Back-END"
        // };

        if(userData){
            window.ipcRenderer.setUserDataCookie(userData).then(() => {
                    window.ipcRenderer.successfulLogin("dashboard/dashboard.html");
            });
        } 
    }
}

function togglePasswordVisibility (){
    const btn = this;
    const inputPassword = document.getElementById("password");

    if(btn.textContent === "Mostrar"){
        inputPassword.type = "text";
        btn.textContent = "Ocultar";
    }else{
        inputPassword.type = "password";
        btn.textContent = "Mostrar";
    }
}

function toggleShowHidePasswordButton(){
    const password = this.value;
    const showHideButton = document.getElementById('show-hide-password');
    
    if(password){
        showHideButton.style.display = 'block';
    }else{
        showHideButton.style.display = 'none';
    }
}

// EVENTS LISTENERS
const btnSubmitForm = document.getElementById("btn");
const btnShowHidePassword = document.getElementById("show-hide-password");
const inputPassword = document.getElementById("password");

btnSubmitForm.addEventListener("click", (event) => {
    event.preventDefault();
    handleLogin()
});
btnShowHidePassword.addEventListener("click", togglePasswordVisibility);
inputPassword.addEventListener("input", toggleShowHidePasswordButton);
