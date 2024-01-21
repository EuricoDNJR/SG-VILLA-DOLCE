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

  state: () => ({
      idProdutos: undefined,
      idPedidoFinished: undefined,
      produtoAdicionado: undefined,
      produtoRemovido: undefined,
      wasCreated: false,
      wasUpdated: false,
      wasFinished: false,
      wasCancelled: false,
      cliente: {nome: "", telefone: ""},
      descontoWasClosed: false,
  }),
  
    getters: {
      getIdProdutos(){
        return this.idProdutos;
      },
      getIdPedidoFinished(){
        return this.idPedidoFinished;
      },
      getProdutoAdicionado(){
        return this.produtoAdicionado;
      },
      getProdutoRemovido(){
        return this.produtoRemovido;
      },
      getWasCreated(){
        return this.wasCreated;
      },
      getWasUpdated(){
        return this.wasUpdated;
      },
      getWasFinished(){
        return this.wasFinished;
      },
      getWasCancelled(){
        return this.wasCancelled;
      },
      getCliente(){
        return this.cliente;
      },
      getProdutosDescontados(){
        return this.produtosDescontados;
      },
      getDescontoWasClosed(){
        return this.descontoWasClosed;
      },
  },
  actions: {
    create(){
      this.wasCreated = !this.wasCreated;
    },
    update(idProdutos){
      this.idProdutos = idProdutos;
      this.wasUpdated = !this.wasUpdated;
    },
    finish(idPedido){
      this.idPedidoFinished = idPedido;
      this.wasFinished = true;
    },
    cancel(){
      this.wasCancelled = true;
    },
    adicionarProduto(produto){
      this.produtoAdicionado = produto;
    },
    removeProduto(produto){
      this.produtoRemovido = produto;
    },
    setCliente(cliente){
      this.cliente = cliente;
    },
    closeDiscount(){
      this.descontoWasClosed = !this.descontoWasClosed;
    },
    reset(){
      this.$reset();
    }
  }
});