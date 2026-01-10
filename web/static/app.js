let editor = null;

function handleTab(cm) {
    if (cm.somethingSelected()) {
        cm.execCommand("indentMore");
    } else {
        const cursor = cm.getCursor();
        cm.replaceSelection(" ".repeat(4 - (cursor.ch % 4)));
    }
}

function handleBackspace(cm) {
    if (cm.somethingSelected()) {
        cm.execCommand("delCharBefore");
        return;
    }
    const cursor = cm.getCursor();
    const beforeCursor = cm.getLine(cursor.line).slice(0, cursor.ch);
    const spaces = beforeCursor.match(/ +$/);
    if (spaces) {
        const count = spaces[0].length % 4 || 4;
        cm.replaceRange(
            "",
            { line: cursor.line, ch: cursor.ch - count },
            cursor,
        );
    } else {
        cm.execCommand("delCharBefore");
    }
}

function app() {
    const self = {
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
            if (this.darkMode) {
                document.documentElement.setAttribute("data-theme", "dark");
            }
            if (!editor) {
                editor = CodeMirror(
                    document.getElementById("editor-container"),
                    {
                        mode: "python",
                        lineNumbers: true,
                        theme: this.darkMode ? "material-darker" : "default",
                        indentUnit: 4,
                        tabSize: 4,
                        autoCloseBrackets: true,
                        matchBrackets: true,
                        styleActiveLine: true,
                        foldGutter: true,
                        gutters: [
                            "CodeMirror-linenumbers",
                            "CodeMirror-foldgutter",
                        ],
                        extraKeys: {
                            Tab: handleTab,
                            "Shift-Tab": "indentLess",
                            "Ctrl-Enter": () => this.submit(),
                            "Cmd-Enter": () => this.submit(),
                            "Ctrl-Space": "autocomplete",
                            Backspace: handleBackspace,
                        },
                    },
                );
            }
            await this.loadExercises();
        },

        async loadExercises() {
            const [catRes, exRes] = await Promise.all([
                fetch("/api/categories"),
                fetch("/api/exercises"),
            ]);
            if (catRes.ok) this.categories = await catRes.json();
            if (exRes.ok) this.exercisesByTopic = await exRes.json();
        },

        setCategory(cat) {
            this.activeCategory = cat;
        },

        getFilteredExercises() {
            const topics = this.categories[this.activeCategory] || [];
            return Object.fromEntries(
                topics
                    .filter((t) => this.exercisesByTopic[t])
                    .map((t) => [t, this.exercisesByTopic[t]]),
            );
        },

        async selectExercise(topic, name) {
            const res = await fetch(`/api/exercises/${topic}/${name}`);
            if (!res.ok) return;
            const data = await res.json();
            this.skeleton =
                data.code.split(/\nif __name__ == /)[0].trimEnd() + "\n";
            this.current = { topic, name };
            this.output = "";
            this.passed = false;
            this.errorType = null;
            editor.setValue(this.skeleton);
            editor.focus();
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
            } finally {
                this.loading = false;
            }
        },

        reset() {
            if (!this.skeleton) return;
            editor.setValue(this.skeleton);
            this.output = "";
            this.passed = false;
            this.errorType = null;
        },

        async resetStats() {
            if (!this.current || !confirm("Reset stats for this exercise?"))
                return;
            await fetch(
                `/api/exercises/${this.current.topic}/${this.current.name}/stats`,
                { method: "DELETE" },
            );
            await this.loadExercises();
        },

        getOutputClass() {
            if (this.passed) return "success";
            return this.output && this.errorType
                ? `error ${this.errorType}-error`
                : "";
        },

        getCurrentPasses() {
            if (!this.current) return 0;
            return (
                this.exercisesByTopic[this.current.topic]?.find(
                    (e) => e.name === this.current.name,
                )?.passes || 0
            );
        },

        toggleTheme() {
            this.darkMode = !this.darkMode;
            document.documentElement.setAttribute(
                "data-theme",
                this.darkMode ? "dark" : "light",
            );
            localStorage.setItem("theme", this.darkMode ? "dark" : "light");
            editor?.setOption(
                "theme",
                this.darkMode ? "material-darker" : "default",
            );
        },
    };
    return self;
}
