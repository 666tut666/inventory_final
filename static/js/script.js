 import Vue from 'vue';
 window.Vue = Vue;

const { createApp } = Vue;
const { createVuetify } = Vuetify;

const vuetify = createVuetify();

const app = createApp({
  template: "#app-template",
  data: () => ({
    visible: false
  })
})
  .use(vuetify)
  .mount("#app");