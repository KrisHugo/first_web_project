<template>
  <div class="app-layout">
    <AppHeader />
    <main class="app-content">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component 
            :is="Component" 
            v-if="$route.meta.keepAlive"
            :key="$route.name"
          />
        </keep-alive>
        <component 
          :is="Component" 
          v-if="!$route.meta.keepAlive"
          :key="$route.name"
        />
      </router-view>
    </main>
    <AppFooter />
  </div>
</template>