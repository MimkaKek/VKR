<script>
import { RouterLink } from 'vue-router';

export default {
    props: {
      logoBack: {
        type: Boolean,
        default: false
      },
      hideMenu: {
        type: Boolean,
        default: false
      },
      shareLink: {
        type: Boolean,
        default: false
      }
    },
    components: {
        RouterLink
    },
    name: 'Header',
    data() {
        return {
            tLogoName: 'VKR',
            tLogout: "Выйти",
            tProject: "Проекты",
            tPubProject: "Публичные проекты",
            tTemplates: "Шаблоны",
            tShare: "Поделиться",
            tRole: "Роли",
            role: 3,
            logged: false
        };
    },
    methods: {
        goBack() {
            this.$router.back();
        }
    },
    computed: {

    },
    mounted() {
    }
};

</script>

<template>
    <header class="header-main mColor">
        <ul class="panel left">
            <li class="panel-item">
                <template v-if="this.logoBack">
                    <RouterLink class="panel-logo" to="#" v-on:click="this.goBack()"> ❮ </RouterLink>
                </template>
                <template v-else>
                    <RouterLink class="panel-logo" to="#">{{ tLogoName }}</RouterLink>
                </template>
                
            </li>
            <li class="panel-divider"></li>
            <template v-if="this.$store.getters['auth/status']">
                <li v-if="this.$store.getters['auth/role'] < 4 && !this.hideMenu" class="panel-item fill">
                    <RouterLink class="panel-btn" to="/projects">{{ tProject }}</RouterLink>
                </li>
                <li v-if="this.$store.getters['auth/role'] < 4 && !this.hideMenu" class="panel-item fill">
                    <RouterLink class="panel-btn" to="/public">{{ tPubProject }}</RouterLink>
                </li>
                <li v-if="this.$store.getters['auth/role'] < 4 && this.shareLink" class="panel-item fill">
                    <RouterLink class="panel-btn" :to="'/project/share/' + this.$route.params.pid">{{ tShare }}</RouterLink>
                </li>
                <li v-if="this.$store.getters['auth/role'] < 3 && !this.hideMenu || this.shareLink" class="panel-divider"></li>
                <li v-if="this.$store.getters['auth/role'] < 4 && this.shareLink" class="panel-item fill"></li>
            </template>
            
        </ul>
        <ul class="panel right">
            <template v-if="this.$store.getters['auth/status']">
                <li v-if="this.$store.getters['auth/role'] < 3 && !this.hideMenu" class="panel-item fill">
                    <RouterLink class="panel-btn" to="/templates">{{ tTemplates }}</RouterLink>
                </li>
                <li v-if="this.$store.getters['auth/role'] < 2 && !this.hideMenu" class="panel-item fill">
                    <RouterLink class="panel-btn" to="/roles">{{ tRole }}</RouterLink>
                </li>
                <li class="panel-divider"></li>
                <li class="panel-item last">
                    <a class="panel-btn" href="/login">
                        {{ tLogout }}
                    </a>
                </li>
            </template>
            
        </ul>
    </header>
    
</template>

<style>
    .mColor {
        --bs-bg-opacity: 1;
        background-color: rgb(51, 51, 51);
    }

    .header-main {
        display: flex;
        font-size: 25px;
        position: sticky;
        top: 0;
        z-index: 1;
        border-bottom: 1px;
        border-style: solid;
        border-color: rgb(74, 74, 74);
    }

    .panel-divider {
        background-color: rgb(74, 74, 74);
        width: 1px;
        margin-left: 5px;
        margin-right: 5px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    ul.panel {
        list-style-type: none;
        width: 100%;
        margin: 0;
        padding: 0;
    }

    ul.left {
        display: flex;
        justify-content: flex-start;
    }

    ul.right {
        display: flex;
        justify-content: flex-end;
    }

    li.fill {
        width: 100%;
    }

    li.panel-item {
        display: inline-block;
        height: 100%;
    }

    li.space {
        margin-left: 5px;
        margin-right: 5px;
    }

    li.last {
        margin-right: 0.625%;
    }

    a {
        color: rgb(226, 226, 226);
        text-decoration: none;
        outline: none;
        width: 100%;
    }

    .panel-btn {
        display: inline-block;
        padding: 5px;
        min-width: 4rem;
        height: inherit;
        text-align: center;
        line-height: 53px;
        -moz-transition: all 0.3s 0.01s ease;
        -o-transition: all 0.3s 0.01s ease;
        -webkit-transition: all 0.3s 0.01s ease;
    }

    .select-btn {
        display: inline-block;
        padding: 5px;
        min-width: 4rem;
        height: inherit;
        text-align: center;
        line-height: 53px;
        color: rgb(226, 226, 226);
        border-width: 0px;
        border-style: none;
    }

    .select-btn:active {
        border: 0px;
    }

    li:last-child a {
        margin-right: 0;
    }

    a:link, a:visited, a:focus {
        background: rgb(51, 51, 51);
    }

    a:hover {
        background: rgb(46, 46, 46);
    }

    a:active {
        background: rgb(40, 40, 40);;
    }

    a.panel-logo {
        display: inline-block;
        padding: 5px;
        min-width: 4rem;
        height: inherit;
        text-align: center;
        line-height: 53px;
    }

    a.panel-logo:active, 
    a.panel-logo:hover, 
    a.panel-logo:link, 
    a.panel-logo:visited, 
    a.panel-logo:focus {
        background-color: rgb(51, 51, 51);
    }

</style>