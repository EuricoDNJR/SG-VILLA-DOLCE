import {createRouter, createWebHistory} from 'vue-router';
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
    path: '/logged', 
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
    history: createWebHistory("/")
});

export default router;