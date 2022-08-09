//
//  CoinManager.swift
//  ByteCoin
//
//  Created by Angela Yu on 11/09/2019.
//  Copyright © 2019 The App Brewery. All rights reserved.
//

import Foundation

protocol CoinManagerDelegate {
    func didUpdateCurrency(_ coinManager: CoinManager, coinPrice: Double)
    func didFailWithError(_ error: Error)
}
struct CoinManager {
    
    let baseURL = "https://rest.coinapi.io/v1/exchangerate/BTC"
    let apiKey = "0146784C-1298-42C4-8B67-7F28221C10AD"
    
    let currencyArray = ["AUD", "BRL","CAD","CNY","EUR","GBP","HKD","IDR","ILS","INR","JPY","MXN","NOK","NZD","PLN","RON","RUB","SEK","SGD","USD","ZAR"]
    
    var delegate: CoinManagerDelegate?
    
    
    func getCoinPrice(for currency: String) {
        let urlString = "\(baseURL)/\(currency)?apikey=\(apiKey)"
        
        //create url
        if let url = URL(string: urlString) {
            //create url session
            let session = URLSession(configuration: .default)
            
            //create task
            let task = session.dataTask(with: url) { (data, response, error) in
                if error != nil {
                    delegate?.didFailWithError(error!)
                    return
                }
                
                if let safeData = data {
                    if let coinPrice = self.parseJSON(data: safeData){
                        self.delegate?.didUpdateCurrency(self, coinPrice: coinPrice)
                    }
                }
            }
            
            //start task
            task.resume()
        }
    }
    
    func parseJSON(data coinData: Data) -> Double? {
        let decoder = JSONDecoder()
        do {
            let decodedData = try decoder.decode(CoinData.self, from: coinData)
            let lastPrice = decodedData.rate
            
            print(lastPrice)
            return lastPrice
        } catch {
            delegate?.didFailWithError(error)
            return nil
        }
    }
}
