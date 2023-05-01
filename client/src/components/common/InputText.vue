<script>
export default {
    props: {
      modelValue: {
        type: String,
        default: null
      },
      textarea: {
        type: Boolean,
        default: false
      },
      placeholder: {
        type: String,
        default: "..."
      },
      locked: {
        type: Boolean,
        default: false
      }
    },
    emits: ['update:modelValue']
}
</script>

<template>
      <input v-if="!this.textarea" :placeholder="placeholder" :readonly="this.locked" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"/>
      <textarea v-else :placeholder="placeholder" :readonly="this.locked" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"></textarea>
</template>

<style scoped>

input, textarea {
    width: 100%;
    height: 100%;
    padding: 12px 20px;
    margin-top: 10px;
    margin-bottom: 10px;
    background-color: rgb(92, 92, 92);
    outline: none;
    border: 2px solid rgb(90, 90, 90);
    border-radius: 15px;
    transition: border 0.25s linear 0s;
    color: rgb(233, 233, 233);
}

textarea:focus, input:focus {
  border: 2px solid rgb(165, 165, 165);
}

textarea {
    resize: none; 
}



</style>