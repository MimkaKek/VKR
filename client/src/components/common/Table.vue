<script>
import Button from "../common/Button.vue"

export default {

    components: {
        Button
    },

    props: {
        tableHead: {
            type: Object,
            default: {msg: "PLACEHOLDER"}
        },
        tableInfo: {
            type: Array,
            default: [{msg: "PLACEHOLDER"}]
        },
        backFunc: {
            type: Function,
            default() {
                return null;
            }
        },
        updateFunc: {
            type: Function,
            default() {
                return null;
            }
        },
        backBtn: {
            type: Boolean,
            default: true
        },
        updBtn: {
            type: Boolean,
            default: true
        }
    },
    data() {
        return {
            text: {
                buttonBack: "Назад",
                buttonUpdate: "Обновить"
            }
        }
    }
}
</script>

<template>
    <table>
        <tr>
            <th v-for="head in tableHead">{{ head }}</th>
        </tr>
        <template v-for="row in tableInfo">
            <tr>
                <td v-for="item in row">{{ item }}</td>
            </tr>
        </template>
    </table>
    <div class="h-divider"></div>
    <div>
        <Button v-if="backBtn" style="margin-left: 0px" class="btn-size" :title="text.buttonBack" :func="backFunc"></Button>
        <Button v-if="updBtn" style="margin-left: 0px" class="btn-size" :title="text.buttonUpdate" :func="updateFunc"></Button>
    </div>
</template>

<style scoped>

.h-divider {
    background-color: rgb(74, 74, 74);
    height: 1px;
    margin-left: 0px;
    margin-right: 0px;
    margin-top: 5px;
    margin-bottom: 5px;
}

table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
  margin: 0px;
}

td, th {
  border: 1px solid #969696;
  text-align: left; 
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #3f3f3f;
}

</style>