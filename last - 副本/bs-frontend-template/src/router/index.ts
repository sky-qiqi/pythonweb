import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import { IMenubarList } from '/@/type/store/layout'
import { components } from '/@/router/asyncRouter'
import { setFlagsFromString } from 'v8'

const Components: IObject<() => Promise<typeof import('*.vue')>> = Object.assign({}, components, {
    Layout: (() => import('/@/layout/index.vue')) as unknown as () => Promise<typeof import('*.vue')>,
    Redirect: (() => import('/@/layout/redirect.vue')) as unknown as () => Promise<typeof import('*.vue')>,
    LayoutBlank: (() => import('/@/layout/blank.vue')) as unknown as () => Promise<typeof import('*.vue')>
})

interface Arg {
    title: string
    name: string
    home?: boolean
    hidden?: boolean
}

function toMenu(arg: Arg): IMenubarList {
    return {
        name: arg.name,
        path: `/${arg.home ? '' : arg.name}`,
        component: Components['Layout'],
        redirect: `/${arg.name}/List`,
        meta: { title: arg.title, icon: 'el-icon-eleme', hidden: Boolean(arg.hidden) },
        children: [
            {
                name: `${arg.name}List`,
                path: `/${arg.name}/List`,
                component: Components[arg.name],
                meta: { title: arg.title, icon: '' }
            }
        ]
    }
}

// 静态路由页面
export const allowRouter: Array<IMenubarList> = [
    toMenu({ name: "Index", title: "首页", home: true }),
    toMenu({ name: "Tag", title: "标签", home: false }),
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
        redirect: '/Collect',
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
        redirect: '/Collect',
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