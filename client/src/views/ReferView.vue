<script>
import Header from '../components/header/Header.vue'
import Refer  from '../components/main/Refer.vue'

export default {
  components: {
    Header,
    Refer
  },
  mounted() {
    console.log("REFER MOUNTED");
  }
}
</script>

<template>
  <Header />
  <Refer />
</template>
