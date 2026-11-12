import request from './request'

export async function fetchMenus() {
  const body = await request.get('/menus')
  return body.data || []
}
