<template>
<div>
    <Navbar/>
    <img src="../assets/lofi_music.jpg" alt="girl" style=" border-radius: 3%; width: 35%; position: relative; left: 900px; top: 100px;">

    <div class="container col-8" style="position: relative;left: 800px; top: 100px; ">
        <h1 class="font"><strong>Play song</strong></h1>
        <br>
        
        
        <audio controls :src="path"></audio>
    </div>

    <div class="col-lg-7 mx-auto" style="border: solid slategrey; border-radius: 3%; padding: 5%; position: relative; bottom: 400px; right: 250px;">
        <div class="btn-group">
            <h2 style="margin-right: 5%; color: rgb(43, 122, 226);">{{song.s_name}}</h2>
        </div>
        
        <button style="margin-left: 30px; color: rgb(43, 122, 226); border-radius: 10% 5px 10% 5px; background-color: rgb(214, 214, 230);"><h2>Rating</h2>{{song.rating}}</button>
        <p>🎙️{{ album.artist }} | {{song.date}}</p>
        <p class="lead mb-4" style="border: solid slategrey; border-radius: 3%; padding: 5%; margin-top: 3%; color: gray;">{{song.lyrics}}
        </p>

    </div>

</div>
</template>

<script>

import Navbar from './Navbar.vue';
export default {
    name: "lyrics",
    components:{
        Navbar,
    },
    data() {
        return {
            song: {},
            album:{},
            path:""
        }
    },
    created() {
        const s_id = this.$route.params.s_id;
        
        this.fetchSong(s_id);

    },
    methods: {
        fetchSong(s_id) {
            fetch(`http://localhost:5000/fetch_lyrics/${s_id}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    this.song = data.data.song;
                    this.album = data.data.album;
                    this.path = data.data.path
                    console.log(this.song);
                    console.log(this.path)
                    // this.path = this.path.concat("",this.song.songMP3)
                    // console.log(this.path.concat("",this.song.songMP3))
                })
                .catch((error) => {
                    console.error("Error fetching lyrics:", error);
                });
        },
        
    }

}
</script>

<style scoped>
.font {
            font-size: 4rem;
            color: rgb(43, 122, 226);
        }
p{
    font-family: 'Montserrat', sans-serif;
}
</style>
