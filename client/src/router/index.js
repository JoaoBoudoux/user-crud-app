import { createRouter, createWebHistory } from 'vue-router';
import UserList from '../components/UserList.vue';
import UserPage from '../components/UserPage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: UserList,
  },
  {
    path: '/user/:id',
    name: 'UserPage',
    component: UserPage,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;