export default{
    name:"UserMixin",
    data(){
        return{
            user:null,
            loggedIn : false,
        }
    },
    async created(){
        await this.checklogin();
    },
    methods:{
        async checklogin(){
            const access_token = localStorage.getItem("access_token");
            if(!access_token){
                this.loggedIn=false;
                return;
            }
            try{
                this.user = await this.fetchuserinfo(access_token);
                this.loggedIn=true;
            }
            catch(error){
                console.log("error feching user info: ",error)
                this.loggedIn=false;
            }
        },
        async fetchuserinfo(access_token){
            const response = await fetch('http://localhost:5000/fetchuserinfo',{
                method : 'GET',
                headers:{
                    "Authorization": `Bearer ${access_token}`
                }
            });
            if(response.status ===401){
                this.loggedIn=false;
                return null;
            }
            return await response.json();
        },
        logout(){
            console.log('button Clicked!')
            fetch('http://localhost:5000/logout',{
                method:"POST",
                credentials:"include",
            })
            .then(() => {
                localStorage.removeItem('access_token');
                this.user = null;
                this.loggedIn=false;
                this.$router.push('/');
            })
            .catch(error =>{
                console.log("Logout error:",error);
            });
        },
        
    }
}