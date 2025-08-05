<!-- 主页视图 -->
<template>
  <main>
    <HeroSection />
    <FeaturesSection />
    <WorkflowSection />
    <AdvantagesSection />
    <ContactSection />
    <FooterSection />
  </main>
</template>

<script setup lang="ts">
import HeroSection from "@/components/home/HeroSection.vue";
import FeaturesSection from "@/components/home/FeaturesSection.vue";
import WorkflowSection from "@/components/home/WorkflowSection.vue";
import AdvantagesSection from "@/components/home/AdvantagesSection.vue";
import ContactSection from "@/components/home/ContactSection.vue";
import FooterSection from "@/components/home/FooterSection.vue";
</script>

<style scoped>
/* 样式已移至内联 Tailwind 类中 */
</style>
