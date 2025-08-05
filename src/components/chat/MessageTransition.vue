<!-- 消息过渡动画组件 -->
<template>
  <transition-group
    name="message"
    tag="div"
    class="space-y-6"
    @before-enter="beforeEnter"
    @enter="enter"
    @leave="leave"
  >
    <slot></slot>
  </transition-group>
</template>

<script setup lang="ts">
import { gsap } from 'gsap'

const beforeEnter = (el: Element) => {
  const element = el as HTMLElement
  element.style.opacity = '0'
  element.style.transform = 'translateY(20px)'
}

const enter = (el: Element, done: () => void) => {
  gsap.to(el, {
    opacity: 1,
    y: 0,
    duration: 0.3,
    onComplete: done
  })
}

const leave = (el: Element, done: () => void) => {
  gsap.to(el, {
    opacity: 0,
    x: -100,
    duration: 0.3,
    onComplete: done
  })
}
</script>

<style scoped>
.message-move {
  transition: all 0.3s ease;
}
</style> 