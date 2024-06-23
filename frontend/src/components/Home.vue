<template>
<div>
    <Navbar />
    <h1 style="text-align: center;">🎶Welcome To Music Streaming Application🎶</h1>
    <div class="container my-4" style="text-align: center;">
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
</template>

<script>
import Navbar from './Navbar.vue';

export default {
    name: "Home",
    components: {
        Navbar,
    },
    data() {
        return {
            songs: [],
            rating: 0,
            stars: [1, 2, 3, 4, 5]
        }
    },
    created() {
        this.fetchSongs();
    },
    methods: {
        fetchSongs() {
            fetch("http://localhost:5000/all_songs", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    this.songs = data.data;
                    console.log(this.songs);
                })
                .catch((error) => {
                    console.error("Error fetching songs:", error);
                });
        },
        rateSong(song, rating) {
            song.rating = rating; // This line is fine
            this.sendRatingToBackend(song.s_id, rating); // Access song ID using song.s_id
        },
        sendRatingToBackend(song_id, rating) {
            fetch(`http://localhost:5000/rate_song/${song_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                    },
                    body: JSON.stringify({
                        rating
                    })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to rate song');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Song rated successfully:', data);
                })
                .catch(error => {
                    console.error('Error rating song:', error);
                    song.rating = 0;
                    alert('Failed to rate song. Please try again later.');
                });
        }
    }
}
</script>

<style scoped>
.rated {
    color: orange;
    cursor: pointer;
}
</style>
