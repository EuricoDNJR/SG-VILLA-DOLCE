import {createRouter, createWebHashHistory} from 'vue-router';
import Login from './components/Login.vue'
import Menu from './components/Menu.vue'
import Dashboard from './components/Dashboard.vue'
import Clientes from './components/Clientes.vue'
import ClientesInfo from './components/ClientesInfo.vue'
import CadastrarCliente from './components/CadastrarCliente.vue'
import Funcionarios from './components/Funcionarios.vue'
import FuncionariosInfo from './components/FuncionariosInfo.vue'
import CadastrarFuncionario from './components/CadastrarFuncionario.vue'



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
        path: 'ver-cliente', 
        name: 'clientesInfo', 
        component: ClientesInfo,
      },
      { 
        path: 'cadastrar-cliente', 
        name: 'cadastrarCliente', 
        component: CadastrarCliente,
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
    ]
  },
];

const router = createRouter({
    routes,
    history: createWebHashHistory("/")
});

export default router;