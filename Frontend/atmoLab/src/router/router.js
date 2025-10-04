import { createRouter, createWebHistory } from 'vue-router';
import { routes } from './routes';

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.afterEach((to, from) => {
    window.scrollTo(0, 0);
});

export default router;