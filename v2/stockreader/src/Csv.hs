{-# LANGUAGE OverloadedStrings #-}

module Csv (readStocks) where

import Control.Monad
import qualified Data.ByteString.Lazy as BL
import Data.Csv
import qualified Data.Vector as V
import System.Directory (doesFileExist)
import Text.Printf

-- data type to model a FinancialInstrument
data FinancialInstrument = FinancialInstrument
  { code :: String,
    name :: String,
    country :: String,
    exchange :: String,
    currency :: String,
    instrumentType :: String
  }
  deriving (Show, Eq)

-- Define how to get a FinancialInstrument from a record (CSV row),
-- by implementing the FromNamedRecord typeclass
instance FromNamedRecord FinancialInstrument where
  parseNamedRecord record =
    FinancialInstrument
      <$> record .: "Code"
      <*> record .: "Name"
      <*> record .: "Country"
      <*> record .: "Exchange"
      <*> record .: "Currency"
      <*> record .: "Type"

-- type synonyms to handle the CSV contents
type ErrorMsg = String

type CsvData = (Header, V.Vector FinancialInstrument)

-- Function to read the CSV
parseCsv :: FilePath -> IO (Either ErrorMsg CsvData)
parseCsv filePath = do
  fileExists <- doesFileExist filePath
  if fileExists
    then decodeByName <$> BL.readFile filePath
    else return . Left $ printf "The file %s does not exist" filePath

-- Discard headers from CsvData
removeHeaders :: CsvData -> V.Vector FinancialInstrument
removeHeaders = snd

-- Given a list, return only the elements with instrumentType "Common Stock"
filterStocks :: V.Vector FinancialInstrument -> V.Vector FinancialInstrument
filterStocks = V.filter isStock
  where
    isStock :: FinancialInstrument -> Bool
    isStock instrument = instrumentType instrument == "Common Stock"

-- Read stocks from a CSV file
readStocks :: FilePath -> IO (Either ErrorMsg (V.Vector FinancialInstrument))
readStocks filePath =
  (fmap . fmap) (filterStocks . removeHeaders) (parseCsv filePath)
