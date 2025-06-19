import { UserConfigExport, ConfigEnv, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { viteMockServe } from 'vite-plugin-mock'
// Change the import to use the named export
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'

const setAlias = (alias: [string, string][]) => alias.map(v => { return { find: v[0], replacement: path.resolve(__dirname, v[1]) } })
const proxy = (list: [string, string][]) => {
    const obj: IObject<any> = {}
    list.forEach((v) => {
        obj[v[0]] = {
            target: v[1],
            changeOrigin: true,
            rewrite: (path: any) => path.replace(new RegExp(`^${v[0]}`), ''),
            ...(/^https:\/\//.test(v[1]) ? { secure: false } : {})
        }
    })
    return obj
}

export default async ({ command, mode }: ConfigEnv): Promise<UserConfigExport> => {
    const root = process.cwd()
    const env = loadEnv(mode, root) as unknown as ImportMetaEnv
    const prodMock = false
    return {
        resolve: {
            alias: setAlias([
                ['/@', 'src'],
                ['/mock', 'mock'],
                ['/server', 'server']
            ])
        },
        server: {
            proxy: env.VITE_PROXY ? proxy(JSON.parse(env.VITE_PROXY)) : {},
            port: env.VITE_PORT
        },
        build: {
            // sourcemap: true,
            outDir: "../dist", // 直接放到上一级目录上
            manifest: false,
            rollupOptions: {
                output: {
                    manualChunks: {
                        'element-plus': ['element-plus'],
                        echarts: ['echarts'],
                        pinyin: ['pinyin']
                    }
                }
            },
            chunkSizeWarningLimit: 600
        },
        plugins: [
            vue(),
            viteMockServe({
                mockPath: 'mock',
                localEnabled: false,
                prodEnabled: false,
                // localEnabled: command === 'serve',
                // prodEnabled: command !== 'serve' && prodMock,
                //  这样可以控制关闭mock的时候不让mock打包到最终代码内
                injectCode: `
                import { setupProdMockServer } from '/mock/mockProdServer';
                setupProdMockServer();
                `
            }),
            // Use the correctly imported function
            createSvgIconsPlugin({
                // Specify the icon folder to be cached
                iconDirs: [path.resolve(process.cwd(), 'src/icons')],
                // Specify symbolId format
                symbolId: 'icon-[dir]-[name]'
            })
        ],
        css: {
            postcss: {
                plugins: [
                    // Use import syntax for ES Modules
                    (await import('autoprefixer')).default,
                    (await import('tailwindcss')).default,
                    (await import('postcss-nested')).default,
                    (await import('postcss-simple-vars')).default,
                    (await import('postcss-import')).default
                ]
            }
        }
    }
}