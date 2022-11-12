<template>
    <div class="container">
        <button type="button" class="btn btn-primary" v-on:click="initDatabase()">{{ init_btn }}</button>
    </div>
    <div class="container">
        <button type="button" class="btn btn-primary" v-on:click="getDatabase()">{{ get_btn }}</button>
    </div>
    <div class="container">
        Response {{ rec_data }}
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TestDB',
  data() {
    return {
      init_btn: 'Init Database',
      get_btn: "Get data from database",
      rec_data: 'wait...'
    };
  },
  methods: {
    initDatabase() {
      const path = 'http://localhost:8000/init_db';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getDatabase() {
      const path = 'http://localhost:8000/get_db';
      axios.get(path)
        .then((res) => {
          this.rec_data = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    }
  },
};
</script>