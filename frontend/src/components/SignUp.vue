<template>
<div class="style">
    <img src="../assets/Sign up-user.png" alt="user" style="width: 30%; position: relative; left: 200px; top: 100px;">
    <div class="col-lg-3 mx-auto" style="position: relative; bottom: 350px;left: 200px;">

        <h3 style="border: solid white; border-radius: 3%; padding: 5%;">Music Streaming app</h3>
        <h1 class="lh">User Sign up</h1>
        <form @submit.prevent="signup" class="lead mb-4" style="border: solid white; border-radius: 3%; padding: 5%; text-align: center;">
            <label for="U_name">Name</label><br>
            <p><input v-model="name" type="text" name="username" id="U_name" style="color: black;" required></p>
            <p><label for="email">Email</label></p>
            <p><input v-model="email" type="email" name="email" id="email" style="color: black;" required></p>
            <p><label for="U_pass">Password</label></p>
            <p><input v-model="password" type="password" name="password" id="U_pass" style="color: black;" required></p>

            <button class="btn btn-primary" type="submit">sign up</button>
        </form>
        <p>Already a member?</p>
        <!-- Login modal -->
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
            Login
        </button>

        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true"  v-show="showModal">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel" style="color: black;">Login</h5>
                        <button type="button" class="btn-close" @click="closeModal" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="login">
                            <div class="mb-3">
                                <label for="email2" style="color: black;">Email</label>
                                <input v-model="email2" type="email" name="email" id="email2" style="color: black;" aria-describedby="emailHelp">
                            </div>
                            <div class="mb-3">
                                <label for="password" style="color: black;">Password</label>
                                <input v-model="password2" type="password" name="password" style="color: black;" id="password">
                            </div>
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>

export default {
    name: "sign_up",
    data() {
        return {
            name: "",
            email: "",
            password: "",
            email2: "",
            password2: "",
            showModal: false,

        };
    },
    methods: {
        async signup() {
            const formdata = {
                username: this.name,
                email: this.email,
                password: this.password,
            }
            try {
                const response = await fetch('http://localhost:5000/sign_up', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(formdata)
                })
                const data = await response.json()
                if (response.ok) {
                    alert(data.message)
                    //push to the login
                    localStorage.setItem('access_token', data.access_token)
                    this.$router.push("/Home")
                } else {
                    alert(data.error)
                }
            } catch (error) {
                console.log("Registration error:", error)
                alert("An error occure while registration")
            }
        },
        async login() {
            const formdata = {
                email: this.email2,
                password: this.password2,
            }
            try {
                const response = await fetch('http://localhost:5000/login', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(formdata)
                })
                const data = await response.json()
                if (response.ok) {
                    alert(data.message)
                    localStorage.setItem('access_token', data.access_token)
                    //push to the login
                    this.showModal=false
                    document.body.style.overflow = 'auto';
                    this.$router.push("/Home")
                    
                } else {
                    alert(data.error)
                }
            } catch (error) {
                console.log("login error:", error)
                alert("An error occure while Login")
            }
        },

    }
}
</script>

<style scoped>
.style {
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab, white);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    height: 100vh;
}

@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

* {
    /* font-family: 'Merriweather', serif;
    /*font-family: 'Montserrat', sans-serif; */
    /* font-family: 'Raleway', sans-serif; */
    font-family: 'Sacramento', cursive;
    color: white;

}
</style>
