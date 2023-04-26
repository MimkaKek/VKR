<script>
import Header from '../components/header/Header.vue'
import Projects  from '../components/main/Projects.vue'

export default {
  components: {
    Header,
    Projects
  }
}
</script>

<template>
  <Header />
  <Projects :type="'public'" />
</template>
