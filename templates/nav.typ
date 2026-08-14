// Navigation bar
#import "../generated/lectures.typ": lectures
#import "../generated/pages_meta.typ": pages
#import "utils.typ": is-html

#let breadcrumb(lecture) = {
  if is-html {
    html.elem("nav", attrs: (class: "breadcrumb"))[
      #link("../index.html")[🏠 Home]
      #html.elem("span", attrs: (class: "breadcrumb-sep"))[/]
      #lecture.category
      #html.elem("span", attrs: (class: "breadcrumb-sep"))[/]
      #lecture.title
    ]
  }
}

#let previous-next(current) = {

  if is-html {

    let index = lectures.position(
      lec => lec.file == current.file
    )

    // If this page is not in generated lectures, show nothing
    if index == none {
      return
    }

    let lec = lectures.at(index)

    html.elem(
      "div",
      attrs: (
        class: "lecture-navigation",
      ),
    )[

      #if lec.previous != none [
        #link(lec.previous.html)[
          ← #lec.previous.title
        ]
      ]

      #h(1fr)

      #if lec.next != none [
        #link(lec.next.html)[
          #lec.next.title →
        ]
      ]

    ]
  }
}

#let html-nav-header() = {
  if sys.inputs.at("format", default: "pdf") == "html" {
    html.elem("nav", attrs: (class: "global-nav-header"))[
      #link("../index.html")[🏠 Home]

      #for lec in lectures {
        text(fill: rgb("#cbd5e1"))[ | ]
        link(lec.file + ".html")[#lec.title]
      }

      #for page in pages {
        text(fill: rgb("#cbd5e1"))[ | ]
        link(page.html)[#page.title]
      }
    ]
  }
}

#let download-buttons(lecture) = {

  if is-html {

    html.elem(
      "div",
      attrs: (
        class: "download-buttons",
      ),
    )[

      #link("../pdf/" + lecture.file + ".pdf")[⬇ PDF]

    ]

  }

}
