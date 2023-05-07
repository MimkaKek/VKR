<script>
import Button from './Button.vue';
import InputText from './InputText.vue';
import axios from 'axios';

export default {
    components: {
        Button,
        InputText
    },
    emits: ["updActive", "removeFile"],
    props: {
        meta: {
            type: Object,
            default: {}
        }
    },
    methods: {
        setActive(filename) {

            if (this.lastActive == null) {
                let currBtn = document.getElementById(filename);
                currBtn.disabled = true;
                currBtn.style = "text-align: left; background-color: rgb(97, 97, 97)";
                this.$emit('updActive', filename);
                this.lastActive = filename;
                return null;
            }

            let lastBtn = document.getElementById(this.lastActive);
            let currBtn = document.getElementById(filename);

            lastBtn.disabled = false;
            currBtn.disabled = true;

            lastBtn.style = "text-align: left;";
            currBtn.style = "text-align: left; background-color: rgb(97, 97, 97)";

            this.$emit('updActive', filename);
            this.lastActive = filename;
        },
        renameFile(filename) {
            this.changedName  = String(filename);
            this.isRename     = String(filename);
        },
        renameFileDone(filename) {
            if (filename == this.changedName) {
                this.isRename = null;
                return null;
            }

            const path = 'http://localhost:8000/project/' + this.$route.params.pid + "/" + filename;
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            let rData = { "data": { "name": this.changedName } }

            axios.patch(path, rData, {params: parameters, headers: headers})
                        .then((response) => {
                            
                            console.log("Response: ");
                            console.log(response.data);

                            if (response.data.status != 0) {
                                console.error("Rename file failed!");
                                console.error("Description: " + response.data.description);

                                this.isRename    = null;
                                this.changedName = null;

                                this.$forceUpdate();

                                return null;
                            }

                            if (filename == this.lastActive) {
                                this.lastActive = this.changedName;
                            }

                            Object.defineProperty(this.meta.files, this.changedName, Object.getOwnPropertyDescriptor(this.meta.files, filename));
                            this.meta.files[this.changedName] = {
                                "actions": {
                                    "url": "/project/"  + this.$route.params.pid + "/" + this.changedName,
                                    "methods": ["GET", "PATCH", "DELETE"]
                                }
                            }
                            delete this.meta.files[filename];

                            this.isRename    = null;
                            this.changedName = null;

                            this.$forceUpdate();
                        })
                        .catch((error) => {
                            console.error(error);
                        });

            
        },
        removeFile(filename) {
            const path = 'http://localhost:8000/project/' + this.$route.params.pid + "/" + filename;
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            axios.delete(path, {params: parameters, headers: headers})
                        .then((response) => {
                            
                            console.log("Response: ");
                            console.log(response.data);

                            if (response.data.status != 0) {
                                console.error("Remove project file failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }

                            delete this.meta.files[filename];

                            if (this.lastActive == filename) {
                                this.lastActive = null;
                            }

                            this.$emit('removeFile', filename);

                            this.$forceUpdate();
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        addFile() {
            this.isRename    = String("ad4asDasAdja3fpoIASi2fh");
            this.isCreate    = String("ad4asDasAdja3fpoIASi2fh");
            this.changedName = "";

            this.meta.files[this.isCreate] = {}

            this.$forceUpdate();
        },
        addFileDone(filename) {
            if (filename == this.changedName) {
                this.isRename = null;
                delete this.meta.files[this.changedName];
                this.$forceUpdate();
                return null;
            }

            const path = 'http://localhost:8000/project/' + this.$route.params.pid + "/" + this.changedName;
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };
            
            axios.put(path, null, {params: parameters, headers: headers})
                        .then((response) => {
                            
                            console.log("Response: ");
                            console.log(response.data);

                            if (response.data.status != 0) {
                                console.error("Add project file failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }

                            if (filename == this.lastActive) {
                                this.lastActive = this.changedName;
                            }

                            Object.defineProperty(this.meta.files, this.changedName, Object.getOwnPropertyDescriptor(this.meta.files, filename));
                            this.meta.files[this.changedName] = {
                                "actions": {
                                    "url": "/project/"  + this.$route.params.pid + "/" + this.changedName,
                                    "methods": ["GET", "PATCH", "DELETE"]
                                }
                            }
                            delete this.meta.files[filename];

                            this.isRename    = null;
                            this.isCreate    = null;
                            this.changedName = null;

                            this.$forceUpdate();
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        }
    },
    data() {
        return {
            changedName: null,
            isRename: null,
            lastActive: null,
            isCreate: null
        }
    },
    mounted() {
    }
}
</script>

<template>
    <div class="add-btn">
        <Button style="width: 17%" :func="this.addFile">
            +
        </Button>
    </div>
    <template v-for="(value, file) in this.meta.files" :key="file">
        <div :id="'file_' + file" class="menu-btn">
            <div class="main-btn">
                <template v-if="this.isRename == file">
                    <InputText class="input-btn" v-model="this.changedName" :placeholder="'...'"></InputText>
                </template>
                <template v-else>
                    <Button :id="file" style="text-align: left;" :func="this.setActive" :fArgs="[ file ]">
                            {{ file }}
                    </Button>
                </template>
            </div>
            <div class="sub-btn">
                <Button v-if="this.isRename != file" :func="this.renameFile" :fArgs="[ file ]">
                    ...
                </Button>
                <Button v-else style="font-size: 17px;" :func="this.isCreate == file ? this.addFileDone : this.renameFileDone" :fArgs="[ file ]">
                    ✔
                </Button>
            </div>
            <div class="sub-btn">
                <Button :func="this.removeFile" :fArgs="[ file ]">
                    –
                </Button>
            </div>
        </div>
    </template>
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

.sub-btn {
    width: 20%;
}

.main-btn {
    width: 100%;
}

.add-btn {
    padding: 5px;
}

.menu-btn {
    display: flex;
}

.input-btn {
    width: 100%;
    height: 100%;
    padding: 0px 0px 0px 10px;
    margin: 0px;
    font-size: 20px;
    background-color: rgb(82, 82, 82);
    outline: none;
    border: 0px;
    transition: auto;
    border-radius: 0px;
    color: rgb(233, 233, 233);
}

.input-wrapper {
    padding: 0px;
}

.input-btn:focus {
  border: 0px;
}

</style>