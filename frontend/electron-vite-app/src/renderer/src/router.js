import {createRouter, createWebHashHistory} from 'vue-router';
import Login from './components/Login.vue'
import Menu from './components/Menu.vue'
import Dashboard from './components/Dashboard.vue'
import ClientesLista from './components/ClientesLista.vue'

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
        path: 'clientes-lista', 
        name: 'Clientes Lista', 
        component: ClientesLista,
      }
    ]
  },
];

const router = createRouter({
    routes,
    history: createWebHashHistory("/")
});

export default router;