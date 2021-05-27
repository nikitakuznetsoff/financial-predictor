<template>
<div>
    <form class="login" @submit.prevent="login">
        <div class="modal-card" style="width:300px;">
            <section class="modal-card-body">
                <b-field label="Электронная почта">
                    <b-input
                        type="email"
                        placeholder="Введите адрес"
                        v-model="email"
                        required>
                    </b-input>
                </b-field>

                <b-field label="Пароль">
                    <b-input
                        type="password"
                        password-reveal
                        placeholder="Введите пароль"
                        v-model="password"
                        required>
                    </b-input>
                </b-field>

                <!-- <b-checkbox>Запомнить меня</b-checkbox> -->
            </section>
            <footer class="modal-card-foot">
                <input type="submit" class="button is-primary" value="Войти">
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
                if (err.response.status == 404) {
                    this.$buefy.toast.open({
                        type: 'is-danger',
                        message: 'Пользователь не найден. Зарегистрируйтесь для использоваения платформы.'
                    }); 
                } else if (err.response.status == 400) {
                    this.$buefy.toast.open({
                        type: 'is-danger',
                        message: 'Неверный пароль'
                    }); 
                } else {
                   this.$buefy.toast.open({
                        type: 'is-danger',
                        message: err.response.data
                    }); 
                }
                
            })
        }
    }
}
</script>
