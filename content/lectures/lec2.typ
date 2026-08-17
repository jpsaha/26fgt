// src/lec1.typ
#import "../../templates/course.typ": *

#let lecture = (
  file: "lec2",
  type: "lecture",
  number: 1,
  title: "Field extensions",
  category: "Fields and Galois theory",
  tags: ["division algorithm", "Gauss' lemma"],
)

#show: lecture-layout(lecture)

#show: doc => {
  reset-counters(lecture.number)
  doc
}

#page-header(lecture, chap: true)

#let defsize = 13pt; //20pt // 11pt
#set text(size: defsize)

#include "lec2_content.typ"

#previous-next(lecture)
