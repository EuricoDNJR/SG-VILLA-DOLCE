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
    horaAbertura: undefined,
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
    getHoraAbertura() {
      return this.horaAbertura;
    },
    getObservacoes() {
      return this.observacoes;
    },
  },
  actions: {
    saveOpenCaixa({idCaixa, SaldoInicial, Observacoes, DataAbertura, HoraAbertura}) {
      this.id = idCaixa;
      this.saldoInicial = SaldoInicial;
      this.dataAbertura = DataAbertura;
      this.horaAbertura = HoraAbertura;
      this.observacoes = Observacoes;
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
// export const useFuncionarioStore = defineStore('pedido', {
//   id: 'pedido',

//   state: () => ({
//       idPedido: "54350a93-af19-42e7-85e5-8125f0a55bea",
//       idCliente: "067b0dc9-54ac-4bb5-876e-f44756eebe0e",
//       nomeCliente: "CLIENTE",
//       idPagamento: "d408286c-e891-4bf7-9ef3-8cd3415331e6",
//       valorTotal: "10.00",
//       valorRecebimento: "12.00",
//       valorDevolvido: "2.00",
//       tipoPagamento: "Dinheiro",
//       idUsuario: "e8717377-f290-49d7-a9e8-39bd44410016",
//       nomeUsuario: "Nome do Usuário",
//       idCaixa: "6e9b0d57-f3c3-4eb8-af6c-7d5e49b6eb58",
//       status: "Pago",
//   }),
  
//   getters: {
//       getIdPedido(){
//         return this.idPedido;
//       }
//   },
//   actions: {
//     saveFuncionarioInfo({idUsuario, nome, email, telefone, cpf, dataNascimento, endereco, cargo}){
//       this.idUsuario = idUsuario;
//       this.nome = nome;
//       this.email = email;
//       this.telefone = telefone;
//       this.cpf = cpf;
//       this.dataNascimento = dataNascimento.replace(/^(\d{4})-(\d{2})-(\d{2})$/, '$3/$2/$1');
//       this.endereco = endereco;
//       this.cargo = cargo;
//     },
//     updateFuncionarioInfo(infos) {
//       Object.assign(this.$state, infos);
//     },
//     reset() {
//       this.idUsuario= null;
//       this.nome = null;
//       this. email = null;
//       this.telefone = null;
//       this.cpf = null;
//       this.dataNascimento = null;
//       this.endereco = null;
//       this.cargo = null;
//     }
//   }
// });