import { createApp } from 'vue'
import { ElButton, ElInput, ElSkeleton, ElTag, ElUpload } from 'element-plus'
import 'element-plus/dist/index.css'
import './style.css'
import App from './App.vue'

createApp(App)
  .use(ElButton)
  .use(ElInput)
  .use(ElSkeleton)
  .use(ElTag)
  .use(ElUpload)
  .mount('#app')
