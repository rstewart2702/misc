;
; Need a way to create a set of rules to assign a "category" to each
; record based on the contents of the record.
;
; I now understand why people make such a fuss over the use of map-reduce
; and its general applicability to many information processing situations.
;
;
; Example of reading-a-file:
; this "lazily" reads from the file, via the doseq function:
(with-open [rdr (io/reader "example.txt")]
           ; the doseq "lazily" processes the elements of the
           ; "sequence" produced, "lazily," by the line-seq?
           (doseq [line (line-seq rdr)]
                  (println line)))

; this "eagerly" reads the file via the doall function (?):
(with-open
 [rdr (io/reader "example.txt")]
 (doall (line-seq rdr)) )

(doseq
 ; this means that line is bound to a "sequence?"
 [line (with-open
        [rdr (io/reader "example.txt")]
        ; the doall eagerly reads in the entire file?
        (doall (line-seq rdr)))]
 ; the following is invoked once for each element of "line"?
 (println line))

; an example of how we might use with-open, along with a "reader"
; and the reduce (aka "fold") function?
;; (with-open
;;   [rdr (clojure.java.io/reader "example.txt")]
;;   (reduce
;;    (fn [mm v] (conj mm v))
;;    []
;;    (line-seq rdr) ) )

;; This turns out to be what we want, I believe, once we got the parse-record
;; to work correctly, or at least to handle records that aren't terminated with
;; a newline!  ARRRGGGHHH, the reader strips out the newline character, it seems?
;; OOOF!!
;;
;; So, the other key strategy that worked well was also to abstract out
;; the reduce-the-map couplet which calculates the record-map into its
;; own function, named rstewart/build-record-map below.
;;
;; Also, at least with the record-parsing as it is now implemented, I
;; can't add fields at the end of the record which are omitted from
;; the source data:  the record parsing functions can only split records
;; by the separators, with the exception that fields can be delimited, also.
;;
(with-open
   [rdr (clojure.java.io/reader "example.txt")]
   (reduce
      (fn [mm v] (conj mm v))
      []
      (map
       (fn [rs] (rstewart/build-record-map rs [:date :amt1 :desc :misc :misc1]))
       (line-seq rdr) ) ) ) 

;; The following two expressions should be viewed as "aborted experiments,"
;; since one of my big problems was that my record-parser couldn't
;; handle "empty strings" and such.  I got all wrapped around the axle
;; about the differences between Clojure nil, '(), and "".  These issues
;; are a bit "exotic," which is a euphemism for "irregular and seemingly
;; inconsistent..."
(with-open
   [rdr (clojure.java.io/reader "example.txt")]
   (reduce
      (fn [vect val] (conj vect val))
      []
      (doseq
        [raw-string (line-seq rdr)]
        (rstewart/build-record-map raw-string [:date :amt1 :desc :misc] ) ) ) )

(with-open
   [rdr (clojure.java.io/reader "example.txt")]
   (reduce
      (fn [vect val] (conj vect val))
      []
      (doseq
        [raw-string (line-seq rdr)]
        (rstewart/build-record-map raw-string [:date :amt1 :desc :misc] ) ) ) )
