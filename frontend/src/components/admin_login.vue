<template>
<div class="style">
    <img src="../assets/Sign up-admin.png" alt="user" style="width: 30%; position: relative; left: 200px; top: 100px;">
    <div class="col-lg-3 mx-auto" style="position: relative; bottom: 300px; left: 200px;">
        <h1 style="border: solid white; border-radius: 3%; padding: 5%;">Music Streaming app</h1>
        <h1 class="lh">Admin Login<svg xmlns="http://www.w3.org/2000/svg" width="10%" height="10%" fill="currentColor" class="bi bi-person-fill-lock" viewBox="0 0 16 16">
                <path d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm-9 8c0 1 1 1 1 1h5v-1a1.9 1.9 0 0 1 .01-.2 4.49 4.49 0 0 1 1.534-3.693C9.077 9.038 8.564 9 8 9c-5 0-6 3-6 4Zm7 0a1 1 0 0 1 1-1v-1a2 2 0 1 1 4 0v1a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1v-2Zm3-3a1 1 0 0 0-1 1v1h2v-1a1 1 0 0 0-1-1Z" />
            </svg></h1>
        <form @submit.prevent="onSubmit" class="lead mb-4" style="border: solid white; border-radius: 3%; padding: 5%; text-align: center;">
            <label for="U_name">Email</label><br>
            <p><input type="email" v-model="email" name="username" id="U_name" style="color: black;" required></p>
            <p><label for="U_pass">Password</label></p>
            <p><input type="password" v-model="password" name="password" id="U_pass" required style="color: black;"></p>
            <button class="btn btn-primary" type="submit">Login</button>
        </form>

    </div>
</div>
</template>

<script>
export default {
    name: 'admin_login',
    data(){
        return{
            email:"",
            password : "",
        }
    },
    methods:{
        async onSubmit(){
            const formdata = {
                email: this.email,
                password: this.password,
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
                    this.$router.push("/admin")
                    
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
*{
    font-family: 'Sacramento', cursive;
    color: white;
}
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
</style>
