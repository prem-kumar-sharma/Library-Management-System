import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import LoginUser from '../components/UserLogin.vue';
import RegisterUser from '../components/RegisterUser.vue';
import AddBooks from '../components/AddBooks.vue';
import AddSection from '../components/AddSection.vue';
import NavBar from '../components/NavBar.vue';
import AdminNav from '../components/AdminNav.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import AdminLogin from '../components/AdminLogin.vue';
import AdminRegistration from '../components/AdminRegistration.vue';
import EditBook from '../components/EditBook.vue';
import EditSection from '../components/EditSection.vue';
import SubmitFeedback from '../components/SubmitFeedback.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/LoginUser', component: LoginUser },
  { path: '/RegisterUser', component: RegisterUser },
  { path: '/AddBooks', component: AddBooks },
  { path: '/AddSection', component: AddSection },
  { path: '/NavBar', component: NavBar },
  { path: '/AdminNav', component: AdminNav },
  { path: '/AdminDashboard', component: AdminDashboard },
  { path: '/AdminLogin', component: AdminLogin },
  { path: '/AdminRegistration', component: AdminRegistration },
  { path: '/EditBook/:bookId', component: EditBook },
  { path: '/EditSection/:bookId', component: EditSection },
  { path: '/SubmitFeedback', component: SubmitFeedback },

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;