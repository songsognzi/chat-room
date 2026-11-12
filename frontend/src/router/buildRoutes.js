/**
 * 把后端返回的菜单转换成 vue-router 路由记录。
 * @param {Array<{code:string,name:string,path:string,component:string,icon?:string}>} menus
 * @param {{views?: Record<string, any>, fallback?: any}} options
 */
export function buildRoutes(menus = [], { views = {}, fallback } = {}) {
  return menus.map((menu) => ({
    path: menu.path,
    name: menu.code,
    component: views[menu.component] || fallback,
    meta: {
      title: menu.name,
      icon: menu.icon,
    },
  }))
}
