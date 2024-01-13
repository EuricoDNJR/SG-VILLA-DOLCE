import {createRouter, createWebHashHistory} from 'vue-router';
import Login from '../pages/Login.vue'
import Menu from '../pages/Menu.vue'
import Dashboard from '../pages/Dashboard.vue'
import Estoque from '../pages/Estoque.vue'
import Clientes from '../pages/Clientes.vue'
import Colaboradores from '../pages/Colaboradores.vue'
import Pedidos from '../pages/Pedidos.vue'
import Configuracoes from '../pages/Configuracoes.vue'
import Produtos from '../pages/Produtos.vue'


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
        path: 'estoque', 
        name: 'estoque', 
        component: Estoque,
      },
      { 
        path: 'clientes', 
        name: 'clientes', 
        component: Clientes,
      },
      { 
        path: 'Colaboradores', 
        name: 'colaboradores', 
        component: Colaboradores,
      },
      {
        path: 'pedidos',
        name: 'pedidos',
        component: Pedidos,
      },
      {
        path: 'configuracoes',
        name: 'configuracoes',
        component: Configuracoes,
      },
      {
        path: 'produtos',
        name: 'produtos',
        component: Produtos,
      },
    ]
  },
];

const router = createRouter({
    routes,
    history: createWebHashHistory("/")
});

export default router;