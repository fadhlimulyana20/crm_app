document.addEventListener('alpine:init', () => {
    Alpine.data('loadingIndicator', () => ({
        loading: true,
        init() {
            console.log("Loading indicator initialized");
            // Simulate loading time, replace with actual loading logic
            setTimeout(() => {
                console.log("Loading complete");
                this.loading = false;
            }, 500); // 500ms for demo
        }
    }));
});