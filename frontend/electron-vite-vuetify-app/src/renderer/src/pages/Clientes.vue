<script setup>
  import { ref, reactive, computed, toRaw, watch, onMounted } from 'vue'
  import { fetchGet, fetchPost, fetchPatch, fetchDelete, getAuthToken, getCargoUser, setMessageSnackbar, createCelula, isEmptyObject, confirmDialog, exist } from '../utils/common'
  import Snackbar from '../components/Snackbar.vue';
  import Pessoas from '../components/Pessoas.vue';
  
  defineOptions({
    inheritAttrs: false
  });

  const clientes = ref([]);
  const configs = ref([
    [createCelula('nome', 'Nome', 'text', true), createCelula('telefone', 'Telefone', 'text', true)],
    [createCelula('email', 'Email', 'text'), createCelula('cpf', 'CPF', 'text')],
  ]);

  if(getCargoUser() == "Admin"){
    configs.value.push([createCelula('dataNascimento', 'Data de Nascimento', 'date'), createCelula('saldo', 'Saldo', 'number', true)])
    configs.value.push([createCelula('endereco', 'Endereço', 'text')]);
  }else{
    configs.value.push([createCelula('dataNascimento', 'Data de Nascimento', 'date'), createCelula('endereco', 'Endereço', 'text')])
  }

  const loadingBtn = reactive({
    cadastrarCliente: false,
  });
  

  async function requestAllClientes(){
    try{
      const url = "http://127.0.0.1:8000/v1/cliente/get_all_clients/";
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          clientes.value = responseJson;
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar clientes", 'warning');
    }
  }

  async function requestCadastrarCliente(body){
    loadingBtn.cadastrarCliente = true;

    try{
        const url = "http://127.0.0.1:8000/v1/cliente/create_client/";
        const token = getAuthToken();

        if(getCargoUser() != "Admin"){
          body.saldo = "0.00";
        }
        
        const response = await fetchPost(url, body, token);
        const responseJson = await response.json();
        
        if(response.status === 201){       
            Object.assign(body, responseJson);    

            adicionarCliente(body);

            setMessageSnackbar("Cliente cadastrado com sucesso", 'success');
        }else{
            setMessageSnackbar(responseJson.message, 'warning');
        }
    }catch(e){
        console.log(e);
        setMessageSnackbar("Falha ao cadastrar cliente", 'warning');
    }        

    loadingBtn.cadastrarCliente = false;
  }

  async function updatePessoaInfo(id=idPessoa.value, rota=props.rotaUpdatePessoa){
    const infoChange = toRaw(pessoaInfoChange.attrs);

    if(!isEmptyObject(infoChange)){
        try{
            const url = rota + `${id}/`;
            const body = infoChange;
            const token = authStore.getToken;   

            const response = await fetchPatch(url, body, token);
            const responseJson = await response.json();
            
            if(response.status === 200){
                pessoaStore.update(infoChange);
                snackbarStore.set(`As informações do ${pessoaStore.getPessoa.nome} foram atualizadas com sucesso`, "success");
            }else{
                snackbarStore.set(responseJson.message, "warning");
            }
        }catch(e){
            console.log(e);
            snackbarStore.set(`Falha ao atualizar informações do ${pessoaStore.getPessoa.nome}`, "warning");
        }
    }
  }

  async function requestRemoverCliente(cliente){
      try{
        const url = `http://127.0.0.1:8000/v1/cliente/delete_cliente/${cliente.idCliente}/`;
        const token = getAuthToken();

        const response = await fetchDelete(url, token);
        const responseJson = await response.json();

        if(response.status === 200){
          removerCliente(cliente.idCliente);
            
          setMessageSnackbar(`${cliente.nome} foi removido do sistema com sucesso`, "success");
        }else{
          setMessageSnackbar(responseJson.message, "warning");
        }
      }catch(e){
        console.log(e);
        setMessageSnackbar(`Falha ao remover ${cliente.nome} do sistema`, "warning");
      }
  }

  function removerClienteConfirmation(cliente){
    confirmDialog(`Tem certeza que deseja remover ${cliente.nome} do sistema?`, () => requestRemoverCliente(cliente));
  }

  function adicionarCliente(body){
    const cliente = {
      idCliente: body.uuid,
      nome:  body.nome,
      telefone:  body.telefone,
      cpf:  body.cpf,
      dataNascimento:  body.dataNascimento,
      email:  body.email,
      endereco:  body.endereco,
      saldo:  body.saldo,
    };

    clientes.value.push(cliente);
  }

  function removerCliente(id){
    clientes.value = clientes.value.filter((cliente) => cliente.idCliente != id);
  }

  onMounted(() => {
    requestAllClientes();
  });
</script>

<template>
    <Snackbar/>

    <Pessoas
      title="Clientes"
      :pessoas="clientes"
      registerTitle="Cadastrar Cliente"
      :loadingBtnRegister="loadingBtn.cadastrarCliente"
      :configs="configs"
      :fixies="[]"
      @cadastrarPessoa="requestCadastrarCliente"
      @removerPessoa="removerClienteConfirmation"
    />
    <!-- rotaUpdatePessoa="http://127.0.0.1:8000/v1/cliente/update_cliente/" -->
</template>

<style scoped>
</style>
