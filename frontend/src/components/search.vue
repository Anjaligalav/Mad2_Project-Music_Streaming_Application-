<template>
<div>
    <Navbar />
    <div class="container my-4" style="text-align: center;">
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
        </div>

        <!-- if no error message -->
        <div v-else>
            <div class="row">
                <div v-for="song in songs" :key="song.s_id" class="col-md-3" style="margin-top: 1%;">
                    <div class="card h-100">
                        <img src="../assets/music_background.jpeg" class="card-img-top" alt="music" style="height: 300px; width: 300px; background-size: contain; background-repeat: no-repeat;">
                        <div class="card-body">
                            <h5 class="card-title"><img src="../assets/music.png" alt="music" style="width: 30px; margin-right: 10px;">{{ song.s_name }}</h5>
                            <p class="card-text">Rating | {{song.rating}}</p>
                            <div>
                                <span v-for="star in stars" :key="star" @click="rateSong(song,star)" :class="{ 'rated': star <= song.rating }">&#9733;</span>
                            </div>
                            <router-link :to="{ name: 'lyrics', params: { s_id: song.s_id } }" class="btn btn-primary">Play</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>
</template>

<script>
import Navbar from './Navbar.vue';
export default {
    name: "search",
    components: {
        Navbar,
    },
    data() {
        return {
            songs: [],
            errorMessage: ""
        }
    },
    created() {
        const search = this.$route.params.search;
        this.fetchSongs(search);
    },
    methods: {
        fetchSongs(search) {
            fetch(`http://localhost:5000/search/${search}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.message) {
                        this.errorMessage = data.message;
                    } else {
                        console.log(data);
                        this.songs = data.data;
                        console.log(this.songs);
                    }
                })
                .catch((error) => {
                    console.error("Error fetching songs:", error);
                });
        }
    }
}
</script>

<style>

</style>
