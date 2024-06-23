<template>
<nav class="navbar navbar-expand-sm navbar-dark bg-dark" aria-label="Third navbar example">
    <div class="container-fluid">
        <!-- <a class="navbar-brand" href="#">Expand at sm       |</a> -->
        <img src="../assets/music.png" alt="music" style="width: 70px;">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample03" aria-controls="navbarsExample03" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarsExample03">
            <ul class="navbar-nav me-auto mb-2 mb-sm-0">
                <li class="nav-item">
                    <router-link class="nav-link active" aria-current="page" to="/Home">Home</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link active" to="/C_LoginOrSignup">Creator_Account</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link active" tabindex="-1" aria-disabled="true" to="/profile">Profile</router-link>
                </li>
                <li class="nav-item">
                    <button @click="logout">Logout</button>

                </li>
            </ul>
            <form style="display: flex;" @submit.prevent="submitSearch">
                <input class="form-control" type="text" placeholder="Search artists and songs" aria-label="Search" v-model="search" @input="clearPlaceholder">
                <button type="submit" class="btn btn-outline-info  my-2 my-lg-0">Search</button>
            </form>
        </div>
    </div>
</nav>
</template>

<script>
import UserMixin from '../mixin/userMixin';
export default {
    mixins: [UserMixin],
    name: "Navbar",
    data() {
        return {
            search: ""
        }
    },
    methods: {
        clearPlaceholder() {
            // Clear the placeholder text when user starts typing
            if (this.search === "Search artists and songs") {
                this.search = "";
            }
        },
        submitSearch() {
            // If the search parameter is empty, prevent navigation
            if (!this.search.trim()) {
                return;
            }
            // Navigate to the search component
            this.$router.push({
                name: "search",
                params: {
                    search: this.search
                }
            });
        }
    },

}
</script>

<style>

</style>
