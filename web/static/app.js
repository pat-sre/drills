// Global editor instance
let editor = null;

function app() {
    return {
        categories: {},
        exercisesByTopic: {},
        activeCategory: "DSA",
        current: null,
        skeleton: "",
        output: "",
        passed: false,
        loading: false,
        errorType: null,
        darkMode: localStorage.getItem("theme") === "dark",

        async init() {
            // Apply saved theme on load
            if (this.darkMode) {
                document.documentElement.setAttribute("data-theme", "dark");
            }

            // Create editor only once
            if (!editor) {
                const container = document.getElementById("editor-container");
                container.innerHTML = "";
                editor = CodeMirror(container, {
                    mode: "python",
                    lineNumbers: true,
                    theme: this.darkMode ? "material-darker" : "default",
                    indentUnit: 4,
                    tabSize: 4,
                    indentWithTabs: false,
                    value: "# Select an exercise from the sidebar",
                    extraKeys: {
                        Tab: (cm) => cm.execCommand("indentMore"),
                        "Shift-Tab": (cm) => cm.execCommand("indentLess"),
                    },
                });
            }

            await this.loadExercises();
        },

        async loadExercises() {
            try {
                const [catRes, exRes] = await Promise.all([
                    fetch("/api/categories"),
                    fetch("/api/exercises"),
                ]);
                if (catRes.ok) {
                    this.categories = await catRes.json();
                }
                if (exRes.ok) {
                    this.exercisesByTopic = await exRes.json();
                }
            } catch (err) {
                console.error("Failed to load exercises:", err);
            }
        },

        setCategory(category) {
            this.activeCategory = category;
        },

        getTopicsForCategory() {
            return this.categories[this.activeCategory] || [];
        },

        getFilteredExercises() {
            const topics = this.getTopicsForCategory();
            const result = {};
            for (const topic of topics) {
                if (this.exercisesByTopic[topic]) {
                    result[topic] = this.exercisesByTopic[topic];
                }
            }
            return result;
        },

        async selectExercise(topic, name) {
            try {
                const res = await fetch(`/api/exercises/${topic}/${name}`);
                if (!res.ok) {
                    throw new Error("Failed to load exercise");
                }

                const data = await res.json();
                // Hide boilerplate (if __name__ block) - show only the function
                const code =
                    data.code.split(/\nif __name__ == /)[0].trimEnd() + "\n";
                this.skeleton = code;
                this.current = { topic, name };
                this.output = "";
                this.passed = false;
                this.errorType = null;

                editor.setValue(this.skeleton);
                editor.focus();
            } catch (err) {
                this.output = err.message;
            }
        },

        async submit() {
            if (!this.current || this.loading) return;

            this.loading = true;
            this.output = "";
            this.errorType = null;

            try {
                const res = await fetch(
                    `/api/exercises/${this.current.topic}/${this.current.name}/run`,
                    {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ code: editor.getValue() }),
                    },
                );

                const data = await res.json();
                this.output = data.output || data.detail || "Unknown error";
                this.passed = data.passed || false;
                this.errorType = data.error_type;

                await this.loadExercises();
            } catch (err) {
                this.output = `Network error: ${err.message}`;
                this.passed = false;
            } finally {
                this.loading = false;
            }
        },

        reset() {
            if (this.skeleton) {
                editor.setValue(this.skeleton);
                this.output = "";
                this.passed = false;
                this.errorType = null;
            }
        },

        async resetStats() {
            if (!this.current) return;
            if (!confirm("Reset stats for this exercise?")) return;

            try {
                await fetch(
                    `/api/exercises/${this.current.topic}/${this.current.name}/stats`,
                    { method: "DELETE" },
                );
                await this.loadExercises();
            } catch (err) {
                console.error("Failed to reset stats:", err);
            }
        },

        getOutputClass() {
            if (this.passed) return "success";
            if (!this.output) return "";
            return this.errorType ? `error ${this.errorType}-error` : "error";
        },

        getCurrentPasses() {
            if (!this.current) return 0;
            const exercises = this.exercisesByTopic[this.current.topic] || [];
            const ex = exercises.find((e) => e.name === this.current.name);
            return ex?.passes || 0;
        },

        toggleTheme() {
            this.darkMode = !this.darkMode;
            const theme = this.darkMode ? "dark" : "light";
            document.documentElement.setAttribute("data-theme", theme);
            localStorage.setItem("theme", theme);

            // Update CodeMirror theme
            if (editor) {
                editor.setOption(
                    "theme",
                    this.darkMode ? "material-darker" : "default",
                );
            }
        },
    };
}
