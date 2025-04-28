<template>
    <Page>
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>我的评论</span>
                </div>
            </template>
            <el-table :data="records" style="width: 100%">
                <el-table-column prop="movie_name" label="电影名">
                    <template #default="{ row }">
                        <el-button type="text" @click="toDetail(row.movie_id)">{{ row.movie_name }}</el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="content" label="评论内容"></el-table-column>
                <el-table-column prop="create_time" label="评论时间">
                    <template #default="{ row }">{{ formatDateTime(new Date(row.create_time)) }}</template>
                </el-table-column>
                <el-table-column label="操作">
                    <template #default="{ row }">
                        <el-button type="danger" @click="deleteComment(row.id)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
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
            records: [],
        }
    },
    created() {
        this.get_records()
    },
    methods: {
        formatDateTime,
        async deleteComment(cid) {
            await request.get(`delete_comment/${cid}`)
            this.$message.success('删除成功')
            this.get_records()
        },
        async get_records() {
            let { data: { Data } } = await request.get('my_comments/')
            this.records = Data
        },
        toRoute(tag) {
            this.$router.replace({ name: "Index", query: { tag } })
        },
        toDetail(id) {
            this.$router.push({ name: 'Detail', params: { id } })
        },
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