import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const types = {
  SET_AUTHENTICATION: "SET_AUTHENTICATION",
  SET_USER : "SET_USER"
}

const state = {
    isAuthenticated : false,
    user : {}
}

const getters = {
    isAuthenticated:state => state.isAuthenticated,
    user: state=>state.use
}

const mutations = {
  [types.SET_AUTHENTICATION](state, isAuthenticated){
    if(isAuthenticated) {
      state.isAuthenticated = isAuthenticated
    }else{
      state.isAuthenticated = false;
    }
  },

  [types.SET_USER](state, user){
    if(user) state.user = user;
    else state.user={}
  }
}


const actions = {
  setAuthenticated: ({ commit }, isAuthenticated) => {
    commit(types.SET_AUTHENTICATION, isAuthenticated)
  },
  setUser: ({ commit }, user) => {
    commit(types.SET_USER, user)
  },
  // 清除token，用户信息(退出登陆的时候调用)
  clearCurrentState: ({ commit }) => {
    commit(types.SET_AUTHENTICATION, false)
    commit(types.SET_USER, null)
  }
}

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})
