<template>
    <Page>
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>个人中心</span>
                </div>
            </template>
            <div class="tags">
                <el-row style="width:100%">
                    <el-col :span="8">
                        <h1>用户名：{{ user.username }}</h1>
                    </el-col>
                    <!-- <el-col :span="8">
                        <h1>邮箱: {{ user.email }}</h1>
                    </el-col> -->
                    <el-col :span="8">
                        <h1>注册日期: {{ formatDateTime(new Date(user.created_time)) }}</h1>
                    </el-col>
                </el-row>

                <el-row style="width:100%;margin-top:30px;">
                    <el-col :span="8">
                        <el-button type="warning" size="large" @click="toRoute('Collect')">我的收藏</el-button>
                    </el-col>
                    <el-col :span="8">
                        <el-button type="primary" size="large" @click="toRoute('Comment')">我的评论</el-button>
                    </el-col>
                    <el-col :span="8">
                        <el-button type="success" size="large" @click="toRoute('Rate')">我的评分</el-button>
                    </el-col>
                </el-row>
            </div>
        </el-card>
    </Page>
</template>

<script>
import { formatDateTime } from "/@/utils/tools"
import request from "/@/utils/request"
import Page from "/@/components/Page/index.vue"
export default {
    components: { Page },
    data() {
        return {
            user: {},
        }
    },
    created() {
        this.get_self()
    },
    methods: {
        formatDateTime,
        async get_self() {
            let { data: { Data } } = await request.get('personal/')
            this.user = Data
        },
        toRoute(name) {
            this.$router.push({ name })
        }
    }
}
</script>
<style lang="postcss" scoped>
h1 {
    font-size: 20px;
}
.card-header {
    display: flex;
    justify-content: center;
    align-items: center;
    span {
        font-size: 30px;
        font-weight: bold;
    }
}
.tags {
    width: 100%;
    display: inline-flex;
    flex-wrap: wrap;
}
</style>