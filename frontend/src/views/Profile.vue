<template>
<div>
    <section class="hero">
        <div class="hero-body">
            <p class="title">
                <b-skeleton size="is-large" :active="loading"></b-skeleton>
                <section v-if="!loading">
                    {{ email }}
                </section>
            </p>
            <p class="subtitle">
                <b-skeleton size="is-large" :active="loading"></b-skeleton>
                <section v-if="!loading">
                    ID: {{ id }}
                </section>
            </p>
        <!-- <p class="desciption">
            Group Name: {{ quote.GROUPNAME.value }}
        </p> -->
        </div>
    </section>
</div>
</template>

<script>
import API_URL from '@/common/config'

export default {
    name: 'Profile',
    data() {
        return {
            loading: true,
            email: null,
            id: null
        }
    },
    methods: {
        getProfileInfo() {
            this.$http.get(API_URL+'/users')
            .then(resp => {
                this.email = resp.data.email;
                this.id = resp.data.id;
            })
            .catch(err => {
                console.log(err);
                if (err.response.status == 401) {
                    this.$store.dispatch('logout')
                    .then(() => this.$router.push('/'));
                } else {
                    this.$buefy.toast.open({
                        type: 'is-danger',
                        message: err.response.data
                    });
                }
            })
            .finally(() => {
                this.loading = false;
            })
        }
    },
    created() {
        this.getProfileInfo()
    }
}
</script>