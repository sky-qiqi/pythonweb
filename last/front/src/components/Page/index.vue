<template>
    <div class="x-container">
        <div class="inner">
            <div class="content">
                <slot />
            </div>
            <div class="right">
                <slot name="right">
                    <el-card class="recent" shadow="always">
                        <template #header>
                            <div class="card-header">
                                <span>最近更新</span>
                            </div>
                        </template>
                        <el-button
                            type="text"
                            v-for="m in recent_movies"
                            :key="m.id"
                            style="margin-bottom:10px;display:block;margin-left:0;text-align:left"
                            @click="toDetail(m.id)"
                        >{{ m.name }}</el-button>
                    </el-card>
                    <el-card class="user-recommand" shadow="always">
                        <template #header>
                            <div class="card-header">
                                <span>基于用户推荐电影</span>
                                <el-button
                                    class="button"
                                    type="primary"
                                    size="mini"
                                    @click="get_user_recommend"
                                >换一批</el-button>
                            </div>
                        </template>
                        <div
                            v-for="m in user_recommend"
                            :key="m.id"
                            class="movie-card-simple"
                            @click="toDetail(m.id)"
                            style="cursor:pointer;"
                        >
                            <img class="cover" v-src="m.image_link" />
                            <div class="desc">
                                <el-button
                                    type="text"
                                    style="margin-bottom:10px;display:block;text-align:left"
                                >{{ m.name }}</el-button>
                                <p>{{ m.years }}</p>
                                <p>评分: {{ m.d_rate }}</p>
                            </div>
                        </div>
                    </el-card>
                </slot>
            </div>
        </div>
    </div>
</template>

<script>
import request from "/@/utils/request"
export default {
    data() {
        return {
            recent_movies: [],
            user_recommend: []
        }
    },
    created() {
        this.get_recent_movies()
        this.get_user_recommend()
    },
    methods: {
        toDetail(id) {
            this.$router.push({ name: 'Detail', params: { id } })
        },
        async get_recent_movies() {
            let { data: { Data } } = await request.get('recent_movies/')
            this.recent_movies = Data
        },
        async get_user_recommend() {
            let { data: { Data } } = await request.get('user_recommend/')
            this.user_recommend = Data
        }
    }
}
</script>

<style lang="postcss" scoped>
.movie-card-simple {
    cursor: pointer;
    display: flex;
    margin: 10px 0; /* Adjust margin */
    padding: 10px; /* Add padding */
    border-radius: 10px; /* Rounded corners */
    background-color: #fff; /* White background */
    transition: transform 0.2s ease-in-out; /* Add hover effect */
    &:hover {
        transform: translateY(-5px); /* Lift on hover */
    }
    img.cover {
        max-width: 100px; /* Smaller image */
        border-radius: 8px; /* Rounded corners for image */
    }
    .desc {
        flex: 1;
        padding: 0 10px; /* Adjust padding */
        p {
            font-size: 13px; /* Slightly larger font */
            color: #555; /* Darker text color */
        }
        p + p {
            margin-top: 5px; /* Smaller margin */
        }
    }
}
.column {
    display: flex;
    flex-direction: column;
}
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    span {
        font-size: 18px; /* Slightly smaller font */
        font-weight: bold;
        color: #ff69b4; /* Hot pink color for headers */
    }
}
.x-container {
    padding: 40px 20px;
    display: flex;
    justify-content: center;
    background-color: #ffe4e1; /* Light pink background */
    .inner {
        width: 90%; /* Slightly wider content area */
        display: flex;
        gap: 20px; /* Add gap between content and right sidebar */
        .content {
            flex: 1;
            background-color: #fff0f5; /* Lighter pink for content background */
            padding: 20px;
            border-radius: 15px; /* Rounded corners */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        }
        .right {
            width: 30%; /* Adjust right sidebar width */
            .el-card {
                margin-bottom: 20px;
                border-radius: 15px; /* Rounded corners for cards */
                background-color: #fffafa; /* White background for cards */
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* Subtle shadow for cards */
            }
        }
    }
}
</style>