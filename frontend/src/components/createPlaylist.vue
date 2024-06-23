<template>
<div>
    <img src="../assets/Playlist-pana.png" alt="girl" style=" width:40%; position: relative; top: 50px; left: 700px;">
    <div class="container my-4" style="position: relative; bottom: 500px;">

        <form @submit.prevent="onSubmit" style="font-size: 30px;">
            <label for="new">Create Playlist:</label>
            <input type="text" v-model="p_name" name="p_name" id="new" placeholder="Name of playlist" required>
            <div v-for="song in songs" :key="song.s_id">

                <p><label :for="song.s_name">{{ song.s_name }} </label>
                <input type="checkbox" v-model="selectedSongs" :value="song.s_id" :id="song.s_name" style="width: 25px; height: 25px;"></p>
            
            </div>
            <button type="submit">Add</button>
        </form>

        <!-- <button style="text-align: center;" ><a href="/playlist" class="btn btn-primary">Add</a></button> -->
    </div>
</div>
</template>

<script>
export default {
    name: "createPlaylist",
    data() {
        return {
            songs: [],
            selectedSongs: [],
            p_name : ""

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
        async onSubmit(){
            const formdata = {
                p_name : this.p_name,
                song_list : this.selectedSongs,
            }
            try {
                const access_token = localStorage.getItem('access_token')
                const response = await fetch('http://localhost:5000/create_playlist', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization:`Bearer ${access_token}`
                    },
                    body: JSON.stringify(formdata)
                })
                const data = await response.json()
                if (response.ok) {
                    alert(data.message)

                    this.$router.push('/profile')
                } else {
                    alert(data.error)
                }
            } catch (error) {
                console.log("upload error:", error)
                alert("An error occure while creating a playlist")
            }
        }
    }
}
</script>

<style>

</style>
