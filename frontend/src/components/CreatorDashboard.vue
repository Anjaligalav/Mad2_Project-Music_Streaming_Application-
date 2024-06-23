<template>
<div>
    <Navbar />
    <div class="container" style="margin-top: 3%;">
        <h1>UserName 's DashBoard</h1>
        <div class="row" style="border: 3px solid rgb(71, 103, 134); padding: auto; border-radius: 2%;background-color: rgb(212, 220, 229);">
            <div class="col-lg-3">
                <span style="display: inline;  font-size: large; color: white;"><strong>Total Songs Uploaded</strong></span>
                <h3 style="text-align: center;">{{ total_song }}</h3>
            </div>
            <div class="col-lg-3">
                <span style="display: inline;  font-size: large; color: white"><strong>Total Number Of Albums </strong></span>
                <h3 style="text-align: center;">{{ total_album }}</h3>
            </div>
            <div class="col-lg-3">
                <span style="display: inline;  font-size: large; color: white"><strong>Avrage Rating</strong></span>
                <h3 style="text-align: center;">{{ avg }}</h3>
            </div>
        </div>
    </div>

    <div class="container" style="margin-top: 3%;">
        <h1>Your Uploads!</h1>
        <div style="display: flex;">

            <!-- button type="button" class="btn btn-outline-info" style="position: relative;left: 70%;"><a href="/upload/{{user.id}}" class="btn btn-outline-secondary"><strong>Albums info</strong></a></button>  < -->
            <!-- Button trigger modal -->
            <button class="btn " style="position: relative;left: 70%;background-color: #8CB9BD;" data-bs-toggle="modal" data-bs-target="#exampleModal">
                <strong>Albums info</strong>
            </button>

            <!-- Modal -->
            <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">All Albums</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div v-for="al in album" :key="al.a_id">
                            <div class="card" style="margin-top: 1%; border: 3px solid slategrey; color: rgb(71, 103, 134);">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-8">
                                            <h5 class="card-title">{{ al.a_name}}</h5>
                                        </div>

                                        <div class="col-4 text-right">
                                            <button class="btn btn-danger mr-2" @click="deleteAlbum(al.a_id)">Delete
                                                    <img src="../assets/delete.png" alt="delete" style="width: 30px;"></button>
                                        </div>

                                    </div>
                                </div>
                            </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>

            <button class="btn btn-outline-info btn-lg" style=" margin-left:72%;">
                <router-link to="/uploadSong" class="btn btn-secondary btn-lg "><strong>Upload a song</strong></router-link>
            </button>
        </div>
        <div v-for="song in song" :key="song.s_id">
            <div class="card" style="margin-top: 1%; border: 3px solid slategrey; color: rgb(71, 103, 134);">
                <div class="card-body">
                    <div class="row">
                        <div class="col-8">
                            <h5 class="card-title">{{song.s_name}}</h5>
                        </div>
                        <div class="col-4 text-right">
                            <router-link :to="{name:'Edit_song',params: { s_id:song.s_id } }" class="btn btn-primary mr-2">Edit ✏ </router-link>
                            <button class="btn btn-danger" @click="deleteSong(song.s_id)">
                                Delete
                                <img src="../assets/delete.png" alt="delete" style="width: 30px;">
                            </button>
                            <router-link :to="{ name: 'lyrics', params: { s_id: song.s_id } }" class="btn mr-2" style="background-color: #59D5E0; border-color: #b8daff;">View <img src="../assets/view.png" alt="view"></router-link>
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
import UserMixin from '../mixin/userMixin';
export default {
    mixins: [UserMixin],
    name: "CreatorDashboard",
    components: {
        Navbar,
    },
    data() {
        return {
            song: [],
            album: [],
            avg: null,
            total_song: null,
            total_album: null,
        }
    },
    created() {
        // Watch for changes in user data
        this.$watch('user', (newValue, oldValue) => {
            if (newValue && newValue.id) {
                const id = newValue.id;
                this.allSongs(id);
            } else {
                console.error("User data is not available.");
            }
        });
    },
    methods: {
        allSongs(id) {
            fetch(`http://localhost:5000/fetch_song_by_creator/${id}`, {
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
                    this.avg = data.data.avg;
                    this.total_song = data.data.total_songs
                    this.total_album = data.data.total_album
                    console.log(this.song);
                })
                .catch((error) => {
                    console.error("Error fetching songs:", error);
                });
        },
        deleteSong(s_id) {
            const confirmed = window.confirm(`Are you sure to delete this Song?`);
            if (!confirmed) {
                return;
            }
            fetch(`http://localhost:5000/C_delete/${s_id}`, {
                    method: "DELETE",
                    headers: {
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('song deletion failed');
                    }
                    return response.json();
                })
                .then((data) => {
                    alert(data.message)
                    this.$router.push("/creator_DashBoard")
                })
                .catch((error) => {
                    console.error("Error deleting song:", error);
                    if (error.message === '404') {
                        alert("User or song not found.");
                    } else {
                        alert("An error occurred while deleting the song. Please try again later.");
                    }
                });;
        },
        deleteAlbum(s_id) {
            const confirmed = window.confirm(`Are you sure to delete this album?`);
            if (!confirmed) {
                return;
            }
            fetch(`http://localhost:5000/C_A_delete/${s_id}`, {
                    method: "DELETE",
                    headers: {
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('song deletion failed');
                    }
                    return response.json();
                })
                .then((data) => {
                    alert(data.message)
                    this.$router.push("/creator_DashBoard")
                })
                .catch((error) => {
                    console.error("Error deleting album:", error);
                    if (error.message === '404') {
                        alert("User or song not found.");
                    } else {
                        alert("An error occurred while deleting the album. Please try again later.");
                    }
                });;
        }
    }
}
</script>

<style scoped>
.col-lg-3 {
    border: 3px solid slategrey;
    border-radius: 4%;
    margin: 4%;
    padding: 5%;
}

.col-lg-3 {
    background-image: url('../assets/background.jpg');
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
}

.row:hover {
    background-color: white;
}

.row {
    background-color: rgb(212, 220, 229);
}

h3 {
    color: white;
}
img{
    width: 20px;
    height: 20px;
}
</style>
