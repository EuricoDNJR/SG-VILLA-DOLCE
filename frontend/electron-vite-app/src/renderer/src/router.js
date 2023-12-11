import {createRouter, createWebHashHistory} from 'vue-router';
import Login from './components/Login.vue'
import Menu from './components/Menu.vue'
import Dashboard from './components/Dashboard.vue'
import ClientesLista from './components/ClientesLista.vue'
import ClientesInfo from './components/ClientesInfo.vue'


const routes = [
  { 
    path: '/', 
    name: 'Login', 
    component: Login,
  },
  { 
    path: '/menu', 
    name: 'Menu', 
    component: Menu,
    children: [
      { 
        path: 'dashboard', 
        name: 'Dashboard', 
        component: Dashboard,
      },
      { 
        path: 'clientes', 
        name: 'Clientes Lista', 
        component: ClientesLista,
      },
      { 
        path: 'ver-cliente', 
        name: 'Ver Cliente', 
        component: ClientesInfo,
      }
    ]
  },
];

const router = createRouter({
    routes,
    history: createWebHashHistory("/")
});

export default router;