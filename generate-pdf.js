#!/usr/bin/env node

const fs = require('fs');
const puppeteer = require('puppeteer');
const MarkdownIt = require('markdown-it');
const md = new MarkdownIt();

async function generatePDF() {
    try {
        // Leer archivo Markdown
        const mdContent = fs.readFileSync('PROPUESTA_DELIVERY_SHOW.md', 'utf-8');

        // Convertir a HTML
        const htmlBody = md.render(mdContent);

        // HTML completo con estilos
        const fullHtml = `
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #333;
            padding: 90px 50px 40px 50px;
            position: relative;
        }
        .header-logo {
            position: absolute;
            top: 20px;
            left: 50px;
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.5rem;
            font-weight: 600;
            font-style: italic;
            color: #722F37;
            letter-spacing: -0.04em;
        }
        .footer-url {
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #ddd;
            text-align: center;
            font-size: 14px;
            color: #5C252C;
        }
        h1 {
            color: #000;
            font-size: 24px;
            margin: 1.5rem 0 1rem 0;
            border-bottom: 2px solid #000;
            padding-bottom: 0.5rem;
            page-break-after: avoid;
            font-weight: 700;
        }
        h2 {
            color: #000;
            font-size: 20px;
            margin: 2rem 0 1rem 0;
            page-break-after: avoid;
            font-weight: 600;
        }
        h3 {
            color: #000;
            font-size: 18px;
            margin: 1.5rem 0 0.4rem 0;
            page-break-after: avoid;
            font-weight: 600;
        }
        p {
            margin: 0.4rem 0;
            text-align: justify;
            font-size: 14px;
        }
        strong {
            color: #000;
            font-weight: 600;
        }
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 2rem 0;
        }
        ul, ol {
            margin: 0.5rem 0 1rem 2rem;
        }
        li {
            margin: 0.3rem 0;
            font-size: 14px;
        }
        blockquote {
            background: #F5F0E6;
            padding: 1rem;
            border-left: 4px solid #722F37;
            margin: 1rem 0;
        }
    </style>
</head>
<body>
<div class="header-logo">Chuchurex</div>
${htmlBody}
<div class="footer-url">https://chuchurex.cl/</div>
</body>
</html>
        `;

        console.log('📄 Generando PDF...');

        // Lanzar navegador
        const browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });

        const page = await browser.newPage();
        await page.setContent(fullHtml, { waitUntil: 'networkidle0' });

        // Generar PDF
        await page.pdf({
            path: 'PROPUESTA_DELIVERY_SHOW.pdf',
            format: 'A4',
            printBackground: true,
            margin: {
                top: '20mm',
                right: '20mm',
                bottom: '20mm',
                left: '20mm'
            }
        });

        await browser.close();

        console.log('✅ PDF generado: PROPUESTA_DELIVERY_SHOW.pdf');

    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

generatePDF();
