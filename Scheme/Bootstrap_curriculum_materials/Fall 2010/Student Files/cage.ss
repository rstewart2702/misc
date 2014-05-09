;; The first three lines of this file were inserted by DrScheme. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname cage) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ())))
(require "Teachpacks/cage-teachpack.ss")

;;;; YOUR CODE HERE
; Don't forget to include a contract and purpose statement.


; offscreen? : Number Number -> Boolean
; is any part of the butterfly off the screen?
(define (offscreen? x y)
  (< x 0))

;; put your examples below this line


;; don't touch anything below this line!
(start offscreen?)