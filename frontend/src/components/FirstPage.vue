<template>
<div class="style">
    <img src="../assets/M4.png" alt="girl" style=" width:30%; position: relative; top: 100px;">
    <img src="../assets/M5.png" alt="girl" style=" width:30%; position: relative; top: 100px; left: 550px;">
    <div class="col-lg-5 mx-4%" style="text-align: center; margin: 3% 25% 0 29%; position: relative; bottom: 400px;">
        <h1 style=" color: white;">Welcom to Music Streaming Application</h1>
        <div class="lead mb-4" style=" padding: 5%; text-align: center;">
            <h2 style="color: white;">Sign Up</h2>
            <!-- <a href="/admin" style="margin-right: 5%;"><button type="button" class="btn btn-primary btn-lg">Admin</button></a><a href="/user"><button type="button" class="btn btn-primary btn-lg">User</button></a> -->
            <div>
                <button @click="adminLogin" style="margin-right: 5%;" class="btn btn-primary btn-lg">Admin</button>
                <button @click="userLogin" class="btn btn-primary btn-lg">User</button>
            </div>
            
        </div>
        <img src="../assets/M3.png" alt="M2" style="width: 50%;">
    </div>
</div>
</template>

<script>
export default {
    name:"FirstPage",
    methods:{
        userLogin(){
            this.$router.push("/sign_up")
        },
        adminLogin(){
          this.$router.push("/admin_login")
        }
    }

}
</script>

<style scoped>
.style{
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab,white);
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
  *{
    /* font-family: 'Merriweather', serif;
    /*font-family: 'Montserrat', sans-serif; */
    /* font-family: 'Raleway', sans-serif; */
    font-family: 'Sacramento', cursive; 
    color:white;
   
  }
</style>
