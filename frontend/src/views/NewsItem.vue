<template>
<div class="newsitem">
    <div class="columns is-centered">
        <div class="column is-half">
            <section v-if="errored">
                <p>We're sorry, we're not able to retrieve this information at the moment, please try back later</p>
                <p>{{ error_text }}</p>
            </section>
            <section class="hero">
                <div class="hero-body">
                    <b-skeleton size="is-large" :active="loading"></b-skeleton>
                    <p class="title" v-if="!loading">
                        {{ article.title }}
                    </p>
                    <p class="subtitle" v-if="!loading">
                        {{ article.published_at }}
                    </p>
                </div>
            </section>
            <div class="content mb-5">
                <b-skeleton size="is-large" :active="loading"></b-skeleton>
                <div v-html="article.body"/>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import axios from 'axios'
import API_URL from '../common/config'

export default {
    name: 'NewsItem',
    data() {
        return {
            article: null,
            body: null,
            loading: true,
            errored: false,
            error_text: null
        }
    },
    mounted() {
        axios.get(API_URL + "/news/moex/" + this.$route.params.id)
        .then(response => {
            this.article = response.data.result;
        })
        .catch(e => {
            console.log(e);
            this.errored = true;
            this.error_text = e;
        })
        .finally(() => (this.loading = false));
    }
}
</script>
