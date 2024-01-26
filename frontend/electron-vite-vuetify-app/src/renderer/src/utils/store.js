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
