<br />

<p align="left">
  <h1>&emsp;<img src="./template/src/image/title.png" width="117" height="23" alt="Papyrus"></h1>
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

##### :paperclip:&ensp;Use case

- Convert a large amount of predetermined data to a PDF.
- Easily edit the appearance and output a PDF.
- Provide a web endpoint for outputting a customized PDF.

If the repository is in its initial state, Only `Japanese [Noto Sans CJK JP]` and `English [Abel]` are supported, but you can specify any font.<br />You can support any language by specifying any font in (S)CSS, adjusting its appearance, and then adding the font installation process to your `Dockerfile`.

##### :paperclip:&ensp;Processing flow

`Webpack` → `Pug + Scss` → `HTML + Css` → `Python [Flask x pdfkit (wkhtmltopdf)]` → `PDF`

##### :paperclip:&ensp;Dependent libraries

| Name | Role | Official | GitHub |
|:-----|:-----|:---------|:-------|
| wkhtmltopdf | HTML to PDF | [https://wkhtmltopdf.org/](https://wkhtmltopdf.org/) | [https://github.com/wkhtmltopdf/wkhtmltopdf](https://github.com/wkhtmltopdf/wkhtmltopdf) |
| Flask | API foundation | [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/) | [https://github.com/pallets/flask](https://github.com/pallets/flask) |
| Pug | HTML compatible | [https://pugjs.org/](https://pugjs.org/) | [https://github.com/pugjs/pug](https://github.com/pugjs/pug) |
| Scss | CSS compatible | [https://sass-lang.com/](https://sass-lang.com/) | [https://github.com/sass/sass](https://github.com/sass/sass) |

You can check in more detail by looking at the `Dockerfile`.

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

If the repository is in its initial state, you can try the PDF output API by executing the following CLI command.<br />Execute the following `Command`.

| Status | Detail | Command | Result |
|:------:|:-------|:--------|:----|
| OK     | Valid parameter ( Items ) | `make check-ok-1` | `.test/template_1_default.pdf` |
| OK     | Valid parameter ( 0 item  ) | `make check-ok-2` | `.test/template_1_none_item.pdf` |
| NG     | Invalid parameter | `make check-ng-1` | `.test/template_2_invalid_parameter.pdf` |
| NG     | Wrong parameter | `make check-ng-2` | `.test/template_2_wrong_parameter.pdf` |
| NG     | None parameter | `make check-ng-3` | `.test/template_2_none_parameter.pdf` |

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
