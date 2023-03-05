<script>
import Table from '../../../common/Table.vue'

export default {
    components: {
        Table
    },
    data() {
        return {
            tableHead: [
                "Название",
                "Тип",
                "Дата",
                "Время"
            ],
            tableInfo: [{
                name: "...",
                type: "...",
                date: "...",
                time: "..."
            }],
        }
    },
    methods: {
        updateTable() {
            console.log("Update button call!");
            return null;
        }
    }
}

</script>

<template>
    <Table :back-btn="false" :update-func="updateTable" :table-head="tableHead" :table-info="tableInfo"></Table>
</template>

<style scoped>

table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
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