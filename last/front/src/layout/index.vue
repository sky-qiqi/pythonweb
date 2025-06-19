<template>
  <div class="layout flex h-screen">
    <div
      class="
        layout-sidebar-mask
        fixed
        w-screen
        h-screen
        bg-black bg-opacity-25
        z-20
      "
      :class="{ hidden: getMenubar.status !== 2 }"
      @click="changeCollapsed"
    />
    <div
      v-if="getSetting.mode === 'vertical' || getMenubar.isPhone"
      class="
        layout-sidebar
        flex flex-col
        h-screen
        transition-width
        duration-200
        shadow
      "
      :class="{
        'w-64': getMenubar.status === 0 || getMenubar.status === 2,
        'w-0': getMenubar.status === 3,
        'w-16': getMenubar.status === 1,
        'absolute z-30': getMenubar.status === 2 || getMenubar.status === 3,
      }"
    >
      <div class="layout-sidebar-logo flex h-12 relative flex-center shadow-lg">
        <img class="w-8 h-8" :src="icon" />
        <span
          v-if="getMenubar.status === 0 || getMenubar.status === 2"
          class="pl-2"
          >{{ ImportMetaEnv.VITE_APP_TITLE }}</span
        >
      </div>
      <div class="layout-sidebar-menubar flex flex-1 overflow-hidden">
        <el-scrollbar wrap-class="scrollbar-wrapper">
          <layout-menubar />
        </el-scrollbar>
      </div>
    </div>
    <div
      class="layout-main flex flex-1 flex-col overflow-x-hidden overflow-y-auto"
    >
      <div
        class="
          layout-main-navbar
          flex
          justify-between
          items-center
          h-12
          shadow-sm
          overflow-hidden
          relative
          z-10
        "
      >
        <layout-navbar />
      </div>
      <div
        v-if="getSetting.showTags"
        class="layout-main-tags h-8 leading-8 text-sm text-gray-600 relative"
      >
        <layout-tags />
      </div>
      <div class="layout-main-content flex-1 overflow-hidden">
        <layout-content />
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import { defineComponent, onMounted } from "vue";
import LayoutContent from "/@/layout/components/content.vue";
import LayoutMenubar from "/@/layout/components/menubar.vue";
import LayoutNavbar from "/@/layout/components/navbar.vue";
import LayoutTags from "/@/layout/components/tags.vue";
import { throttle } from "/@/utils/tools";
import { useLayoutStore } from "/@/store/modules/layout";
import icon from "/@/assets/img/icon.png";

export default defineComponent({
  name: "Layout",
  components: {
    LayoutContent,
    LayoutMenubar,
    LayoutNavbar,
    LayoutTags,
  },
  setup() {
    const { changeDeviceWidth, changeCollapsed, getMenubar, getSetting } =
      useLayoutStore();

    onMounted(async () => {
      changeDeviceWidth();
      const throttleFn = throttle(300);
      let throttleF = async function () {
        await throttleFn();
        changeDeviceWidth();
      };
      window.addEventListener("resize", throttleF, true);
    });

    return {
      getMenubar,
      getSetting,
      changeCollapsed,
      icon,
    };
  },
});
</script>

<style lang='postcss' scoped>
/* 可爱风格布局样式 */

.layout {
  background-color: #fce4ec; /* 非常浅的粉色背景 */
}

.layout-sidebar {
  background-color: #f8bbd0; /* 浅粉色侧边栏背景 */
  box-shadow: 2px 0 10px rgba(244, 143, 177, 0.3); /* 可爱粉色阴影 */
}

.layout-sidebar-logo {
  background-color: #f48fb1; /* 可爱粉Logo背景 */
  color: white; /* 白色文字 */
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(244, 143, 177, 0.4);
}

.layout-sidebar-menubar ::v-deep(.el-scrollbar__wrap) {
  background-color: #f8bbd0; /* 侧边栏菜单背景 */
}

.layout-sidebar-menubar ::v-deep(.el-menu) {
  border-right: none;
  background-color: transparent; /* 菜单背景透明 */
}

.layout-sidebar-menubar ::v_deep(.el-menu-item),
.layout-sidebar-menubar ::v_deep(.el-sub-menu__title) {
  color: #880e4f; /* 深粉色文字 */
}

.layout-sidebar-menubar ::v_deep(.el-menu-item:hover),
.layout-sidebar-menubar ::v_deep(.el-sub-menu__title:hover) {
  background-color: #f06292; /* 亮粉色悬停背景 */
}

.layout-sidebar-menubar ::v_deep(.el-menu-item.is-active) {
  background-color: #e91e63; /* 鲜艳粉色选中背景 */
  color: white; /* 白色文字 */
}

.layout-main-navbar {
  background-color: #f8bbd0; /* 浅粉色导航栏背景 */
  box-shadow: 0 2px 5px rgba(244, 143, 177, 0.3);
}

.layout-main-tags {
  background-color: #fce4ec; /* 非常浅的粉色标签背景 */
  border-bottom: 1px solid #f48fb1; /* 可爱粉底部边框 */
}

.layout-main-content {
  background-color: #ffffff; /* 白色内容区域背景 */
  /* 可以考虑添加一个可爱的背景图片 */
  /* background-image: url('/@/assets/img/ai/hallowkity.jpg'); */
  /* background-repeat: repeat; */
  /* background-size: auto; */
  /* opacity: 0.8; */
}

/* 覆盖Element Plus默认样式以匹配可爱风格 */
::v_deep(.el-drawer__header) {
  margin-bottom: 0;
  color: #e91e63; /* 抽屉头部文字颜色 */
}

::v_deep(.el-menu--horizontal > .el-menu-item) {
  height: 48px;
}

::v_deep(.el-menu--horizontal > .el-sub-menu .el-sub-menu__title) {
  height: 48px;
  line-height: 48px;
}

::v_deep(.el-tag) {
  background-color: #f06292; /* 标签背景 */
  border-color: #e91e63; /* 标签边框 */
  color: white; /* 标签文字颜色 */
}

::v_deep(.el-tag .el-tag__close) {
  color: white; /* 标签关闭按钮颜色 */
}

::v_deep(.el-tag .el-tag__close:hover) {
  background-color: #880e4f; /* 标签关闭按钮悬停背景 */
  color: white; /* 标签关闭按钮悬停颜色 */
}
</style>