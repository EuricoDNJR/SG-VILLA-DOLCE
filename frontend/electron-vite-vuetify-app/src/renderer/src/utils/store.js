import { defineStore } from 'pinia';

export const useAuthStore = defineStore('userData', {
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
      pessoa: null,
      infoChange: null,
      idDeleted: null,
      wasUpdated: false,
      wasCreated: false,
  }),
  
  getters: {
    getPessoa(){
      return this.pessoa;
    },
    getInfoChange(){
      return this.infoChange;
    },
    getIdDeleted(){
      return this.idDeleted;
    },
    getWasUpdated(){
      return this.wasUpdated;
    },
    getWasCreated(){
      return this.wasCreated;
    },
  },
  actions: {
    setPessoa(pessoa){
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
      this.idDeleted = id;
    },
    update(pessoa){
      Object.assign(this.pessoa, pessoa);
      this.infoChange = {...pessoa};
      this.wasUpdated = !this.wasUpdated;
    },
    create(pessoa){
      this.pessoa = {...pessoa};
      this.pessoa.saldo = "0.00";
      this.wasCreated = !this.wasCreated;
    }
  }
});

export const useFuncionarioStore = defineStore('funcionario', {
  id: 'funcionario',

  state: () => ({
      idUsuario: null,
      nome: null,
      email: null,
      telefone: null,
      cpf: null,
      dataNascimento: null,
      endereco: null,
      cargo: null,
  }),
  
  getters: {
      getIdUsuario() {
        return this.idUsuario;
      },
      getNome() {
        return this.nome;
      },
      getEmail() {
        return this.email;
      },
      getTelefone() {
        return this.telefone;
      },
      getCpf() {
        return this.cpf;
          },
      getDataNascimento() {
        return this.dataNascimento;
      },
      getEndereco() {
        return this.endereco;
      },
      getCargo() {
        return this.cargo;
      },
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
    text: "",
    messageType: 'info',
  }),
  getters: {
    getWasActivated(){
      return this.wasActivated;
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
    saveOpenCaixa({uuid, SaldoInicial, Observacoes, DataAbertura, HoraAbertura}) {
      this.id = uuid;
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