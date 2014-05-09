;; Turns out that the -> operator is a macro, and is a
;; kind of function composition operator:

; example functions used later:
(defn f [x] (+ x 3))
(defn g [x] (* 14 x))
(defn compose [f g] (fn [x] (-> x g f)))
(defn compose1 [f g] (fn [x] (f (g x))))


(-> 1 g f)
;; is the same as:
((compose1 f g) 1)
;; is the same as:
((compose f g) 1)
;; and that is the same as:
(-> 1 ( (fn [x] (* x 14) ) ) ( (fn [x] (+ x 3) ) ) )

;; So, it's something a bit more "primitive" that provides a
;; convenient way to compose functions, if needed, because
;; it takes advantage of how s-expressions specify function
;; invocation...