;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname flags) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ())))
(require "Teachpacks/function-teachpack.rkt")

;; define some numbers
(define x 5)
(define foo 10.5)

;; define some strings
(define name "Cassandra")
(define food "pizza")


;; define some images
(define pic (circle 50 "solid" "purple"))
(define pic2 (star 5 100 200 "solid" "orange"))

;; define a 100x100 empty scene
(define scene (empty-scene 100 100))

;; put a circle at the bottom of a 100x100 scene
(define pic3 (place-image (circle 50 "solid" "blue")
                          50 100
                          (empty-scene 100 100)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;; let's make some flags! ;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; a blank flag is a rectangle, placed at the center of an empty scene
(define blank (place-image (rectangle 400 250 "outline" "black") 
                          200 125 
                          (empty-scene 400 250)))

;; the flag of Japan is a red circle, placed at the center of an outlined 
;; rectangle, placed at the center of an empty scene.
(define japan (place-image (circle 75 "solid" "red") 
                           200 125 
                           (place-image (rectangle 400 250 "outline" "black") 
                                        200 125 
                                        (empty-scene 400 250))))

;; the flag of Poland is a red rectangle that is half as tall as the flag,
;; placed on the bottom half of an outlined rectangle, placed at the center
;; of an empty scene
(define poland (place-image (rectangle 400 125 "solid" "red") 
                             200 190 
                             (place-image (rectangle 400 250 "outline" "black") 
                                          200 125 
                                          (empty-scene 400 250))))



;; the flag of Somalia is a white star, placed at the center of a blue 
;; rectangle, placed at the center of an outlined rectangle, placed at
;; the center of an empty scene.
