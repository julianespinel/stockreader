module Main where

import Lib
import System.Environment

-- How to run?
-- stack run "resources/US_LIST_OF_SYMBOLS.csv"
main :: IO ()
main = do
  args <- getArgs
  readStocks (head args) >>= print
