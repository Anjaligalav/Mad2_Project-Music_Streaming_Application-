<template>
<div class="body">
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
        <h1 style="color: white;">Administrator DashBoard</h1>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item" style="margin-left: 500%;">
                    <router-link to="/admin2" class="nav-link"><h1>Tracks</h1></router-link>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container" style="margin-top: 3%;">
        <div class="row" style="border: 3px solid slategrey; padding: auto; border-radius: 2%;">
            <div class="col-lg-3">
                <span style="display: inline;  font-size: large; color: white;"><strong>Total_no._of_users<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
                            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z" />
                        </svg></strong></span>
                <h3 style="text-align: center; color: white;">{{total_user}}</h3>
            </div>
            <div class="col-lg-3">
                <span style="display: inline;  font-size: large; color: white;"><strong>Total_no._Of_tracks </strong></span>
                <p style="margin-left: 60px; color: white;;"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-disc-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-6 0a2 2 0 1 0-4 0 2 2 0 0 0 4 0zM4 8a4 4 0 0 1 4-4 .5.5 0 0 0 0-1 5 5 0 0 0-5 5 .5.5 0 0 0 1 0zm9 0a.5.5 0 1 0-1 0 4 4 0 0 1-4 4 .5.5 0 0 0 0 1 5 5 0 0 0 5-5z" />
                    </svg></p>
                <h3 style="text-align: center;color: white;">{{total_song}}</h3>
            </div>
            <div class="col-lg-3">
                <span style="display: inline;  font-size: large; color: white;"><strong>Total_Number_Of_Albums </strong></span>
                <h3 style="text-align: center;color: white;">{{total_album}}</h3>
            </div>
            <div class="col-lg-3">
                <span style="display: inline;  font-size: large; color: white;"><strong>Total_Number_Of_Genre </strong></span>
                <h3 style="text-align: center;color: white;">{{total_genre}}</h3>
            </div>
        </div>

        <div class="row" style="border: 3px solid slategrey; padding: auto; border-radius: 2%; margin-top: 3%;">
            <div class="col-lg-4">
                <span style="display: inline;  font-size: large; color: white;"><strong>Total Number of Creators🙍‍♂️ </strong></span>
                <h3 style="text-align: center;color: white;">{{total_creator}}</h3>
                <img src="../assets/Admin1.png" alt="M2" style="width: 120%;">
            </div>
            <div class="col-lg-8">
                <canvas id="myChart" width="400" height="400"></canvas>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Chart from 'chart.js/auto';
export default {
    name: "admin",
    data() {
        return {
            total_song: "",
            total_album: "",
            total_user: "",
            total_creator: "",
            total_genre: "",
            genres_list: [],
            avg_list: [],
        }
    },
    mounted() {
        // Call fetchadminInfo method when the component is mounted
        this.fetchadminInfo();
    },
    methods: {
        fetchadminInfo() {
            fetch("http://localhost:5000/fetchAdminInfo", {
                    method: "GET",
                    headers: {
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    this.total_song = data.data.total_album;
                    this.total_album = data.data.total_album;
                    this.total_user = data.data.total_user;
                    this.total_creator = data.data.total_creator;
                    this.total_genre = data.data.total_genre;
                    this.avg_list = data.data.avg_list
                    this.genres_list = data.data.genres_list

                    this.createChart();
                })
                .catch((error) => {
                    console.error("Error fetching songs:", error);
                });
        },
        createChart() {
            const ctx = document.getElementById('myChart').getContext('2d');

            if (!ctx) {
                console.error("Canvas element not found");
                return;
            }

            if (this.avg_list.length === 0 || this.genres_list.length === 0) {
                console.error("Data arrays are empty");
                return;
            }

            const chartData = {
                labels: this.genres_list,
                datasets: [{
                    label: 'Average Rating',
                    data: this.avg_list,
                    backgroundColor: 'rgba(255, 102, 102, 0.2)',
                    borderColor: 'rgba(255, 51, 51, 1)',
                    borderWidth: 1
                }]
            };

            new Chart(ctx, {
                type: 'bar',
                data: chartData,
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                color: 'white' // Change color of Y-axis labels to white
                            }
                        },
                        x: {
                            ticks: {
                                color: 'white' // Change color of X-axis labels to white
                            }
                        }
                    }
                }
            });
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

.col-lg-3 {
    border: 3px solid slategrey;
    border-radius: 4%;

    padding: 4%;
}

.col-lg-6 {
    border: 3px solid slategrey;
    border-radius: 4%;

}

.col-lg-4 {
    border: 3px solid slategrey;
    border-radius: 4%;
    padding: 4%;
}

.col-lg-3:hover {
    background-color: rgb(212, 220, 229, 0.3);
}

.col-lg-4:hover {
    background-color: rgb(212, 220, 229, 0.3);
}

* {
    font-family: 'Sacramento', cursive;
}

.body {
    background-image: url('../assets/background.jpg');
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
}
</style>
