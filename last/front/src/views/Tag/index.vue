<template>
    <Page>
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>电影分类</span>
                </div>
            </template>
            <div class="tags">
                <span v-for="t in tags" :key="t.id">
                    <el-button
                        type="text"
                        style="font-size:20px;"
                        @click="toRoute(t.id)"
                    >{{ t.name }}</el-button>
                </span>
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
            tags: [],
        }
    },
    created() {
        this.get_tags()
    },
    methods: {
        async get_tags() {
            let { data: { Data } } = await request.get('all_tags/')
            this.tags = Data
        },
        toRoute(tag) {
            this.$router.replace({ name: "Index", query: { tag } })
        }
    }
}
</script>
<style lang="postcss" scoped>
.card-header {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #ffb6c1; /* 粉色背景 */
    padding: 15px;
    border-radius: 10px 10px 0 0; /* 圆角 */
    span {
        font-size: 30px;
        font-weight: bold;
        color: #fff; /* 白色字体 */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); /* 阴影 */
    }
}
.tags {
    width: 100%;
    display: flex; /* 使用flexbox */
    flex-wrap: wrap;
    justify-content: center; /* 居中对齐 */
    padding: 20px;
    background-color: #ffe4e1; /* 浅粉色背景 */
    border-radius: 0 0 10px 10px; /* 圆角 */
    span {
        display: flex;
        justify-content: center;
        width: 20%; /* 调整宽度 */
        margin: 10px; /* 增加间距 */
    }
}

.el-card {
    border-radius: 10px; /* 整体圆角 */
    overflow: hidden; /* 隐藏溢出部分 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 柔和阴影 */
}

.el-button--text {
    color: #ff69b4; /* 可爱的粉色字体 */
    font-size: 20px; /* 字体大小 */
    font-weight: bold;
    transition: color 0.3s ease; /* 过渡效果 */

    &:hover {
        color: #ff1493; /* 悬停时的深粉色 */
        text-decoration: underline; /* 悬停时加下划线 */
    }
}
</style>