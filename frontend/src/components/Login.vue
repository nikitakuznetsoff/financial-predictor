<template>
<div>
    <form class="login" @submit.prevent="login">
        <div class="modal-card" style="width:300px;">
            <section class="modal-card-body">
                <b-field label="Email">
                    <b-input
                        type="email"
                        placeholder="Your email"
                        v-model="email"
                        required>
                    </b-input>
                </b-field>

                <b-field label="Password">
                    <b-input
                        type="password"
                        password-reveal
                        placeholder="Your password"
                        v-model="password"
                        required>
                    </b-input>
                </b-field>

                <b-checkbox>Remember me</b-checkbox>
            </section>
            <footer class="modal-card-foot">
                <input type="submit" class="button is-primary" value="Login">
            </footer>
        </div>
    </form>
</div>
</template>

<script>
export default {
    name: 'Login',
    data() {
        return {
            email: null,
            password: null,
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
                    message: err.response.data
                });
            })
        }
    }
}
</script>
