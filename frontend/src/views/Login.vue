<template>
    <div>
        <section class="hero">
            <div class="conteiner has-text-centered">
                <div class="hero-body">
                    <p class="title">
                        Authorization
                    </p>
                </div>
            </div>
        </section>
        <div class="columns is-centered mb-5">
            <div class="column is-half">
                <form class="register" @submit.prevent="login()">
                    <section>
                        <!-- <b-field label="Name">
                            <b-input placeholder="name"
                                v-model="name"
                            ></b-input>
                        </b-field> -->
                        <!-- type="is-danger"
                        message="This email is invalid" -->
                        <b-field label="Email">
                            <b-input type="email"
                                maxlength="30"
                                placeholder="email"
                                v-model="email"
                            >
                            </b-input>
                        </b-field>
                        <!-- type="is-warning"
                        :message="['Password is too short', 'Password must have at least 8 characters']" -->
                        <b-field label="Password">
                            <b-input type="password" 
                                maxlength="30"
                                placeholder="password"
                                v-model="password"
                            ></b-input>
                        </b-field>
                        <input class="button is-primary" type="submit" value="Login">
                    </section>
                </form>
   
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Registration',
    data() {
        return {
            email: null,
            password: null,
            label_type: null,
            label_text: null
        }
    },
    methods: {
        login() {
            let email = this.email;
            let password = this.password;
            this.$store.dispatch('login', { email, password })
            .then(() => this.$router.push('/'))
            .catch(err => {
                console.log(err);
                this.$buefy.toast.open({
                    type: 'is-danger',
                    message: err
                });
            })
        }
    } 
}
</script>