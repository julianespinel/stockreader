{-# LANGUAGE OverloadedStrings #-}

module Lib (printStocks) where

import Control.Monad
import qualified Data.ByteString.Lazy as BL
import Data.Csv
import qualified Data.Vector as V

-- data type to model a stock
data Stock = Stock
  { code :: String,
    name :: String,
    country :: String,
    exchange :: String,
    currency :: String,
    instrumentType :: String
  }
  deriving (Show)

instance FromNamedRecord Stock where
  parseNamedRecord record =
    Stock
      <$> record .: "Code"
      <*> record .: "Name"
      <*> record .: "Country"
      <*> record .: "Exchange"
      <*> record .: "Currency"
      <*> record .: "Type"

-- type synonyms to handle the CSV contents
type ErrorMsg = String

type CsvData = (Header, V.Vector Stock)

-- Function to read the CSV
parseCSV :: FilePath -> IO (Either ErrorMsg CsvData)
parseCSV filePath = do
  contents <- BL.readFile filePath
  return $ decodeByName contents

-- Discard headers from CsvData
removeHeaders :: CsvData -> V.Vector Stock
removeHeaders = snd

-- Check if the given element is a Common Stock
isStock :: Stock -> Bool
isStock stock = instrumentType stock == "Common Stock"

filterStocks :: V.Vector Stock -> V.Vector Stock
filterStocks = V.filter isStock

-- Print the stocks from the CSV file
printStocks :: FilePath -> IO ()
printStocks filePath =
  parseCSV filePath
    >>= print . fmap (filterStocks . removeHeaders)
