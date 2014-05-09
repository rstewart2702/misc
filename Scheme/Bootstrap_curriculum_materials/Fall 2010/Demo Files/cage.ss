;; The first three lines of this file were inserted by DrScheme. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname cage) (read-case-sensitive #t) (teachpacks ((lib "cage-teachpack.ss" "installed-teachpacks"))) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ((lib "cage-teachpack.ss" "installed-teachpacks")))))
;;;; YOUR CODE HERE
; offscreen? : Number Number -> Boolean
; returns true is the coordinates (x,y) are offscreen
(define (offscreen? x y)
  (or (or (< x 0) (> x 400) )
      (or (< y 0) (> y 200) )))

(EXAMPLE (offscreen? -100 100) true)





(start offscreen?)