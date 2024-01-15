import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    id: 'auth',
    state: () => ({
        token: null,
        img: null,
        nome: null,
        cargo: null
    }),
    getters: {
        getToken() {
          return this.token;
        },
        getNome() {
          return this.nome;
        },
        getCargo() {
          return this.cargo;
        },
      },
    actions: {
      successfulLogin({token, img, nome, cargo}) {
        this.token = token;
        this.img = img;
        this.nome = nome;
        this.cargo = cargo;
      },
      reset() {
        this.token = null;
        this.img = null;
        this.nome = null;
        this.cargo = null;
      }
    }
});

export const usePessoaStore = defineStore('pessoa', {
  id: 'pessoa',

  state: () => ({
      tipoPessoa: null,
      pessoa: null,
      oldPessoa: null,
      infoChange: null,
      wasDeleted: false,
      wasUpdated: false,
      wasCreated: false,
  }),
  
  getters: {
    idPessoa(){
      return this.getId(this.pessoa);
    },
    getPessoa(){
      return this.pessoa;
    },
    getOldPessoa(){
      return this.oldPessoa;
    },
    getInfoChange(){
      return this.infoChange;
    },
    getWasDeleted(){
      return this.wasDeleted;
    },
    getWasUpdated(){
      return this.wasUpdated;
    },
    getWasCreated(){
      return this.wasCreated;
    },
  },
  actions: {
    setTipoPessoa(tipoPessoa){
      this.tipoPessoa = tipoPessoa;
    },
    setPessoa(pessoa){
      this.oldPessoa = {...this.pessoa};
      this.pessoa = {};

      for (let attr in pessoa) {
        if (pessoa[attr] === null) {
          this.pessoa[attr] = "";
        }else{
          this.pessoa[attr] = pessoa[attr];
        }
      }
    },
    setAttrPessoa(attr, value){
      this.pessoa[attr] = value;
    },
    delete(id){
      this.wasDeleted = !this.wasDeleted;
    },
    update(pessoa){
      this.infoChange = {...pessoa};
      Object.assign(this.pessoa, pessoa);
      this.wasUpdated = !this.wasUpdated;
    },
    create(pessoa){
      this.pessoa = {...pessoa};
      if(this.tipoPessoa === "Clientes"){
        this.pessoa.saldo = "0.00";
      }
      this.wasCreated = !this.wasCreated;
    },
    getId(pessoa){
      const tipoPessoa = this.tipoPessoa.toLowerCase();
      let id = undefined;

      if(tipoPessoa === "clientes"){
        id = pessoa.idCliente;
      }else if(tipoPessoa === "colaboradores"){
        id = pessoa.idUsuario;
      }
  
      return id;
    },
  }
});

export const useCargosStore = defineStore('cargos', {
  id: 'cargos',

  state: () => ({
      cargos: []
  }),

  getters: {
      getCargos() {
        return this.cargos;
      },
  },

  actions: {
    saveCargos(cargos){
      this.cargos = cargos;
    },
    reset() {
      this.cargos = [];
    }
  }
});

export const useSnackbarStore = defineStore('snackbar', {
  id:'snackbar',

  state: () => ({
    wasActivated: false,
    wasClosed: false,
    text: "",
    messageType: 'info',
  }),
  getters: {
    getWasActivated(){
      return this.wasActivated;
    },
    getWasClosed(){
      return this.wasClosed;
    },
    getText(){
      return this.text;
    },
    getMessageType(){
      return this.messageType;
    },
  },
  actions: {
    set(text, messageType){
      this.wasActivated = !this.wasActivated;
      this.text = text;
      this.messageType = messageType;
    },
    close(){
      this.wasClosed = !this.wasClosed;
    }
  }
});

export const useCaixaStore = defineStore('caixa', {
  state: () => ({
    id: undefined,
    status: 'fechado',
    action: 'Abrir',
    saldoInicial: 0,
    dataAbertura: undefined,
    observacoes: '',  
  }),
  getters: {
    getId(){
      return this.id;
    },
    getStatus() {
      return this.status;
    },
    getAction() {
      return this.action;
    },
    getSaldoInicial() {
      return this.saldoInicial;
    },
    getDataAbertura() {
      let dataAbertura = this.dataAbertura;

      if(dataAbertura){
        dataAbertura = this.dataAbertura.replace(/^(\d{4})-(\d{2})-(\d{2})$/, '$3/$2/$1');
      }
      
      return dataAbertura
    },
    getObservacoes() {
      return this.observacoes;
    },
  },
  actions: {
    saveOpenCaixa({idCaixa, saldoInicial, observacoes, dataAbertura}) {
      this.id = idCaixa;
      this.saldoInicial = saldoInicial;
      this.dataAbertura = dataAbertura;
      this.observacoes = observacoes;
      this.status = 'aberto';
      this.action =  'Fechar';
    },
    resetCaixa() {
      this.$reset();

      const resettedCaixa = {
        saldoInicialR: this.saldoInicial,
        observacoesR: this.observacoes,
      };

      return resettedCaixa
    }
  }
});

export const useFormStore = defineStore('form', {
  id: 'form',

  state: () => ({
      obj: null,
      from: "",
  }),
  
  getters: {
    getObj(){
      return this.obj;
    },
    getFrom(){
      return this.from;
    },
  },
  actions: {
    send(from, obj){
      this.obj = obj;
      this.from = from;
    },
  }
});

export const usePedidoStore = defineStore('pedido', {
  id: 'pedido',

  // "Pagamento": {
  //     "valorTotal": 10.00,
  //     "valorRecebimento": 30.00,
  //     "valorDevolvido": 20.00,
  //     "tipoPagamento": "Dinheiro"
  // },
          
  // "idProdutos": [
  //     {
  //     "idProduto": "4718af40-ee5d-486f-8a8a-d1ffe3604a2a",
  //     "quantidade": 0.450,
  //     "valorVendaUnd": 40.00,
  //     "desconto": 15.00
  //     },
  //     {
  //     "idProduto": "8c9228f3-8d77-47fd-89e3-1ee7bb9b376e",
  //     "quantidade": 2,
  //     "valorVendaUnd": 5.00
  //     }
  // ],
  state: () => ({
      idPedido: undefined,
      idCliente: undefined,
      Pagamento: {},
      idCaixa: undefined,
      idProdutos: [],
      status: undefined,
      desconto: true,
  }),
  
  getters: {
      getIdPedido(){
        return this.idPedido;
      }
  },
  actions: {
    saveFuncionarioInfo({idUsuario, nome, email, telefone, cpf, dataNascimento, endereco, cargo}){
      this.idUsuario = idUsuario;
      this.nome = nome;
      this.email = email;
      this.telefone = telefone;
      this.cpf = cpf;
      this.dataNascimento = dataNascimento.replace(/^(\d{4})-(\d{2})-(\d{2})$/, '$3/$2/$1');
      this.endereco = endereco;
      this.cargo = cargo;
    },
    updateFuncionarioInfo(infos) {
      Object.assign(this.$state, infos);
    },
    reset() {
      this.idUsuario= null;
      this.nome = null;
      this. email = null;
      this.telefone = null;
      this.cpf = null;
      this.dataNascimento = null;
      this.endereco = null;
      this.cargo = null;
    }
  }
});