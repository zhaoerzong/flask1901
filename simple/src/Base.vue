<template>
  <div id="app">
    <div class="app-head">
      <div class="app-head-inner">
        <img src="./assets/logo.png" alt=""><span class="app-title">海马生鲜商场</span>
        <div class="head-nav">
          <ul>
            <li>登录</li>
            <li class="nav-pile">|</li>
            <li>注册</li>
            <li class="nav-pile">|</li>
            <li>关于</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="app-content">
      <keep-alive>
      <router-view></router-view>
      </keep-alive>
    </div>
    <div class="app-foot">
      <p>&copy; 1901C - 2020</p>
    </div>
    
  </div>
</template>

<script>


export default {
  name: 'app',
  data () {
    return {
    };
  },
  components:{

  }
}
</script>

<style>
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed, 
figure, figcaption, footer, header, hgroup, 
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
	margin: 0;
	padding: 0;
	border: 0;
	font-size: 100%;
	font: inherit;
	vertical-align: baseline;
  text-decoration: none;
}
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure, 
footer, header, hgroup, menu, nav, section {
	display: block;
}
body {
	line-height: 1;
}
ol, ul {
	list-style: none;
}
blockquote, q {
	quotes: none;
}
blockquote:before, blockquote:after,
q:before, q:after {
	content: '';
	content: none;
}
table {
	border-collapse: collapse;
	border-spacing: 0;
}


/* Base.vue 样式 */
body{
  background: #f0f3f5;
  font-size: 14px;
  color:#444;
}
.app-head{
  width:100%;
  height: 90px;
  line-height: 90px;
  color:#b2b2b2;
  background: #363636;
}
.app-head-inner{
  width:1200px;
  margin:0 auto;
}
.app-head-inner img{
  width: 50px;
  margin-top:20px;
  float:left;
}
.app-title{
  font-size: 48px;
}
.head-nav{
  float:right;
}
.head-nav li{
  float:left;
  cursor: pointer;
}
.nav-pile{
  padding:0 10px;
}
.app-foot{
  text-align: center;
  height: 80px;
  line-height: 80px;
  width: 100%;
  background: #e3e4e8;
  margin-top:30px
}
.app-content{
  width:1200px;
  margin:0 auto;
}
</style>
