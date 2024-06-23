<template>
<div class="body">
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
        <h1 style="color: white;">Administrator</h1>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item" style="margin-left: 400%;">
                    <router-link to="/admin" class="nav-link"><h1>Dashboard</h1></router-link>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container" style="margin-top: 3%;">
        <h1 style="color: white;">All Songs</h1>
        <div v-for="(song, index) in songs" :key="song.s_id">
            <div class="card" style="margin-top: 1%; border: 3px solid slategrey; color: rgb(71, 103, 134);">
                <div class="card-body">
                    <div class="row">
                        <div class="col-8">
                            <h5 class="card-title">{{ song.s_name }}</h5>
                        </div>
                        <div class="col-4 text-right">
                            
                            <button class="btn btn-danger mr-2" style="margin-left: 20%;" @click="deleteSong(song.s_id)">
                            Delete
                            </button>
                            <!-- Button trigger modal -->
                            <button class="btn btn-info btn-lg" style="margin-left: 10%;" data-bs-toggle="modal" :data-bs-target="'#exampleModal' + index">
                                View
                            </button>

                            <!-- Modal -->
                            <div class="modal fade" :id="'exampleModal' + index" tabindex="-1" :aria-labelledby="'exampleModalLabel' + index" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" :id="'exampleModalLabel' + index">Lyrics</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            {{song.lyrics}}
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>
</template>

<script>
export default {
    name: "admin2",
    data() {
        return {
            songs: [],
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
        deleteSong(s_id) {
            const confirmed = window.confirm(`Are you sure to delete this Song?`);
            if (!confirmed) {
                return;
            }
            fetch(`http://localhost:5000/admin_delete/${s_id}`, {
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
                    this.$router.push("/admin2")
                })
                .catch((error) => {
                    console.error("Error deleting song:", error);
                    if (error.message === '404') {
                        alert("song not found.");
                    } else {
                        alert("An error occurred while deleting the song. Please try again later.");
                    }
                });;
        }
        
    }

}
</script>

<style scoped>
/* Custom CSS for navbar */
.navbar-custom {
    background-color: #343a40;
    /* Dark background color */
}

.navbar-custom .navbar-brand,
.navbar-custom .navbar-nav .nav-link {
    color: #fff;
    /* Text color */
}

.row:hover {
    background-color: rgb(212, 220, 229);
}

* {
    font-family: 'Sacramento', cursive;
}

.body {
    background-image: url("../assets/background.jpg");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
}
</style>
