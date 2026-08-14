#import "utils.typ": is-html
#import "colors.typ": code-colors

// ------------------------------------------------------------
// Generic code block
// ------------------------------------------------------------

#let code-block(kind, content) = {

  let c = code-colors.at(kind)

  let language = c.name
  let border = c.border
  let bg = c.bg

  if is-html {

    html.elem(
      "div",
      attrs: (
        class: "code-block " + kind,
        style:
          "margin:24px 0;" +
          "border-left:5px solid " + border + ";" +
          "background:" + bg + ";" +
          "border-radius:6px;" +
          "overflow:hidden;",
      ),
    )[

      #html.elem(
        "div",
        attrs: (
          class: "code-header",
          style:
            "background:" + border + ";" +
            "color:white;" +
            "padding:8px 12px;" +
            "font-weight:bold;" +
            "font-family:system-ui,sans-serif;",
        ),
      )[
        #language
      ]

      #html.elem(
        "pre",
        attrs: (
          class: "code-body",
          style:
            "margin:0;" +
            "padding:14px;" +
            "overflow-x:auto;" +
            "font-family:monospace;" +
            "font-size:0.95em;",
        ),
      )[

        #html.elem(
          "code",
        )[
          #content
        ]

      ]

    ]

  } else {

    block(
      width: 100%,
      stroke: (left: 4pt + rgb(border)),
      fill: rgb(bg),
      inset: 0pt,
      radius: (right: 4pt),
      breakable: true,
    )[

      rect(
        width: 100%,
        fill: rgb(border),
        inset: 8pt,
      )[
        #text(
          fill: white,
          weight: "bold",
        )[
          #language
        ]
      ]

      #block(
        inset: 12pt,
      )[

        #set text(
          font: "DejaVu Sans Mono",
          size: 9pt,
        )

        #content

      ]

    ]

  }

}


// ------------------------------------------------------------
// Language wrappers
// ------------------------------------------------------------

#let python(content) = code-block("python", content)

#let sage(content) = code-block("sage", content)

#let lean(content) = code-block("lean", content)

#let julia(content) = code-block("julia", content)

#let asy(content) = code-block("asy", content)