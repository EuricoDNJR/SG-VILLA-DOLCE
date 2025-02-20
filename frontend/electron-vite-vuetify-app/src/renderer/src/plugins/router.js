import {createRouter, createWebHashHistory} from 'vue-router';

const Login = () => import('../pages/Login.vue');
const Menu = () => import('../pages/Menu.vue');
const Dashboard = () => import('../pages/Dashboard.vue');
const Estoque = () => import('../pages/Estoque.vue');
const Clientes = () => import('../pages/Clientes.vue');
const Colaboradores = () => import('../pages/Colaboradores.vue');
const Pedidos = () => import('../pages/Pedidos.vue');
const Produtos = () => import('../pages/Produtos.vue');
const HistoricoCaixas = () => import('../pages/HistoricoCaixas.vue');

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
        path: 'produtos',
        name: 'produtos',
        component: Produtos,
      },
      {
        path: 'historico-caixas',
        name: 'historico-caixas',
        component: HistoricoCaixas,
      },
    ]
  },
];

const router = createRouter({
    routes,
    history: createWebHashHistory("/")
});

export default router;