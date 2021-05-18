<template>
    <div>
        <section class="hero">
            <div class="conteiner has-text-centered">
                <div class="hero-body">
                    <p class="title">
                    Регистрация
                    </p>
                </div>
            </div>
        </section>
        <div class="columns is-centered mb-5">
            <div class="column is-half">
                <form class="register" @submit.prevent="register()">
                    <section>
                        <!-- <b-field label="Name">
                            <b-input placeholder="name"
                                v-model="name"
                            ></b-input>
                        </b-field> -->
                        <!-- type="is-danger"
                        message="This email is invalid" -->
                        <b-field label="Электронная почта">
                            <b-input type="email"
                                maxlength="30"
                                placeholder="почта"
                                v-model="email"
                            >
                            </b-input>
                        </b-field>
                        <!-- type="is-warning"
                        :message="['Password is too short', 'Password must have at least 8 characters']" -->
                        <b-field label="Пароль">
                            <b-input type="password" 
                                maxlength="30"
                                placeholder="пароль"
                                v-model="password"
                            ></b-input>
                        </b-field>
                        <b-field label="Подтвеждение пароля"
                            v-bind:type="label_type"
                            v-bind:message="label_text"
                        >
                            <b-input type="password" 
                                maxlength="30"
                                placeholder="подтверждение пароля"
                                v-model="password_confirmation"
                            ></b-input>
                        </b-field>
                        <input class="button is-primary" type="submit" value="Зарегистрироваться">
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
            // name: null,
            email: null,
            password: null,
            password_confirmation: null,
            label_type: null,
            label_text: null
        }
    },
    methods: {
        register() {
            let email = this.email;
            let password = this.password;
            let pass_conf = this.password_confirmation;
            if (password != pass_conf) {
                this.label_type = 'is-danger';
                this.label_text = 'Пароли не совпадают'
            } else {
                this.$store.dispatch('register', { email, password })
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
}
</script>