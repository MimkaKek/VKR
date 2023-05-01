<script>
import Header from '../components/header/Header.vue'
import Settings  from '../components/main/Settings.vue'

export default {
  components: {
    Header,
    Settings
  }
}
</script>

<template>
  <Header :logo-back="true" />
  <Settings :create="true" />
</template>
