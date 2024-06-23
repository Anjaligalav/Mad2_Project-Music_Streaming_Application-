<template>
<div>
    <Navbar />
    <div class="main">
        <div class="card">
            <img src="../assets/profilepic.jpg" alt="profile pic">
            <div class="desc">
                <h1>{{ Myuser.username }}</h1>
                <p>I am a {{ Myuser.role }}.</p>
            </div>
        </div>
        <router-link to="/createPlaylist" class="btn btn-secondary btn-block">Create new Playlist</router-link>

        <div v-if="Object.keys(play).length > 0">
            <div class="dropdown" style="margin: 10px;">
                <button class="btn btn-info dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false" style="margin-left:6%; margin-bottom: 3.5%;">
                    Your Playlist
                </button>

                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                    <li v-for="play in play" :key="play.id">
                        <div style="display: flex;">
                            <router-link :to="{name: 'myPlaylist' ,params:{ id : play.id } }" class="dropdown-item">{{ play.name }}</router-link>
                            <div class="col-4 text-right">
                                <button @click="deletePlaylist(play.id)" class="btn-dark">delete</button>
                            </div>
                        </div>
                        <hr size="6">
                    </li>
                </ul>

            </div>
            <!-- :to="{ name: 'myPlaylist', params: { p_name: play.name } }" -->
        </div>
        <p v-else>Create a new PlayList</p>
    </div>
</div>
</template>

<script>
import Navbar from './Navbar.vue';
import UserMixin from '../mixin/userMixin';
export default {
    mixins: [UserMixin],
    name: "profile",
    components: {
        Navbar,
    },

    data() {
        return {
            Myuser: {},
            play: {},
        }
    },
    created() {
        // Watch for changes in user data
        this.$watch('user', (newValue, oldValue) => {
            if (newValue && newValue.id) {
                const id = newValue.id;
                this.playLists(id);
                this.Myuser = newValue;
            } else {
                console.error("User data is not available.");
            }
        });
    },
    methods: {
        playLists(id) {
            fetch(`http://localhost:5000/single_playlist/${id}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    this.play = data.data
                    console.log(typeof (this.play))
                })
                .catch((error) => {
                    console.error("Error fetching songs:", error);
                });
        },
        deletePlaylist(id) {
            const confirmed = window.confirm(`Are you sure to delete this Song?`);
            if (!confirmed) {
                return;
            }
            fetch(`http://localhost:5000/delete_playlist/${id}`, {
                    method: "DELETE",
                    headers: {
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Playlist deletion failed');
                    }
                    return response.json();
                })
                .then((data) => {
                    alert(data.message)
                })
                .catch((error) => {
                    console.error("Error deleting playlist:", error);
                    if (error.message === '404') {
                        alert("User or playlist not found.");
                    } else {
                        alert("An error occurred while deleting the playlist. Please try again later.");
                    }
                });
        }
    }

}
</script>

<style scoped>
.card {
    width: 300px;
    height: 400px;
    border: 2px solid black;
    align-items: center;
    margin: 10px;
    border-radius: 5px;
    box-shadow: 7px 7px 8px black;
    transition: 1s;
}

.desc {
    padding: 0 2px 0 2px;
}

.card:hover {
    box-shadow: 0 15px 20px goldenrod;
}

img {
    width: 100%;
}

.main {
    display: flex;

}

.btn {
    width: 200px;
    height: 50px;
    /* margin: 10px; */
    border: 2px solid black;
    margin: 10px;
    border-radius: 5px;
    box-shadow: 7px 7px 8px black;
    transition: 1s;
}

.btn:hover {
    box-shadow: 0 15px 20px goldenrod;
}
</style>
