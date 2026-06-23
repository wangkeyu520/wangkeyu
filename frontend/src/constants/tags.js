export const FEELING_TAGS = [
  { id: 'service', label: '服务好', icon: '😊' },
  { id: 'fast', label: '出餐快', icon: '⚡' },
  { id: 'clean', label: '环境干净', icon: '✨' },
  { id: 'beautiful', label: '饮品颜值高', icon: '🥤' },
  { id: 'tasty', label: '味道很棒', icon: '😋' },
  { id: 'cheap', label: '价格实惠', icon: '💰' },
  { id: 'large', label: '份量足', icon: '👍' },
  { id: 'good', label: '性价比高', icon: '⭐' },
]

export const TAG_LABEL_MAP = Object.fromEntries(
  FEELING_TAGS.map((tag) => [tag.id, tag.label])
)

export function getTagLabels(tagIds) {
  return tagIds.map((id) => TAG_LABEL_MAP[id] || id)
}

export const PLATFORMS = [
  {
    id: 'xiaohongshu',
    name: '小红书',
    icon: '📕',
    description: '种草分享',
    gradient: 'linear-gradient(135deg, #f87171, #ec4899)',
  },
  {
    id: 'google',
    name: 'Google',
    icon: '🔍',
    description: '英文评价',
    gradient: 'linear-gradient(135deg, #60a5fa, #06b6d4)',
  },
]

export const PLATFORM_LABEL_MAP = Object.fromEntries(
  PLATFORMS.map((p) => [p.id, p.name])
)

export const STORE_INFO = {
  name: 'Sunny Tea House',
  location: 'San Jose',
  rating: 4.8,
}
