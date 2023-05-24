<script>
import Header from '../components/header/Header.vue'
import Share  from '../components/main/Share.vue'

export default {
  components: {
    Header,
    Share
  }
}
</script>

<template>
  <Header :hide-menu="true" :logo-back="true" />
  <Share />
</template>
