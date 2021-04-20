<template>
    <div>
        <section class="hero">
            <div class="conteiner has-text-centered">
                <div class="hero-body">
                    <p class="title">
                    Registration
                    </p>
                </div>
            </div>
        </section>
        <div class="columns is-centered mb-5">
            <div class="column is-half">
                <section>
                    <b-field label="Name">
                        <b-input placeholder="name"
                            v-model="name"
                        ></b-input>
                    </b-field>
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

                    <b-field label="Confirm password">
                        <b-input type="password" 
                            maxlength="30"
                            placeholder="confirm password"
                            v-model="password_confirmation"
                        ></b-input>
                    </b-field>

                    <input class="button is-primary" type="submit" value="Register">
                </section>   
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Registration',
    data() {
        return {
            name: null,
            email: null,
            password: null,
            password_confirmation: null
        }
    },
    methods: {
        register() {
            // let name = this.name;
            // let email = this.email;
            // let password = this.password;

        }
    } 
}
</script>