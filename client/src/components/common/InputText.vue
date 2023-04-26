<script>
export default {
    props: {
      modelValue: {
        type: Object,
        default: null
      },
      textarea: {
        type: Boolean,
        default: false
      },
      placeholder: {
        type: String,
        default: "..."
      }
    },
    emits: ['update:modelValue']
}
</script>

<template>
    <input :placeholder="placeholder" v-if="!this.textarea" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"/>
    <textarea v-if="this.textarea" :placeholder="placeholder" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"></textarea>
</template>

<style scoped>

input, textarea {
    width: 100%;
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

textarea {
    resize: none; 
}

input:focus {
  border: 2px solid rgb(165, 165, 165);
}

</style>