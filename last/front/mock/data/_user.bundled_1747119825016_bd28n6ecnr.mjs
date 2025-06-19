// mock/data/user.ts
var user = [
  { name: "admin", pwd: "admin" },
  { name: "dev", pwd: "dev" },
  { name: "test", pwd: "test" }
];
var role = [
  { name: "admin", description: "\u7BA1\u7406\u5458" },
  { name: "dev", description: "\u5F00\u53D1\u4EBA\u5458" },
  { name: "test", description: "\u6D4B\u8BD5\u4EBA\u5458" }
];
var user_role = [
  { userName: "admin", roleName: "admin" },
  { userName: "dev", roleName: "dev" },
  { userName: "test", roleName: "test" }
];
var permission = [
  { name: "add", description: "\u65B0\u589E" },
  { name: "update", description: "\u4FEE\u6539" },
  { name: "remove", description: "\u5220\u9664" }
];
var role_route = [
  { roleName: "admin", id: 1, permission: [] },
  { roleName: "admin", id: 10, permission: [] },
  { roleName: "admin", id: 2, permission: [] },
  { roleName: "admin", id: 20, permission: [] },
  { roleName: "admin", id: 21, permission: [] },
  { roleName: "admin", id: 22, permission: [] },
  { roleName: "admin", id: 3, permission: [] },
  { roleName: "admin", id: 30, permission: [] },
  { roleName: "admin", id: 300, permission: [] },
  { roleName: "admin", id: 31, permission: [] },
  { roleName: "admin", id: 310, permission: [] },
  { roleName: "admin", id: 4, permission: [] },
  { roleName: "admin", id: 40, permission: [] },
  { roleName: "admin", id: 41, permission: [] },
  { roleName: "admin", id: 42, permission: [] },
  { roleName: "admin", id: 43, permission: [] },
  { roleName: "admin", id: 5, permission: [] },
  { roleName: "admin", id: 50, permission: ["add", "update", "remove"] },
  { roleName: "dev", id: 1, permission: [] },
  { roleName: "dev", id: 10, permission: [] },
  { roleName: "dev", id: 5, permission: [] },
  { roleName: "dev", id: 50, permission: ["add"] },
  { roleName: "test", id: 1, permission: [] },
  { roleName: "test", id: 10, permission: [] },
  { roleName: "test", id: 5, permission: [] },
  { roleName: "test", id: 50, permission: ["update"] }
];
var route = [
  // {
  //     id: 2,
  //     parentId: 0,
  //     name: 'Project',
  //     path: '/Project',
  //     component: 'Layout',
  //     redirect: '/Project/ProjectList',
  //     meta: { title: '项目管理', icon: 'el-icon-phone' }
  // },
  // {
  //     id: 20,
  //     parentId: 2,
  //     name: 'ProjectList',
  //     path: '/Project/ProjectList',
  //     component: 'ProjectList',
  //     meta: { title: '项目列表', icon: 'el-icon-goods' }
  // },
  // {
  //     id: 21,
  //     parentId: 2,
  //     name: 'ProjectDetail',
  //     path: '/Project/ProjectDetail/:projName',
  //     component: 'ProjectDetail',
  //     meta: { title: '项目详情', icon: 'el-icon-question', activeMenu: '/Project/ProjectList', hidden: true }
  // },
  // {
  //     id: 22,
  //     parentId: 2,
  //     name: 'ProjectImport',
  //     path: '/Project/ProjectImport',
  //     component: 'ProjectImport',
  //     meta: { title: '项目导入', icon: 'el-icon-help' }
  // },
  // {
  //     id: 3,
  //     parentId: 0,
  //     name: 'Nav',
  //     path: '/Nav',
  //     component: 'Layout',
  //     redirect: '/Nav/SecondNav/ThirdNav',
  //     meta: { title: '多级导航', icon: 'el-icon-picture' }
  // },
  // {
  //     id: 30,
  //     parentId: 3,
  //     name: 'SecondNav',
  //     path: '/Nav/SecondNav',
  //     redirect: '/Nav/SecondNav/ThirdNav',
  //     component: 'SecondNav',
  //     meta: { title: '二级导航', icon: 'el-icon-camera', alwaysShow: true }
  // },
  // {
  //     id: 300,
  //     parentId: 30,
  //     name: 'ThirdNav',
  //     path: '/Nav/SecondNav/ThirdNav',
  //     component: 'ThirdNav',
  //     meta: { title: '三级导航', icon: 'el-icon-s-platform' }
  // },
  // {
  //     id: 31,
  //     parentId: 3,
  //     name: 'SecondText',
  //     path: '/Nav/SecondText',
  //     redirect: '/Nav/SecondText/ThirdText',
  //     component: 'SecondText',
  //     meta: { title: '二级文本', icon: 'el-icon-s-opportunity', alwaysShow: true }
  // },
  // {
  //     id: 310,
  //     parentId: 31,
  //     name: 'ThirdText',
  //     path: '/Nav/SecondText/ThirdText',
  //     component: 'ThirdText',
  //     meta: { title: '三级文本', icon: 'el-icon-menu' }
  // },
  // {
  //     id: 4,
  //     parentId: 0,
  //     name: 'Components',
  //     path: '/Components',
  //     component: 'Layout',
  //     redirect: '/Components/OpenWindowTest',
  //     meta: { title: '组件测试', icon: 'el-icon-phone' }
  // },
  // {
  //     id: 40,
  //     parentId: 4,
  //     name: 'OpenWindowTest',
  //     path: '/Components/OpenWindowTest',
  //     component: 'OpenWindowTest',
  //     meta: { title: '选择页', icon: 'el-icon-goods' }
  // },
  // {
  //     id: 41,
  //     parentId: 4,
  //     name: 'CardListTest',
  //     path: '/Components/CardListTest',
  //     component: 'CardListTest',
  //     meta: { title: '卡片列表', icon: 'el-icon-question' }
  // },
  // {
  //     id: 42,
  //     parentId: 4,
  //     name: 'TableSearchTest',
  //     path: '/Components/TableSearchTest',
  //     component: 'TableSearchTest',
  //     meta: { title: '表格搜索', icon: 'el-icon-question' }
  // },
  // {
  //     id: 43,
  //     parentId: 4,
  //     name: 'ListTest',
  //     path: '/Components/ListTest',
  //     component: 'ListTest',
  //     meta: { title: '标签页列表', icon: 'el-icon-question' }
  // },
  // {
  //     id: 5,
  //     parentId: 0,
  //     name: 'Permission',
  //     path: '/Permission',
  //     component: 'Layout',
  //     redirect: '/Permission/Directive',
  //     meta: { title: '权限管理', icon: 'el-icon-phone', alwaysShow: true }
  // },
  // {
  //     id: 50,
  //     parentId: 5,
  //     name: 'Directive',
  //     path: '/Permission/Directive',
  //     component: 'Directive',
  //     meta: { title: '指令管理', icon: 'el-icon-goods' }
  // }
];
export {
  permission,
  role,
  role_route,
  route,
  user,
  user_role
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsibW9jay9kYXRhL3VzZXIudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9faW5qZWN0ZWRfZmlsZW5hbWVfXyA9IFwiQzpcXFxcVXNlcnNcXFxccWlxaVxcXFxPbmVEcml2ZVxcXFxEZXNrdG9wXFxcXGNvZGVcXFxccHl0aG9ud2ViXFxcXGxhc3RcXFxcZnJvbnRcXFxcbW9ja1xcXFxkYXRhXFxcXHVzZXIudHNcIjtjb25zdCBfX2luamVjdGVkX2Rpcm5hbWVfXyA9IFwiQzpcXFxcVXNlcnNcXFxccWlxaVxcXFxPbmVEcml2ZVxcXFxEZXNrdG9wXFxcXGNvZGVcXFxccHl0aG9ud2ViXFxcXGxhc3RcXFxcZnJvbnRcXFxcbW9ja1xcXFxkYXRhXCI7Y29uc3QgX19pbmplY3RlZF9pbXBvcnRfbWV0YV91cmxfXyA9IFwiZmlsZTovLy9DOi9Vc2Vycy9xaXFpL09uZURyaXZlL0Rlc2t0b3AvY29kZS9weXRob253ZWIvbGFzdC9mcm9udC9tb2NrL2RhdGEvdXNlci50c1wiO2ltcG9ydCB7IElNZW51YmFyTGlzdCB9IGZyb20gJy9AL3R5cGUvc3RvcmUvbGF5b3V0J1xuZXhwb3J0IGNvbnN0IHVzZXIgPSBbXG4gICAgeyBuYW1lOiAnYWRtaW4nLCBwd2Q6ICdhZG1pbicgfSxcbiAgICB7IG5hbWU6ICdkZXYnLCBwd2Q6ICdkZXYnIH0sXG4gICAgeyBuYW1lOiAndGVzdCcsIHB3ZDogJ3Rlc3QnIH1cbl1cblxuZXhwb3J0IGNvbnN0IHJvbGUgPSBbXG4gICAgeyBuYW1lOiAnYWRtaW4nLCBkZXNjcmlwdGlvbjogJ1x1N0JBMVx1NzQwNlx1NTQ1OCcgfSxcbiAgICB7IG5hbWU6ICdkZXYnLCBkZXNjcmlwdGlvbjogJ1x1NUYwMFx1NTNEMVx1NEVCQVx1NTQ1OCcgfSxcbiAgICB7IG5hbWU6ICd0ZXN0JywgZGVzY3JpcHRpb246ICdcdTZENEJcdThCRDVcdTRFQkFcdTU0NTgnIH1cbl1cblxuZXhwb3J0IGNvbnN0IHVzZXJfcm9sZSA9IFtcbiAgICB7IHVzZXJOYW1lOiAnYWRtaW4nLCByb2xlTmFtZTogJ2FkbWluJyB9LFxuICAgIHsgdXNlck5hbWU6ICdkZXYnLCByb2xlTmFtZTogJ2RldicgfSxcbiAgICB7IHVzZXJOYW1lOiAndGVzdCcsIHJvbGVOYW1lOiAndGVzdCcgfVxuXVxuXG5leHBvcnQgY29uc3QgcGVybWlzc2lvbiA9IFtcbiAgICB7IG5hbWU6ICdhZGQnLCBkZXNjcmlwdGlvbjogJ1x1NjVCMFx1NTg5RScgfSxcbiAgICB7IG5hbWU6ICd1cGRhdGUnLCBkZXNjcmlwdGlvbjogJ1x1NEZFRVx1NjUzOScgfSxcbiAgICB7IG5hbWU6ICdyZW1vdmUnLCBkZXNjcmlwdGlvbjogJ1x1NTIyMFx1OTY2NCcgfVxuXVxuXG5leHBvcnQgY29uc3Qgcm9sZV9yb3V0ZSA9IFtcbiAgICB7IHJvbGVOYW1lOiAnYWRtaW4nLCBpZDogMSwgcGVybWlzc2lvbjogW10gfSxcbiAgICB7IHJvbGVOYW1lOiAnYWRtaW4nLCBpZDogMTAsIHBlcm1pc3Npb246IFtdIH0sXG4gICAgeyByb2xlTmFtZTogJ2FkbWluJywgaWQ6IDIsIHBlcm1pc3Npb246IFtdIH0sXG4gICAgeyByb2xlTmFtZTogJ2FkbWluJywgaWQ6IDIwLCBwZXJtaXNzaW9uOiBbXSB9LFxuICAgIHsgcm9sZU5hbWU6ICdhZG1pbicsIGlkOiAyMSwgcGVybWlzc2lvbjogW10gfSxcbiAgICB7IHJvbGVOYW1lOiAnYWRtaW4nLCBpZDogMjIsIHBlcm1pc3Npb246IFtdIH0sXG4gICAgeyByb2xlTmFtZTogJ2FkbWluJywgaWQ6IDMsIHBlcm1pc3Npb246IFtdIH0sXG4gICAgeyByb2xlTmFtZTogJ2FkbWluJywgaWQ6IDMwLCBwZXJtaXNzaW9uOiBbXSB9LFxuICAgIHsgcm9sZU5hbWU6ICdhZG1pbicsIGlkOiAzMDAsIHBlcm1pc3Npb246IFtdIH0sXG4gICAgeyByb2xlTmFtZTogJ2FkbWluJywgaWQ6IDMxLCBwZXJtaXNzaW9uOiBbXSB9LFxuICAgIHsgcm9sZU5hbWU6ICdhZG1pbicsIGlkOiAzMTAsIHBlcm1pc3Npb246IFtdIH0sXG4gICAgeyByb2xlTmFtZTogJ2FkbWluJywgaWQ6IDQsIHBlcm1pc3Npb246IFtdIH0sXG4gICAgeyByb2xlTmFtZTogJ2FkbWluJywgaWQ6IDQwLCBwZXJtaXNzaW9uOiBbXSB9LFxuICAgIHsgcm9sZU5hbWU6ICdhZG1pbicsIGlkOiA0MSwgcGVybWlzc2lvbjogW10gfSxcbiAgICB7IHJvbGVOYW1lOiAnYWRtaW4nLCBpZDogNDIsIHBlcm1pc3Npb246IFtdIH0sXG4gICAgeyByb2xlTmFtZTogJ2FkbWluJywgaWQ6IDQzLCBwZXJtaXNzaW9uOiBbXSB9LFxuICAgIHsgcm9sZU5hbWU6ICdhZG1pbicsIGlkOiA1LCBwZXJtaXNzaW9uOiBbXSB9LFxuICAgIHsgcm9sZU5hbWU6ICdhZG1pbicsIGlkOiA1MCwgcGVybWlzc2lvbjogWydhZGQnLCAndXBkYXRlJywgJ3JlbW92ZSddIH0sXG5cbiAgICB7IHJvbGVOYW1lOiAnZGV2JywgaWQ6IDEsIHBlcm1pc3Npb246IFtdIH0sXG4gICAgeyByb2xlTmFtZTogJ2RldicsIGlkOiAxMCwgcGVybWlzc2lvbjogW10gfSxcbiAgICB7IHJvbGVOYW1lOiAnZGV2JywgaWQ6IDUsIHBlcm1pc3Npb246IFtdIH0sXG4gICAgeyByb2xlTmFtZTogJ2RldicsIGlkOiA1MCwgcGVybWlzc2lvbjogWydhZGQnXSB9LFxuXG4gICAgeyByb2xlTmFtZTogJ3Rlc3QnLCBpZDogMSwgcGVybWlzc2lvbjogW10gfSxcbiAgICB7IHJvbGVOYW1lOiAndGVzdCcsIGlkOiAxMCwgcGVybWlzc2lvbjogW10gfSxcbiAgICB7IHJvbGVOYW1lOiAndGVzdCcsIGlkOiA1LCBwZXJtaXNzaW9uOiBbXSB9LFxuICAgIHsgcm9sZU5hbWU6ICd0ZXN0JywgaWQ6IDUwLCBwZXJtaXNzaW9uOiBbJ3VwZGF0ZSddIH1cbl1cblxuZXhwb3J0IGNvbnN0IHJvdXRlOkFycmF5PElNZW51YmFyTGlzdD4gPSBbXG4gICAgLy8ge1xuICAgIC8vICAgICBpZDogMixcbiAgICAvLyAgICAgcGFyZW50SWQ6IDAsXG4gICAgLy8gICAgIG5hbWU6ICdQcm9qZWN0JyxcbiAgICAvLyAgICAgcGF0aDogJy9Qcm9qZWN0JyxcbiAgICAvLyAgICAgY29tcG9uZW50OiAnTGF5b3V0JyxcbiAgICAvLyAgICAgcmVkaXJlY3Q6ICcvUHJvamVjdC9Qcm9qZWN0TGlzdCcsXG4gICAgLy8gICAgIG1ldGE6IHsgdGl0bGU6ICdcdTk4NzlcdTc2RUVcdTdCQTFcdTc0MDYnLCBpY29uOiAnZWwtaWNvbi1waG9uZScgfVxuICAgIC8vIH0sXG4gICAgLy8ge1xuICAgIC8vICAgICBpZDogMjAsXG4gICAgLy8gICAgIHBhcmVudElkOiAyLFxuICAgIC8vICAgICBuYW1lOiAnUHJvamVjdExpc3QnLFxuICAgIC8vICAgICBwYXRoOiAnL1Byb2plY3QvUHJvamVjdExpc3QnLFxuICAgIC8vICAgICBjb21wb25lbnQ6ICdQcm9qZWN0TGlzdCcsXG4gICAgLy8gICAgIG1ldGE6IHsgdGl0bGU6ICdcdTk4NzlcdTc2RUVcdTUyMTdcdTg4NjgnLCBpY29uOiAnZWwtaWNvbi1nb29kcycgfVxuICAgIC8vIH0sXG4gICAgLy8ge1xuICAgIC8vICAgICBpZDogMjEsXG4gICAgLy8gICAgIHBhcmVudElkOiAyLFxuICAgIC8vICAgICBuYW1lOiAnUHJvamVjdERldGFpbCcsXG4gICAgLy8gICAgIHBhdGg6ICcvUHJvamVjdC9Qcm9qZWN0RGV0YWlsLzpwcm9qTmFtZScsXG4gICAgLy8gICAgIGNvbXBvbmVudDogJ1Byb2plY3REZXRhaWwnLFxuICAgIC8vICAgICBtZXRhOiB7IHRpdGxlOiAnXHU5ODc5XHU3NkVFXHU4QkU2XHU2MEM1JywgaWNvbjogJ2VsLWljb24tcXVlc3Rpb24nLCBhY3RpdmVNZW51OiAnL1Byb2plY3QvUHJvamVjdExpc3QnLCBoaWRkZW46IHRydWUgfVxuICAgIC8vIH0sXG4gICAgLy8ge1xuICAgIC8vICAgICBpZDogMjIsXG4gICAgLy8gICAgIHBhcmVudElkOiAyLFxuICAgIC8vICAgICBuYW1lOiAnUHJvamVjdEltcG9ydCcsXG4gICAgLy8gICAgIHBhdGg6ICcvUHJvamVjdC9Qcm9qZWN0SW1wb3J0JyxcbiAgICAvLyAgICAgY29tcG9uZW50OiAnUHJvamVjdEltcG9ydCcsXG4gICAgLy8gICAgIG1ldGE6IHsgdGl0bGU6ICdcdTk4NzlcdTc2RUVcdTVCRkNcdTUxNjUnLCBpY29uOiAnZWwtaWNvbi1oZWxwJyB9XG4gICAgLy8gfSxcbiAgICAvLyB7XG4gICAgLy8gICAgIGlkOiAzLFxuICAgIC8vICAgICBwYXJlbnRJZDogMCxcbiAgICAvLyAgICAgbmFtZTogJ05hdicsXG4gICAgLy8gICAgIHBhdGg6ICcvTmF2JyxcbiAgICAvLyAgICAgY29tcG9uZW50OiAnTGF5b3V0JyxcbiAgICAvLyAgICAgcmVkaXJlY3Q6ICcvTmF2L1NlY29uZE5hdi9UaGlyZE5hdicsXG4gICAgLy8gICAgIG1ldGE6IHsgdGl0bGU6ICdcdTU5MUFcdTdFQTdcdTVCRkNcdTgyMkEnLCBpY29uOiAnZWwtaWNvbi1waWN0dXJlJyB9XG4gICAgLy8gfSxcbiAgICAvLyB7XG4gICAgLy8gICAgIGlkOiAzMCxcbiAgICAvLyAgICAgcGFyZW50SWQ6IDMsXG4gICAgLy8gICAgIG5hbWU6ICdTZWNvbmROYXYnLFxuICAgIC8vICAgICBwYXRoOiAnL05hdi9TZWNvbmROYXYnLFxuICAgIC8vICAgICByZWRpcmVjdDogJy9OYXYvU2Vjb25kTmF2L1RoaXJkTmF2JyxcbiAgICAvLyAgICAgY29tcG9uZW50OiAnU2Vjb25kTmF2JyxcbiAgICAvLyAgICAgbWV0YTogeyB0aXRsZTogJ1x1NEU4Q1x1N0VBN1x1NUJGQ1x1ODIyQScsIGljb246ICdlbC1pY29uLWNhbWVyYScsIGFsd2F5c1Nob3c6IHRydWUgfVxuICAgIC8vIH0sXG4gICAgLy8ge1xuICAgIC8vICAgICBpZDogMzAwLFxuICAgIC8vICAgICBwYXJlbnRJZDogMzAsXG4gICAgLy8gICAgIG5hbWU6ICdUaGlyZE5hdicsXG4gICAgLy8gICAgIHBhdGg6ICcvTmF2L1NlY29uZE5hdi9UaGlyZE5hdicsXG4gICAgLy8gICAgIGNvbXBvbmVudDogJ1RoaXJkTmF2JyxcbiAgICAvLyAgICAgbWV0YTogeyB0aXRsZTogJ1x1NEUwOVx1N0VBN1x1NUJGQ1x1ODIyQScsIGljb246ICdlbC1pY29uLXMtcGxhdGZvcm0nIH1cbiAgICAvLyB9LFxuICAgIC8vIHtcbiAgICAvLyAgICAgaWQ6IDMxLFxuICAgIC8vICAgICBwYXJlbnRJZDogMyxcbiAgICAvLyAgICAgbmFtZTogJ1NlY29uZFRleHQnLFxuICAgIC8vICAgICBwYXRoOiAnL05hdi9TZWNvbmRUZXh0JyxcbiAgICAvLyAgICAgcmVkaXJlY3Q6ICcvTmF2L1NlY29uZFRleHQvVGhpcmRUZXh0JyxcbiAgICAvLyAgICAgY29tcG9uZW50OiAnU2Vjb25kVGV4dCcsXG4gICAgLy8gICAgIG1ldGE6IHsgdGl0bGU6ICdcdTRFOENcdTdFQTdcdTY1ODdcdTY3MkMnLCBpY29uOiAnZWwtaWNvbi1zLW9wcG9ydHVuaXR5JywgYWx3YXlzU2hvdzogdHJ1ZSB9XG4gICAgLy8gfSxcbiAgICAvLyB7XG4gICAgLy8gICAgIGlkOiAzMTAsXG4gICAgLy8gICAgIHBhcmVudElkOiAzMSxcbiAgICAvLyAgICAgbmFtZTogJ1RoaXJkVGV4dCcsXG4gICAgLy8gICAgIHBhdGg6ICcvTmF2L1NlY29uZFRleHQvVGhpcmRUZXh0JyxcbiAgICAvLyAgICAgY29tcG9uZW50OiAnVGhpcmRUZXh0JyxcbiAgICAvLyAgICAgbWV0YTogeyB0aXRsZTogJ1x1NEUwOVx1N0VBN1x1NjU4N1x1NjcyQycsIGljb246ICdlbC1pY29uLW1lbnUnIH1cbiAgICAvLyB9LFxuICAgIC8vIHtcbiAgICAvLyAgICAgaWQ6IDQsXG4gICAgLy8gICAgIHBhcmVudElkOiAwLFxuICAgIC8vICAgICBuYW1lOiAnQ29tcG9uZW50cycsXG4gICAgLy8gICAgIHBhdGg6ICcvQ29tcG9uZW50cycsXG4gICAgLy8gICAgIGNvbXBvbmVudDogJ0xheW91dCcsXG4gICAgLy8gICAgIHJlZGlyZWN0OiAnL0NvbXBvbmVudHMvT3BlbldpbmRvd1Rlc3QnLFxuICAgIC8vICAgICBtZXRhOiB7IHRpdGxlOiAnXHU3RUM0XHU0RUY2XHU2RDRCXHU4QkQ1JywgaWNvbjogJ2VsLWljb24tcGhvbmUnIH1cbiAgICAvLyB9LFxuICAgIC8vIHtcbiAgICAvLyAgICAgaWQ6IDQwLFxuICAgIC8vICAgICBwYXJlbnRJZDogNCxcbiAgICAvLyAgICAgbmFtZTogJ09wZW5XaW5kb3dUZXN0JyxcbiAgICAvLyAgICAgcGF0aDogJy9Db21wb25lbnRzL09wZW5XaW5kb3dUZXN0JyxcbiAgICAvLyAgICAgY29tcG9uZW50OiAnT3BlbldpbmRvd1Rlc3QnLFxuICAgIC8vICAgICBtZXRhOiB7IHRpdGxlOiAnXHU5MDA5XHU2MkU5XHU5ODc1JywgaWNvbjogJ2VsLWljb24tZ29vZHMnIH1cbiAgICAvLyB9LFxuICAgIC8vIHtcbiAgICAvLyAgICAgaWQ6IDQxLFxuICAgIC8vICAgICBwYXJlbnRJZDogNCxcbiAgICAvLyAgICAgbmFtZTogJ0NhcmRMaXN0VGVzdCcsXG4gICAgLy8gICAgIHBhdGg6ICcvQ29tcG9uZW50cy9DYXJkTGlzdFRlc3QnLFxuICAgIC8vICAgICBjb21wb25lbnQ6ICdDYXJkTGlzdFRlc3QnLFxuICAgIC8vICAgICBtZXRhOiB7IHRpdGxlOiAnXHU1MzYxXHU3MjQ3XHU1MjE3XHU4ODY4JywgaWNvbjogJ2VsLWljb24tcXVlc3Rpb24nIH1cbiAgICAvLyB9LFxuICAgIC8vIHtcbiAgICAvLyAgICAgaWQ6IDQyLFxuICAgIC8vICAgICBwYXJlbnRJZDogNCxcbiAgICAvLyAgICAgbmFtZTogJ1RhYmxlU2VhcmNoVGVzdCcsXG4gICAgLy8gICAgIHBhdGg6ICcvQ29tcG9uZW50cy9UYWJsZVNlYXJjaFRlc3QnLFxuICAgIC8vICAgICBjb21wb25lbnQ6ICdUYWJsZVNlYXJjaFRlc3QnLFxuICAgIC8vICAgICBtZXRhOiB7IHRpdGxlOiAnXHU4ODY4XHU2ODNDXHU2NDFDXHU3RDIyJywgaWNvbjogJ2VsLWljb24tcXVlc3Rpb24nIH1cbiAgICAvLyB9LFxuICAgIC8vIHtcbiAgICAvLyAgICAgaWQ6IDQzLFxuICAgIC8vICAgICBwYXJlbnRJZDogNCxcbiAgICAvLyAgICAgbmFtZTogJ0xpc3RUZXN0JyxcbiAgICAvLyAgICAgcGF0aDogJy9Db21wb25lbnRzL0xpc3RUZXN0JyxcbiAgICAvLyAgICAgY29tcG9uZW50OiAnTGlzdFRlc3QnLFxuICAgIC8vICAgICBtZXRhOiB7IHRpdGxlOiAnXHU2ODA3XHU3QjdFXHU5ODc1XHU1MjE3XHU4ODY4JywgaWNvbjogJ2VsLWljb24tcXVlc3Rpb24nIH1cbiAgICAvLyB9LFxuICAgIC8vIHtcbiAgICAvLyAgICAgaWQ6IDUsXG4gICAgLy8gICAgIHBhcmVudElkOiAwLFxuICAgIC8vICAgICBuYW1lOiAnUGVybWlzc2lvbicsXG4gICAgLy8gICAgIHBhdGg6ICcvUGVybWlzc2lvbicsXG4gICAgLy8gICAgIGNvbXBvbmVudDogJ0xheW91dCcsXG4gICAgLy8gICAgIHJlZGlyZWN0OiAnL1Blcm1pc3Npb24vRGlyZWN0aXZlJyxcbiAgICAvLyAgICAgbWV0YTogeyB0aXRsZTogJ1x1Njc0M1x1OTY1MFx1N0JBMVx1NzQwNicsIGljb246ICdlbC1pY29uLXBob25lJywgYWx3YXlzU2hvdzogdHJ1ZSB9XG4gICAgLy8gfSxcbiAgICAvLyB7XG4gICAgLy8gICAgIGlkOiA1MCxcbiAgICAvLyAgICAgcGFyZW50SWQ6IDUsXG4gICAgLy8gICAgIG5hbWU6ICdEaXJlY3RpdmUnLFxuICAgIC8vICAgICBwYXRoOiAnL1Blcm1pc3Npb24vRGlyZWN0aXZlJyxcbiAgICAvLyAgICAgY29tcG9uZW50OiAnRGlyZWN0aXZlJyxcbiAgICAvLyAgICAgbWV0YTogeyB0aXRsZTogJ1x1NjMwN1x1NEVFNFx1N0JBMVx1NzQwNicsIGljb246ICdlbC1pY29uLWdvb2RzJyB9XG4gICAgLy8gfVxuXSJdLAogICJtYXBwaW5ncyI6ICI7QUFDTyxJQUFNLE9BQU87QUFBQSxFQUNoQixFQUFFLE1BQU0sU0FBUyxLQUFLLFFBQVE7QUFBQSxFQUM5QixFQUFFLE1BQU0sT0FBTyxLQUFLLE1BQU07QUFBQSxFQUMxQixFQUFFLE1BQU0sUUFBUSxLQUFLLE9BQU87QUFDaEM7QUFFTyxJQUFNLE9BQU87QUFBQSxFQUNoQixFQUFFLE1BQU0sU0FBUyxhQUFhLHFCQUFNO0FBQUEsRUFDcEMsRUFBRSxNQUFNLE9BQU8sYUFBYSwyQkFBTztBQUFBLEVBQ25DLEVBQUUsTUFBTSxRQUFRLGFBQWEsMkJBQU87QUFDeEM7QUFFTyxJQUFNLFlBQVk7QUFBQSxFQUNyQixFQUFFLFVBQVUsU0FBUyxVQUFVLFFBQVE7QUFBQSxFQUN2QyxFQUFFLFVBQVUsT0FBTyxVQUFVLE1BQU07QUFBQSxFQUNuQyxFQUFFLFVBQVUsUUFBUSxVQUFVLE9BQU87QUFDekM7QUFFTyxJQUFNLGFBQWE7QUFBQSxFQUN0QixFQUFFLE1BQU0sT0FBTyxhQUFhLGVBQUs7QUFBQSxFQUNqQyxFQUFFLE1BQU0sVUFBVSxhQUFhLGVBQUs7QUFBQSxFQUNwQyxFQUFFLE1BQU0sVUFBVSxhQUFhLGVBQUs7QUFDeEM7QUFFTyxJQUFNLGFBQWE7QUFBQSxFQUN0QixFQUFFLFVBQVUsU0FBUyxJQUFJLEdBQUcsWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUMzQyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM1QyxFQUFFLFVBQVUsU0FBUyxJQUFJLEdBQUcsWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUMzQyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM1QyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM1QyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM1QyxFQUFFLFVBQVUsU0FBUyxJQUFJLEdBQUcsWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUMzQyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM1QyxFQUFFLFVBQVUsU0FBUyxJQUFJLEtBQUssWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM3QyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM1QyxFQUFFLFVBQVUsU0FBUyxJQUFJLEtBQUssWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM3QyxFQUFFLFVBQVUsU0FBUyxJQUFJLEdBQUcsWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUMzQyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM1QyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM1QyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM1QyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUM1QyxFQUFFLFVBQVUsU0FBUyxJQUFJLEdBQUcsWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUMzQyxFQUFFLFVBQVUsU0FBUyxJQUFJLElBQUksWUFBWSxDQUFDLE9BQU8sVUFBVSxRQUFRLEVBQUU7QUFBQSxFQUVyRSxFQUFFLFVBQVUsT0FBTyxJQUFJLEdBQUcsWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUN6QyxFQUFFLFVBQVUsT0FBTyxJQUFJLElBQUksWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUMxQyxFQUFFLFVBQVUsT0FBTyxJQUFJLEdBQUcsWUFBWSxDQUFDLEVBQUU7QUFBQSxFQUN6QyxFQUFFLFVBQVUsT0FBTyxJQUFJLElBQUksWUFBWSxDQUFDLEtBQUssRUFBRTtBQUFBLEVBRS9DLEVBQUUsVUFBVSxRQUFRLElBQUksR0FBRyxZQUFZLENBQUMsRUFBRTtBQUFBLEVBQzFDLEVBQUUsVUFBVSxRQUFRLElBQUksSUFBSSxZQUFZLENBQUMsRUFBRTtBQUFBLEVBQzNDLEVBQUUsVUFBVSxRQUFRLElBQUksR0FBRyxZQUFZLENBQUMsRUFBRTtBQUFBLEVBQzFDLEVBQUUsVUFBVSxRQUFRLElBQUksSUFBSSxZQUFZLENBQUMsUUFBUSxFQUFFO0FBQ3ZEO0FBRU8sSUFBTSxRQUE0QjtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUF1SXpDOyIsCiAgIm5hbWVzIjogW10KfQo=
