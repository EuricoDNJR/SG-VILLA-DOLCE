<script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore, useCargosStore } from '../utils/store';
  import { getAllRolesArray, fetchPost } from '../utils/common'
  
  const router = useRouter();
  const cellphone = ref('');
  const password = ref('');
  const message = ref('');
  const messageType = ref('info');
  const loaderIsVisible = ref(false);
  const messageIsVisible = ref(false);
  const passwordFieldType = ref("password");
  const showHideBtnText = ref('Mostrar');
  const backgroundColorVariable = ref('');
  const authStore = useAuthStore();
  const cargoStore = useCargosStore();

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

  function printMessage(msg){
      message.value = msg;
      messageIsVisible.value = true;
  }

  function printErrorMessage(msg){
    backgroundColorVariable.value = "#ff3333";
    messageType.value = "error";
    printMessage(msg);
  }

  function printLoginSuccessfulMessage(){
    backgroundColorVariable.value = "#33ff66";
    messageType.value = "success";
    printMessage("Login efetuado com sucesso", );
  }

  async function requestLogin(data){   
      let userData = null;

      loaderIsVisible.value = true;
      
      try {
        const response = await fetchPost("http://127.0.0.1:8000/v1/usuario/login/", data);
        const responseJson = await response.json();

        if(response.status === 200){
            printLoginSuccessfulMessage();
            
            userData = {
                token: responseJson.token,
                nome: responseJson.nome,
                cargo: responseJson.cargo
            };
        }else{
            printErrorMessage(responseJson.message);
        }
      } catch (error) {
        console.log(error);
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
  
    if(userData){
        authStore.successfulLogin({...userData, img: null});

        const cargos = await getAllRolesArray(userData.token);
        cargoStore.saveCargos(cargos);

        router.push('/menu/dashboard');

        console.log("User ID: " + authStore.getToken + "           Login.vue in handleLogin function");
    } 
  }

  function isMostrarBtn(){
    return showHideBtnText.value === "Mostrar";
  }

  function setMostrarBtn(){
      passwordFieldType.value = "password";
      showHideBtnText.value = "Mostrar";
  }

  function setPasswordBtn(){
      passwordFieldType.value = "text";
      showHideBtnText.value = "Ocultar";
  }

  function togglePasswordVisibility (){
      if(isMostrarBtn()){
        setPasswordBtn();
      }else{
        setMostrarBtn();
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
            <input 
              :class="{ cellphoneHasText: cellphone }"
              v-model="cellphone"
              type="text"
              maxlength="20"
              required>
            <label for="cellphone">Telefone</label>
          </div>

          <div class="input-centralize">
            <input
              :class="{ passwordHasText: password }"
              v-model="password"
              :type="passwordFieldType"
              maxlength="20" 
              required
            >
            <label for="password">Senha</label>
            
            <button  
              @mousedown.prevent
              v-show="password"
              id="show-hide-password"
              @click="togglePasswordVisibility"
              type="button"
            >
              {{ showHideBtnText }}
            </button>
          </div>
        </div>
        
        <v-alert
          :text="message"
          :type="messageType"
          variant="tonal"
          v-show="messageIsVisible"
          density="compact"
        ></v-alert>

        <v-btn
          :loading="loaderIsVisible"
          class="flex-grow-1"
          height="48"
          variant="flat"
          type="submit"
          color="grey-darken-4"
          block
          >
          Entrar
        </v-btn>
      </form>
    </div>
  </main>
</template>

<style scoped>

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

  button {
      font-size: 20px;
      border-radius: 10px;
      margin-top: 20px;
  }
</style>