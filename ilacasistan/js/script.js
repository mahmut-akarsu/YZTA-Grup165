class MedicineApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.initializeNavigation();
        this.stream = null;
        this.medicineData = this.getMedicineDatabase();
    }

    initializeElements() {
        this.medicineInput = document.getElementById('medicineInput');
        this.cameraBtn = document.getElementById('cameraBtn');
        this.searchBtn = document.getElementById('searchBtn');
        this.cameraSection = document.getElementById('cameraSection');
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.captureBtn = document.getElementById('captureBtn');
        this.closeCameraBtn = document.getElementById('closeCameraBtn');
        this.resultsSection = document.getElementById('resultsSection');
        this.loading = document.getElementById('loading');
        this.errorMessage = document.getElementById('errorMessage');
        
        // Result elements
        this.medicineImage = document.getElementById('medicineImage');
        this.medicineName = document.getElementById('medicineName');
        this.activeIngredient = document.getElementById('activeIngredient');
        this.manufacturer = document.getElementById('manufacturer');
        this.form = document.getElementById('form');
        this.usage = document.getElementById('usage');
        this.sideEffects = document.getElementById('sideEffects');
        this.dosage = document.getElementById('dosage');
    }

    bindEvents() {
        this.searchBtn.addEventListener('click', () => this.searchMedicine());
        this.cameraBtn.addEventListener('click', () => this.openCamera());
        this.captureBtn.addEventListener('click', () => this.capturePhoto());
        this.closeCameraBtn.addEventListener('click', () => this.closeCamera());
        
        this.medicineInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchMedicine();
            }
        });
    }

    initializeNavigation() {
        // Sayfa geçiş fonksiyonunu global scope'a ekle
        window.showPage = (pageId) => {
            // Tüm sayfaları gizle
            const pages = document.querySelectorAll('.page');
            pages.forEach(page => page.classList.remove('active'));
            
            // Tüm nav linklerinden active class'ını kaldır
            const navLinks = document.querySelectorAll('.nav-link');
            navLinks.forEach(link => link.classList.remove('active'));
            
            // Seçilen sayfayı göster
            const targetPage = document.getElementById(pageId);
            if (targetPage) {
                targetPage.classList.add('active');
            }
            
            // Aktif nav link'i işaretle
            const activeNavLink = document.querySelector(`[onclick="showPage('${pageId}')"]`);
            if (activeNavLink) {
                activeNavLink.classList.add('active');
            }
        };
    }

    getMedicineDatabase() {
        return {
            'parol': {
                name: 'Parol',
                activeIngredient: 'Parasetamol 500mg',
                manufacturer: 'Atabay İlaç',
                form: 'Tablet',
                usage: 'Ağrı kesici, ateş düşürücü',
                sideEffects: 'Nadir: Mide bulantısı, alerjik reaksiyonlar',
                dosage: 'Günde 3-4 kez 1 tablet (Max: 4g/gün)',
                image: 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=200&fit=crop'
            },
            'aspirin': {
                name: 'Aspirin',
                activeIngredient: 'Asetilsalisilik Asit 500mg',
                manufacturer: 'Bayer',
                form: 'Tablet',
                usage: 'Ağrı kesici, ateş düşürücü, kan sulandırıcı',
                sideEffects: 'Mide irritasyonu, kanama riski',
                dosage: 'Günde 1-3 kez 1 tablet',
                image: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=300&h=200&fit=crop'
            },
            'nurofen': {
                name: 'Nurofen',
                activeIngredient: 'İbuprofen 400mg',
                manufacturer: 'Reckitt Benckiser',
                form: 'Tablet',
                usage: 'Ağrı kesici, ateş düşürücü, antiinflamatuar',
                sideEffects: 'Mide bulantısı, baş dönmesi',
                dosage: 'Günde 3-4 kez 1 tablet',
                image: 'https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=300&h=200&fit=crop'
            },
            'voltaren': {
                name: 'Voltaren',
                activeIngredient: 'Diklofenak Sodyum 50mg',
                manufacturer: 'Novartis',
                form: 'Tablet',
                usage: 'Antiinflamatuar, ağrı kesici',
                sideEffects: 'Mide ağrısı, baş ağrısı',
                dosage: 'Günde 2-3 kez 1 tablet',
                image: 'https://images.unsplash.com/photo-1576602976047-174e57a47881?w=300&h=200&fit=crop'
            }
        };
    }

    async searchMedicine() {
        const medicineName = this.medicineInput.value.trim().toLowerCase();
        
        if (!medicineName) {
            this.showError('Lütfen ilaç adını girin.');
            return;
        }

        this.showLoading();
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const medicine = this.medicineData[medicineName];
        
        if (medicine) {
            this.displayMedicine(medicine);
        } else {
            this.showError('İlaç bulunamadı. Lütfen doğru isim girdiğinizden emin olun.');
        }
    }

    displayMedicine(medicine) {
        this.hideAllSections();
        
        this.medicineImage.src = medicine.image;
        this.medicineName.textContent = medicine.name;
        this.activeIngredient.textContent = medicine.activeIngredient;
        this.manufacturer.textContent = medicine.manufacturer;
        this.form.textContent = medicine.form;
        this.usage.textContent = medicine.usage;
        this.sideEffects.textContent = medicine.sideEffects;
        this.dosage.textContent = medicine.dosage;
        
        this.resultsSection.classList.add('active');
    }

    async openCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: 'environment' } 
            });
            this.video.srcObject = this.stream;
            this.cameraSection.classList.add('active');
            this.hideOtherSections();
        } catch (error) {
            alert('Kameraya erişim sağlanamadı. Lütfen izin verdiğinizden emin olun.');
            console.error('Kamera hatası:', error);
        }
    }

    async capturePhoto() {
        const context = this.canvas.getContext('2d');
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        
        context.drawImage(this.video, 0, 0);
        
        // Simulate photo processing
        this.showLoading();
        this.closeCamera();
        
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Simulate random medicine recognition
        const medicines = Object.keys(this.medicineData);
        const randomMedicine = medicines[Math.floor(Math.random() * medicines.length)];
        const medicine = this.medicineData[randomMedicine];
        
        this.displayMedicine(medicine);
    }

    closeCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        this.cameraSection.classList.remove('active');
    }

    showLoading() {
        this.hideAllSections();
        this.loading.classList.add('active');
    }

    showError(message) {
        this.hideAllSections();
        this.errorMessage.querySelector('p').textContent = message;
        this.errorMessage.classList.add('active');
    }

    hideAllSections() {
        this.resultsSection.classList.remove('active');
        this.loading.classList.remove('active');
        this.errorMessage.classList.remove('active');
        this.cameraSection.classList.remove('active');
    }

    hideOtherSections() {
        this.resultsSection.classList.remove('active');
        this.loading.classList.remove('active');
        this.errorMessage.classList.remove('active');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MedicineApp();
});