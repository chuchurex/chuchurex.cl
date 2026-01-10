/**
 * CHUCHUREX - Internationalization (i18n)
 * Supports: Spanish (es), English (en), Portuguese (pt)
 */

const translations = {
    es: {
        // Meta
        pageTitle: "Chuchurex",
        metaDescription: "Desarrollo de proyectos web con IA",

        // Header
        headerTitle: "Desarrollo Web e Inteligencia Artificial",

        // Chat
        placeholder: "Describe tu proyecto y te ayudo a desarrollar tu idea...",

        // PDF
        pdfLoading: "Generando tu propuesta...",
        pdfReady: "Tu propuesta está lista",
        pdfDownload: "Descargar Propuesta PDF",

        // Errors
        errorGeneric: "Ups, algo salió mal. ¿Puedes intentar de nuevo?",

        // Footer
        footerAbout: "Acerca",
        footerPrivacy: "Privacidad",

        // Modal
        modalTitle: "Sobre Chuchurex",
        modalDescription1: "Soy Carlos, desarrollador web en Santiago de Chile. Trabajo con SASS + JavaScript vanilla y uso IA como multiplicador de productividad.",
        modalDescription2: "Chuchurex te ayuda a desarrollar tu idea, estructurarla y cotizarla.",
        modalContact: "Contacto:",

        // Privacy page
        privacyTitle: "Política de Privacidad - Chuchurex",
        privacyHeader: "Política de Privacidad",
        privacyBetaLabel: "Beta:",
        privacyBetaText: "Este servicio se encuentra en fase de prueba. Durante este período, las conversaciones pueden ser almacenadas temporalmente para análisis y mejora del sistema.",
        privacyResponsibleLabel: "Responsable:",
        privacyDataLabel: "Datos recopilados:",
        privacyDataText: "Durante la fase beta, las conversaciones del chat pueden ser almacenadas para mejorar el servicio. No se recopilan datos personales identificables.",
        privacyCookiesLabel: "Cookies:",
        privacyCookiesText: "No utilizamos cookies de seguimiento ni publicidad.",
        privacyThirdPartyLabel: "Terceros:",
        privacyThirdPartyText: "El chat utiliza la API de Anthropic para procesar mensajes. Consulta su",
        privacyThirdPartyLink: "política de privacidad",
        privacyRightsLabel: "Derechos:",
        privacyRightsText: "Puedes contactarnos en carlos@chuchurex.cl para cualquier consulta.",
        privacyBackHome: "Volver al inicio",
    },
    en: {
        // Meta
        pageTitle: "Chuchurex",
        metaDescription: "Web development projects with AI",

        // Header
        headerTitle: "Web Development and Artificial Intelligence",

        // Chat
        placeholder: "Describe your project and I'll help you develop your idea...",

        // PDF
        pdfLoading: "Generating your proposal...",
        pdfReady: "Your proposal is ready",
        pdfDownload: "Download Proposal PDF",

        // Errors
        errorGeneric: "Oops, something went wrong. Can you try again?",

        // Footer
        footerAbout: "About",
        footerPrivacy: "Privacy",

        // Modal
        modalTitle: "About Chuchurex",
        modalDescription1: "I'm Carlos, a web developer in Santiago, Chile. I work with SASS + vanilla JavaScript and use AI as a productivity multiplier.",
        modalDescription2: "Chuchurex helps you develop your idea, structure it, and get a quote.",
        modalContact: "Contact:",

        // Privacy page
        privacyTitle: "Privacy Policy - Chuchurex",
        privacyHeader: "Privacy Policy",
        privacyBetaLabel: "Beta:",
        privacyBetaText: "This service is in beta testing phase. During this period, conversations may be temporarily stored for analysis and system improvement.",
        privacyResponsibleLabel: "Responsible:",
        privacyDataLabel: "Data collected:",
        privacyDataText: "During the beta phase, chat conversations may be stored to improve the service. No personally identifiable data is collected.",
        privacyCookiesLabel: "Cookies:",
        privacyCookiesText: "We do not use tracking or advertising cookies.",
        privacyThirdPartyLabel: "Third parties:",
        privacyThirdPartyText: "The chat uses the Anthropic API to process messages. Check their",
        privacyThirdPartyLink: "privacy policy",
        privacyRightsLabel: "Rights:",
        privacyRightsText: "You can contact us at carlos@chuchurex.cl for any inquiries.",
        privacyBackHome: "Back to home",
    },
    pt: {
        // Meta
        pageTitle: "Chuchurex",
        metaDescription: "Desenvolvimento de projetos web com IA",

        // Header
        headerTitle: "Desenvolvimento Web e Inteligência Artificial",

        // Chat
        placeholder: "Descreva seu projeto e eu ajudo a desenvolver sua ideia...",

        // PDF
        pdfLoading: "Gerando sua proposta...",
        pdfReady: "Sua proposta está pronta",
        pdfDownload: "Baixar Proposta PDF",

        // Errors
        errorGeneric: "Ops, algo deu errado. Pode tentar de novo?",

        // Footer
        footerAbout: "Sobre",
        footerPrivacy: "Privacidade",

        // Modal
        modalTitle: "Sobre Chuchurex",
        modalDescription1: "Sou Carlos, desenvolvedor web em Santiago do Chile. Trabalho com SASS + JavaScript vanilla e uso IA como multiplicador de produtividade.",
        modalDescription2: "Chuchurex ajuda você a desenvolver sua ideia, estruturá-la e orçá-la.",
        modalContact: "Contato:",

        // Privacy page
        privacyTitle: "Política de Privacidade - Chuchurex",
        privacyHeader: "Política de Privacidade",
        privacyBetaLabel: "Beta:",
        privacyBetaText: "Este serviço está em fase de testes. Durante este período, as conversas podem ser armazenadas temporariamente para análise e melhoria do sistema.",
        privacyResponsibleLabel: "Responsável:",
        privacyDataLabel: "Dados coletados:",
        privacyDataText: "Durante a fase beta, as conversas do chat podem ser armazenadas para melhorar o serviço. Não são coletados dados pessoais identificáveis.",
        privacyCookiesLabel: "Cookies:",
        privacyCookiesText: "Não utilizamos cookies de rastreamento nem publicidade.",
        privacyThirdPartyLabel: "Terceiros:",
        privacyThirdPartyText: "O chat utiliza a API da Anthropic para processar mensagens. Consulte a",
        privacyThirdPartyLink: "política de privacidade",
        privacyRightsLabel: "Direitos:",
        privacyRightsText: "Você pode nos contatar em carlos@chuchurex.cl para qualquer dúvida.",
        privacyBackHome: "Voltar ao início",
    }
};

/**
 * Detect browser language and return supported language code
 */
function detectLanguage() {
    const browserLang = navigator.language || navigator.userLanguage;
    const langCode = browserLang.split('-')[0].toLowerCase();

    // Return supported language or default to Spanish
    if (translations[langCode]) {
        return langCode;
    }
    return 'es';
}

/**
 * Get current language (from localStorage or detect)
 */
function getCurrentLanguage() {
    const stored = localStorage.getItem('chuchurex_lang');
    if (stored && translations[stored]) {
        return stored;
    }
    return detectLanguage();
}

/**
 * Set language and save to localStorage
 */
function setLanguage(lang) {
    if (translations[lang]) {
        localStorage.setItem('chuchurex_lang', lang);
        applyTranslations(lang);
        return true;
    }
    return false;
}

/**
 * Get translation for a key
 */
function t(key) {
    const lang = getCurrentLanguage();
    return translations[lang][key] || translations['es'][key] || key;
}

/**
 * Apply translations to the page
 */
function applyTranslations(lang) {
    if (!lang) lang = getCurrentLanguage();
    const trans = translations[lang];

    // Update HTML lang attribute
    document.documentElement.lang = lang;

    // Update page title
    document.title = trans.pageTitle;

    // Update meta description
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) metaDesc.setAttribute('content', trans.metaDescription);

    // Update OG description
    const ogDesc = document.querySelector('meta[property="og:description"]');
    if (ogDesc) ogDesc.setAttribute('content', trans.metaDescription);

    // Update elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (trans[key]) {
            el.textContent = trans[key];
        }
    });

    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (trans[key]) {
            el.placeholder = trans[key];
        }
    });
}

// Export for use in app.js
window.i18n = {
    translations,
    detectLanguage,
    getCurrentLanguage,
    setLanguage,
    t,
    applyTranslations
};
