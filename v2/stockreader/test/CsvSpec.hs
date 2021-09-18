module CsvSpec where

import Csv
import GHC.Base
import Test.Hspec
import Test.Hspec.Expectations.Contrib
import Test.Hspec.QuickCheck
import Text.Printf

spec :: Spec
spec = do
  describe "readStocks" $ do
    it "returns IO (Left ErrorMsg) when the file does not exist" $ do
      let nonExistentFile = "test-resources/no-file.csv"
      let errorMessage = printf "The file %s does not exist" "test-resources/no-file.csv"
      readStocks nonExistentFile `shouldReturn` Left errorMessage

    it "returns 'not enough input' when the file is empty" $ do
      let emptyFile = "test-resources/empty-file.csv"
      let errorMessage = "parse error (not enough input) at \"\""
      readStocks emptyFile `shouldReturn` Left errorMessage

    it "returns the same rows as the file when the file only contains stocks" $ do
      let stocksOnlyFile = "test-resources/stocks-only.csv"
      either <- readStocks stocksOnlyFile
      either `shouldSatisfy` isRight
      length <$> either `shouldBe` Right 5

    it "returns the less rows than the file because filters out non-stocks" $ do
      let stocksAndFundsFile = "test-resources/stocks-and-funds.csv"
      either <- readStocks stocksAndFundsFile
      either `shouldSatisfy` isRight
      length <$> either `shouldBe` Right 7
