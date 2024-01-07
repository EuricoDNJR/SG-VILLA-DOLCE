import {createRouter, createWebHashHistory} from 'vue-router';
import Login from './components/Login.vue'
import Menu from './components/Menu.vue'
import Dashboard from './components/Dashboard.vue'
import Clientes from './components/Clientes.vue'
import CadastrarCliente from './components/CadastrarCliente.vue'
import Funcionarios from './components/Funcionarios.vue'
import FuncionariosInfo from './components/FuncionariosInfo.vue'
import CadastrarFuncionario from './components/CadastrarFuncionario.vue'
import Caixa from './components/Caixa.vue'
import Pedidos from './components/Pedidos.vue'
import CriarPedido from './components/CriarPedido.vue'



const routes = [
  { 
    path: '/', 
    name: 'login', 
    component: Login,
  },
  { 
    path: '/menu', 
    name: 'menu', 
    component: Menu,
    children: [
      { 
        path: 'dashboard', 
        name: 'dashboard', 
        component: Dashboard,
      },
      { 
        path: 'clientes', 
        name: 'clientes', 
        component: Clientes,
      },
      { 
        path: 'funcionarios', 
        name: 'funcionarios', 
        component: Funcionarios,
      },
      { 
        path: 'ver-funcionario', 
        name: 'funcionariosInfo', 
        component: FuncionariosInfo,
      },
      { 
        path: 'cadastrar-funcionario', 
        name: 'cadastrarFuncionario', 
        component: CadastrarFuncionario,
      },
      { 
        path: 'caixa', 
        name: 'caixa', 
        component: Caixa,
      },
      {
        path: 'pedidos',
        name: 'pedidos',
        component: Pedidos,
      },
      { 
        path: 'criar-pedido', 
        name: 'criarPedido', 
        component: CriarPedido,
      },
    ]
  },
];

const router = createRouter({
    routes,
    history: createWebHashHistory("/")
});

export default router;