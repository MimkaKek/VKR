<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
    name: 'Header',
    data() {
        return {
            tLogoName: 'VKR',
            tLogin: "Войти",
            tLogout: "Выйти",
            tSettings: "Настройки"
        };
    },
    methods: {},
    computed: {
        /* ...mapGetters(["listOpt"]),
        selected: {
            get() { 
                return this.$store.state.opt;
            },
            set(value) { 
                this.$store.commit('changeState', { opt: value } );
            }
        } */
    }
};

</script>

<template>
    
    <header class="header-main mColor">
        <ul class="panel left">
            <li class="panel-item logo">
                <a class="panel-logo" href="#">{{ tLogoName }}</a>
            </li>
            <li class="panel-divider"></li>
        </ul>
        <ul class="panel right">
            <li class="panel-divider"></li>
            <li class="panel-item last">
                <a class="panel-btn" href="#">
                    {{ tLogout }}
                </a>
            </li>
        </ul>
    </header>
    
</template>

<style>
    .mColor {
        --bs-bg-opacity: 1;
        background-color: rgb(51, 51, 51);
    }

    .settingsMenu {
        display: none;
        position: absolute;
        top: 100%;
        background-color: rgb(51, 51, 51);
    }
    
    .settingsMenu.visible {
        display: inherit;
    }

    nav ul div {
        min-width:170px;
        float:none;
        display:list-item;
        position: relative;
    }

    .header-main {
        display: flex;
        min-height: 7.2%;
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

    .logo {
        margin-right: 0.625%;
    }

    li.panel-item {
        display: inline-block;
        height: 100%;
        padding: 1px;
    }

    li.last {
        margin-right: 0.625%;
    }

    a {
        color: rgb(226, 226, 226);
        text-decoration: none;
        outline: none;
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

    option {
        color: rgb(226, 226, 226);
        background-color: rgb(51, 51, 51);
    }

    option:hover {
        background: rgb(46, 46, 46);
    }

    button.panel-btn {
        color: rgb(226, 226, 226);
        background-color: rgb(51, 51, 51);
        font-size: 25px;
    }

    li:last-child a {
        margin-right: 0;
    }

    a:link, a:visited, a:focus, button:focus {
        background: rgb(51, 51, 51);
    }

    a:hover, button:hover {
        background: rgb(46, 46, 46);
    }

    a:active, button:active {
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

    select {
        appearance: none;
        background-color: transparent;
        border: none;
        padding: 0 1em 0 0;
        margin: 0;
        width: 100%;
        font-family: inherit;
        font-size: inherit;
        cursor: inherit;
        line-height: inherit;
    }
</style>