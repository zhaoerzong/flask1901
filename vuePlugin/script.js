import Vue from 'vue/dist/vue.js'
import VueMathPlugin from './VueMathPlugin.js'
import Vuex from 'vuex'

Vue.use(VueMathPlugin)
Vue.use(Vuex)


var store = new Vuex.Store({
    state:{message:'hello!'},
    mutations:{}
})

new Vue({
    el:"#app",
    data:{
        item:20
    },
    store:store
})