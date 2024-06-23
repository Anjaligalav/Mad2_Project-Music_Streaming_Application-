<template>
<div>
    <Navbar />
    <h1 style="color: rgb(101, 43, 226); text-align: center;">{{ play.name }}</h1>

    <div class="container my-4" style="text-align: center;">
        <div class="row">
            <div v-for="song in song_list" :key="song.s_id" :class="calculateColumnClass(song_list.length)" style="margin-top: 1%;">
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
    name: "myPlaylist",
    components: {
        Navbar,
    },
    data() {
        return {
            id: null,
            song_list: [],
            play: {},
            rating: 0,
            stars: [1, 2, 3, 4, 5],
        }
    },
    created() {
        this.id = this.$route.params.id
        this.playLists(this.id)
    },
    methods: {
        playLists(id) {
            fetch(`http://localhost:5000/myPlaylist/${id}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    this.song_list = data.song_list;
                    this.play = data.play;
                    console.log(typeof (this.song_list));
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
        },
        calculateColumnClass(length) {
            // Calculate the column class based on the number of songs
            switch (length) {
                case 1:
                    return "col-md-12";
                case 2:
                    return "col-md-6";
                case 3:
                    return "col-md-4";
                case 4:
                    return "col-md-3";
                default:
                    return "col-md-3"; // Fallback to 1/4 width
            }
        },
    }
}
</script>

<style scoped>
.rated {
    color: orange;
    cursor: pointer;
}
/* .card-body{
    background-image: url('../assets/music_background.jpeg'); 
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
   
} */

</style>
