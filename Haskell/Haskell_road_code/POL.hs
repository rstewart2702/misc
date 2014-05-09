module POL

where

import Ratio
import Polynomials

difs :: [Integer] -> [Integer]
difs [] = []
difs [n] = []
difs (n:m:ks) = m-n : difs (m:ks)

difLists :: [[Integer]]->[[Integer]]
difLists [] = []
difLists lists@(xs:xss) = 
  if constant xs then lists else difLists ((difs xs):lists)

constant (n:m:ms) = all (==n) (m:ms) 
constant  _       = error "lack of data or not a polynomial fct"

genDifs :: [Integer] -> [Integer]
genDifs xs = map last (difLists [xs])

nextD :: [Integer] -> [Integer]
nextD [] = error "no data"
nextD [n] = [n]
nextD (n:m:ks) = n : nextD (n+m : ks)

next :: [Integer] -> Integer
next = last . nextD . genDifs

continue ::  [Integer] -> [Integer]
continue xs = map last (iterate nextD differences)
  where 
  differences = nextD (genDifs xs)

degree :: [Integer] -> Int
degree xs = length (difLists [xs]) - 1

type Matrix = [Row]
type Row    = [Integer]

rows, cols :: Matrix -> Int
rows m = length m
cols m | m == []   = 0 
       | otherwise = length (head m)

genMatrix :: [Integer] -> Matrix
genMatrix xs = zipWith (++) (genM d) [ [x] | x <- xs ]
  where 
  d      = degree xs 
  genM n = [ [ (toInteger x^m) | m <- [0..n] ] | x <- [0..n] ]

adjustWith :: Row -> Row -> Row
adjustWith (m:ms) (n:ns) = zipWith (-) (map (n*) ms) (map (m*) ns)

echelon   :: Matrix -> Matrix 
echelon rs
    | null rs || null (head rs) = rs
    | null rs2                  = map (0:) (echelon (map tail rs))
    | otherwise                 = piv : map (0:) (echelon rs')
      where rs'            = map (adjustWith piv) (rs1++rs3)
            (rs1,rs2)      = span leadZero rs
            leadZero (n:_) = n==0
            (piv:rs3)      = rs2

eliminate :: Rational -> Matrix -> Matrix 
eliminate p rs = map (simplify c a) rs
  where
  c = numerator   p 
  a = denominator p 
  simplify c a row = init (init row') ++ [a*d - b*c] 
    where 
    d    = last row 
    b    = last (init row) 
    row' = map (*a) row

backsubst :: Matrix -> [Rational]
backsubst rs = backsubst' rs []
  where 
  backsubst' [] ps = ps 
  backsubst' rs ps = backsubst' rs' (p:ps) 
    where 
    a     = (last rs) !! ((cols rs) - 2) 
    c     = (last rs) !! ((cols rs) - 1) 
    p     = c % a 
    rs'   = eliminate p (init rs)

solveSeq :: [Integer] -> [Rational]
solveSeq = backsubst . echelon . genMatrix

choose n k = (product [(n-k+1)..n]) `div` (product [1..k])

choose' n 0 = 1 
choose' n k | n < k     = 0 
            | n == k    = 1 
            | otherwise = 
                 choose' (n-1) (k-1) + (choose' (n-1) (k))

binom n 0 = 1 
binom n k | n < k     = 0 
          | otherwise = (n * binom (n-1) (k-1)) `div` k 

comp1 :: Num a => [a] -> [a] -> [a] 
comp1 _ [] = error ".."  
comp1 [] _ = [] 
comp1 (f:fs) gs = [f] + (gs * comp1 fs gs)

