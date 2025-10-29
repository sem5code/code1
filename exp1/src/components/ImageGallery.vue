<template>
  <div class="app">
    <header class="header">
      <h1>
        Gallery <span class="count">{{ filteredImages.length }}</span>
      </h1>
      <input v-model="searchTerm" placeholder="Search..." class="search" />
    </header>

    <main class="main">
      <div v-if="filteredImages.length" class="grid">
        <div
          v-for="(img, i) in filteredImages"
          :key="i"
          class="card"
          @click="selectImage(i)"
        >
          <img :src="img.src" :alt="img.alt" />
          <h3>{{ img.alt }}</h3>
          <button @click.stop="deleteImage(i)" class="del">×</button>
        </div>
      </div>
      <div v-else class="empty">🖼️ No artworks found</div>
    </main>

    <div v-if="isLightboxActive" class="lightbox" @click="closeLightbox">
      <div class="modal" @click.stop>
        <button @click="closeLightbox" class="close">×</button>
        <div class="viewer">
          <button @click="prevImage" :disabled="selectedImageIndex === 0">
            ‹
          </button>
          <img
            :src="selectedImage.src"
            :alt="selectedImage.alt"
            :style="{ transform: `scale(${zoom})` }"
            @wheel="zoomImage"
          />
          <button
            @click="nextImage"
            :disabled="selectedImageIndex >= images.length - 1"
          >
            ›
          </button>
        </div>
        <p class="info">{{ selectedImageIndex + 1 }} of {{ images.length }}</p>
      </div>
    </div>

    <button v-if="deletedImages.length" @click="restoreImage" class="restore">
      ↺ Restore ({{ deletedImages.length }})
    </button>
  </div>
</template>

<script>
export default {
  name: "ImageGallery",
  data: () => ({
    images: Array.from({ length: 12 }, (_, i) => ({
      src: `https://picsum.photos/seed/${i + 100}/800/600`,
      alt: `Artwork ${i + 1}`,
    })),
    deletedImages: [],
    selectedImageIndex: null,
    zoom: 1,
    searchTerm: "",
  }),
  computed: {
    isLightboxActive() {
      return this.selectedImageIndex !== null;
    },
    selectedImage() {
      return this.images[this.selectedImageIndex];
    },
    filteredImages() {
      return this.searchTerm
        ? this.images.filter((img) =>
            img.alt.toLowerCase().includes(this.searchTerm.toLowerCase())
          )
        : this.images;
    },
  },
  methods: {
    selectImage(i) {
      this.selectedImageIndex = i;
      this.zoom = 1;
    },
    closeLightbox() {
      this.selectedImageIndex = null;
    },
    deleteImage(i) {
      this.deletedImages.push(this.images.splice(i, 1)[0]);
    },
    restoreImage() {
      if (this.deletedImages.length) this.images.push(this.deletedImages.pop());
    },
    zoomImage(e) {
      e.preventDefault();
      this.zoom = Math.max(
        0.5,
        Math.min(this.zoom + (e.deltaY > 0 ? -0.1 : 0.1), 3)
      );
    },
    prevImage() {
      if (this.selectedImageIndex > 0) {
        this.selectedImageIndex--;
        this.zoom = 1;
      }
    },
    nextImage() {
      if (this.selectedImageIndex < this.images.length - 1) {
        this.selectedImageIndex++;
        this.zoom = 1;
      }
    },
  },
};
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 50%, #f1f5f9 100%);
  font-family: -apple-system, sans-serif;
}
.header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #e2e8f0;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.header h1 {
  font-size: 2rem;
  font-weight: 300;
  color: #1e293b;
  margin: 0;
}
.count {
  margin-left: 12px;
  font-size: 0.875rem;
  color: #64748b;
  background: #f1f5f9;
  padding: 4px 12px;
  border-radius: 20px;
}
.search {
  width: 256px;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.7);
  outline: none;
  transition: all 0.3s;
}
.search:focus {
  border-color: #64748b;
  box-shadow: 0 0 0 3px rgba(100, 116, 139, 0.1);
}
.main {
  padding: 48px 24px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 32px;
}
.card {
  position: relative;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.5s;
}
.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1);
}
.card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  transition: transform 0.7s;
}
.card:hover img {
  transform: scale(1.1);
}
.card h3 {
  padding: 16px;
  font-size: 1.125rem;
  font-weight: 500;
  color: #1e293b;
  margin: 0;
}
.del {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  opacity: 0;
  transition: all 0.3s;
  cursor: pointer;
  color: #64748b;
  font-size: 1.2rem;
}
.card:hover .del {
  opacity: 1;
}
.del:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}
.empty {
  text-align: center;
  padding: 80px 0;
  color: #64748b;
  font-size: 1.125rem;
}
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}
.modal {
  background: white;
  border-radius: 24px;
  max-width: 1200px;
  width: 100%;
  overflow: hidden;
  position: relative;
}
.close {
  position: absolute;
  top: 24px;
  right: 24px;
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  z-index: 10;
}
.viewer {
  background: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
  position: relative;
  min-height: 400px;
}
.viewer button {
  position: absolute;
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  color: #374151;
}
.viewer button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
.viewer button:first-child {
  left: 16px;
}
.viewer button:last-child {
  right: 16px;
}
.viewer img {
  max-width: 100%;
  max-height: 500px;
  object-fit: contain;
  transition: transform 0.3s;
  border-radius: 8px;
}
.info {
  padding: 24px;
  text-align: center;
  color: #94a3b8;
  margin: 0;
  border-top: 1px solid #e2e8f0;
}
.restore {
  position: fixed;
  bottom: 32px;
  right: 32px;
  background: #1e293b;
  color: white;
  border: none;
  padding: 16px 24px;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}
.restore:hover {
  background: #334155;
  transform: translateY(-2px);
}
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 16px;
  }
  .search {
    width: 100%;
  }
  .grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 24px;
  }
  .main {
    padding: 32px 16px;
  }
}
</style>
