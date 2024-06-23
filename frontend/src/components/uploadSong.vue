<template>
<div>
    
    <div class="col-lg-6 mx-auto bg_img" style="margin-top: 2%;">
        <h1 style="text-align: center;">Upload your song.</h1>
        <form @submit.prevent="onSubmit" enctype="multipart/form-data" class="lead mb-4" style="border: solid slategrey; border-radius: 3%; padding: 10%;">
            <label for="sname">Song Name</label><br><br>
            <input v-model="sname" class="upload" type="text" name="sName" id="sName" required><br><br>
            <p><label for="date">Release Date</label></p>
            <p><input v-model="date" class="upload" type="date" name="date" id="date" required></p>
            <p><label for="maker">Album_Name</label></p>
            <p><input v-model="album" class="upload" type="text" name="album_name" id="maker" required></p>
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
    name: "uploadSong",
    data() {
        return {
            sname: "",
            date: "",
            album: "",
            lyrics: "",
            artist: "",
            genre: "",
            song: "",

        }
    },
    methods: {
        async onSubmit() {
            let formData = new FormData(); //its a object 
            formData.append('sname', this.sname);
            formData.append('date', this.date);
            formData.append('album_name', this.album);
            formData.append('lyrics', this.lyrics);
            formData.append('artist', this.artist);
            formData.append('genre', this.genre);
            formData.append('songmp3', this.song);
            
            try {
                const access_token = localStorage.getItem('access_token')
                const response = await fetch('http://localhost:5000/upload', {
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
                console.log("upload error:", error)
                alert("An error occure while uploading a song")
            }
        },
        handleFileUpload(event) {
            this.song = event.target.files[0];
        }
    }
}
</script>

<style scoped>
.upload:hover {
    background-color: rgb(212, 220, 229);
}

.bg_img {
    background-image: url('../assets/M2.png');
    background-repeat: no-repeat;
    background-size: contain;
}

label {
    font-weight: bold;
}
</style>
