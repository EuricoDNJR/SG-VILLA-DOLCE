import {createRouter, createWebHashHistory} from 'vue-router';
import Login from './components/Login.vue'
import Menu from './components/Menu.vue'
import Dashboard from './components/Dashboard.vue'
import Clientes from './components/Clientes.vue'
import ClientesInfo from './components/ClientesInfo.vue'
import CadastrarCliente from './components/CadastrarCliente.vue'



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
      }
    ]
  },
];

const router = createRouter({
    routes,
    history: createWebHashHistory("/")
});

export default router;