<template>
<div>
    <Navbar />
    <div class="bgimg">
        <div class="container" style="border: solid; margin-top: 5%; height: 400px; width: 400px; padding: 50px;">
            <h1>Register as a creator</h1><img src="../assets/creator.png" alt="creator"><br>
            <h3>create new songs Albums and much more.</h3>
            <!-- Role change as creator -->
            <button type="button" @click="newRole()" class="btn btn-primary">
                Register
            </button>
        </div>
    </div>
</div>
</template>

<script>
import Navbar from './Navbar.vue';
export default {
    name: "CreatorRegister",
    components: {
        Navbar,
    },
    data() {
        return {
            username: "",
            role: "",

        }
    },
    methods: {
        async newRole() {
            console.log("button click")
            try {
                const access_token = localStorage.getItem('access_token')
                console.log(access_token)
                const response = await fetch('http://localhost:5000/C_register', {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${access_token}`
                    },
                })
                const data = await response.json()
                if (response.ok) {
                    alert(data.message)
                    //push to the creator dashboard
                    this.$router.push("/creator_DashBoard")
                } else {
                    alert(data.error)
                }
            } catch (error) {
                console.log("Registration error:", error)
                alert("An error occure while registration")
            }
        }

    }

}
</script>

<style scoped>
img {
    width: 15%;
}

.bgimg {
    background-image: url('../assets/B2.jpg');
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    width: 100%;
    height: 100%;
}
</style>
