<template>
   <div>
    <div v-if="loggedIn">
      <CreatorDashboard v-if="user && user.role === 'creator'" />
      <CreatorRegister v-else />
    </div>
    <p v-else>You are not logged in</p>
   </div>
  
</template>

<script>
import CreatorRegister from './CreatorRegister.vue';
import CreatorDashboard from './CreatorDashboard.vue';
import UserMixin from '../mixin/userMixin';
export default {
    mixins:[UserMixin],
    name:"C_LoginOrSignup",
    components:{
        CreatorRegister,
        CreatorDashboard
    }
}
</script>

<style>

</style>