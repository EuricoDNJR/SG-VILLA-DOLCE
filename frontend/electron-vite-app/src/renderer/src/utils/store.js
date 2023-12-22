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

export const useClienteStore = defineStore('clienteData', {
  id: 'cliente',

  state: () => ({
      idCliente: null,
      nome: null,
      email: null,
      telefone: null,
      cpf: null,
      dataNascimento: null,
      endereco: null,
      saldo: null,
      pontos: null
  }),
  
  getters: {
      getIdCliente() {
        return this.idCliente;
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
      getSaldo() {
        return this.saldo;
          },
      getPontos() {
        return this.pontos;
      }
  },
  actions: {
    saveClienteInfo({idCliente, nome, email, telefone, cpf, dataNascimento, endereco, saldo, pontos}){
      this.idCliente = idCliente;
      this.nome = nome;
      this.email = email;
      this.telefone = telefone;
      this.cpf = cpf;
      this.dataNascimento = dataNascimento.replace(/^(\d{4})-(\d{2})-(\d{2})$/, '$3/$2/$1');
      this.endereco = endereco;
      this.saldo = saldo;
      this.pontos = pontos;
    },
    updateClienteInfo(infos) {
      Object.assign(this.$state, infos);
    },
    reset() {
      this.idCliente = null;
      this.nome = null;
      this. email = null;
      this.telefone = null;
      this.cpf = null;
      this.dataNascimento = null;
      this.endereco = null;
      this.saldo = null;
      this.pontos = null;
    }
  }
});

export const useFuncionarioStore = defineStore('funcionarioData', {
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

export const useCargosStore = defineStore('cargosData', {
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