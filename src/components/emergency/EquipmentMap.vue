# 创建医疗设备位置地图组件
<template>
  <div class="relative w-full h-full">
    <!-- 地图容器 -->
    <div ref="mapContainer" class="w-full h-full"></div>

    <!-- 加载状态 -->
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/80">
      <LoadingDots />
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="absolute inset-0 flex items-center justify-center bg-white/80">
      <div class="text-center">
        <i class="fas fa-exclamation-circle text-3xl text-danger mb-2"></i>
        <p class="text-sm text-gray-600">{{ error }}</p>
        <button 
          class="mt-4 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
          @click="initMap"
        >
          重试
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import LoadingDots from '@/components/chat/LoadingDots.vue'

// 声明高德地图类型
declare global {
  interface Window {
    AMap: any
  }
}

const props = defineProps<{
  equipment: Array<{
    id: string
    name: string
    type: string
    location: string
    distance: number
    coordinates: [number, number]
  }>
  userLocation?: {
    latitude: number
    longitude: number
  }
}>()

const mapContainer = ref<HTMLElement | null>(null)
const loading = ref(false)
const error = ref('')
let map: any = null // 地图实例

// 初始化地图
const initMap = async () => {
  if (!mapContainer.value) return

  loading.value = true
  error.value = ''

  try {
    // 这里使用高德地图 SDK
    // 注意：需要先在 index.html 中引入高德地图 SDK
    if (window.AMap) {
      map = new window.AMap.Map(mapContainer.value, {
        zoom: 15,
        center: props.userLocation 
          ? [props.userLocation.longitude, props.userLocation.latitude]
          : [116.397428, 39.90923] // 默认位置：北京
      })

      // 添加定位标记
      if (props.userLocation) {
        new window.AMap.Marker({
          map,
          position: [props.userLocation.longitude, props.userLocation.latitude],
          icon: new window.AMap.Icon({
            size: new window.AMap.Size(32, 32),
            image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png'
          })
        })
      }

      // 添加设备标记
      props.equipment.forEach(item => {
        const marker = new window.AMap.Marker({
          map,
          position: item.coordinates,
          icon: new window.AMap.Icon({
            size: new window.AMap.Size(32, 32),
            image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png'
          })
        })

        // 添加信息窗体
        const infoWindow = new window.AMap.InfoWindow({
          content: `
            <div class="p-2">
              <h3 class="font-bold">${item.name}</h3>
              <p class="text-sm text-gray-600">${item.location}</p>
              <p class="text-sm text-gray-600">距离：${item.distance}米</p>
            </div>
          `,
          offset: new window.AMap.Pixel(0, -32)
        })

        // 点击标记时显示信息窗体
        marker.on('click', () => {
          infoWindow.open(map, marker.getPosition())
        })
      })
    } else {
      throw new Error('地图 SDK 未加载')
    }
  } catch (err) {
    console.error('初始化地图失败:', err)
    error.value = '加载地图失败，请检查网络连接'
  } finally {
    loading.value = false
  }
}

// 监听设备列表变化
watch(() => props.equipment, () => {
  if (map) {
    initMap()
  }
}, { deep: true })

// 生命周期钩子
onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.destroy()
    map = null
  }
})
</script>

<style scoped>
.amap-marker-label {
  border: none;
  background-color: transparent;
}
</style> 