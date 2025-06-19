<template>
    <Page>
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>{{ title }}</span>
                    <div>
                        <el-select
                            clearable
                            filterable
                            class="button"
                            type="primary"
                            size="large"
                            @change="changeOrder"
                            v-model="form.tag"
                            placeholder="电影标签"
                        >
                            <el-option v-for="t in tags" :key="t.id" :label="t.name" :value="t.id"></el-option>
                        </el-select>

                        <el-select
                            style="margin-left:10px;"
                            class="button"
                            type="primary"
                            size="large"
                            @change="changeOrder"
                            v-model="form.order"
                        >
                            <el-option
                                v-for="label, key in orders"
                                :key="key"
                                :label="label"
                                :value="key"
                            ></el-option>
                        </el-select>
                    </div>
                </div>
            </template>
            <div class="movies">
                <el-card
                    class="movie"
                    shadow="hover"
                    v-for="m in movies"
                    :key="m.id"
                    @click="toDetail(m.id)"
                    style="cursor:pointer;"
                >
                    <img v-src="m.image_link" />
                    <el-button type="text">{{ m.name }}</el-button>
                    <span style="text-align:center;font-size:12px">{{ m.years }}</span>
                </el-card>
            </div>
            <div style="display:flex;justify-content:center;margin-top:30px;">
                <el-pagination
                    @current-change="handleCurrentChange"
                    :current-page="form.page"
                    :page-size="form.pagesize"
                    layout="prev, pager, next, jumper, total"
                    :total="form.total"
                    background
                ></el-pagination>
            </div>
        </el-card>
    </Page>
</template>

<script>
import request from "/@/utils/request"
import Page from "/@/components/Page/index.vue"
export default {
    components: { Page },
    data() {
        return {
            movies: [],
            tags: [],
            form: {
                tag: null,
                order: 'num',
                page: 1,
                pagesize: 15,
                total: 0,
            },
            orders: {
                collect: '收藏排序',
                rate: '评分排序',
                years: '时间排序',
                num: '热度排序',
            }
        }
    },
    async created() {
        await this.get_tags()
        this.form.tag = this.$route.query.tag
        if (this.form.tag) {
            this.form.tag = Number(this.form.tag)
        }
        await this.search()
    },
    computed: {
        title() {
            const t = this.tags.find((v) => {
                return v.id === this.form.tag
            }) || {}
            return [t.name, this.orders[this.form.order]].filter(v => v).join(' - ')
        }
    },
    methods: {
        toDetail(id) {
            this.$router.push({ name: 'Detail', params: { id } })
        },
        handleCurrentChange(page) {
            this.form.page = page;
            this.search()
        },
        changeOrder() {
            this.form.page = 1
            this.search()
        },
        async search() {
            let { data: { Data: { total, results } } } = await request.post('movies/', this.form)
            this.movies = results
            this.form.total = total
        },
        async get_tags() {
            let { data: { Data } } = await request.get('all_tags/')
            this.tags = Data
        }
    }
}
</script>
<style lang="postcss" scoped>
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #ffb6c1; /* 可爱的粉色背景 */
    padding: 15px;
    border-radius: 10px 10px 0 0; /* 圆角 */
    span {
        font-size: 22px; /* 字体稍大 */
        font-weight: bold;
        color: #fff; /* 白色字体 */
        text-shadow: 1px 1px 2px #ff69b4; /* 粉色阴影 */
    }
}
.movies {
    display: flex; /* 使用 flex 布局 */
    flex-wrap: wrap;
    justify-content: center; /* 居中对齐 */
    padding: 20px;
    background-color: #ffe4e1; /* 淡粉色背景 */
    ::v-deep(.el-card) {
        width: 200px; /* 固定宽度 */
        margin: 15px; /* 增加间距 */
        border-radius: 15px; /* 更大的圆角 */
        overflow: hidden; /* 隐藏溢出内容 */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 柔和阴影 */
        transition: transform 0.3s ease; /* 添加过渡效果 */
        &:hover {
            transform: translateY(-5px); /* 悬停上移 */
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* 悬停阴影 */
        }
    }
    ::v_deep(.el-card__body) {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center; /* 居中对齐 */
        padding: 10px; /* 调整内边距 */
        img {
            width: 100%; /* 图片宽度填充卡片 */
            height: 150px; /* 固定图片高度 */
            object-fit: cover; /* 保持图片比例 */
            border-radius: 10px; /* 图片圆角 */
            margin-bottom: 10px; /* 图片下方间距 */
        }
        .el-button--text {
            color: #ff69b4; /* 粉色按钮文字 */
            font-size: 16px; /* 按钮字体大小 */
            font-weight: bold;
            margin-bottom: 5px; /* 按钮下方间距 */
        }
        span {
            text-align: center;
            font-size: 14px; /* 年份字体大小 */
            color: #888; /* 灰色字体 */
        }
    }
}
.el-pagination {
    margin-top: 30px;
    ::v-deep(.el-pager li.active) {
        background-color: #ff69b4 !important; /* 分页选中背景色 */
        color: #fff; /* 分页选中字体颜色 */
    }
    ::v-deep(.el-pager li:hover) {
        color: #ff69b4; /* 分页悬停颜色 */
    }
    ::v-deep(.btn-prev, .btn-next) {
        color: #ff69b4; /* 分页按钮颜色 */
    }
}
</style>