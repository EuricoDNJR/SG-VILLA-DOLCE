<script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '../store.js';
  
  const router = useRouter();
  const cellphone = ref('');
  const password = ref('');
  const message = ref('');
  const loaderIsVisible = ref(false);
  const messageIsVisible = ref(false);
  const passwordFieldType = ref("password");
  const showHideBtnText = ref('Mostrar');
  const backgroundColorVariable = ref('');
  const authStore = useAuthStore()

  function getDadosLoginForm() {
    return {
          telefone: cellphone.value,
          senha: password.value
      };
  }

  function formatDadosLogin(data) {
    const formatedData = { ...data };

    formatedData.telefone = data.telefone.replace(/\D/g, '');

    return formatedData;
  }

  function resetMessage() {
    messageIsVisible.value = false;
  }

  function printMessage(msg,){
      message.value = msg;
      messageIsVisible.value = true;
  }

  function printErrorMessage(msg){
    backgroundColorVariable.value = "#ff3333";
    printMessage("*" + msg);
  }

  function printLoginSuccessfulMessage(){
    backgroundColorVariable.value = "#33ff66";
    printMessage("Login efetuado com sucesso", );
  }

  async function requestLogin(data){   
      let userData = null;

      loaderIsVisible.value = true;
      
      try {
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
            printLoginSuccessfulMessage();
            
            userData = {
                token: responseJson.token,
                nome: responseJson.nome,
                cargo: responseJson.cargo
            };
        }
      } catch (error) {
        printErrorMessage("Erro inesperado, tente novamente");
      }

      loaderIsVisible.value = false;

      return userData;
  }

  async function handleLogin() {
    resetMessage();

    const data = getDadosLoginForm();
    
    const formatedData = formatDadosLogin(data);

    const userData = await requestLogin(formatedData);

    // const userData = {
    //     token: "gd4fsd-0e9-af",
    //     nome: "Eurico Delmondes do Nascimento Junior",
    //     cargo: "Dev Back-END"
  
    // };
  
    if(userData){
        authStore.successfulLogin({...userData, img: null});

        router.push('/menu/dashboard');
    } 
  }

  function togglePasswordVisibility (){
      if(showHideBtnText.value === "Mostrar"){
          passwordFieldType.value = "text";
          showHideBtnText.value = "Ocultar";
      }else{
          passwordFieldType.value = "password";
          showHideBtnText.value = "Mostrar";
      }
  }
</script>

<template>
  <main>
    <div class="left-box">
      <img src="../assets/login-imgs/logo-villa-dolce.jpeg" alt="logo">
    </div>

    <div class="right-box">
      <form @submit.prevent="handleLogin">
        <h1>Login</h1>

        <div class="input-field">
          <div class="input-centralize">
            <input :class="{ cellphoneHasText: cellphone }" v-model="cellphone" type="text" maxlength="20" required>
            <label for="cellphone">Telefone</label>
          </div>

          <div class="input-centralize">
            <input :class="{ passwordHasText: password }" v-model="password" :type="passwordFieldType" maxlength="20" required>
            <label for="password">Senha</label>
            <button  @mousedown.prevent v-show="password" id="show-hide-password" @click="togglePasswordVisibility" type="button">{{ showHideBtnText }}</button>
          </div>
        </div>

        <div class="message-box">
          <p v-show="loaderIsVisible" id="loader"></p>
          <p v-show="messageIsVisible" id="message" :style="{ backgroundColor: backgroundColorVariable}">{{ message }}</p>
        </div>

        <button type="submit">Entrar</button>
      </form>
    </div>
  </main>
</template>

<style scoped>
  @keyframes spin {
      0% {
          transform: rotate(0deg);
      }
      100% {
          transform: rotate(360deg);
      }
  }

  main {
    background: linear-gradient(to right, #ffffff 40%, #6940AA);
      display: flex;
      justify-content: space-around;
      align-items: center;
      width: 100vw;
      height: 100vh;;
  }

  form {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column
  }

  h1 {
      font-size: 40px;
  }

  .left-box img{
      width: 50vw;
      height: auto;
      max-height: 100vh;
      mix-blend-mode: multiply;
  }

  .right-box{
      background-color: white;
      padding: 1.5vw 2.5vw 2.5vw 2.5vw;
      border-radius: 0.25em;
      box-shadow: 0px 2px 2px 1px rgba(0, 0, 0, 0.45);
  }

  .input-field {
      display: flex;
      flex-direction: column;
      margin: 30px 0 5px 0;
  }

  .input-centralize{
      position: relative;
      margin-bottom: 10px;
  }

  .input-field label {
      position: absolute;
      left: 17px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 25px;
      font-weight: 500;
      color: rgb(95, 95, 95);
      transition: all 0.3s;
      pointer-events: none;
  }

  .input-field input {
      width: 320px;
      height: 50px;
      border-radius: 10px;
      border-color: rgb(95, 95, 95);
      border-style: solid;
      outline: none;
      padding: 5px;
      font-size: 20px;
      font-weight: 500;
      padding: 15px 25% 0px 15px;
      transition: all 0.3s;
  }

  .input-field input:focus + label, .cellphoneHasText + label, .passwordHasText + label{
      transform: translate(-25%, -85%) scale(0.5);
      color: rgb(102, 12, 185);
  }

  .input-field input:hover{
      border-color: #000;
  }

  .input-field input:focus, .input-field .cellphoneHasText, .input-field .passwordHasText{
      border-color: rgb(102, 12, 185);
  }

  #show-hide-password{
      all: unset;
      position: absolute;
      font-size: 1.2em;
      right: 4%;
      top: 50%;
      transform: translateY(-50%);
      color:rgb(28, 28, 28);
      cursor: pointer;
  }

  #show-hide-password:hover{
      color:rgb(124, 124, 124);
  }

  #message{
      color: #eaeaea;
      border-radius: 0.2rem;
      padding: 10px 5px;
  }

  #loader {
      border: 4px solid rgba(0, 0, 0, 0.1);
      border-top: 4px solid #333;
      border-radius: 50%;
      width: 30px;
      height: 30px;
      animation: spin 1s linear infinite; /* Aplica a animação */
  }

  button {
      width: 320px;
      height: 50px;
      background: #000;
      color: #ffffff;
      font-size: 25px;
      border-radius: 10px;
      border-style: none;
      margin-top: 20px;
  }

  button:hover{
      background-color: #111111;
  }

  button:active{
      background-color: #1a1a1a;
  }
</style>