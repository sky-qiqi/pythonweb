// src/store/index.ts
import { createPinia } from 'pinia';

export const pinia = createPinia();

// 导入并重新导出你的 chat store
// 确保这个路径是正确的，指向你的 chat.ts 文件
export * from './modules/chat';

// 如果你将来有其他 Pinia 模块 (例如，user.ts, settings.ts)，你也可以在这里重新导出它们：
// export * from './modules/user';
// export * from './modules/settings';

// 如果你需要使用 pinia-plugin-persistedstate 来实现状态持久化，
// 请确保已经安装该插件 (npm install pinia-plugin-persistedstate)，
// 并在 `main.ts` 中 Pinia 初始化之后添加 pinia.use(piniaPluginPersistedstate);
// 然后在对应的 store (例如 chat.ts) 中添加 persist: true。
/*
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
pinia.use(piniaPluginPersistedstate);
*/