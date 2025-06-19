<template>
    <div>
        <el-color-picker
            v-model='defaultTheme'
            :predefine='["#409EFF", "#1890ff", "#304156","#212121","#11a983", "#13c2c2", "#6959CD", "#f5222d" ]'
            size='mini'
            @change='changeThemeColor'
        />
    </div>
</template>
<script lang='ts'>
import { defineComponent, ref } from 'vue'
import { useLayoutStore } from '/@/store/modules/layout'
import changeThemeColor from '/@/utils/changeThemeColor'

export default defineComponent({
    name: 'LayoutTheme',
    setup() {
        const { getSetting } = useLayoutStore()
        const defaultTheme = ref(getSetting.color.primary)
        return {
            defaultTheme,
            changeThemeColor
        }
    }
})
</script>
<style lang='postcss' scoped>
.el-color-picker__trigger {
    border-color: #ffb6c1; /* 可爱的粉色边框 */
    border-radius: 8px; /* 圆角 */
    box-shadow: 0 2px 5px rgba(255, 105, 180, 0.2); /* 粉色柔和阴影 */
    transition: all 0.3s ease; /* 添加过渡效果 */
}

.el-color-picker__trigger:hover {
    border-color: #ff69b4; /* 悬停时更深的粉色 */
    box-shadow: 0 4px 8px rgba(255, 105, 180, 0.3); /* 悬停时阴影更明显 */
}

.el-color-picker__color {
    border-radius: 6px; /* 颜色块圆角 */
}

.el-color-picker__color-inner {
     border-radius: 6px; /* 颜色块内部圆角 */
}

.el-color-picker__empty {
    border-radius: 6px; /* 空颜色块圆角 */
}

.el-color-picker__icon {
    color: #ff69b4; /* 图标颜色 */
}

/* 可以根据需要进一步美化面板 */
::v-deep(.el-color-dropdown__main-wrapper) {
    border-radius: 10px; /* 面板圆角 */
    box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15); /* 面板阴影 */
}

::v-deep(.el-color-dropdown__btns) {
    border-top: 1px solid #ffb6c1; /* 按钮区域分隔线 */
}

::v-deep(.el-button--mini) {
    border-radius: 5px; /* 按钮圆角 */
    font-size: 12px; /* 按钮字体大小 */
}

::v-deep(.el-button--primary) {
    background-color: #ff69b4; /* 主要按钮背景色 */
    border-color: #ff69b4; /* 主要按钮边框色 */
}

::v-deep(.el-button--primary:hover) {
    background-color: #ff1493; /* 主要按钮悬停背景色 */
    border-color: #ff1493; /* 主要按钮悬停边框色 */
}

::v-deep(.el-button--text) {
    color: #ff69b4; /* 文本按钮颜色 */
}

::v-deep(.el-button--text:hover) {
    color: #ff1493; /* 文本按钮悬停颜色 */
}
</style>