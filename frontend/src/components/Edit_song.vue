<template>
<div>
    <h1>Edit song</h1>
    <div class="col-lg-6 mx-auto bg_img" style="margin-top: 2%;">
        <h1 style="text-align: center;">Upload your song.</h1>
        <form @submit.prevent="onSubmit" enctype="multipart/form-data" class="lead mb-4" style="border: solid slategrey; border-radius: 3%; padding: 10%;">
            <label for="sname">Song Name</label><br><br>
            <input v-model="sname" class="upload" type="text" name="sName" id="sName" required><br><br>
            <p><label for="date">Release Date</label></p>
            <p><input v-model="date" class="upload" type="date" name="date" id="date" required></p>
            <p><label for="maker">Album_Name</label></p>
            <p><input v-model="albumName" class="upload" type="text" name="album_name" id="maker" required></p>
            <p><label for="lyrics">Lyrics</label></p>
            <p><input v-model="lyrics" class="upload" type="text" name="lyrics" id="lyrics" required></p>
            <p><label for="artist">Artist Name</label></p>
            <p><input v-model="artist" class="upload" type="text" name="artist" id="artist" required></p>
            <p><label for="genre">Genre</label></p>
            <p><input v-model="genre" class="upload" type="text" name="genre" id="genre" required></p>
            <div class="mb-3">
                <label for="song" class="upload">Select an MP3 File</label>
                <input @change="handleFileUpload" type="file"  name="songmp3" accept=".mp3" required class="form-control">
            </div>
            <button type="submit" class="btn btn-outline-secondary">Upload</button>
        </form>

    </div>
</div>
</template>

<script>
export default {
    name: "Edit_song",
    data() {
        return {
            song: {},
            album: {},
            sname: "",
            date: "",
            albumName: "",
            lyrics: "",
            artist: "",
            genre: "",
            id :null,
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

                    this.sname = this.song.s_name;
                    this.date = this.song.date;
                    this.albumName = this.album.a_name;
                    this.lyrics = this.song.lyrics;
                    this.artist = this.album.artist;
                    this.genre = this.album.genre;
                    this.id = this.song.s_id;
                    console.log(this.song);
                })
                .catch((error) => {
                    console.error("Error fetching singleSong:", error);
                });
        },
        async onSubmit() {
            let formData = new FormData(); //its a object 
            formData.append('sname', this.sname);
            formData.append('date', this.date);
            formData.append('album_name', this.albumName);
            formData.append('lyrics', this.lyrics);
            formData.append('artist', this.artist);
            formData.append('genre', this.genre);
            formData.append('songmp3', this.song);
            
            try {
                const access_token = localStorage.getItem('access_token')
                const response = await fetch(`http://localhost:5000/C_edit/${this.id}`, {
                    method: "POST",
                    headers: {
                        Authorization:`Bearer ${access_token}`
                    },
                    body: formData
                })
                const data = await response.json()
                if (response.ok) {
                    alert(data.message)
                    //push to the login
                    this.$router.push("/creator_DashBoard")
                } else {
                    alert(data.error)
                }
            } catch (error) {
                console.log("edit error:", error)
                alert("An error occure while editing a song")
            }
        },
        handleFileUpload(event) {
            this.song = event.target.files[0];
        }

    }

}
</script>

<style>

</style>
