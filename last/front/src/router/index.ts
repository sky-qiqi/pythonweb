import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import { IMenubarList } from '/@/type/store/layout'
// 从 asyncRouter 中导入 components 映射表
import { components } from '/@/router/asyncRouter'
// import { setFlagsFromString } from 'v8' // 这行导入似乎不是必需的，如果报错可以删除

// 这里直接使用从 asyncRouter 导入的 components 映射表，并合并其他固定布局组件
const Components: IObject<() => Promise<typeof import('*.vue')>> = Object.assign({}, components, {
    Layout: (() => import('/@/layout/index.vue')) as unknown as () => Promise<typeof import('*.vue')>,
    Redirect: (() => import('/@/layout/redirect.vue')) as unknown as () => Promise<typeof import('*.vue')>,
    LayoutBlank: (() => import('/@/layout/blank.vue')) as unknown as () => Promise<typeof import('*.vue')>
    // asyncRouter.ts 已经动态导入了 views 目录下的组件，包括 AI/ai.vue
    // asyncRouter.ts 应该会将 src/views/AI/ai.vue 映射到键 'ai' (小写)
})

interface Arg {
    title: string // 菜单显示的标题
    name: string // 对应 components 映射表中的键名，也用于生成 path 和 name
    home?: boolean // 是否是首页
    hidden?: boolean // 是否隐藏菜单项
}

function toMenu(arg: Arg): IMenubarList {
    return {
        name: arg.name, // 路由名称
        path: `/${arg.home ? '' : arg.name}`, // 路由路径，首页特殊处理
        component: Components['Layout'], // 外层使用 Layout 布局
        redirect: `/${arg.name}/List`, // 重定向到子路由
        meta: { title: arg.title, icon: 'el-icon-eleme', hidden: Boolean(arg.hidden) }, // meta 信息
        children: [
            {
                // 子路由的 name 和 path 应该与外层 name 相关联
                name: `${arg.name}List`, // 子路由名称 (例如 aiList)
                path: `/${arg.name}/List`, // 子路由路径 (例如 /ai/List)
                // 这里使用 Components[arg.name] 来引用对应的组件
                // 根据 asyncRouter.ts 的逻辑，这个键应该是 'ai'
                component: Components[arg.name], // <--- 确保 Components['ai'] 存在且指向你的 ai.vue 组件
                meta: { title: arg.title, icon: '' } // 子路由的 meta 信息
            }
        ]
    }
}

// 静态路由页面
export const allowRouter: Array<IMenubarList> = [
    toMenu({ name: "Index", title: "首页", home: true }),
    toMenu({ name: "Tag", title: "标签", home: false }),

    // **添加 AI 对话的路由**
    // 根据 asyncRouter.ts 的命名逻辑，views/AI/ai.vue 很可能被映射为键 'ai' (小写)
    // 因此 name 参数使用 'ai'
    toMenu({ name: "ai", title: "AI 对话", home: false }), // <--- 添加这一行

    {
        name: 'ChooseTag_',
        path: '/ChooseTag_',
        component: Components['Layout'],
        meta: { title: '选择标签', icon: '', hidden: true },
        children: [
            {
                name: 'ChooseTag',
                path: '/ChooseTag',
                meta: {
                    title: '选择标签',
                    icon: ''
                },
                component: Components.ChooseTag
            }
        ]
    },
    {
        name: 'Detail_',
        path: '/Detail',
        component: Components['Layout'],
        meta: { title: '电影详情', icon: '', hidden: true },
        children: [
            {
                name: 'Detail',
                path: '/Detail/:id',
                meta: {
                    title: '电影详情',
                    icon: ''
                },
                props: true,
                component: Components.Detail
            }
        ]
    },
    {
        name: 'Personal_',
        path: '/Personal_',
        redirect: '/Personal',
        component: Components['Layout'],
        meta: { title: '个人中心', icon: '', hidden: true },
        children: [
            {
                name: 'Personal',
                path: '/Personal',
                meta: {
                    title: '个人中心',
                    icon: ''
                },
                component: Components.Personal
            }
        ]
    },
    {
        name: 'Collect_',
        path: '/Collect_',
        redirect: '/Collect',
        component: Components['Layout'],
        meta: { title: '我的收藏', icon: '', hidden: true },
        children: [
            {
                name: 'Collect',
                path: '/Collect',
                meta: {
                    title: '我的收藏',
                    icon: ''
                },
                component: Components.Collect
            }
        ]
    },
    {
        name: 'Comment_',
        path: '/Comment_',
        redirect: '/Collect', // TODO: 重定向路径可能是 /Comment ?
        component: Components['Layout'],
        meta: { title: '我的评论', icon: '', hidden: true },
        children: [
            {
                name: 'Comment',
                path: '/Comment',
                meta: {
                    title: '我的评论',
                    icon: ''
                },
                component: Components.Comment
            }
        ]
    },
    {
        name: 'Rate_',
        path: '/Rate_',
        redirect: '/Collect', // TODO: 重定向路径可能是 /Rate ?
        component: Components['Layout'],
        meta: { title: '我的评分', icon: '', hidden: true },
        children: [
            {
                name: 'Rate',
                path: '/Rate',
                meta: {
                    title: '我的评分',
                    icon: ''
                },
                component: Components.Rate
            }
        ]
    },
    {
        name: 'ErrorPage',
        path: '/ErrorPage',
        meta: { title: '错误页面', icon: 'el-icon-eleme', hidden: true },
        component: Components.Layout,
        redirect: '/ErrorPage/404',
        children: [
            {
                name: '401',
                path: '/ErrorPage/401',
                component: Components['401'],
                meta: { title: '401', icon: 'el-icon-s-tools' }
            },
            {
                name: '404',
                path: '/ErrorPage/404',
                component: Components['404'],
                meta: { title: '404', icon: 'el-icon-s-tools' }
            }
        ]
    },
    {
        name: 'RedirectPage',
        path: '/redirect',
        component: Components['Layout'],
        meta: { title: '重定向页面', icon: 'el-icon-eleme', hidden: true },
        children: [
            {
                name: 'Redirect',
                path: '/redirect/:pathMatch(.*)*',
                meta: {
                    title: '重定向页面',
                    icon: ''
                },
                component: Components.Redirect
            }
        ]
    },
    {
        name: 'Login',
        path: '/Login',
        component: Components.Login,
        meta: { title: '登录', icon: 'el-icon-eleme', hidden: true }
    },
    {
        name: 'Register',
        path: '/Register',
        component: Components.Register,
        meta: { title: '注册', icon: 'el-icon-eleme', hidden: true }
    },
]

const router = createRouter({
    history: createWebHashHistory(), // createWebHistory
    routes: allowRouter as RouteRecordRaw[]
})

export default router