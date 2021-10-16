<br />

<p align="left">
  <h1><img src="./template/src/image/title.png" width="117" height="23" alt="Papyrus"></h1>
</p>

<br />

<p align="center">
  <img src="./template/src/image/logo.png" alt="logo" width="180" height="180">
</p>

<br />

##### :paperclip:&ensp;Overview

This project will generate a PDF from any HTML.<br />PDF can be output through API.<br />You can define your own headers, footers, and data structures in HTML.<br />By default, an A4 size PDF (landscape) is generated, but you can set the PDF size and margins as you like.

<p align="left">
  <a href="sample/template_1.pdf" target="_blank">Sample 1</a>&emsp;<a href="sample/template_2.pdf" target="_blank">Sample 2</a>
</p>

##### :paperclip:&ensp;Processing flow

`Webpack` → `Pug + Scss` → `HTML + Css` → `Python [Flask x pdfkit (wkhtmltopdf)]` → `PDF`

##### :paperclip:&ensp;Dependent libraries

You can check in more detail by looking at the `Dockerfile`.

| Name | Role | Official | GitHub |
|:-----|:-----|:---------|:-------|
| wkhtmltopdf | HTML to PDF | [https://wkhtmltopdf.org/](https://wkhtmltopdf.org/) | [https://github.com/wkhtmltopdf/wkhtmltopdf](https://github.com/wkhtmltopdf/wkhtmltopdf) |
| Flask | API foundation | [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/) | [https://github.com/pallets/flask](https://github.com/pallets/flask) |
| Pug | HTML compatible | [https://pugjs.org/](https://pugjs.org/) | [https://github.com/pugjs/pug](https://github.com/pugjs/pug) |
| Scss | CSS compatible | [https://sass-lang.com/](https://sass-lang.com/) | [https://github.com/sass/sass](https://github.com/sass/sass) |

<br />

#### :paperclip:&ensp;How to initialize

**Step 1. Python >= 3.7.3**

Create a directory `.test` for CLI testing and install modules.

```sh
make init
```

**Step 2. Node.js >= 12.16.3**

Install `npm` modules for PDF templates.

```sh
npm install
```

<br />

#### :paperclip:&ensp;How to maintenance

In this project, we first need to use Pug and Scss to generate the HTML file that is the basis of the PDF.<br />The generated HTML becomes a PDF through an API created by the Flask framework.<br />We have prepared a CLI command to generate a sample PDF, so please give it a try.<br />Of course, you can freely edit the design of the sample PDF and the information to be displayed to your liking.

**Step 1. Improve HTML (PDF Template)**

```sh
cd template
npm run serve
```

<p align="right">
  You can see : <a href="http://localhost:8080" target="_blank">http://localhost:8080/</a>
</p>

**Step 2. Output HTML (PDF Template)**

```sh
cd template
npm run build
```

If the repository is in its initial state, 2 HTML templates (`template_1.html`, `template_2.html`) will be generated.

<p align="right">
  HTML files will be generated @ <code>./template/dist</code>
</p>

**Step 3. Activate PDF Generator API**

```sh
cd .
make cli
```

<p align="right">
  You can see : <a href="http://localhost:3020/template" target="_blank">http://localhost:3020/template</a>
</p>

**Step 4. Try PDF Generator API**

OK : Valid parameter ( Items )

```sh
cd .
make check-ok-1
```

<p align="right">
  Your PDF will be generated @ <code>./.test/template_1_default.pdf</code>
</p>

OK : Valid parameter ( 0 item  )

```sh
cd .
make check-ok-2
```

<p align="right">
  Your PDF will be generated @ <code>./.test/template_1_none_item.pdf</code>
</p>

NG : Invalid parameter

```sh
cd .
make check-ng-1
```

<p align="right">
  Your PDF will be generated @ <code>./.test/template_2_invalid_parameter.pdf</code>
</p>

NG : Wrong parameter

```sh
cd .
make check-ng-2
```

<p align="right">
  Your PDF will be generated @ <code>./.test/template_2_wrong_parameter</code>
</p>

NG : None parameter

```sh
cd .
make check-ng-3
```

<p align="right">
  Your PDF will be generated @ <code>./.test/template_2_none_parameter.pdf</code>
</p>

<br />

#### :paperclip:&ensp;How to build

This project will be reproduced in a Docker container `Alpine`.<br />As a completely independent API, it can be deployed to various cloud services.

**Step 1. Build Docker Image**

```sh
cd .
make docker-build
```

**Step 2. Run Docker Image**

```sh
cd .
make docker-run
```

<br />
