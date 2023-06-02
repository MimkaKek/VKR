<script>
import Button from '../common/Button.vue';
import Sidebar from '../common/Sidebar.vue';
import { Codemirror } from 'vue-codemirror';
import { javascript } from '@codemirror/lang-javascript';
import { html } from '@codemirror/lang-html';
import { css } from '@codemirror/lang-css';
import { oneDark } from '@codemirror/theme-one-dark';
import axios from 'axios';
import { _ } from 'lodash'

export default {
    props: {
    },
    components: {
        Button,
        Codemirror,
        Sidebar
    },
    data() {
        return {
            meta: {},
            content: "",
            activeFile: "",
            rootFile: null,
            languages: {
                "html": html,
                "css": css,
                "js": javascript
            },
            preview: "",
            extensions: [oneDark]
        }
    },
    methods: {
        removeFile(filename) {
            if (this.activeFile == filename) {
                this.content = "";
            }
        },
        getFileContent(filename) {

            if (filename.includes(".")) {
                let lang = filename.split(".")[1];
                this.extensions = [this.languages[lang](), oneDark];
            }
            else {
                this.extensions = [oneDark];
            }


            const path = 'http://localhost:8000/project/' + this.$route.params.pid + "/" + filename;
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            axios.get(path, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Get project data failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }
                            this.content = response.data.data;
                            this.activeFile = filename;
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        getPreview() {

            if (!this.rootFile) {
                return null;
            }

            const path = 'http://localhost:8000/project/' + this.$route.params.pid + "/" + this.rootFile + "/preview";
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            axios.get(path, {params: parameters, headers: headers})
                        .then((response) => {
                            this.preview = response.data;
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        setPreview() {
            this.rootFile = this.activeFile;
            this.getPreview();
        },
        autoSave: _.debounce(function () {
            const path = 'http://localhost:8000/project/' + this.$route.params.pid + "/" + this.activeFile;
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };
            
            let rData = { "data": {"content": this.content }}

            axios.patch(path, rData, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Patch project file failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }
                            this.getPreview();
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        }, 1000)
    },
    mounted() {
        const path = 'http://localhost:8000/project/' + this.$route.params.pid;
            
        var sid = this.$store.getters['auth/sid'];
        const parameters = {
            sid: sid
        };

        const headers = {
            'Content-Type': 'application/json'
        };

        axios.get(path, {params: parameters, headers: headers})
                    .then((response) => {
                        if (response.data.status != 0) {
                            console.error("Get project data failed!");
                            console.error("Description: " + response.data.description);
                            return null;
                        }

                        this.meta = response.data.data;
                    })
                    .catch((error) => {
                        console.error(error);
                    });
    }
}

</script>

<template>
    <div class="main">
        <div class="sidebar">
            <Sidebar :meta="this.meta" v-on:updActive="this.getFileContent" v-on:removeFile="this.removeFile">

            </Sidebar>
        </div>
        <div class="editor">
            <codemirror
                id="editor"
                v-on:change="this.autoSave"
                v-model="this.content"
                placeholder="..."
                :style="{ height: '100%' }"
                :autofocus="true"
                :indent-with-tab="true"
                :tab-size="4"
                :extensions="this.extensions"
            />
        </div>
        <div class="root-wrapper">
            <div class="root-btn">
                <Button :func="this.setPreview"> > </Button>
            </div>
        </div>
        <div class="preview">
            <iframe seamless
                    allow="accelerometer; ambient-light-sensor; camera; display-capture; encrypted-media; geolocation; gyroscope; microphone; midi; payment; vr" 
                    allowfullscreen="true" allowpaymentrequest="true" allowtransparency="true"
                    sandbox="allow-forms allow-modals allow-pointer-lock allow-popups allow-same-origin allow-scripts allow-top-navigation-by-user-activation allow-downloads allow-presentation"
                    :srcdoc="this.preview"></iframe>
        </div>
    </div>
</template>

<style scoped>
.main {
    position: absolute;
    top: 0px;
    left: 0px;
    height: 100%;
    width: 100%;
    padding-top: 64px;
    display: flex;
    background-color: rgb(41, 41, 41);
}

.sidebar {
    width: 350px;
    font-size: 20px;
    background-color: rgb(55, 55, 55);
    border-right: 1px solid rgb(88 88 88);
}

.editor {
    width: 50%;
    font-size: 20px;
    background-color: rgb(25, 25, 25);
    border-right: 1px solid rgb(88 88 88);
    overflow-x: auto;
}

.preview {
    width: 50%;
    font-size: 20px;
    background: white;
    overflow-y: auto;
}
.root-wrapper {
    height: 0px;
    width: 0px;
    overflow: visible;
}
.root-btn {
    position: relative;
    left: -25px;
    top: 400px;
    height: 50px;
    width: 50px;
    border-radius: 100%;
    border: 1px solid rgb(88 88 88);
    background-color: rgb(119, 119, 119);
    overflow: hidden;
}

iframe {
    width: 100%;
    min-height: 100%;
}

</style>