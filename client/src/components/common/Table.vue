<script>
import Button from './Button.vue';

export default {
    components: {
        Button
    },
    props: {
        tHead: {
            type: Array,
            default: ["Head 1", "Head 2", "Head 3"]
        },
        tData: {
            type: Array,
            default: [["Data 1-1", "Data 1-2", "Data 1-3"], ["Data 2-1", "Data 2-2", "Data 2-3"], ["Data 3-1", "Data 3-2", "Data 3-3"]]
        },
        tActions: {
            type: Array,
            default: [[null, null, null], [null, null, null], [null, null, null]]
        },
        isArray: {
            type: Array,
            default: [false, false, false]
        }
    },
    data() {
        return {}
    }
}
</script>

<template>
    <table>
        <tr>
            <th v-for="headItem in tHead">
                {{ headItem }} 
            </th>
        </tr>
        <template v-for="(line, yPos) in tData">
            <tr>
                <template v-for="(item, xPos) in line">
                    <template v-if="this.isArray[xPos]">
                        <td class="btn">
                            <div class="many-items-inline">
                                <template v-for="(subItem, zPos) in item">
                                    <template v-if="this.tActions[yPos][xPos][zPos] == null">
                                        {{ subItem }}
                                    </template>
                                    <template class="btn" v-else>
                                        <Button :func="this.tActions[yPos][xPos][zPos][0]" :fArgs="this.tActions[yPos][xPos][zPos][1]">
                                            {{ subItem }}
                                        </Button>
                                    </template>
                                </template>
                            </div>
                        </td>
                    </template>
                    <template v-else>
                        <td v-if="this.tActions[yPos][xPos] == null">
                            {{ item }}
                        </td>
                        <td class="btn" v-else>
                            <Button :func="this.tActions[yPos][xPos][0]" :fArgs="this.tActions[yPos][xPos][1]">
                                {{ item }}
                            </Button>
                        </td>
                    </template>
                </template>
            </tr>
        </template>
    </table>
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

  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

td, th {
  border: 1px solid #969696;
  text-align: center; 
  padding: 8px;
}
tr {
  background-color: rgb(65, 65, 65);
}

td.btn, div.btn {
    padding: 0px;
}
.many-items-inline {
    display: flex;
}
tr {
  background-color: rgb(65, 65, 65);
}

</style>