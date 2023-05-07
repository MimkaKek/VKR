<script>
import Header from '../components/header/Header.vue'
import Editor from '../components/main/Editor.vue'

export default {
  components: {
    Header,
    Editor
  }
}
</script>

<template>
  <Header :logoBack="true" :hideMenu="true" />
  <Editor />
</template>
