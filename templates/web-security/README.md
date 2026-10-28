# 🛡️ Web Security, Bot Defense & Open Graph Template Suite

This suite contains production-grade security header configurations, `robots.txt` crawler policies, and **Open Graph (OG) banner requirements & generator scripts**. You can drop these configurations directly into your other websites regardless of whether you host on **Firebase Hosting, Cloudflare Pages, Netlify, Vercel, Nginx, or Apache**.

---

## 📁 Included Template Files

| File | Purpose / Platform |
| :--- | :--- |
| **`robots.template.txt`** | Universal `robots.txt` allowing verified search engines (Google, Bing, Apple) & social previewers (WhatsApp, Twitter, Slack), while blocking aggressive scrapers, AI dataset harvesters, exploit tools, and download folder indexing. |
| **`firebase.template.json`** | Complete `firebase.json` headers configuration for Firebase Hosting with HSTS, strict CSP, X-Frame-Options, Permissions-Policy, and download protection. |
| **`_headers.template`** | Universal `_headers` file for **Cloudflare Pages**, **Netlify**, or **Vercel**. |
| **`security-headers.nginx.conf`** | Drop-in snippet for **Nginx** `server { ... }` blocks. |
| **`.htaccess.template`** | Drop-in snippet for **Apache HTTP Server** (`.htaccess`). |
| **`html-head-meta.template.html`** | HTML `<head>` SEO, OpenGraph cards, Twitter cards, PWA manifest, and canonical link boilerplate. |
| **`opengraph-banner-requirements.template.md`** | Complete technical specifications for Open Graph banners: `1200 x 630` px dimensions, safe zone margins, the `< 300 KB` WhatsApp rule, and platform-by-platform behavior. |
| **`generate_og_banner.template.py`** | Reusable standalone Python script using Pillow (`PIL`) that automatically creates a pixel-perfect, dark-gradient 1200x630 banner (< 300 KB) for any website in seconds. |

---

## 🎨 Open Graph Banner Requirements Summary

When generating an Open Graph banner (`og:image`) for any website:

1. **Dimensions**: Exactly **`1200 x 630` px** (Aspect ratio `1.91:1`).
2. **File Size**: Must be **under 300 KB** (WhatsApp will refuse to display previews automatically if the image is > 300 KB).
3. **Safe Zone**: Keep all essential titles, logos, and badges at least **80 px away from left/right** and **60 px away from top/bottom** to prevent cropping in mobile chat bubbles.
4. **Instant Generation**: Run the included Python generator:
   ```bash
   pip install pillow
   python templates/web-security/generate_og_banner.template.py
   ```
   *(Outputs an optimized `og-image.png` at ~20-50 KB with a high-contrast dark gradient, title, and badge pill).*

---

## 🚀 How to Apply to Another Website

### 1. Configure `robots.txt`
1. Copy `robots.template.txt` to your website's public web root as `robots.txt`.
2. Replace `https://example.com/sitemap.xml` with your actual domain's sitemap URL.
3. Adjust the `Disallow: /downloads/` paths to match your site's heavy asset or protected folders.

### 2. Configure HTTP Security Headers

Pick the configuration file corresponding to your hosting provider:

* **Firebase Hosting**: Use `firebase.template.json`. Copy the `"headers"` array into your `firebase.json`.
* **Cloudflare Pages / Netlify**: Copy `_headers.template` into your publish root as `_headers`.
* **Nginx**: Include `security-headers.nginx.conf` inside your `server { ... }` block (`include /path/to/security-headers.nginx.conf;`) and reload Nginx (`sudo nginx -s reload`).
* **Apache**: Copy the contents of `.htaccess.template` into your root `.htaccess` file.

### 3. Customize Content Security Policy (CSP)
In the CSP header string:
- If your website uses Google Tag Manager / Analytics, keep `https://www.googletagmanager.com` and `https://*.google-analytics.com`.
- If your website loads external fonts (e.g. Google Fonts), add `font-src 'self' https://fonts.gstatic.com;` and `style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;`.
- If you use Stripe or payment gateways, add `https://js.stripe.com` to `script-src` and `frame-src`.

---

## 🔍 How to Test & Verify

Once deployed on your other website, you can verify your score using these free industry testing tools:

1. **Social Share Preview & Debugger**:
   - Test at [https://www.opengraph.xyz](https://www.opengraph.xyz) or [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
2. **Security Headers Grade (Target: A+)**:
   - Test at [https://securityheaders.com](https://securityheaders.com)
3. **CSP Evaluation**:
   - Test at Google CSP Evaluator: [https://csp-evaluator.withgoogle.com](https://csp-evaluator.withgoogle.com)
4. **Robots.txt & Sitemap Inspection**:
   - Test in Google Search Console -> Settings -> Robots.txt.
