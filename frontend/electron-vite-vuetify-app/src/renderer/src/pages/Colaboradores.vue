<script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { fetchGet, fetchPost, fetchPatch, fetchDelete, getAuthToken, setAuthNomeECargo, setMessageSnackbar, createCelula, confirmDialog } from '../utils/common'
  import Snackbar from '../components/Snackbar.vue';
  import Pessoas from '../components/Pessoas.vue';
  
  defineOptions({
    inheritAttrs: false
  });

  const colaboradores = ref([]);
  const cargos = ref([]);

  const reloadPessoaInfo = ref(false);
  const loadingCardUpdate = ref(false);


  const loadingBtn = reactive({
    cadastrarColaborador: false,
  });
  

  async function requestAllColaboradores(){
    try{
      const url = "http://127.0.0.1:8000/v1/usuario/get_all_users/";
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          colaboradores.value = responseJson;
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar colaboradores", 'warning');
    }
  }

  async function requestAllCargos(){
    try{
      const url = "http://127.0.0.1:8000/v1/cargo/get_all_roles/";
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          cargos.value = responseJson;
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar cargos", 'warning');
    }
  }
  
  async function requestCadastrarColaborador(body){
    loadingBtn.cadastrarColaborador = true;

    try{
        const url = "http://127.0.0.1:8000/v1/usuario/create_user/";
        const token = getAuthToken();
        
        const response = await fetchPost(url, body, token);
        const responseJson = await response.json();
        
        if(response.status === 201){       
            Object.assign(body, responseJson);    

            adicionarColaborador(body);

            setMessageSnackbar("Colaborador cadastrado com sucesso", 'success');
        }else{
            setMessageSnackbar(responseJson.message, 'warning');
        }
    }catch(e){
        console.log(e);
        setMessageSnackbar("Falha ao cadastrar colaborador", 'warning');
    }        

    loadingBtn.cadastrarColaborador = false;
  }

  async function requestAtualizarColaborador(colaborador, infosChange){
    loadingCardUpdate.value = true;

    try{
      const url = `http://127.0.0.1:8000/v1/usuario/update_user/${colaborador.idUsuario}/`;
      const body = infosChange;
      const token = getAuthToken();   

      const response = await fetchPatch(url, body, token);
      const responseJson = await response.json();
      
      if(response.status === 200){
        for(let key in infosChange){
          colaborador[key] = infosChange[key];
        }

        setAuthNomeECargo(infosChange.nome, infosChange.cargo);
        
        reloadPessoaInfo.value = !reloadPessoaInfo.value;

        setMessageSnackbar(`As informações do ${colaborador.nome} foram atualizadas com sucesso`, "success");
      }else{
        setMessageSnackbar(responseJson.message, "warning");
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar(`Falha ao atualizar informações do ${colaborador.nome}`, "warning");
    }

    loadingCardUpdate.value = false;
  }

  async function requestRemoverColaborador(colaborador){
      try{
        const url = `http://127.0.0.1:8000/v1/usuario/delete_user/${colaborador.idUsuario}/`;
        const token = getAuthToken();

        const response = await fetchDelete(url, token);
        const responseJson = await response.json();

        if(response.status === 200){
          removerColaborador(colaborador.idUsuario);
            
          setMessageSnackbar(`${colaborador.nome} foi removido do sistema com sucesso`, "success");
        }else{
          setMessageSnackbar(responseJson.message, "warning");
        }
      }catch(e){
        console.log(e);
        setMessageSnackbar(`Falha ao remover ${colaborador.nome} do sistema`, "warning");
      }
  }

  function removerColaboradorConfirmation(colaborador){
    confirmDialog(`Tem certeza que deseja remover ${colaborador.nome} do sistema?`, () => requestRemoverColaborador(colaborador));
  }

  function adicionarColaborador(body){
    const colaborador = {
      idUsuario: body.uuid,
      nome:  body.nome,
      senha:  body.senha,
      telefone:  body.telefone,
      cpf:  body.cpf,
      dataNascimento:  body.dataNascimento,
      email:  body.email,
      endereco:  body.endereco,
      cargo:  body.cargo,
    };

    colaboradores.value.push(colaborador);
  }

  function removerColaborador(id){
    colaboradores.value = colaboradores.value.filter((colaborador) => colaborador.idUsuario != id);
  }

  onMounted(() => {
    requestAllColaboradores();
    requestAllCargos();
  });
</script>

<template>
    <Snackbar/>

    <Pessoas
      title="Colaboradores"
      :pessoas="colaboradores"
      registerTitle="Cadastrar Colaborador"
      :loadingBtnRegister="loadingBtn.cadastrarColaborador"
      :configsRegister="[
        [createCelula({key:'nome', title:'Nome', required:true}), createCelula({key:'senha', title:'Senha', required:true})],
        [createCelula({key:'telefone', title:'Telefone', required:true}), createCelula({key:'email', title:'Email', required:true})],
        [createCelula({key:'dataNascimento', title:'Data de Nascimento', type: 'date', required:true}), createCelula({key:'cpf', title:'CPF', required:true})],
        [createCelula({key:'endereco', title:'Endereço', required:true}), createCelula({key:'cargo', title:'Cargo', type: 'select', required:true, initialValue: cargos[0]})]
      ]"
      :fixiesRegister="[
        ['Cargo.items', cargos],
        ['Cargo.itemsTitle', 'nome'],
        ['Cargo.itemsValue', 'nome'],
      ]"
      :configsPessoaInfo="[
        [createCelula({key:'nome', title:'Nome', readonly:true, variant:'underlined'}), createCelula({key:'telefone', title:'Telefone', readonly:true, variant:'underlined'})],
        [createCelula({key:'email', title:'Email', readonly:true, variant:'underlined'}), createCelula({key:'cpf', title:'CPF', readonly:true, variant:'underlined'})],
        [createCelula({key:'dataNascimento', title:'Data de Nascimento', type: 'date', readonly:true, variant:'underlined'}), createCelula({key:'endereco', title:'Endereço', readonly:true, variant:'underlined'})],
        [createCelula({key:'cargo', title:'Cargo', type: 'select', card: {color: 'black', icon: 'mdi-shield-star'}, readonly:true, variant:'underlined'})]
      ]"
      :fixiesPessoaInfo="[
        ['Cargo.items', cargos],
        ['Cargo.itemsTitle', 'nome'],
        ['Cargo.itemsValue', 'nome'],
      ]"
      @cadastrarPessoa="requestCadastrarColaborador"
      @removerPessoa="removerColaboradorConfirmation"
      @atualizarPessoa="requestAtualizarColaborador"
      :reloadPessoaInfo="reloadPessoaInfo"
      :loadingCardUpdate="loadingCardUpdate"
    />
</template>

<style scoped>
</style>
