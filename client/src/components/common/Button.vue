<script>
export default {
    props: {
        title: {
            type: String,
            default: "PLACEHOLDER"
        },
        func: {
            type: Function,
            default() {
                return null;
            }
        }
    }
}
</script>

<template>
    <button class="f-btn" @click="func()">
        {{ title }}
    </button>
</template>

<style scoped>

.f-btn {
    display: inline-block;
    border: 0px;
    padding: 8px;
    border: 1px;
    border-style: solid;
    border-color: rgb(70, 70, 70);
    font-size: 20px;
    color: rgb(226, 226, 226);
    background-color: rgb(58, 58, 58);
}

.f-btn:link, .f-btn:visited, .f-btn:focus {
    background: rgb(58, 58, 58);
}

.f-btn:hover {
    background: rgb(65, 65, 65);
}

.f-btn:active {
    background: rgb(63, 63, 63);
}

</style>