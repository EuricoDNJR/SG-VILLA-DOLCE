<script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { fetchGet, fetchPost, fetchPatch, fetchDelete, getAuthToken, getCargoUser, setMessageSnackbar, createCelula, confirmDialog } from '../utils/common'
  import Snackbar from '../components/Snackbar.vue';
  import Pessoas from '../components/Pessoas.vue';
  
  defineOptions({
    inheritAttrs: false
  });

  const clientes = ref([]);
  const configsRegister = ref([
    [createCelula({key:'nome', title:'Nome', required:true}), createCelula({key:'telefone', title:'Telefone', required:true})],
    [createCelula({key:'email', title:'Email'}), createCelula({key:'cpf', title:'CPF'})],
  ]);
  const configsPessoasInfo = ref([
    [createCelula({key:'nome', title:'Nome', readonly:true, variant:'underlined'}), createCelula({key:'telefone', title:'Telefone', readonly:true, variant:'underlined'})],
    [createCelula({key:'email', title:'Email', readonly:true, variant:'underlined'}), createCelula({key:'cpf', title:'CPF', readonly:true, variant:'underlined'})],
    [createCelula({key:'dataNascimento', title:'Data de Nascimento', type: 'date', readonly:true, variant:'underlined'}), createCelula({key:'endereco', title:'Endereço', readonly:true, variant:'underlined'})],
  ]);

  const reloadPessoaInfo = ref(false);
  const loadingCardUpdate = ref(false);
  
  if(getCargoUser() == "Admin"){
    configsRegister.value.push([createCelula({key:'dataNascimento', title:'Data de Nascimento', type: 'date'}), createCelula({key:'saldo', title:'Saldo', type: 'number', required:true})]);
    configsRegister.value.push([createCelula({key:'endereco', title:'Endereço'})]);

    configsPessoasInfo.value.push([createCelula({key:'saldo', title:'Saldo', type: 'number', card: {color: 'green-darken-1', icon: 'mdi-currency-brl'}, readonly:true, variant:'underlined'})]);
  }else{
    configsRegister.value.push([createCelula({key:'dataNascimento', title:'Data de Nascimento', type: 'date'}), createCelula({key:'endereco', title:'Endereço'})]);

    configsPessoasInfo.value.push([createCelula({key:'saldo', title:'Saldo', type: 'number', isEditable: false, card: {color: 'green-darken-1', icon: 'mdi-currency-brl'}, readonly:true, variant:'underlined'})]);
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

  async function requestAtualizarCliente(cliente, infosChange){
    loadingCardUpdate.value = true;

    try{
      const url = `http://127.0.0.1:8000/v1/cliente/update_cliente/${cliente.idCliente}/`;
      const body = infosChange;
      const token = getAuthToken();   

      const response = await fetchPatch(url, body, token);
      const responseJson = await response.json();
      
      if(response.status === 200){
        for(let key in infosChange){
          cliente[key] = infosChange[key];
        }

        reloadPessoaInfo.value = !reloadPessoaInfo.value;

        setMessageSnackbar(`As informações do ${cliente.nome} foram atualizadas com sucesso`, "success");
      }else{
        setMessageSnackbar(responseJson.message, "warning");
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar(`Falha ao atualizar informações do ${cliente.nome}`, "warning");
    }

    loadingCardUpdate.value = false;
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
      :configsRegister="configsRegister"
      :fixiesRegister="[]"
      :configsPessoaInfo="configsPessoasInfo"
      :fixiesPessoaInfo="[]"
      @cadastrarPessoa="requestCadastrarCliente"
      @removerPessoa="removerClienteConfirmation"
      @atualizarPessoa="requestAtualizarCliente"
      :reloadPessoaInfo="reloadPessoaInfo"
      :loadingCardUpdate="loadingCardUpdate"
    />
</template>

<style scoped>
</style>
