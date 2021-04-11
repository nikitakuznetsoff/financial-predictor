<template>
  <div class="news mx-3">
    <div class="columns">
      <div class="column is-two-thirds">
        <News></News>
      </div>
      <div class="column">
        <section class="hero">
          <div class="hero-body">
            <p class="title">
              Second
            </p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
// import HelloWorld from '@/components/HelloWorld.vue'
import News from '@/components/News.vue'

export default {
  name: 'Home',
  components: {
    News
  }
}
</script>
