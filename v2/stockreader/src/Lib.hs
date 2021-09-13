module Lib (sayHelloToAll) where

import Data.Char (isSpace)
import System.Environment
import Text.Printf

isValid :: String -> Bool
isValid name = not (null name || all isSpace name)

sayHello :: String -> String
sayHello = printf "Hello %s from Haskell!"

printAll :: [String] -> IO ()
printAll = mapM_ print

sayHelloToAll :: IO ()
sayHelloToAll = do
  print "start"
  args <- getArgs
  --   stocks <- downloadStocksToAnalyse
  printAll $ (map sayHello . filter isValid) args
  print "end"
