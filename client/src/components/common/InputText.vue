<script>
export default {
    props: ['modelValue'],
    emits: ['update:modelValue']
}
</script>

<template>
    <input
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<style scoped>

input {
    width: 90%;
    padding: 12px 20px;
    margin-top: 20px;
    background-color: rgb(92, 92, 92);
    outline: none;
    border: 2px solid rgb(90, 90, 90);
    border-radius: 15px;
    transition: border 0.25s linear 0s;
}

input:focus {
  border: 2px solid rgb(165, 165, 165);
}

</style>