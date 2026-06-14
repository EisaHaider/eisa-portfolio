const translations = {

    en: {

        direction: "ltr",

        nav_profile: "Profile",
        nav_projects: "Projects",
        nav_domains: "Domains",
        nav_insights: "Insights",
        nav_contact: "Contact",

        hero_title: "Information Systems Architect",

        hero_text:
            "Designing business applications, leading digital transformation initiatives, and developing modern information systems.",

        btn_profile: "Professional Profile",
        btn_projects: "Selected Projects",

        domains_title: "Professional Domains",

        domain_1: "Enterprise Information Systems",
        domain_2: "Document Management",
        domain_3: "Workflow Automation",
        domain_4: "Digital Transformation",
        domain_5: "Rapid Application Development",
        domain_6: "Cloud Solutions",

        summary_title: "Executive Summary",

        projects_title: "Selected Projects & Initiatives",

        insights_title: "Insights",

        contact_title: "Contact",

        language_button: "EN | AR",

        theme_button: "Theme"
    },

    ar: {

        direction: "rtl",

        nav_profile: "الملف المهني",
        nav_projects: "المشاريع",
        nav_domains: "المجالات",
        nav_insights: "الاهتمامات",
        nav_contact: "التواصل",

        hero_title: "محلل نظم معلومات",

        hero_text:
            "تطوير تطبيقات الأعمال، ومبادرات التحول الرقمي، وتطوير أنظمة المعلومات.",

        btn_profile: "الملف المهني",
        btn_projects: "المشاريع المختارة",

        domains_title: "المجالات المهنية",

        domain_1: "نظم المعلومات المؤسسية",
        domain_2: "إدارة الوثائق",
        domain_3: "أتمتة الإجراءات",
        domain_4: "التحول الرقمي",
        domain_5: "تطوير البرمجيات",
        domain_6: "الحلول السحابية",

        summary_title: "الملخص المهني",

        projects_title: "المشاريع والمبادرات",

        insights_title: "الاهتمامات",

        contact_title: "التواصل",

        language_button: "EN | AR",

        theme_button: "المظهر"
    }

};

function updateTexts(lang) {

    document.querySelectorAll("[data-i18n]").forEach(el => {

        const key = el.dataset.i18n;

        if (translations[lang][key]) {

            el.textContent =
                translations[lang][key];

        }

    });

}

function applyLanguage(lang) {

    localStorage.setItem(
        "language",
        lang
    );

    document.documentElement.lang =
        lang;

    document.documentElement.dir =
        translations[lang].direction;

    updateTexts(lang);

}

function toggleLanguage() {

    const current =
        localStorage.getItem("language")
        || "en";

    const next =
        current === "en"
            ? "ar"
            : "en";

    applyLanguage(next);

}

function applyTheme(theme) {

    localStorage.setItem(
        "theme",
        theme
    );

    if (theme === "light") {

        document.documentElement
            .classList.add("light");

    } else {

        document.documentElement
            .classList.remove("light");

    }

}

function toggleTheme() {

    const current =
        localStorage.getItem("theme")
        || "dark";

    const next =
        current === "dark"
            ? "light"
            : "dark";

    applyTheme(next);

}

function revealElements() {

    const elements =
        document.querySelectorAll(".fade-up");

    const observer =
        new IntersectionObserver(

            entries => {

                entries.forEach(entry => {

                    if (entry.isIntersecting) {

                        entry.target
                            .classList
                            .add("show");

                    }

                });

            },

            {
                threshold: 0.1
            }

        );

    elements.forEach(el => {

        observer.observe(el);

    });

}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const savedLang =
            localStorage.getItem("language")
            || "en";

        const savedTheme =
            localStorage.getItem("theme")
            || "dark";

        applyLanguage(savedLang);
        applyTheme(savedTheme);

        const langBtn =
            document.getElementById(
                "language-toggle"
            );

        if (langBtn) {

            langBtn.addEventListener(
                "click",
                toggleLanguage
            );

        }

        const themeBtn =
            document.getElementById(
                "theme-toggle"
            );

        if (themeBtn) {

            themeBtn.addEventListener(
                "click",
                toggleTheme
            );

        }

        revealElements();

    }
);