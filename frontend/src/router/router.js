import { createRouter, createWebHistory } from "vue-router";
import FirstPage from '../components/FirstPage.vue'
import Home from '../components/Home.vue'
import sing_up from '../components/SignUp.vue'
import CreatorRegister from '../components/CreatorRegister.vue'
import CreatorDashboard from '../components/CreatorDashboard.vue'
import C_LoginOrSignup from '../components/C_LoginOrSignup.vue'
import profile from '../components/profile.vue'
import uploadSong from '../components/uploadSong.vue'
import lyrics from '../components/lyrics.vue'
import Edit_song from '../components/Edit_song.vue'
import createPlaylist from "../components/createPlaylist.vue";
import myPlaylist from '../components/myPlaylist.vue'
import admin_login from "../components/admin_login.vue"
import admin from "../components/admin.vue"
import admin2 from "../components/admin2.vue"
import search from "../components/search.vue"

const routes = [
    {
        path: '/',
        name : "FirstPage",
        component : FirstPage

    },

    {
        path: '/sign_up',
        name : "sign-Up",
        component : sing_up

    },
    {
        path: '/admin_login',
        name : "admin_login",
        component : admin_login

    },
    {
        path: '/admin',
        name : "admin",
        component : admin

    },
    {
        path: '/admin2',
        name : "admin2",
        component : admin2

    },

    {
        path: '/Home',
        name : "Home",
        component : Home

    },

    {
        path: '/C_LoginOrSignup',
        name : "C_LoginOrSignup",
        component : C_LoginOrSignup

    },

    {
        path: '/creator_register',
        name : "CreatorRegister",
        component : CreatorRegister

    },

    {
        path: '/creator_DashBoard',
        name : "CreatorDashboard",
        component : CreatorDashboard

    },
    {
        path: '/profile',
        name : "profile",
        component : profile,

    },
    {
        path: '/uploadSong',
        name : "uploadSong",
        component : uploadSong

    },
    {
        path: '/lyrics/:s_id',
        name : "lyrics",
        component : lyrics

    },
    {
        path: "/edit-song/:s_id",
        name : "Edit_song",
        component : Edit_song,
    },
    {
        path : "/createPlaylist",
        name :"createPlaylist",
        component : createPlaylist
    },
    {
        path : "/myPlaylist/:id",
        name :"myPlaylist",
        component : myPlaylist
    },
    {
        path : "/search/:search",
        name : "search",
        component : search
    }
]




const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;