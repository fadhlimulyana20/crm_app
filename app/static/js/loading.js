document.addEventListener('alpine:init', () => {
    Alpine.data('loadingIndicator', () => ({
        loading: true,
        init() {
            // Simulate loading time, replace with actual loading logic
            setTimeout(() => {
                this.loading = false;
            }, 2000); // 2 seconds for demo
        }
    }));
});