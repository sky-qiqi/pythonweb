<template>
    <Page v-if="detail">
        <div class="info">
            <img v-src="detail.image_link" />
            <el-descriptions :column="2">
                <el-descriptions-item label="电影名:">{{ detail.name }}</el-descriptions-item>
                <el-descriptions-item label="上映日期:">{{ detail.years }}</el-descriptions-item>
                <el-descriptions-item label="导演:">{{ detail.director }}</el-descriptions-item>
                <el-descriptions-item label="主演:">{{ wrapText(detail.leader, 20) }}</el-descriptions-item>
                <el-descriptions-item label="豆瓣评分:">{{ detail.d_rate }}</el-descriptions-item>
                <el-descriptions-item label="收藏人数:">{{ detail.collect_count }}</el-descriptions-item>
                <el-descriptions-item label="标签:">
                    <el-tag
                        style="margin-right:5px;cursor:pointer"
                        v-for="t in detail.all_tags"
                        :key="t.id"
                        type="info"
                        effect="plain"
                        @click="toRoute(t.id)"
                    >{{ t.name }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item>
                    <el-link
                        :href="`https://v.qq.com/x/search/?q=${detail.name}&stag=0&smartbox_ab=`"
                        target="_blank"
                        type="success"
                        style="font-size:25px"
                        :underline="'hover'"
                    >前往观看</el-link>
                </el-descriptions-item>
                <el-descriptions-item label="添加评分">
                    <template v-if="detail.user_rate == null">
                        <el-select size="mini" v-model="score">
                            <el-option v-for="i in 5" :label="i" :key="i" :value="i"></el-option>
                        </el-select>
                        <el-button
                            type="primary"
                            size="mini"
                            style="margin-left:10px;"
                            @click="addScore"
                        >提交</el-button>
                    </template>
                    <span v-else>您已进行打分: {{ detail.user_rate.mark }}</span>
                </el-descriptions-item>
                <el-descriptions-item>
                    <el-button
                        size="large"
                        type="primary"
                        @click="collect"
                        v-if="detail.is_collect == null"
                    >点击收藏</el-button>
                    <el-button size="large" type="warning" @click="decollect" v-else>取消收藏</el-button>
                </el-descriptions-item>
            </el-descriptions>
        </div>
        <div class="desc">{{ detail.intro }}</div>
        <el-card class="item-recommand" shadow="always">
            <template #header>
                <div class="card-header">
                    <span>基于物品推荐电影</span>
                    <el-button
                        class="button"
                        type="primary"
                        size="mini"
                        @click="get_item_recommend"
                    >换一批</el-button>
                </div>
            </template>
            <div
                v-for="m in item_recommend"
                :key="m.id"
                class="movie-card-simple"
                @click="toDetail(m.id)"
                style="cursor:pointer;"
            >
                <img class="cover" v-src="m.image_link" />
                <div class="desc2">
                    <el-button
                        type="text"
                        style="margin-bottom:10px;display:block;text-align:left"
                    >{{ m.name }}</el-button>
                    <p>{{ m.years }}</p>
                </div>
            </div>
        </el-card>
        <div class="comment-part">
            <div style="display:flex;">
                <el-input placeholder="快来说点什么吧~" style="flex:1" v-model="comment"></el-input>
                <el-button
                    :disabled="comment.length === 0"
                    type="success"
                    size="large"
                    style="margin-left:10px;"
                    @click="makeComment"
                >提交评论</el-button>
            </div>
            <el-tabs type="card" style="margin-top:10px;">
                <el-tab-pane label="评论">
                    <template v-if="detail.comments.length != 0">
                        <div v-for="c in detail.comments" class="comment-card" :key="c.id">
                            <el-avatar shape="square" :size="50">{{ c.userName }}</el-avatar>
                            <div class="wrap">
                                <p>{{ c.content }}</p>
                                <p>{{ c.userName }} 发表于{{ formatDateTime(new Date(c.create_time)) }}</p>
                            </div>
                        </div>
                    </template>
                    <h1
                        v-else
                        style="font-weight:bold;color:#888,font-size:25px;text-align:center;"
                    >暂无评论</h1>
                </el-tab-pane>
            </el-tabs>
        </div>
    </Page>
</template>

<script>
import { formatDateTime } from "/@/utils/tools"
import request from "/@/utils/request"
import Page from "/@/components/Page/index.vue"
export default {
    props: {
        id: Number,
    },
    components: { Page },
    data() {
        return {
            item_recommend: [],
            detail: null,
            score: 1,
            comment: ''
        }
    },
    created() {
        this.get_movie()
        this.get_item_recommend()
    },
    methods: {
        formatDateTime,
        async makeComment() {
            await request.post(`comment/${this.detail.id}/`, { comment: this.comment })
            this.comment = ''
            this.$message.success('评论成功')
            this.get_movie()
        },
        async collect() {
            await request.get(`collect/${this.detail.id}/`)
            this.$message.success('收藏成功')
            this.get_movie()
        },
        async decollect() {
            await request.get(`decollect/${this.detail.id}/`)
            this.$message.success('取消收藏成功')
            this.get_movie()
        },
        async addScore() {
            await request.post(`score/${this.detail.id}/`, { score: this.score })
            this.$message.success('评分成功')
            this.get_movie()
        },
        async get_item_recommend() {
            let { data: { Data } } = await request.get('item_recommend/')
            this.item_recommend = Data
        },
        async get_movie() {
            let { data: { Data } } = await request.get(`movie/${this.id}`)
            this.detail = Data
        },
        wrapText(text, limit = 50) {
            if (text.length > limit) {
                return text.substring(0, limit) + '...'
            } else {
                return text
            }
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
.comment-card {
    display: flex;
    margin-bottom: 15px;
    border: 2px solid #ffb6c1; /* Light pink border */
    border-radius: 10px; /* Rounded corners */
    padding: 15px;
    background-color: #fff0f5; /* Lavender blush background */
    .wrap {
        margin-left: 20px;
        flex: 1;
        p:nth-child(1) {
            font-weight: bold;
            margin-bottom: 10px;
            color: #ff69b4; /* Hot pink color */
        }
        p:nth-child(2) {
            color: #ff1493; /* Deep pink color */
            font-size: 13px;
        }
    }
}
.comment-part {
    margin-top: 25px;
}
.item-recommand {
    ::v-deep(.el-card__body) {
        display: flex;
        flex-wrap: wrap; /* Allow wrapping */
        justify-content: center; /* Center items */
    }
    border: 2px dashed #ff69b4; /* Hot pink dashed border */
    border-radius: 15px; /* More rounded corners */
    padding: 10px;
}
.card-header {
    display: flex;
    justify-content: space-between; /* Space between title and button */
    align-items: center;
    span {
        font-size: 25px; /* Slightly smaller font */
        font-weight: bold;
        color: #ff69b4; /* Hot pink color */
    }
}
.info {
    display: flex;
    align-items: flex-start; /* Align items to the top */
    flex-wrap: wrap; /* Allow wrapping */
    ::v-deep(.el-descriptions) {
        flex: 1;
        margin-left: 20px; /* Add some left margin */
        .el-descriptions__body {
            background-color: transparent !important;
            .el-descriptions__cell {
                font-size: 16px; /* Slightly smaller font */
                padding-bottom: 5px; /* Reduce bottom padding */
                .el-descriptions__label {
                    color: #ff1493; /* Deep pink color */
                    font-weight: bold;
                }
                .el-descriptions__content {
                    color: #ff69b4; /* Hot pink color for content */
                }
            }
        }
    }
    img {
        width: 180px; /* Slightly smaller image */
        margin-right: 15px;
        border-radius: 8px; /* Rounded image corners */
        border: 2px solid #ffb6c1; /* Light pink border */
    }
}
.desc {
    margin-top: 25px;
    margin-bottom: 25px;
    padding: 25px;
    box-shadow: 2px 2px 8px #ffb6c1; /* Light pink shadow */
    border-radius: 10px; /* Rounded corners */
    background-color: #fff0f5; /* Lavender blush background */
    color: #ff1493; /* Deep pink color */
}
.movie-card-simple {
    flex: 0 0 calc(33.333% - 20px); /* Adjust flex basis for 3 items per row with margin */
    max-width: calc(33.333% - 20px); /* Ensure max width */
    cursor: pointer;
    display: flex;
    flex-direction: column;
    margin: 10px;
    border: 1px solid #ffb6c1; /* Light pink border */
    border-radius: 8px; /* Rounded corners */
    overflow: hidden; /* Hide overflow for rounded corners */
    img {
        width: 100%;
        height: auto; /* Maintain aspect ratio */
    }
    .desc2 {
        flex: 1;
        padding: 8px;
        p {
            font-size: 11px; /* Slightly smaller font */
            color: #ff1493; /* Deep pink color */
        }
        p + p {
            margin-top: 8px;
        }
    }
}

/* Additional styles for cute theme */
.el-tag {
    background-color: #ffb6c1 !important; /* Light pink tag background */
    color: #ff1493 !important; /* Deep pink tag text */
    border-color: #ff69b4 !important; /* Hot pink tag border */
    border-radius: 12px; /* More rounded tags */
}

.el-link.el-link--success {
    color: #ff1493 !important; /* Deep pink link color */
    font-size: 22px !important; /* Slightly smaller font */
    text-decoration: underline wavy #ff69b4; /* Wavy underline */
}

.el-button--primary {
    background-color: #ff69b4 !important; /* Hot pink button background */
    border-color: #ff1493 !important; /* Deep pink button border */
    color: white !important; /* White text */
    border-radius: 20px; /* Pill-shaped buttons */
}

.el-button--warning {
    background-color: #ffb6c1 !important; /* Light pink button background */
    border-color: #ff69b4 !important; /* Hot pink button border */
    color: #ff1493 !important; /* Deep pink text */
    border-radius: 20px; /* Pill-shaped buttons */
}

.el-select__inner {
    border-color: #ffb6c1 !important; /* Light pink select border */
    border-radius: 8px; /* Rounded select */
}

.el-tabs__item.is-active {
    color: #ff1493 !important; /* Deep pink active tab text */
}

.el-tabs__item {
    color: #ff69b4 !important; /* Hot pink tab text */
}

.el-tabs__nav-wrap::after {
    background-color: #ffb6c1 !important; /* Light pink tab underline */
}

h1 {
    color: #ff1493 !important; /* Deep pink color for h1 */
}

</style>